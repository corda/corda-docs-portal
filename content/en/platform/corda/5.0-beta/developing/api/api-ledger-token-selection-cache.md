---
date: '2023-01-31'
title: "Token Selection Cache Sync"
menu:
  corda-5-beta:
    identifier: corda-5-beta-api-ledger-utxo-token-selection-cache
    parent: corda-5-beta-api-ledger-utxo-token-selection
    weight: 1000
section_menu: corda-5-beta
---
The fundamental purpose of the Token Selection service is to allow flows to claim tokens for spending without the need for expensive or intrusive database operations. To achieve this, the service uses a cache to store tokens and their lock status. This cache is backed by the messaging APIs. 

This means we need to solve the problem of: Hydrating the cache, updating the cache in near real-time with DB updates, checking the cache/DB are in-sync and re-syncing the cache when needed.

## Use Cases
The system will support a re-sync request that will force a complete re-publish from the DB to the cache, this can be triggered manually via an API call or self triggered when the system detects it is out of sync. The assumption is that on a full reset, the system will start, run a sync test, realize it’s out of sync and request a re-sync request.

On a state produce or consume event in the DB the system will publish and update to the cache.

To cover missing states from the cache, the system will periodically (~every 10 mins) publish a batch of unconsumed state refs (~5K) as a sync check. the cache should validate these refs are in the cache, if any are missing it should publish a resync request to signal the system to perform a full re-sync. the batch of state refs published should be on a rolling basis from oldest to newest.

To cover stale states in the cache, the cache will periodically publish a block of state refs (~5k) back to the DB to check if any are consumed, if any are consumed the DB should publish consume events for them to bring the cache back inline with the DB.

 

Events
Sync Request - Triggers a DB worker to perform a full re-publish of all unspent states.

Stale Sync Check - Event containing a list of state refs for the DB to check are still unspent.

Token Event (Type = update) - List of produced and consumed states used to update the cache

Token Event (Type = Sync) - unspent states, used to re-sync the cache.

