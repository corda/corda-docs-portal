---
title: CDL to code
date: 2020-10-15T00:00:00+01:00
menu:
  cdl:
    identifier: "cdl-to-code"
    name: "Converting CDL smart contracts to code"
    weight: 300
tags:
- cdl
- cordapp design language
- contract to code
- cordapp diagram
- cdl-example
---

# Converting CDL smart contracts to code

Once you are happy with the structured design of your CorDapp, it's time to convert your design into executable code. Use this guide to establish a structured and systematic approach to converting your CDL smart contract diagrams into CorDapp code.

The examples in this section are taken from the cdl-example CorDapp located in the Corda Open Source Github repo: [corda/cdl-example](https://github.com/corda/cdl-example)

At present the examples are only available in Kotlin. However, the principles being employed will translate to Java and the functions provided in ContractUtils.kt can still be used by Contracts written in Java.

{{< note >}}
You should be aware that the cdl-example CorDapp is for use as an example only - it is not an official Corda product. It is only an illustration of one way a CDL Smart Contract view could be implemented. It has not gone through the rigorous Product and QA procedures that are part of the Corda platform development process, and should not be relied upon as production grade code.
{{< /note >}}
