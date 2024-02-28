---
description: Learn about the R3 notary protocols.
date: '2024-02-27'
title: "Notary Protocols"
menu:
  corda52:
    identifier: corda52-develop-notary-protocols
    parent: corda52-develop-notaries
    weight: 1000
---
# Notary Protocols

Notary functionality is provided in the form of plugin CorDapps. In theory, anyone can write a new notary protocol by implementing their own CorDapps. However, initially, it is expected to only use protocols provided by R3. For a given notary protocol, two {{< tooltip >}}CPBs{{< /tooltip >}} are required:

* A **client**, or **application** CPB, which is used to generate a {{< tooltip >}}CPI{{< /tooltip >}} associated with application virtual nodes. At a minimum, this contains a {{< tooltip >}}CPK{{< /tooltip >}} that has an initiating {{< tooltip >}}flow{{< /tooltip >}} that is automatically invoked by the Corda 5 flow framework to initiate a notarization request.
* A **notary server** CPB, which is used to generate a CPI associated with notary virtual nodes. At a minimum, this contains a CPK that has a responder flow to what is packaged in the client CPB.

For {{< version >}}, a [non-validating notary protocol]({{< relref "./non-validating-notary/_index.md" >}}) and a********
The non-validating notary protocol supports the UTXO ledger model. As outlined in the [Ledger section](******), this backchain verification based model is not suitable for a large scale token network that also needs very high performance, such as a digital currency.
The [contract-verifying notary protocol](****) provides an alternative approach to verifying that inputs to a transaction are trustworthy.

## Selecting a Protocol

This section outlines the [benefits](#backchain-skipping-benefits) and [drawbacks](#backchain-skipping-drawbacks) of backchain skipping (contract-verifying notary protocol) versus backchain resolution (non-validating notary protocol).

### Backchain Skipping Benefits

* **Enhanced privacy between participants**  - Participants only see the transactions that they are party to. While they need to see the inputs to a transaction to verify it before signing, they receive those as part of filtered transactions, so they only see exactly the required inputs.
* **Enhanced performance** - Instead of an ever growing backchain, Corda only requires a bundle with the direct inputs for each new transaction, so the throughput of the system will not start to degrade with long time use of tokens.
* **Reduced storage footprint** - Each member node only needs to store transactions it is involved in, and the direct inputs. Depending on the nature of the network application, this can lead to a drastic reduction in required database space.
* **Easier archiving** - Once all outputs from a transaction are spent, the transaction it will no longer be required, making it easier to deduce which parts of the ledger can be archived.
* **Eliminates denial of state attacks** - Running verification on the notary eliminates any risk of denial of state attacks by requesting notarizations of bogus transactions with known inputs. Every transaction has to conform to the contract rules of the network and is checked to carry the required signatures.

### Backchain Skipping Drawbacks

* **More trust in the notary operator** - Participants must all rely on the contract verifying notary working correctly, and the network traffic to the notary is increased. This must be taken into consideration when planning the network layout.
Furthermore, it will often be impossible to prove the validity of a transaction locally without relying on the verification run on the notary to endorse the validity of the inputs.
* **Increased notary operator responsibility** - Depending on the legal frameworks around the application network, the notary operator might become liable for the correctness of the contract verification.
* **Loss of privacy towards the notary operator** - In the classic UTXO model, only participants involved in transactions see the transaction and the backchain. The network operator and the notary never see any contents of the transactions, only the hashes and indices denoting the consumed and created states. In the contract-verifying model, the notary must process all transaction content, to enable a total view of all interactions on the global ledger. However, there is no requirement for the notary to store a copy of all the transaction data.
* **Loss of history** - No provenance or audit trail of a state is maintained without introducing special virtual nodes to observe all transactions in the network. If necessary, for example supply chain tracing this must be enforced by the smart contracts.
