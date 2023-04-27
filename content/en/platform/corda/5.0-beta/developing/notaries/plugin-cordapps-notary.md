---
date: '2022-01-05'
title: "Notary Plugin CorDapps"
menu:
  corda-5-beta:
    parent: corda-5-beta-notaries-overview
    identifier: corda-5-beta-notary-plugin-cordapps
    weight: 6000
section_menu: corda-5-beta

---

# Notary Plugin CorDapps

In Corda 5, notary functionality is provided in the form of plugin CorDapps. In theory, anyone can write a new notary protocol by implementing their own CorDapps. However, initially, it is expected to only have protocols provided by R3. For a given notary protocol, two CPBs (Corda Package Bundles) are expected to be required:

* A **client**, or **application** CPB, which should be used to generate a CPI (Corda Package Installer) associated with application virtual nodes. At a minimum, this would contain a CPK (Corda Package) that has an initiating flow that is automatically invoked by the Corda 5 flow framework to initiate a notarization request.

* A **notary server** CPB (Corda Package Bundle), which should be used to generate a CPI associated with notary virtual nodes. At a minimum, this would contain a CPK that has a responder flow to what is packaged in the client CPB.

For Corda 5.0, only a single notary protocol will be provided, the **non-validating notary protocol**.

## Plugin Packaging
The details of this architecture and the steps you need to take in order to successfully build your CorDapp will be outlined in the following sections. For information on how to deploy a functioning network, see the [deployment]({{< relref "../../../5.0-beta/deploying/notaries/notary-deployment.md" >}}) section.

{{< figure src="c5-non-validating-notary.png" figcaption="The CPKs, CPBs and CPIs involved in getting a functioning network that can run a notary (and by extension, UTXO ledger functionality)" alt="Corda 5 non-validating notary" >}}

## Notary CPKs
There are four modules/CPKs of relevance to the non-validating notary protocol, which are then packaged into two different CPBs. These are:

* **`notary-common`**: This contains useful library functionality that is not specific to a particular notary protocol. For example, it defines the structure of an error that may be returned by a notary protocol. This is an example of something that must be standard cross-protocol, because the UTXO ledger depends on this format to perform processing, and the ledger has no visibility of the specific notary protocol that performs notarisation.

* **`non-validating-notary-api`**: This contains the payload definition that is used to communicate between the non-validating notary client and server CPKs. Extreme caution must be taken when making changes to this module, as backwards compatibility concerns must be taken into account.

* **`non-validating-notary-client`**: This is intended to run on application virtual nodes, and provides a sub-flow that initiates a notarization request to a notary virtual node when requested by the ledger finality flow.

* **`non-validating-notary-server`**: This provides a responder flow to the corresponding initiator flow in the client package, and will perform notarization processing.

The source code for all of these modules can be found under the [notary-plugins area of corda-runtime-os](https://github.com/corda/corda-runtime-os/tree/release/os/5.0/notary-plugins).

## Notary Server CPB

The non-validating notary server CPB only contains CPKs that are produced by R3. Therefore, to improve the user experience, R3 also produces a standard non-validating notary server CPB. 

### Downloading the CPB

This CPB is available from our [GitHub release page](https://github.com/corda/corda-runtime-os/releases/).

The following is an example Gradle configuration fragment that downloads this:

```kotlin
configurations {
    notaryServerCPB {
        canBeConsumed = false
        canBeResolved = true
    }
}

dependencies {
    notaryServerCPB("com.r3.corda.notary.plugin.nonvalidating:notary-plugin-non-validating-server:$cordaNotaryPluginsVersion") {
        artifact {
            classifier = 'package'
            extension = 'cpb'
        }
    }
}

tasks.register("getNotaryServerCPB", Copy) {
    group = pluginImplGroupName
    from configurations.notaryServerCPB
    into cordaNotaryServerDir
}
```

### Trust the Signing Key

For this beta release, the notary server CPB is signed with a test signing key. To use it, import the certificate, as follows:
1. Save the following text into a file named `beta-ca-root.pem`:
   ```shell
   -----BEGIN CERTIFICATE-----
   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
   0OXjjmtQ
   -----END CERTIFICATE-----
   ```
   
   2. Import the `beta-ca-root.pem` file into the keystore:
   ```
   keytool -importcert -keystore signingkeys.pfx -storepass "keystore password" -noprompt -alias beta-ca-root -file beta-ca-root.pem
   ```

## Application CPB

It is not possible to provide a standard application CPB, because the contents of this depend on the writer of a CorDapp. The writer of a CorDapp must decide which CPKs they will bundle together to provide their application CPB. This will be comprised of one or more CPKs which provide the application functionality. However, the CorDapp developer must also bundle the appropriate CPKs for the notary protocols their CorDapp will support.

The decision on which protocols to support is trivial at present, given there is only a single notary protocol to choose; the decision is purely based on whether the CorDapp is using the UTXO ledger model or not. If it is, then the CorDapp developer must bundle the `notary-common`, `non-validating-notary-api` and `non-validating-notary-client` CPKs when creating their CPB. Otherwise, there is no requirement to bundle any additional CPKs (as the notary is not involved in flow only or consensual ledger based CorDapps).

The easiest way to ensure your CorDapp includes the necessary CPKs is to use the CorDapp dependency functionality of the CPK Gradle plugin. You need to add the following to your Gradle dependency configuration, where `cordaNotaryPluginsVersion` is an appropriate version of `corda-runtime-os`, as the notary plugin currently lives as part of this repository.

```kotlin

cordapp "com.r3.corda.notary.plugin.nonvalidating:notary-plugin-non-validating-client:$cordaNotaryPluginsVersion"

```


{{< note >}}
It is only necessary to specify a dependency on the client CPK; this itself depends on the API and notary common CPKs, so these transitive dependencies will also be pulled in when constructing your application CPB.
{{< /note >}}

The other way to form your application CPB is to use the `corda-cli` tool. However, if you choose to use this, you will need to explicitly specify all three of the required CPKs (`notary-common`, `non-validating-notary-api` and `non-validating-notary-client`).

## CPI Creation

Having two CPBs for the application and notary virtual node roles on the network also extends to needing two different CPIs. This process is unchanged but ensure the following:
* the notary server CPB signing key is used to create the CPI and and then imported to Corda
* the same group policy file is used when creating both the application and notary CPIs
