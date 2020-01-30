---
title: "Workflow"
date: 2020-01-08T09:59:25Z
---


# Workflow
The certificate signing request and certificate revocation request workflow can be extended by custom workflow plugin.
            This can be used to synchronise statuses and interact between the ENM workflow and external workflow/ticketing system
            like JIRA.


## Adding workflow plugin
The workflow plugin can be configured via config file.

For certificate signing request:

```guess
workflow {
    issuer {
        type = ISSUANCE
        updateInterval = 10000

        enmListener = {
            port = 6000
        }

        workflow {
            plugin = "com.r3.enm.services.identitymanager.workflow.StubbedWorkflowPlugin"
            config {
                customConfig = "some config"
                .
                .
                .
            }
        }
    }
}
```
For certificate revocation request:

```guess
workflow {
    issuer {
        type = ISSUANCE
        updateInterval = 10000

        enmListener = {
            port = 6000
        }

        plugin {
            pluginClass = "com.r3.enm.services.identitymanager.workflow.StubbedWorkflowPlugin"
            config {
                customConfig = "some config"
                .
                .
                .
            }
        }
    },
    revoker {
        type = REVOCATION
        crlCacheTimeout = 1000
        crlFiles = ["./crl-files/subordinate.crl"]
        enmListener = {
            port = 6001
            reconnect = true
            ssl = {
                keyStore = {
                    location = ./certificates/corda-ssl-identity-manager-keys.jks
                    password = password
                }
                trustStore = {
                    location = ./certificates/corda-ssl-trust-store.jks
                    password = trustpass
                }
            }
        }

        plugin = {
            pluginClass = "com.r3.enm.services.identitymanager.workflow.StubbedWorkflowPlugin"
            config {
                customConfig = "some config"
                .
                .
                .
            }
        }
    }
}
```

## Creating a workflow plugin
The workflow plugin must extend *WorkflowPlugin* for certificate signing request or certificate revocation request respectively, issuance and revocation workflows
                can be configured with specific plugin classes as per the configuration shown above. The plugin will need to be made available to the ENM process by including the plugin jar in the classpath.
                This can be done by specifying the jar path via the *pluginJar* configuration option.


{{< note >}}
For release 1.0 only a simple issuance and optional revocation workflow pair are supported.


{{< /note >}}

{{< note >}}
Currently, any implementation of the *WorkflowPlugin* interface **must** provide a constructor which takes exactly two arguments of types *com.typesafe.config.Config* and *com.r3.enm.workflow.api.plugins.PluginLogger* (in this order).


{{< /note >}}

{{< note >}}
CSR requests can contain additional information that can be used in the workflow plugins (see *Example 2*). This information comes in the form of a *String* token retrieved via **CertificateSigningRequest.submissionToken**. This submission token
                    can be added to the node’s configuration via the property *networkServices.csrToken*


{{< /note >}}

## Example 1
This sample workflow plugin creates a request file in *basedir* when the Identity Manager received a certificate signing request, user can then approve or reject the request by moving the request files to *approved* or *rejected* folder.
                The certificate signing process will then issue a certificate for the request (require signer configuration), and move the request files to *done* folder.

Config file:

```guess
address = "localhost:1300"

workflow {
     issuer {
         type = ISSUANCE
         updateInterval = 10000

         enmListener = {
             port = 6000
         }

         plugin {
            pluginClass = "com.r3.enm.workflow.api.example.FileBaseCSRPlugin"
            config {
                baseDir = "workflowDirectory"
            }
         }
     }
 }
```
File base plugin implementation:


## Example 2
This sample workflow auto-approves CSRs based on a token provided in the request.

Config file:

```guess
address = "localhost:1300"

    workflow {
         issuer {
             type = ISSUANCE
             updateInterval = 10000

             enmListener = {
                 port = 6000
             }

             plugin {
                pluginClass = "com.r3.enm.csrplugin.ExamplePlugin"
                pluginJar = "workflowPluginExample.jar"
                config {
                    .
                    .
                    .
                }
             }
         }
     }
```
```guess
class ExamplePlugin(config: Config?, val logger: PluginLogger) : WorkflowPlugin<CertificateSigningRequest> {

    private val done = ConcurrentHashMap<String, WorkflowPluginRequest?>()
    private val approved = ConcurrentHashMap<String, WorkflowPluginRequest?>()
    private val rejected = ConcurrentHashMap<String, WorkflowPluginRequest?>()

    override fun createTicket(request: CertificateSigningRequest) {
        logger.info {"Creating CSR with id ${request.requestId}"}
        if (validate(request.submissionToken)) {
            approved[request.requestId] = WorkflowPluginRequest(request.requestId, RequestStatus.APPROVED, "Me")
        } else {
            rejected[request.requestId] = WorkflowPluginRequest(request.requestId, RequestStatus.REJECTED, "Me", RejectionData(
                RejectionReason.UNPARSEABLE("Missing or unknown CSR token"), "Git gud!")
            )
        }
    }

    override fun getRequest(requestId: String): WorkflowPluginRequest? {
        logger.info { "Fetching request $requestId" }
        return done.getOrDefault(requestId, approved.getOrDefault(requestId, rejected.getOrDefault(requestId, null)))
    }

    override fun markAsDone(request: CertificateSigningRequest) {
        logger.info { "Marking CSR ${request.requestId} as done" }
        with (request.requestId) {
            if (approved.containsKey(this)) {
                done[this] = approved[this]?.copy(status = RequestStatus.DONE)?.also { approved.remove(this) }
            } else if (rejected.contains(this)) {
                done[this] = rejected[this]?.copy(status = RequestStatus.DONE)?.also { rejected.remove(this) }
            }
        }
    }

    private fun validate(token: String?): Boolean {
        return token?.let {
            it == "CENM"
        } ?: false
    }
}
```

## Certificate Signing Request Rejection Reasons
The workflow is expected to provide a valid rejection reason (see below for allowed values) for each certificate
                signing request being rejected.
                Those rejection reasons are then forwarded and passed to a node in its certificate
                signing request polling status check response. Specifically, such response will have the rejection reason code set in its
                response “CSR-Rejection-Reason” header as well as in the response body, which additionally is extended with the natural-language
                description of the rejection reason.

Permitted certificate signing request rejection reasons are as follows:


{{< table >}}

|Rejection Code|Type|Rejection Description|
|--------------------|---------------------------------|----------------------------------------------------------------------------------------------------|
|0|UNKNOWN|The rejection reason is not known.|
|1|INCORRECT_X500_NAME_FORMAT|Legal name is incorrectly formatted.|
|2|DUPLICATE_X500_NAME|Legal name is duplicated.|
|3|DUPLICATE_PUBLIC_KEY|Public key is duplicated.|
|4|CERTIFICATE_ROLE_NOT_ALLOWED|Requested certificate role is not allowed.|
|5|REQUESTED_BY_NODE_OPERATOR|Rejection requested by the node operator.|
|6|REQUESTED_BY_NETWORK_OPERATOR|Rejection requested by the business network operator.|
|7|CHECK_NOT_PASSED|Legal entity check not passed.|
|8|SANCTIONED|On a Sanctions Watchlist.|
|9|EMAIL_DOES_NOT_MATCH|Domain of email address listed in X500 does not match Legal Entity owner (according to whois.com).|
|10|PTOU_NOT_SIGNED|Participant Terms Of Use not signed.|
|11|OTHER|Other.|

{{< /table >}}

{{< warning >}}
The above are the only values accepted from the workflow plugin. Any other values will result in UNKNOWN reason
                    being set.


{{< /warning >}}

### Node CSR Rejection Response
Node CSR rejection response follows the following format:

“Rejection reason code: <<Rejection Code>>. Rejection reason description: <<Rejection Description>>. Additional remark: <<Remark If Any>>.”

**Example response to a node when its CSR has been rejected:**

HTTP Response header:

“CSR-Rejection-Reason”: [“8”]

Response Body:

Rejection reason code: 8. Description: On a Sanctions Watchlist. Additional remark: No additional remark.”


