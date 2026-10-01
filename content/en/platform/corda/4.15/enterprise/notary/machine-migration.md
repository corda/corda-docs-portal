---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-14:
    parent: corda-enterprise-4-14-corda-nodes-notary-operate
tags:
- machine
- migration
title: Migrating notary workers
weight: 2
---


# Migrating notary workers

To migrate a notary worker from one physical machine or VM to another,
follow the steps below.

{{< note >}}
This procedure applies to to the Corda notary worker and not the underlying database.
Please refer to the data migration documentation of the database, in case
a database service is located on the same machine as the notary worker.

{{< /note >}}

1. Stop the service on the notary worker you are going to migrate. Other notary worker
nodes are still able to handle requests, so no service downtime is expected.
2. Copy the certificates directory, configuration files and Corda JAR file to the new machine.
3. Update the P2P address configuration in the config file on the new machine if required.
4. Start the notary worker on the new machine.
5. Check the logs and monitoring service to see if the notary worker node started as expected and is successfully handling notarisation requests.
6. Dispose of the old machine once the service is up and running on the new machine.

