---
aliases:
- /releases/release-1.0/workflow.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-0:
    identifier: cenm-1-0-workflow
    parent: cenm-1-0-configuration
    weight: 250
tags:
- workflow
title: Workflow
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
            plugin = "com.r3.enmplugins.StubbedWorkflowPlugin"
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
            pluginClass = "com.r3.enmplugins.StubbedWorkflowPlugin"
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
            pluginClass = "com.r3.enmplugin.StubbedWorkflowPlugin"
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


## Creating workflow plugin

The workflow plugin must extend *CsrWorkflowPlugin* or *CrrWorkflowPlugin* for certificate signing request or certificate revocation request respectively, issuance and revocation workflows
can be configured with specific plugin classes as per the configuration show above.

{{< note >}}
for release 1.0 only a sinlle issuance and optional reovation workflow pair are supported.

{{< /note >}}
The plugin will need to be made available to the ENM process by including the plugin jar in the classpath.

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

package com.r3.corda.networkmanage.api.workflow

import com.r3.corda.networkmanage.api.model.Request

/**
 * Workflow plugin interface for adding custom functionality to the network services workflow.
 * @param <R> Type of the request
 */
interface WorkflowPlugin<R : Request> {
    /**
     * Create ticket in the external system. The method will ensure that the ticket is created.
     */
    fun createTicket(request: R)

    /**
     * Move ticket status to done state, the status of the request will be updated to [RequestStatus.DONE] once this method is executed successfully.
     */
    fun markAsDone(request: R)

    /**
     * Retrieve ticket with the given request ID
     */
    fun getRequest(requestId: String): WorkflowPluginRequest?
}

/**
 * A class representing the workflow plugin request data.
 */
data class WorkflowPluginRequest(val requestId: String,
                                 val status: RequestStatus,
                                 val modifiedBy: String? = null,
                                 val rejectionData: RejectionData? = null)
```

## Example

This sample workflow plugin creates a request file in *basedir* when the Identity Manager received a certificate signing request, user can then approve or reject the request by moving the request files to *approved* or *rejected* folder.
The certificate signing process will then issue a certificate for the request (require signer configuration), and move the request files to *done* folder

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
            pluginClass = "com.r3.corda.networkmanage.api.workflow.example.FileBaseCSRPlugin"
            config {
                baseDir = "workflowDirectory"
            }
         }
     }
 }
```

File base plugin implementation:

```kotlin
package com.r3.corda.networkmanage.api.workflow.example

import com.r3.corda.networkmanage.api.model.CertificateSigningRequest
import com.r3.corda.networkmanage.api.model.RejectionReason
import com.r3.corda.networkmanage.api.workflow.RejectionData
import com.r3.corda.networkmanage.api.workflow.RequestStatus
import com.r3.corda.networkmanage.api.workflow.WorkflowPlugin
import com.r3.corda.networkmanage.api.workflow.WorkflowPluginRequest
import com.typesafe.config.Config
import net.corda.core.internal.createDirectories
import net.corda.core.internal.list
import net.corda.core.utilities.loggerFor
import org.bouncycastle.openssl.jcajce.JcaPEMWriter
import org.bouncycastle.util.io.pem.PemObject
import java.io.StringWriter
import java.nio.file.Files
import java.nio.file.Path
import java.nio.file.Paths
import java.nio.file.attribute.FileOwnerAttributeView

class FileBaseCSRPlugin(
        config: Config
) : WorkflowPlugin<CertificateSigningRequest> {
    private val logger = loggerFor<FileBaseCSRPlugin>()
    private val baseDir = Paths.get(config.getString("baseDir")).also { it.createDirectories() }
    private val approvedFolder = baseDir.resolve("approved").also { it.createDirectories() }
    private val rejectedFolder = baseDir.resolve("rejected").also { it.createDirectories() }
    private val doneFolder = baseDir.resolve("done").also { it.createDirectories() }

    override fun getRequest(requestId: String): WorkflowPluginRequest? {
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
        Files.move(approvedFolder.resolve(request.requestId), doneFolder.resolve(request.requestId))
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


# Example response to a node when its CSR has been rejected:

HTTP Response header:

“CSR-Rejection-Reason”: [“8”]

Response Body:

Rejection reason code: 8. Description: On a Sanctions Watchlist. Additional remark: No additional remark.”
