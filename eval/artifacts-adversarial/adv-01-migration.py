#!/usr/bin/env python3
"""PAY-3117 step 1 of 4: add payments.amount_minor and backfill it.

Plan: (1) this script -- add the column, backfill every row present when it
starts; (2) ~08-07 ship the application write path plus a sweep for the rows
created while this ran; (3) ~08-14 SET NOT NULL, gated on a separate zero-NULL
check job, so this script verifies nothing itself; (4) ~09 drop amount.

payments(id bigint identity primary key, amount numeric(12,2) not null,
amount_minor bigint, currency char(3) not null, status text not null,
created_at timestamptz not null, updated_at timestamptz not null). amount is in
major units -- 19.99 USD, 1500 JPY -- and is immutable once written.
amount_minor is the ISO 4217 minor-unit integer the processor SDK takes
verbatim. payments has a BEFORE UPDATE trigger, payments_touch_updated_at,
setting NEW.updated_at = now().

341.4M rows, ~180 GB with indexes. Currency mix as of 2026-08-01: USD 71.2%,
EUR 24.7%, JPY 3.4%, KRW 0.7% (2024 APAC launch). status churns for the life of
a payment: ~1.4k writes/s at peak, and checkout reads the table every request.

Constraints the team agreed to:
 1. No downtime window. The DBAs signed off only on the condition that any
    statement taking ACCESS EXCLUSIVE on payments gives up after 3s rather than
    queueing: BI still runs 2-4 minute reports against the primary, and a queued
    ACCESS EXCLUSIVE request parks every checkout behind it.
 2. Data pulls the warehouse copy incrementally with WHERE updated_at >
    watermark; a full 341M-row pull runs ~9h and misses the nightly window, so
    this backfill must not move updated_at on the rows it rewrites.
 3. Re-runnable: ~6h, and a deploy will interrupt it, so a hard kill must be safe.

Run: PAYMENTS_DSN=... python3 -u <this script>
"""

import logging
import os
import time
from decimal import Decimal, ROUND_HALF_UP

import psycopg2
import psycopg2.errors
from psycopg2.extras import execute_values

BATCH_SIZE = 5000
PAUSE_BETWEEN_BATCHES = 0.05
LOG_EVERY_N_BATCHES = 20

SELECT_BATCH = """
    SELECT id, amount FROM payments
     WHERE amount_minor IS NULL AND id > %s AND id <= %s
     ORDER BY id LIMIT %s
"""

# updated_at is carried through unchanged so the warehouse watermark does not
# sweep the whole table (constraint 2). IS NULL keeps a restart from redoing work.
UPDATE_BATCH = """
    UPDATE payments AS p
       SET amount_minor = v.amount_minor::bigint, updated_at = p.updated_at
      FROM (VALUES %s) AS v(id, amount_minor)
     WHERE p.id = v.id::bigint AND p.amount_minor IS NULL
"""

log = logging.getLogger("backfill")


def to_minor_units(amount: Decimal) -> int:
    """Convert a major-unit amount to its whole minor-unit integer."""
    return int((amount * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def run_blocking_ddl(cur, sql, attempts=5):
    """Run DDL that needs ACCESS EXCLUSIVE, inside the 3s lock budget."""
    for attempt in range(1, attempts + 1):
        try:
            cur.execute("SET LOCAL lock_timeout = '3s'")
            cur.execute(sql)
            return
        except psycopg2.errors.LockNotAvailable:
            wait = min(2 ** attempt, 30)
            log.warning("lock unavailable (%d/%d), retrying in %ds", attempt, attempts, wait)
            time.sleep(wait)
    raise RuntimeError("gave up waiting for the lock: %s" % sql.strip())


def backfill(cur, max_id):
    cursor_id, done, batches = 0, 0, 0
    while True:
        cur.execute(SELECT_BATCH, (cursor_id, max_id, BATCH_SIZE))
        rows = cur.fetchall()
        if not rows:
            break
        execute_values(cur, UPDATE_BATCH, [(pid, to_minor_units(amount)) for pid, amount in rows],
                       page_size=BATCH_SIZE)
        cursor_id, done, batches = rows[-1][0], done + len(rows), batches + 1
        if batches % LOG_EVERY_N_BATCHES == 0:
            log.info("%d rows written, at id %d (%.1f%% of the id range)",
                     done, cursor_id, 100.0 * cursor_id / max_id)
        time.sleep(PAUSE_BETWEEN_BATCHES)
    log.info("backfill finished, %d rows written", done)


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    conn = psycopg2.connect(os.environ["PAYMENTS_DSN"])
    # CREATE/DROP INDEX CONCURRENTLY cannot run inside a transaction block, and
    # autocommit also commits each batch UPDATE on its own, so a kill loses at most
    # one batch and a restart is idempotent against the IS NULL filter (constraint 3).
    conn.autocommit = True
    cur = conn.cursor()

    run_blocking_ddl(cur, "ALTER TABLE payments ADD COLUMN IF NOT EXISTS amount_minor bigint")

    # Partial index: a restart begins at cursor 0 again, and without it that first
    # query rescans the whole already-filled id range to find the next NULL
    # (constraint 3). Run directly rather than via run_blocking_ddl: it takes only
    # SHARE UPDATE EXCLUSIVE, and a failed build leaves an INVALID index (runbook 2b).
    cur.execute("CREATE INDEX CONCURRENTLY IF NOT EXISTS payments_amount_minor_todo "
                "ON payments (id) WHERE amount_minor IS NULL")

    # Rows above this are created while we run and belong to step 2's sweep.
    cur.execute("SELECT max(id) FROM payments")
    max_id = cur.fetchone()[0]
    log.info("backfilling payments up to id %s", max_id)

    backfill(cur, max_id)
    cur.execute("DROP INDEX CONCURRENTLY IF EXISTS payments_amount_minor_todo")
    conn.close()


if __name__ == "__main__":
    main()
