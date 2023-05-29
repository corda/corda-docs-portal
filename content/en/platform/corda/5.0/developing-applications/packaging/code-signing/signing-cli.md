---
date: '2023-05-18'
version: 'Corda 5.0'
title: "Signing Packages Using Corda CLI"
menu:
  corda5:
    parent: corda5-develop-packaging-code-signing
    identifier: corda5-develop-packaging-code-signing-signing-cli
    weight: 2000
section_menu: corda5
---

# Signing Packages Using Corda CLI

You can sign the CPK, CPB, and CPI packages using Corda CLI. Corda CLI is particularly useful for CorDapp developers or CorDapp distributors
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

2. Build a CPI version 2:
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

3. Pipe group policy into CPI version 2:
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

