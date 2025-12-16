---
aliases:
- /upgrade-notes.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-5:
    identifier: cenm-1-5-upgrade-notes
    parent: cenm-1-5-cenm-releases
    weight: 180
    name: Upgrading CENM
tags:
- upgrade
- notes
title: Upgrading the Network Manager
---


# Upgrading Corda Enterprise Network Manager

This topic describes how to upgrade CENM from v1.3.x or v1.4.x to v1.5, including the following services:

- Identity Manager Service (formerly Doorman)
- Network Map Service
- Signing Service
- Zone Service
- Auth Service
- Angel Service

Also see the relevant [CENM Release Notes]({{< relref "release-notes.md" >}}) of the release in question. If not specified, you may assume the versions you are currently using are still in force.

{{< warning >}}
Before you start the upgrade, you must consult the above release notes to confirm all changes between releases.
{{< /warning >}}

## 1.3.x or 1.4.x to 1.5

### Database migrations

The Identity Manager Service, the Network Map Service, the Zone Service, and the Auth Service all require database migration.
To enable database migration, set `runMigration = true` in the database configuration. If a service is connecting to a database with restricted user,
you must temporarily change the service settings to connect with a privileged user (a user able to modify a database schema).

### Auth Service

The `baseline` configuration entry is obsolete and should be removed.
Ensure you have the CENM baseline JAR file `accounts-baseline-cenm-1.5.jar` that contains the set
of available permissions and predefined roles. Copy this file to a directory called `plugins`, located inside the working directory.

If existing passwords are not complex, add the configuration option to allow weaker passwords:

    passwordPolicy {
        ...
        mustMeetComplexityRequirements = false
    }

This new setting can be change to `true` or removed only after all users have changed their passwords to meet complexity requirements:

* Minimum 8 characters long.
* Maximum 50 characters long.
* Contains at least one number, one lower case character, and one upper case character.
* Does not contain regular sequences (like `abcdf` or `1234`) that are longer than three characters.
* Does not contain the user name.

### Identity Manager Workflow Plugin changes

If you are using a custom Identity Manager Workflow Plugin then
a non-backwards compatible change introduced in CENM 1.5 may require to recompile your plugin.

One of the API classes has been modified to contain a new field related to certificate re-issuance.
If you are running Identity Manager Service with your own custom `com.r3.enm.workflow.api.WorkFlowPlugin` implementation,
you may require to recompile the plugin code.
If certificate re-issuance is planned to be performed, then the new field can be used in your plugin.

The class `com.r3.enm.workflow.api.WorkflowPlugin` is parameterised by `com.r3.enm.model.Request` type.
A plugin code for CSR may use the concrete version of this type com.r3.enm.model.CertificateSigningRequest.
If you instantiate CertificateSigningRequest class in your plugin then you need to recompile the plugin code.
The class CertificateSigningRequest contains new member field `type` of `Enum` type `com.r3.enm.model.CsrRequestType`.
The Enum has 3 possible values `CSR`, `REISSUE_SIGNED`, `REISSUE_UNSIGNED` denoting respectively a normal CSR requests,
a re-issue request, and a re-issue request additionally singed by the existing certificate
(see detailed explanation in the certificate re-issuance documentation).
You may use the new field to perform additional operation, for example a request marked as `REISSUE_SIGNED` can be automatically
marked by your plugin as approved in your Workflow Management System.

You don't need to change your code if you are not intended to use CENM certificate re-issuance functionalities.
If your plugin class doesn't use CertificateSigningRequest class and only abstract type Request,
then there's no need to recompile plugin.

### Gateway Service - new CENM Web UI

In Gateway Service create a new directory called `plugins`, located inside the working directory.
Copy the `cenm-gateway-plugin-1.5.0.jar`. The plugin contains the new CENM Web UI.