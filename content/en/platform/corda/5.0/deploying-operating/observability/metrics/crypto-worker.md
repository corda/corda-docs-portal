---
date: '2023-06-14'
version: 'Corda 5.0 Beta 4'
title: "Crypto Worker"
version: 'Corda 5.0 Beta 4'
menu:
  corda5:
    parent: corda5-cluster-metrics
    identifier: corda5-cluster-crypto-worker
    weight: 12000
section_menu: corda5
---

# Crypto Worker

The crypto worker is responsible for handling crypto operations in Corda, such as signing. It is the only worker that
hosts keys owned by the Corda cluster, as well as keys owned by the virtual nodes required for crypto operations.

The keys of the virtual nodes are stored in dedicated databases per virtual node, while the keys of the Corda cluster
are stored in a dedicated database for cluster keys. In addition to the database, there are caches universal to all
virtual nodes that hold the keys in memory for faster lookup.

The crypto requests could be categorized into flow requests and everything else. Flow requests are, seemingly,
of more importance in terms of metrics as they are directly involved in flows lifecycle.
With the crypto worker metrics, you can measure the below crypto requests within the crypto worker:

* Flow-crypto requests, which consist of the operations:
  * `SigningService.sign`: The `sign` operation is performed on the flow side and sends to the crypto worker the bytes
    to be signed along with the public part of the signing key and the signature spec.
    On the crypto worker side, the crypto worker attempts to find the key in the keys hosted for the virtual node that
    sent the request and if found, it signs the bytes and returns the signature.
   The metrics in the following table pertain to the time taken to handle the entire
    `sign` request. Additionally, there are more detailed metrics related to key caches and the 'sign' operation itself.
  * `SigningService.findMySigningKeys`: The `findMySigningKeys` operation sends a set of keys to the crypto worker,
    which then filters and returns the keys owned by the calling virtual node.
    The metrics in the following table are related to the time taken to
    handle the entire `findMySigningKeys` request. Additionally, there are metrics related to key caches.

* Admin or other requests, which involve operations such as creating a new key pair for a virtual node, or list
  information about the keys owned by a virtual node. Regarding metrics for these requests, the following metrics pertain
  to the time taken to handle the requests as a whole.

<style>
table th:first-of-type {
    width: 25%;
}
table th:nth-of-type(2) {
    width: 10%;
}
table th:nth-of-type(3) {
    width: 20%;
}
table th:nth-of-type(4) {
    width: 45%;
}
</style>

| Metric | Type | Tags | Description |
| :----------- | :----------- | :----------- | :----------- |
| `corda_crypto_flow_processor_execution_time_seconds` | Timer | <ul><li>`operation_name`</li></ul> | The time taken by crypto worker to process operations requested by flow operations. |
| `corda_crypto_processor_execution_time_seconds` | Timer | <ul><li>`operation_name`</li></ul> | The time taken by crypto worker to process operations requested from other endpoints. |
| `corda_crypto_wrapping_key_creation_time_seconds` | Timer | <ul><li>`tenant`</li></ul> | The time taken for wrapping key creation in crypto operations. |
| `corda_entity_manager_factory_creation_time_seconds` | Timer | <ul><li>`tenant`</li></ul> | The time taken to create entity manager factories. |
| `corda_crypto_sign_time_seconds` | Timer | <ul><li>`signature_spec`</li></ul> | The time taken for crypto signing. |
| `corda_crypto_sigining_key_lookup_time_seconds` | Timer | <ul><li>`lookup_method`</li></ul> | The time taken for crypto signing key lookup. |
| `corda_crypto_signing_repository_get_instance_time_seconds` | Timer | <ul><li>`tenant`</li></ul> | The time taken to get crypto signing repository instances. |
| `corda_crypto_get_owned_key_record_time_seconds` | Timer | <ul><li>`operation_name`</li><li>`publickey_type`</li></ul> | The time taken to look up tenant’s owned keys. |
| `corda_crypto_cipher_scheme_time_seconds` | Timer | <ul><li>`operation_name`</li></ul> | The time taken for crypto cipher scheme encoding and decoding operations. |
| `corda_crypto_signature_spec_time_seconds` | Timer | <ul><li>`operation_name`</li></ul> | The time taken for crypto signature spec operations including deserializing wire objects to signature spec and vice versa. |

Tags:
* `operation_name`: The name of the operation that the metric is related to.
* `tenant`: The identifier of a tenant: it's either a virtual node identifier or cluster level tenant ID.
* `signature_spec`: The signature signing scheme name to create signatures during crypto signing operations.
* `lookup_method`: The method used to look up signing key IDs, either public key IDs or public key short IDs.
* `publickey_type`: The type of public key used in sign operations.
