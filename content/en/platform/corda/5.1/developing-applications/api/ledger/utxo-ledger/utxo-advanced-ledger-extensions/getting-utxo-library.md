---
date: '2023-07-04'
title: "Getting the UTXO Library"
project: corda
version: 'Corda 5.1'
menu:
  corda51:
    identifier: corda51-utxo-ledger-getting-utxo-library
    parent: corda51-utxo-advanced-ledger-extensions
    weight: 4490
section_menu: corda51
---

# Getting the UTXO Library

The Corda 5 Advanced {{< tooltip >}}UTXO{{< /tooltip >}} Ledger Extensions library is an external library and not part of Corda 5. It needs to be sourced
from Maven Central Repository or similar.

1. Ensure that the repositories block of the project has `mavenCentral()` declared in the following way:

   ```
   repositories {
       mavenCentral()
       // other repos
   }
   ```

2. Add the following code to the project's main `build.gradle` file:

   ```
   cordaUtxoLibGroupId=com.r3.corda.ledger.utxo
   cordaUtxoLibVersion=0.9.0
   ```

3. Add the following dependencies to the project's contract sub-module `build.gradle` file:

   ```
   dependencies {
       cordapp "$cordaUtxoLibGroupId:corda-ledger-extensions-base:$cordaUtxoLibVersion"
       cordapp "$cordaUtxoLibGroupId:corda-ledger-extensions-fungible:$cordaUtxoLibVersion"
       cordapp "$cordaUtxoLibGroupId:corda-ledger-extensions-identifiable:$cordaUtxoLibVersion"
       cordapp "$cordaUtxoLibGroupId:corda-ledger-extensions-issuable:$cordaUtxoLibVersion"
       cordapp "$cordaUtxoLibGroupId:corda-ledger-extensions-ownable:$cordaUtxoLibVersion"

       ...etc.
   }
   ```
