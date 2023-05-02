---
date: '2023-02-23'
title: "Packaging"
project: corda
version: 'Corda 5.0'
menu:
  corda5:
    identifier: corda5-develop-packaging
    parent: corda5-develop
    weight: 4000
section_menu: corda5
---
Just like a regular application, your CorDapp must be packaged for distribution and installation. Corda takes a three-layered model to its packaging design to allow maximum reusability and portability:

1. **Corda Package (CPK)** — represents a single code-entity authored by a CorDapp developer. CPKs are the Corda equivalent of a software library. They represent testable, reusable, sub-components of a final application. Corda runs each CPK in its own sandbox, isolated from other CPKs.
2. **Corda Package Bundle (CPB)** — built using a collection of CPKs, which represents a full application. CPBs are complete applications minus the “run time information” needed to onboard entities into it. CPBs represent the final efforts of the development team, a discrete and testable application, encapsulating the solution to a problem that can be deployed to form an application network.
3. **Corda Package Installer (CPI)** — contains the CPB and information about the network. The Network Operator builds this when [onboarding members]({{< relref "../../application-networks/creating/members/_index.md" >}}).

## Build a CPK

To build a CPK:

1. Add the CPK plugin to your project by adding the following to the top of the `build.gradle` file of your CorDapp Gradle project:
   ```
   plugins {
       id 'net.corda.plugins.cordapp-cpk2'
   }
   ```

2. Run the `jar` Gradle task:
   ```
   ./gradlew jar
   ```

## Build a CPB



### Build a CPB Using Gradle

To build a CPB:

1. Add the add the CPB plugin to your project by adding the following to the top of the `build.gradle` file of your CorDapp Gradle project:
   ```
   plugins {
       id 'net.corda.plugins.cordapp-cpb2'
   }
   ```

2. Run the `cbp` Gradle task:
   ```
   ./gradlew cpb
   ```

#### Build a CPB Using the Corda CLI



For more information about the Corda CLI `package` command, see the [Corda CLI Refernce]({{< relref "../../../reference/corda-cli/package.md" >}}).

## Sign a CPB

CPBs muct be signed with a key that you can share with the Network Operator responsible for building the CPI from the CPB. 

{{< note >}} 
You should always sign test CPBs with a different key used only for testing. The final key that the Network Operator uses should not be used for signing until you are ready to release.
{{< /note >}}

For example, to generate a code signing key:

```
keytool -genkeypair -alias "<key-alias>" -keystore <signingkeys.pfx> -storepass "<keystore-password>" -dname "cn=<CPI Plugin Example - Signing Key 1, o=R3, L=London, c=GB>" -keyalg RSA -storetype pkcs12 -validity 4000
```

{{< warning >}}
Never commit your keystore to git.
{{< /warning >}}