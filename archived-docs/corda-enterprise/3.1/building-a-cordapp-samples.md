---
aliases:
- /releases/3.1/building-a-cordapp-samples.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-3-1:
    identifier: corda-enterprise-3-1-building-a-cordapp-samples
    parent: corda-enterprise-3-1-building-a-cordapp-index
    weight: 1140
tags:
- building
- cordapp
- samples
title: CorDapp samples
---
{{% important %}}
This documentation is unsupported.
Try [Corda Enterprise 3.3 documentation](/docs/corda-enterprise/3.3/_index.md) instead
{{% /important %}}


# CorDapp samples

There are two distinct sets of samples provided with Corda, one introducing new developers to how to write CorDapps, and
more complex worked examples of how solutions to a number of common designs could be implemented in a CorDapp.
The former can be found on [the Corda website](https://www.corda.net/samples/). In particular, new developers
should start with the [example CorDapp](tutorial-cordapp.md).

The advanced samples are contained within the *samples/* folder of the Corda repository. The most generally useful of
these samples are:


* The *trader-demo*, which shows a delivery-vs-payment atomic swap of commercial paper for cash
* The *attachment-demo*, which demonstrates uploading attachments to nodes
* The *bank-of-corda-demo*, which shows a node acting as an issuer of assets (the Bank of Corda) while remote client
applications request issuance of some cash on behalf of a node called Big Corporation

Documentation on running the samples can be found inside the sample directories themselves, in the *README.md* file.

{{< note >}}
If you would like to see flow activity on the nodes type in the node terminal `flow watch`.

{{< /note >}}
Please report any bugs with the samples on [GitHub](https://github.com/corda/corda/issues).

