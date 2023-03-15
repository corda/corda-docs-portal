---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-8:
    parent: corda-enterprise-4-8-monitoring-logging
tags:
- checkpoint
- tooling
title: Troubleshooting stuck flows
weight: 120
---

Use the checkpoint tools to diagnose the causes of stuck flows.

## Identify the stuck flow logs and checkpoints

1. Use the `flow watch` command to see the flows in progress on your node. Flows that are marked `In progress` have not completed and will have saved checkpoints.

2. Check the node log file for *hospitalisation* and/or *flow retry* messages. The node logs can be found in the `logs` directory.

    ```
    [INFO ] 2019-07-11T17:56:43,227Z [pool-12-thread-1] statemachine.FlowMonitor. - Flow with id 90613d6f-be78-41bd-98e1-33a756c28808 has been waiting for 97904 seconds to receive messages from parties [O=BigCorporation, L=New York, C=US].
    ```
3. In the node logs, search for the flow ID of the potentially stuck flow to find any hospitalization or flow retry messages.

4. From the CRaSH shell, run the checkpoint dumper tool using the `checkpoints dump` command to create a zipped diagnostic file in the node's `logs` directory.

5. Unzip the `<NODE_BASE>\logs\checkpoints_dump-<date>.zip` file. Inside the `.zip` file there are `.json` files for each checkpoint.

## Recovering stuck flows

There are a few possible recovery actions for a stuck flow. You can:

- Kill and retry the flow.
- Run a graceful shutdown and restart of the node.
- Contact other network participants if their nodes are not responding to an initiated flow.

### Kill and retry the flow

To kill a flow, use the [Corda shell]({{< relref "../../../../../../../../en/platform/corda/4.8/enterprise/node/operating/shell.md" >}}).

1. Open the node shell.
2. Run the `flow kill <flow-id>`, where `<flow-id>` is the unique flow ID. The output will look something like this:

    ```
    [ERROR] 20:24:18+0100 [Node thread-1] corda.flow. - Flow interrupted while waiting for events, aborting immediately {actor_id=bankUser, actor_owning_identity=O=BankOfCorda, L=London, C=GB, actor_store_id=NODE_CONFIG, fiber-id=10000003, flow-id=15f16740-4ea2-4e48-bcb3-fd9051d5ba59, invocation_id=45622dc7-c4cf-4d11-85ad-1c45e0943455, invocation_timestamp=2019-07-11T18:19:40.519Z, origin=bankUser, session_id=02010e15-8e7a-46f7-976b-5e0626451c54, session_timestamp=2019-07-11T18:19:32.285Z, thread-id=176}
    Killed flow [90613d6f-be78-41bd-98e1-33a756c28808]
    ```
3. Use the node shell to run the `flow start` command with the correct flow parameters to re-run the flow.
4. Check the node logs for stuck flows.

### Run a graceful shutdown and restart of the node

The node has a graceful shutdown mode that drains outstanding flows to checkpoints and prevents other flows from starting. The graceful shutdown can be initiated from the node shell.

1. Open the node shell.
2. Run the `gracefulShutdown` command.
3. Wait until the node has shut down. Restart the node with the flow draining mode disabled using the `run setFlowsDrainingModeEnabled enabled: false` command.

### Contact other network participants

If a peer node is not responding to an initiated flow, you may need to contact the node operator. The checkpoint dump includes diagnostic information including the destination peer participant node that is not responding. For more information on the checkpoint tools available, see the [checkpoint tooling documentation]({{< relref "../../../../../../../../en/platform/corda/4.8/enterprise/node/operating/monitoring-and-logging/checkpoint-tooling.md" >}}).
