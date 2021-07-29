---
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-4:
    identifier: cenm-1-4-cenm-error-codes
    parent: cenm-1-4-operations
    weight: 350
tags:
- CENM
- error
- codes
title: CENM error codes
---


# Overview of CENM error codes

Corda Enterprise Network Manager can report a number of error codes. The tables below provide details about such error codes for errors related to configuration parsing and validation.

* The CENM error codes are listed in the [CENM error codes table](#cenm-error-codes-table) below.
* The RPC Admin API error codes are listed in the [RPC Admin API error codes table](#rpc-admin-api-error-codes-table) below.

For each error code in the tables, there is additional information about its aliases, the reason why that error occurred, and (for the main CENM errors) instructions on what actions
you can take to address the problem reported by the error.

{{< note >}}
The set of error codes listed on this page is not exhaustive.
{{< /note >}}

Table contents:
 - **Error code**: the error code as reported by the Corda node.
 - **Description**: a description of what has gone wrong.
 - **Actions to fix**: what actions to take in order to address the problem (only available for the main CENM error codes in the first table below).

To make use of this table, search the console or node logs for lines indicating an error has occurred. Errors that have
corresponding codes will contain a message with the error code and a link pointing to this page.

## CENM error codes table

{{< table >}}

| Error code               | Description                                                                   | Actions to fix                                                                                                                 |
| :---------- | :------- | :----------- |
| `config-parsing-and-validation-error` | This error indicates that there were both parsing and validating issues with the config. | Check the additional details and double check that your configs are lining up with the [most recent CENM documentation](https://docs.corda.net/docs/cenm/index.html). |
| `config-parse-error`                  | This error indicates that an error has occurred during configuration parsing.            | Check the additional details and double check that your configs are lining up with the [most recent CENM documentation](https://docs.corda.net/docs/cenm/index.html). |
| `config-file-doesnt-exist`            | This error indicates that the configuration file that was provided does not exist.       | Check that the provided path is correct and that the file is actually there. |
| `config-file-not-readable`            | This error indicates that the configuration file could not be read.                      | Make sure you have the rights to read the configuration file. |
| `config-validation-error`             | This error indicates that there were validating issues with the configuration            | Check the additional details and double check that your configurations are lined up with the [most recent CENM documentation](https://docs.corda.net/docs/cenm/index.html). |
| `config-substitution-error`           | This error indicates that a substitution did not resolve to anything.                    | Check if the entries in your configuration file are specified correctly. |

{{< /table >}}

## RPC Admin API error codes table

These error codes are a bit different than the CENM error codes in the table above. They are attached to the RPC errors that are thrown when using the CENM services' RPC Admin API.

These error codes can be accessed by using the `code` property when encountering the error in the RPC client.

{{< table >}}

| Error code | Description
| :---------- | :------- |
| `GENERAL_ERROR`                              | Used when the server throws a more general exception - for example, `RuntimeException` or when the server responds with an error type that is unknown or the error type is not present.                                                                              |
| `CLIENT_REQUEST_PROCESSING_ERROR`            | Used when the client's request is being marshalled into a JSON. If there is a processing exception during that phase, this error type will be used.                                                                                                       |
| `CLIENT_RESPONSE_PROCESSING_ERROR`           | Used when the server's response (body) cannot be un-marshalled into the given object. This can happen because of various reasons - see the attached cause in the `RpcClientException` class for more specific reason.                                       |
| `CLIENT_RESPONSE_MISSING_BODY`               | Used when the server's response (body) is missing, and the call requires a response.                                                                                                                                                                     |
| `NETWORK_MAP_NODE_INFO_DECODING_FAILED`      | Decoding uploaded node info `String` to `ByteArray` failed.                                                                                                                                                                                              |
| `NETWORK_MAP_HASH_PARSING_FAILED`            | Parsing uploaded node info or Network Parameters to `SecureHash` failed.                                                                                                                                                                                 |
| `NETWORK_MAP_NODE_INFO_WRITE_FAILED`         | Writing node info to disk file failed.                                                                                                                                                                                                                   |
| `NETWORK_MAP_PARAMETERS_FILE_NOT_FOUND`      | Provided Network Parameters file (argument provided by Angel Service when starting Network Map) doesn't exist.                                                                                                                                           |
| `NETWORK_MAP_PARAMETERS_FILE_CORRUPT`        | Provided Network Parameters file (argument provided by Angel Service when starting Network Map) failed parsing or validation.                                                                                                                            |
| `NETWORK_MAP_PARAMETERS_UNCHANGED`           | New advertised Network Parameters update is same to existing Network Parameters.                                                                                                                                                                         |
| `NETWORK_MAP_PARAMETERS_UPDATE_NOT_FOUND`    | No parameters update found for given Network Parameters's hash or there are no scheduled updates at all.                                                                                                                                                 |
| `NETWORK_MAP_UPDATE_DEADLINE_NOT_REACHED`    | Update deadline specified in advertised parameters update hasn't passed yet.                                                                                                                                                                             |
| `NETWORK_MAP_PARAMETERS_NOT_SIGNED`          | Advertised parameters update hasn't been signed yet.                                                                                                                                                                                                     |
| `IDENTITY_MANAGER_LEGAL_NAME_PARSING_FAILED` | Provided legal name `String` failed to be parsed to `CordaX500Name`.                                                                                                                                                                                     |
| `IDENTITY_MANAGER_INVALID_REVOCATION_REASON` | Provided revocation reason is not in the list of supported reasons (`CRLReason.KEY_COMPROMISE`, `CRLReason.CA_COMPROMISE`, `CRLReason.AFFILIATION_CHANGED`, `CRLReason.SUPERSEDED`, `CRLReason.CESSATION_OF_OPERATION`, `CRLReason.PRIVILEGE_WITHDRAWN`).|
| `IDENTITY_MANAGER_CERTIFICATE_NOT_FOUND`     | Certificate to be revoked doesn't exist.                                                                                                                                                                                                                 |
| `SIGNER_SIGNING_PROCESS_NOT_FOUND`           | Signing process used for fetching or signing provided data type (`CSR`, `CRL`, `NETWORK_MAP`, `NETWORK_PARAMETERS`) doesn't exist.                                                                                                                               |
| `SIGNER_SIGNING_FAILED`                      | There was an error during actual material signing.                                                                                                                                                                                                       |
| `UNKNOWN_FUNCTION`                           | The function used in the request cannot be recognised.                                                                                                                                                                                                   |
| `UNKNOWN_MESSAGE_TYPE`                       | The message type used in the request cannot be recognised.                                                                                                                                                                                               |
| `INVALID_REQUEST_CONTENT`                    | The content used in the request cannot be recognised.                                                                                                                                                                                                    |
| `USER_TOKEN_ERROR`                           | Used when the user token is invalid.                                                                                                                                                                                                                     |
| `AUTHORISATION_ERROR`                        | Used when a call is made that the user does not have authorisation for.                                                                                                                                                                                  |
| `ZONE_SERVICE_SUBZONE_NOT_FOUND`             | Sub-zone with provided `subZoneId` doesn't exist.                                                                                                                                                                                                        |
| `ZONE_SERVICE_CONFIG_PARSING_FAILED`         | Provided configuration to be uploaded failed parsing.                                                                                                                                                                                                    |
| `ZONE_SERVICE_CONFIG_VALIDATION_FAILED`      | Provided configuration to be uploaded failed user validation rules (non-runtime dependent ones).                                                                                                                                                         |
| `ZONE_SERVICE_LABEL_VALIDATION_FAILED`       | Provided label data to be uploaded failed validation (text is empty or colour is not formatted as RGB hex code).                                                                                                                                          |

{{< /table >}}

## Corda Enterprise error codes

For a list of node error codes in Corda Enterprise, see [Node error codes](../../corda-enterprise/4.6/node/operating/error-codes.md).
