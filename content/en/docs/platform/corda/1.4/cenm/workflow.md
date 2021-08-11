---
aliases:
- /workflow.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-4:
    identifier: cenm-1-4-workflow
    parent: cenm-1-4-configuration
    weight: 260
tags:
- workflow
title: Workflow
---


# Workflow

The certificate signing request and certificate revocation request workflow can be extended by custom workflow plugin.
This can be used to synchronise statuses and interact between the CENM workflow and external workflow/ticketing system
like JIRA.


## Adding workflow plugin

The workflow plugin can be configured via configuration file.

For certificate signing request:

```guess
workflows {
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
    }
}
```

For certificate revocation request:

```guess
workflows {
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

The workflow plugin must extend `WorkflowPlugin` for certificate signing request or certificate revocation request respectively, issuance and revocation workflows
can be configured with specific plugin classes as per the configuration shown above. The plugin will need to be made available to the CENM process by including the plugin `.jar` in the classpath.
This can be done by specifying the `.jar` path via the `pluginJar` configuration option.

{{< note >}}
For release 1.0 only a simple issuance and optional revocation workflow pair are supported.

{{< /note >}}
```kotlin
/*
 * R3 Proprietary and Confidential
 *
 * Copyright (c) 2018 R3 Limited.  All rights reserved.
 *
 * The intellectual and technical concepts contained herein are proprietary to R3 and its suppliers and are protected by trade secret law.
 *
 * Distribution of this file or any portion thereof via any medium without the express permission of R3 is strictly prohibited.
 */

package com.r3.enm.workflow.api

import com.r3.enm.model.Request
import com.r3.enm.nsdefaults.ENMDefaults
import net.corda.core.identity.CordaX500Name

/**
 * Workflow plugin interface for adding custom functionality to the network services workflow.
 * @param <R> Type of the request
 */
interface WorkflowPlugin<R : Request> {
    /**
     * Create ticket in the external system. The method will ensure that the ticket is created.
     * The request remains in [RequestStatus.NEW] state and a workflow may keep trying to create the ticket
     * in the external system until the request is updated to [RequestStatus.APPROVED],
     * [RequestStatus.REJECTED] or [RequestStatus.DONE].
     */
    fun createTicket(request: R)

    /**
     * Move ticket status to done state, the status of the request will be updated to [RequestStatus.DONE] once this method is executed successfully.
     */
    fun markAsDone(request: R)

    /**
     * Retrieve ticket with the given request ID.
     */
    fun getRequest(requestId: String): WorkflowPluginRequest?

    /**
     * Runs the interactive shell commands of the plugin.
     */
    fun runCommandDriver() {}

    /**
     * Retrieve the alias for the plugin.
     */
    fun getAlias(): String = ENMDefaults.NOT_AVAILABLE
}

/**
 * Command driver interface for adding custom functionality for interacting with users via the interactive shell
 */
interface CommandDriver {
/**
 * Outputs a menu based on the available commands defined within the class, containing the methods for handling any
 * further interaction logic.
 */
    fun showMenu()
}

/**
 * A class representing the workflow plugin request data.
 */
data class WorkflowPluginRequest(val requestId: String,
                                 val status: RequestStatus,
                                 val modifiedBy: String? = null,
                                 val rejectionData: RejectionData? = null,
                                 val legalName: CordaX500Name? = null)

```

{{< note >}}
Currently, any implementation of the `WorkflowPlugin` interface **must** provide a constructor which takes
exactly two arguments of types `com.typesafe.config.Config` and `com.r3.enm.workflow.api.plugins.PluginLogger` (in this order).

{{< /note >}}
{{< note >}}
CSR requests can contain additional information that can be used in the workflow plugins (see *Example 2*).
This information comes in the form of a `String` token retrieved via `CertificateSigningRequest.submissionToken`.
This submission token can be added to the node’s configuration via the property `networkServices.csrToken`.

{{< /note >}}

## Example 1

This sample workflow plugin creates a request file in *basedir* when the Identity Manager received a certificate signing request, user can then approve or reject the request by moving the request files to *approved* or *rejected* folder.
The certificate signing process will then issue a certificate for the request (require signer configuration), and move the request files to *done* folder.

Config file:

```guess
address = "localhost:1300"

workflows {
    issuer {
        type = ISSUANCE
        updateInterval = 10000

        enmListener = {
            port = 6000
        }

        plugin {
            pluginClass = "com.r3.enmplugins.example.FileBaseCSRPlugin"
            config {
                baseDir = "workflowDirectory"
            }
        }
    }
}
```

File base plugin implementation:

```kotlin
package com.r3.enmplugins.example

import com.r3.enm.model.CertificateSigningRequest
import com.r3.enm.model.RejectionReason
import com.r3.enm.workflow.api.RejectionData
import com.r3.enm.workflow.api.RequestStatus
import com.r3.enm.workflow.api.WorkflowPlugin
import com.r3.enm.workflow.api.WorkflowPluginRequest
import com.r3.enm.workflow.api.plugins.PluginLogger
import com.typesafe.config.Config
import net.corda.core.internal.createDirectories
import net.corda.core.internal.list
import org.bouncycastle.openssl.jcajce.JcaPEMWriter
import org.bouncycastle.util.io.pem.PemObject
import java.io.StringWriter
import java.nio.file.Files
import java.nio.file.Path
import java.nio.file.Paths
import java.nio.file.attribute.FileOwnerAttributeView

class FileBaseCSRPlugin(
        config: Config?,
        val logger: PluginLogger
) : WorkflowPlugin<CertificateSigningRequest> {
    private val baseDir = if (config != null) {
        Paths.get(config.getString("baseDir") ?: "workflowDirectory")
    } else {
        Paths.get("workflowDirectory")
    }.also { it.createDirectories() }
    private val approvedFolder = baseDir.resolve("approved").also { it.createDirectories() }
    private val rejectedFolder = baseDir.resolve("rejected").also { it.createDirectories() }
    private val doneFolder = baseDir.resolve("done").also { it.createDirectories() }

    override fun getRequest(requestId: String): WorkflowPluginRequest? {
        logger.info("Retrieving CSR with id $requestId")
        return findWorkflowPluginRequest(requestId, baseDir, RequestStatus.NEW)
                ?: findWorkflowPluginRequest(requestId, approvedFolder, RequestStatus.APPROVED)
                ?: findWorkflowPluginRequest(requestId, rejectedFolder, RequestStatus.REJECTED)
                ?: findWorkflowPluginRequest(requestId, doneFolder, RequestStatus.DONE)
    }

    private fun findWorkflowPluginRequest(requestId: String, directory: Path, status: RequestStatus): WorkflowPluginRequest? {
        return directory.list().findLast { it.toFile().name == requestId }?.let {
            WorkflowPluginRequest(
                    requestId,
                    status,
                    Files.getFileAttributeView(it, FileOwnerAttributeView::class.java).owner.name,
                    RejectionData(RejectionReason.UNKNOWN, "Not specified"))
        }
    }

    override fun createTicket(request: CertificateSigningRequest) {
        val subject = request.legalName

        val data = mapOf(
                "Common Name" to subject.commonName,
                "Organisation" to subject.organisation,
                "Organisation Unit" to subject.organisationUnit,
                "State" to subject.state,
                "Nearest City" to subject.locality,
                "Country" to subject.country,
                "X500 Name" to subject.toString())

        val requestPemString = StringWriter().apply {
            JcaPEMWriter(this).use {
                it.writeObject(PemObject("CERTIFICATE REQUEST", request.pkcS10CertificationRequest.encoded))
            }
        }.toString()

        val ticketDescription = data.filter { it.value != null }.map { "${it.key}: ${it.value}" } + requestPemString

        Files.write(baseDir.resolve(request.requestId), ticketDescription)

        logger.info("Creating Certificate Signing Request ticket for request : ${request.requestId}")
    }

    override fun markAsDone(request: CertificateSigningRequest) {
        logger.info("Marking CSR as done")
        Files.move(approvedFolder.resolve(request.requestId), doneFolder.resolve(request.requestId))
    }
}

```


## Example 2

This sample workflow auto-approves CSRs based on a token provided in the request.

Config file:

```guess
address = "localhost:1300"

workflows {
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

Auto-approval plugin implementation:

```Kotlin
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

{{< note >}}
This example is not included in CENM and the user is expected to copy, modify or build as is,
deploy and test it.

{{< /note >}}

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
