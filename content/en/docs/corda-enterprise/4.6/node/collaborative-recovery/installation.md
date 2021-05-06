---
date: '2020-04-24T12:00:00Z'
menu:
  corda-enterprise-4-6:
    parent: corda-enterprise-4-6-corda-nodes-collaborative-recovery
tags:
- disaster recovery
- collaborative recovery
- install
- node operator

title: Install Collaborative Recovery V1.1
weight: 150
---

# Install the Collaborative Recovery CorDapps V1.1

**Who this documentation is for:**
* Node operators
* Business Network Operators (BNOs)
* Corda developers

For Collaborative Recovery to be effective if it’s ever needed, you should install the required CorDapps as early as possible. You may be able to install them during a disaster scenario, but it saves valuable time to prepare in advance. This also allows other nodes in the network to reconcile/recover from you.

If you are part of an operating Business Network, Corda Network or Segregated Sub-Zone that does not currently mandate that all nodes run disaster recovery, you should recommend these measures are taken. Collaborative Recovery can only be successful if all nodes on the network have the appropriate CorDapps installed and up to date.

Outline of steps for installation:

1.  Check the requirements for Collaborative Recovery - both on your local environment and your Business Network.

2.  Database requirements and operations outline.

3.  Prepare your node for installation.

4.  Install and check the CorDapps.

5.  Run database migrations.

6.  Verify installation.


## Requirements

* [**LedgerGraph** CorDapp](./../operating/ledger-graph). The collaborative recovery CorDapps depend on the LedgerGraph CorDapp.

* **Corda Enterprise** Corda nodes must be running Corda Enterprise in order to initiate or participate in Collaborative Recovery. This feature is not available for Corda Open Source nodes.

* **Node Minimum Platform Version (MPV) > 6** Collaborative Recovery requires operative Corda nodes to have a Corda Platform Version (CPV) of 6 or greater. This version number is related to the version of Corda a node is running.

* **Network MPV > 6** In addition to a CPV of greater than 6, the network itself must have a sufficient MPV.

* **Database requirements** Collaborative Recovery CorDapps are tested against Corda Enterprise and will work according to the [platform support matrix](../../platform-support-matrix).


## Install the CorDapps

### Pre-installation check

The first step in the installation of Collaborative Recovery CorDapps is to obtain the `.jar` files (distributable binaries that the Corda node will run). These should be provided by your Corda Representative.
Once you have obtained these CorDapps in a distributable format, you are ready to install them into your operating Corda node.

{{< attention >}}
If possible, you should perform this installation in a maintenance window or other prescheduled and communicated time slot, as the process requires your node to be down for a short period of time. This means your node will be unable to receive or sign incoming transactions for the duration of the installation process.
{{< /attention >}}

You should have access to two individual `.jar` files - representing LedgerSync and LedgerRecovery respectively. You should be able to access these files readily on the machine from which you will be performing the installation.

### Step 1: Initiate flow draining mode

In order to safely install the Collaborative Recovery CorDapps, all pending Corda Flows must finish executing. This can be accomplished by enabling `flowDrainingMode`, which is a configuration setting that causes the node to no longer accept any incoming instructions to initiate new flows or accept newly initiated incoming flows. Instead, only currently checkpointed flows will continue to execute until the node is `drained` of any pending activity. This can be done in one of two ways:

1. Via RPC - By using the `setFlowsDrainingModeEnabled` method with the parameter `true`.
2. Via the CRaSH Shell - By issuing the following command:
    `run setFlowsDrainingModeEnabled enabled: true`.

### Step 2: Shut down the node

Once the node has been successfully drained of any pending activity, you will be able to shut it down safely. Use the following command to output a JSON representation of remaining checkpoints:

```ssh
checkpoints dump
```

If the resultant list is empty, the node has been successfully drained. If the list contains representations of in-flight flows, and continues to do so for an unreasonable amount of time, the flows may have become stuck. At this point, you may wish to kill the flows explicitly using the [`killFlow` API](../../cordapps/api-flows#killing-flows).

### Step 3: Install the CorDapps

There are three CorDapps to install:

* **LedgerSync**
* **LedgerRecovery**
* **LedgerGraph** if you have not already installed this separately.

Using the file transfer protocol of your choice, transfer the `.jar` files representing the required CorDapps to the `cordapps` directory of the Corda node.

Before proceeding, verify that the transfer was completed successfully by checking that the files are present in the CorDapps directory *and* the file sizes are the same as the sizes of the source `.jar` files you received.

### Step 4: Run any necessary database migrations

If you are using Corda with a permissioned database, you may need to [perform database migrations](../operating/node-operations-cordapp-deployment).

### Step 5: Restart the node

Restart the node in the manner in which the node was [originally started by the node operator](../deploy/deploying-a-node).

You have enabled your Corda node for Collaborative Recovery in the event of a disaster scenario.

### Step 6: Verify installation

Now that you have successfully installed the Collaborative Recovery CorDapps, you can verify that they are available for use. You can do this by
requesting a list of the flows available for initiating via the CRaSH shell.

In the CRaSH shell, run the following command:
`flow list`

You should now see a list of flows printed to the console, including those required to initiate Collaborative Recovery. Collaborative Recovery contains many
initiating flows, described in detail in this documentation. Verify that the list printed includes:

- `ScheduleReconciliationFlow`
- `AutomaticLedgerRecoverFlow`
- `InitiateManualRecoveryFlow`

## Next steps

Now that you have successfully installed and verified your Collaborative Recovery CorDapps, you can familiarise yourself with their use and configuration.
