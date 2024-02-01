---
description: "Learn how to build a Corda Package Bundle (CPB) from your Corda Package (CPK) files using Gradle or the Corda CLI."
date: '2023-02-23'
title: "Build a CPB"
menu:
  corda51:
    parent: corda51-develop-packaging
    identifier: corda51-develop-packaging-cbp
    weight: 2000
---
# Build a CPB

You can build a CPB from your CPK files using one of the following:

* [Gradle]({{< relref "#build-a-cpb-using-gradle" >}})
* [Corda CLI]({{< relref "#build-a-cpb-using-the-corda-cli" >}})

## Build a CPB Using Gradle

To build a CPB using Gradle:

1. Add the CPB plugin to your project by adding the following to the start of the `build.gradle` file of your {{< tooltip >}}CorDapp{{< /tooltip >}} Gradle project:
   ```
   plugins {
       id 'net.corda.plugins.cordapp-cpb2'
   }
   ```

2. To sign your CPB, add a `cordapp/signing` section to the project `settings.gradle` file.

   {{< note >}}
By default, the CPB plugin signs with a default key. This key should only be used for local testing. You can deploy locally on a static network, using the [CSDE]({{< relref "../../../../../tools-corda5/csde/_index.md">}}).
CPBs for deployment on a dynamic network must be signed with a key that you can share with the Network Operator responsible for building the CPI from the CPB. 
You should always sign test CPBs with a different key used only for testing. The final key that the Network Operator uses should not be used for signing until you are ready to release. You can re-sign a CPB without building the project from source, using the [Corda CLI]({{< relref "#build-a-cpb-using-the-corda-cli" >}}).
   {{< /note >}}

3. Run the `cbp` Gradle task:
   ```
   ./gradlew cpb
   ```

## Build a CPB Using the Corda CLI

To build a CPB using the {{< tooltip >}}Corda CLI{{< /tooltip >}}:

1. Generate a code signing key. For example:

   ```
   keytool -genkeypair -alias "<key-alias>" -keystore <signingkeys.pfx> -storepass "<keystore-password>" -dname "cn=<CPI Plugin Example - Signing Key 1, o=R3, L=London, c=GB>" -keyalg <RSA> -storetype <pkcs12> -validity <4000>
   ```
   {{< note >}}
CPBs for deployment on a dynamic network must be signed with a key that you can share with the Network Operator responsible for building the CPI from the CPB. 
You should always sign test CPBs with a different key used only for testing. The final key that the Network Operator uses should not be used for signing until you are ready to release.
   {{< /note >}}

   {{< warning >}}
   Never commit your keystore to git.
   {{< /warning >}}

2. Use the Corda CLI `package` command, specifying the CPK files, the name, version, and file name of the CPB, and the details of the signing key:

   {{< tabs name="create-cpb">}}
   {{% tab name="Bash" %}}
   ```sh
   ./corda-cli.sh package create-cpb \
    <mycpk0.cpk> <mycpk1.cpk> \
    --cpb-name <manifest-attribute-cpb-name> \
    --cpb-version <manifest-attribute-cpb-version> \
    --file <output.cpb> \
    --keystore <signingkeys.pfx> \
    --storepass <"keystore password"> \
    --key <"signing key 1">
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
    ./corda-cli.cmd package create-cpb `
    <mycpk0.cpk> <mycpk1.cpk> `
    --cpb-name <manifest-attribute-cpb-name> `
    --cpb-version <manifest-attribute-cpb-version> `
    --file <output.cpb> `
    --keystore <signingkeys.pfx> `
    --storepass <"keystore password"> `
    --key <"signing key 1">
   ```
   {{% /tab %}}
   {{< /tabs >}}

   For more information about the Corda CLI `package` command, see the [Corda CLI Reference]({{< relref "../../reference/corda-cli/package.md" >}}) section.
