---
date: '2023-01-06'
menu:
  corda5:
    identifier: corda5-cordacli-develop-commands
    weight: 4000
    parent: corda5-cli-reference
section_menu: corda5
title: "package"
---

This section lists the Corda CLI `package` arguments. You can use these commands to execute operations for working with CPB and CPI files<!--, as described in the [CorDapp Packaging]() tutorial-->.

| <div style="width:160px">Argument</div> | Description                                        |
| --------------------------------------- | -------------------------------------------------- |
| \-\-create-cpb                          | Creates a CPB file. See [create-cpb](#create-cpb). |
| \-\-create-cpi                          | Creates a CPI file. See [create-cpi](#create-cpi). |

## create-cpb

The `create-cpb` argument creates a CPB file from a set of CPK files using the following arguments:

| <div style="width:160px">Argument</div> | Description                                        |
| --------------------------------------- | -------------------------------------------------- |
| \-\-cpb-name                            | Specifies a name for the CPB.                      |
| \-\-cpb-version                         | Specifies the CPB version.                         |
| \-\-file                                | Specifies the name of the CPB file to create.      |
| \-\-keystore                            | Specifies the keystore file used to sign the file. |
| \-\-storepass                           | Specifies the password for the keystore.           |
| \-\-key                                 | Specifies the name of the key.                     |

For example:

   {{< tabs name="create-cpb">}}
   {{% tab name="Bash" %}}
   ```sh
   ./corda-cli.sh package create-cpb \
    mycpk0.cpk mycpk1.cpk \
    --cpb-name manifest-attribute-cpb-name \
    --cpb-version manifest-attribute-cpb-version \
    --file output.cpb \
    --keystore signingkeys.pfx \
    --storepass "keystore password" \
    --key "signing key 1"
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
    ./corda-cli.cmd package create-cpb `
    mycpk0.cpk mycpk1.cpk `
    --cpb-name manifest-attribute-cpb-name `
    --cpb-version manifest-attribute-cpb-version `
    --file output.cpb `
    --keystore signingkeys.pfx `
    --storepass "keystore password" `
    --key "signing key 1"
   ```
   {{% /tab %}}
   {{< /tabs >}}

## create-cpi

The `create-cpi` argument creates a CPI file using the following arguments:

| <div style="width:160px">Argument</div> | Description                                                                                 |
| --------------------------------------- | ------------------------------------------------------------------------------------------- |
| \-\-cpb                                 | Specifies the CPB file to include in the CPI.                                               |
| \-\-group-policy                        | Specifies the [group policy file](../../deploying/group-policy.html) to include in the CPI. |
| \-\-cpi-name                            | Specifies a name for the CPI.                                                               |
| \-\-cpi-version                         | Specifies the CPI version.                                                                  |
| \-\-file                                | Specifies the name of the CPI file to create.                                               |
| \-\-keystore                            | Specifies the keystore file used to sign the file.                                          |
| \-\-storepass                           | Specifies the password for the keystore.                                                    |
| \-\-key                                 | Specifies the name of the key.                                                              |

For example:

   {{< tabs name="create-cpi">}}
   {{% tab name="Bash" %}}
   ```sh
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
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
    ./corda-cli.cmd package create-cpi `
    --cpb mycpb.cpb `
    --group-policy TestGroupPolicy.json `
    --cpi-name "cpi name" `
    --cpi-version "1.0.0.0-SNAPSHOT" `
    --file output.cpi `
    --keystore signingkeys.pfx `
    --storepass "keystore password" `
    --key "signing key 1"
   ```
   {{% /tab %}}
   {{< /tabs >}}
