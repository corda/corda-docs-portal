---
aliases:
- /tool-crr-submission.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-4:
    identifier: cenm-1-4-tool-crr-submission
    parent: cenm-1-4-tools-index
    weight: 1030
tags:
- tool
- crr
- submission
title: Certificate Revocation Request Submission Tool
---


# Certificate Revocation Request Submission Tool

The purpose of the Certificate Revocation Request (CRR) Submission Tool is to facilitate the process of creating a CRR.
The tool is designed with the support line in mind, and assumes it is for internal (i.e. within the Identity Manager Service managing company) usage.

It retrieves all the necessary data (for the CRR submission) throughout the execution process by asking the user for particular inputs.
The expected input from the user is following:


* Certificate Serial Number (if not known, it can be omitted)
* Certificate Signing Request Identifier (if not known, it can be omitted)
* Legal Name (if not known, it can be omitted)
* Revocation Reason (select one from the displayed list)
* Reporter (name or identifier of the person issuing the revocation request).

{{< note >}} You must provide a value for at least one of the first three input options. {{< /note >}}


## Running Tool

At start-up, the Certificate Revocation Request Submission Tool takes only one command-line argument: `--submission-url`,
that should be followed by the url to the certificate revocation request submission endpoint.

Example:

```bash
java -jar crrsubmissiontool.jar --submission-url http://<<CORDA_DOMAIN>>/certificate-revocation-request
```
