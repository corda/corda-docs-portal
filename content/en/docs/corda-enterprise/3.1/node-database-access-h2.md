---
aliases:
- /releases/3.1/node-database-access-h2.html
date: '2020-01-08T09:59:25Z'
menu: 
  corda-enterprise-3-1:
    parent: corda-enterprise-3-1-corda-nodes-index
    weight: 1085
tags:
- node
- database
- access
- h2
title: Database access when running H2
---
{{% important %}}
This documentation is unsupported.
Try [Corda Enterprise 3.3 documentation](/docs/corda-enterprise/3.3/_index.md) instead
{{% /important %}}


# Database access when running H2

When running a node using the H2 database, the node can be configured to expose its internal database over socket which
can be browsed using any tool that can use JDBC drivers.
The JDBC URL is printed during node startup to the log and will typically look like this:


`jdbc:h2:tcp://localhost:31339/node`


The username and password can be altered in the [Node configuration](corda-configuration-file.md) but default to username “sa” and a blank
password.

Any database browsing tool that supports JDBC can be used, but if you have IntelliJ Ultimate edition then there is
a tool integrated with your IDE. Just open the database window and add an H2 data source with the above details.
You will now be able to browse the tables and row data within them.

By default the node will expose its database on the localhost network interface. This behaviour can be
overridden by specifying the full network address (interface and port), using the new h2Settings
syntax in the node configuration:

The configuration above will restrict the H2 service to run on localhost. If remote access is required, the address
can be changed to 0.0.0.0. However it is recommended to change the default username and password
before doing so.

