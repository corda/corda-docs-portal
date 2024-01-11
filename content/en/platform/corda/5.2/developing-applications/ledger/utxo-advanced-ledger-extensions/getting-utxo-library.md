---
description: "Learn how to include the Corda 5 Advanced UTXO Ledger Extensions library in your project."
date: '2023-07-04'
title: "Including the UTXO Extensions Library"
project: corda
version: 'Corda 5.2'
menu:
  corda52:
    identifier: corda52-utxo-ledger-getting-utxo-library
    parent: corda52-utxo-advanced-ledger-extensions
    weight: 1000
section_menu: corda52
---

# Including the UTXO Extensions Library

The Advanced UTXO Ledger Extensions library is an external library and not part of Corda 5. To source it
from Maven Central Repository, do the following:

1. Ensure that the repositories block of the project has `mavenCentral()` declared in the following way:

   ```
   repositories {
       mavenCentral()
       // other repos
   }
   ```

2. Add the following code to the project's main `build.gradle` file:

   ```gradle
   cordaUtxoLibGroupId=com.r3.corda.ledger.utxo
   cordaUtxoLibVersion=0.9.0
   ```

3. Add the following dependencies to the project's contract sub-module `build.gradle` file:

   ```gradle
   dependencies {
       cordapp "$cordaUtxoLibGroupId:corda-ledger-extensions-base:$cordaUtxoLibVersion"
       cordapp "$cordaUtxoLibGroupId:corda-ledger-extensions-fungible:$cordaUtxoLibVersion"
       cordapp "$cordaUtxoLibGroupId:corda-ledger-extensions-identifiable:$cordaUtxoLibVersion"
       cordapp "$cordaUtxoLibGroupId:corda-ledger-extensions-issuable:$cordaUtxoLibVersion"
       cordapp "$cordaUtxoLibGroupId:corda-ledger-extensions-ownable:$cordaUtxoLibVersion"

       ...etc.
   }
   ```
