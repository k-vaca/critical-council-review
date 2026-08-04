# Runbook: `search-indexer` lag alert

**Applies to:** the `SearchIndexerLagHigh` alert only. For indexer crashes see `search-indexer-crash.md`.
**Audience:** platform on-call, no prior knowledge of the indexer assumed.
**Last validated:** 2026-07-02 against production, by running steps 1 to 4 during a synthetic lag event.

## What the alert means

The indexer consumes from the `documents` Kafka topic and writes to OpenSearch. The alert fires when consumer-group lag exceeds 50,000 messages for 10 consecutive minutes. Users see stale search results: a document edited now may not appear in search for as long as the lag implies.

This is not a paging alert outside business hours unless lag is also rising. Steady lag above the threshold degrades freshness; rising lag ends in disk pressure on the brokers, which is a page.

## Step 1 — Decide whether it is rising

```
kubectl -n search exec deploy/kafka-tools -- \
  kafka-consumer-groups --bootstrap-server $BROKERS \
  --group search-indexer --describe
```

Run it twice, 60 seconds apart. Compare the `LAG` column totals.

- **Falling or flat:** the indexer is keeping up or catching up. Note the number in the alert thread and stop here. Re-check in 30 minutes.
- **Rising:** continue to step 2.

## Step 2 — Check whether OpenSearch is rejecting writes

```
curl -s "$OS_ENDPOINT/_cat/thread_pool/write?v&h=node_name,active,queue,rejected"
```

A non-zero and growing `rejected` count means OpenSearch is the bottleneck, not the indexer. If so, go to step 4. Otherwise continue to step 3.

## Step 3 — Scale the indexer

The indexer partitions are fixed at 24. Replicas above 24 do nothing, so scale to at most 24.

```
kubectl -n search scale deploy/search-indexer --replicas=24
```

Watch lag for 10 minutes using the step 1 command. If lag begins falling, stop here and record the change in the alert thread; the deployment autoscaler will return replicas to baseline within the hour.

If lag does not fall with 24 replicas, the bottleneck is downstream. Continue to step 4.

## Step 4 — Shed load

Only with an incident commander's agreement, because it drops freshness for one document class.

```
kubectl -n search set env deploy/search-indexer SKIP_ATTACHMENT_INDEXING=true
```

Attachment bodies stop being indexed; titles and metadata continue. Attachments are roughly 60% of index write volume and about 4% of search queries. Backfill by removing the variable and running `bin/reindex --since <timestamp>`.

## Escalation

If lag is still rising 20 minutes after step 4, page the search team lead. Include: the two lag readings from step 1, the thread-pool output from step 2, the replica count, and whether step 4 was applied.

## Known false positive

A broker restart resets the consumer group's committed offset reporting for up to 2 minutes and can show a large spurious lag. If the alert fired within 2 minutes of a broker restart (`kubectl -n search get pods -l app=kafka --sort-by=.status.startTime`), re-run step 1 before acting.
