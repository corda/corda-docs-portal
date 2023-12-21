---
description: "Learn how to sign Corda Package (CPK), Corda Package Bundle (CPB), and Corda Package Installer (CPI) files using the Corda CLI."
date: '2023-08-10'
version: 'Corda 5.1'
title: "Signing Packages Using Corda CLI"
menu:
  corda51:
    parent: corda51-develop-packaging-code-signing
    identifier: corda51-develop-packaging-code-signing-signing-cli
    weight: 2000
section_menu: corda51
---

# Signing Packages Using Corda CLI

You can sign the CPK, CPB, and CPI packages using {{< tooltip >}}Corda CLI{{< /tooltip >}}. Corda CLI is particularly useful for {{< tooltip >}}CorDapp{{< /tooltip >}} developers or CorDapp distributors
who need to sign their files after the QA process, when they are ready to release.
The following steps will guide you through the process of removing existing (development) signatures and applying new ones.

1. Remove the existing signatures and apply new ones:
```shell
./corda-cli.sh package sign \
mycpb.cpb \
--file signed.cpb \
--keystore signingkeys.pfx \
--storepass "keystore password" \
--key "signing key 1"
```

2. Build a CPI (version 2).
   You can supply the group policy file into the CPI by either passing it to the CLI `package` command parameters as a file
   or by piping it to the CLI `package` command as shown below:

   * Use a command:
   ```shell
   ./corda-cli.sh package create-cpi \
   --cpb mycpb.cpb \
   --group-policy TestGroupPolicy.json \
   --cpi-name "cpi name" \
   --cpi-version "1.0.0.0-SNAPSHOT" \
   --file output.cpi \
   --keystore signingkeys.pfx \
   --storepass "keystore password" \
   --key "signing key 1"
   ```

   * Or pipe the group policy:
   ```shell
   ./corda-cli.sh mgm groupPolicy | ./corda-cli.sh package create-cpi \
   --cpb mycpb.cpb \
   --group-policy - \
   --cpi-name "cpi name" \
   --cpi-version "1.0.0.0-SNAPSHOT" \
   --file output.cpi \
   --keystore signingkeys.pfx \
   --storepass "keystore password" \
   --key "signing key 1"
   ```

4. Check signatures using `jarsigner`:
```shell
jarsigner -keystore signingkeys.pfx -storepass "keystore password" -verbose -certs  -verify output.cpi
```

