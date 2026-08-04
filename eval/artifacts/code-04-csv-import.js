// jobs/importSubscribers.js
//
// Nightly import of the subscriber export from the marketing platform.
// Files arrive on S3 and run from 40 MB to about 900 MB depending on the
// campaign. The `subscribers` table has a unique index on `email` and a
// foreign key `segment_id -> segments(id)`.
//
// Ops requirement from the 2026-02 review: a failed import must leave the
// table exactly as it was before the job started. Partial state is what
// caused the February incident.

const fs = require('fs');
const { parse } = require('csv-parse/sync');
const db = require('../db');

async function importSubscribers(localPath) {
  const raw = fs.readFileSync(localPath, 'utf8');
  const rows = parse(raw, { columns: true, skip_empty_lines: true });

  let inserted = 0;
  let failed = 0;

  for (const row of rows) {
    try {
      await db.query(
        'INSERT INTO subscribers (email, name, segment_id, signed_up_at) VALUES ($1, $2, $3, $4)',
        [row.email, row.name, row.segment_id, row.signed_up_at]
      );
      inserted++;
    } catch (err) {
      console.log('row failed: ' + err.message);
      failed++;
    }
  }

  console.log(`imported ${inserted}, failed ${failed}`);
  return { inserted, failed };
}

async function run() {
  const path = process.argv[2];
  const result = await importSubscribers(path);
  if (result.failed > 0) {
    process.exit(1);
  }
}

run();
