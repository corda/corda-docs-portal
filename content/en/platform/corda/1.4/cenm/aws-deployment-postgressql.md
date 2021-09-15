---
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-4:
    parent: cenm-1-4-aws-deployment-guide
tags:
- config
- AWS
- PostgreSQL
title: Deploy CENM 1.4 with AWS and PostgreSQL
weight: 300
---

# CENM 1.4 reference deployment using AWS and PostgreSQL

You can use CENM database and services documentation to complete a reference or test deployment of CENM using AWS and PostgreSQL. The references provided here refer to in depth documentation for databases and services in CENM.

## Supported deployment options

The following deployment options are supported in CENM:

* AWS with external PostgreSQL.
* Azure with PostgreSQL deployed in cluster.
* Azure with external PostgreSQL.

Not supported:

* AWS with PostgreSQL deployed in cluster.

## Reference guide

To set up a reference deployment of CENM using AWS and PostgreSQL:

### Set up a PostgreSQL database for each CENM service

You must ensure that each CENM service has it's own PostgreSQL database. Complete the steps referenced below for each of the following:

* [Auth service](auth-service).
* [Gateway service](gateway-service).
* [Identity manager](identity-manager).
* [Network Map](network-map).
* [Signer service](signing-service).
* [Zone service](zone-service).
* [Angel service](angel-service).

To set up each database:

1. Set up a PostgreSQL database in AWS - follow the instructions in the [AWS documentation](https://aws.amazon.com/rds/postgresql).
2. Connect to the database, using the details of the database in AWS.
3. Create a database user and a schema namespace [with restricted permissions](database-set-up.html#1-create-a-database-user-with-schema-permissions). Follow the [steps for PostgreSQL](database-set-up.html#postgresql).
4. Create the [database schema](database-set-up.html#2-database-schema-creation) for each service.
5. Perform [CENM Service configuration](database-set-up.html#3-cenm-service-configuration) - follow the [steps for PostgreSQL](database-set-up.html#postgresql-1). See also the [database configuration documentation](config-database.html).

{{< note >}}
In step 4 above, you must create a schema for each CENM service. The guide provided has steps for a restricted database schema that is used in a live production environment. You may prefer to use a less restricted database to reduce complexity in this reference environment setup.
{{< /note >}}

### Deploy CENM services

1. Deploy the [Auth Service](auth-service.html) using PostgreSQL on AWS.
2. Deploy the [Identity Manager Service](identity-manager.html) using PostgreSQL on AWS.
3. Deploy the [Network Map Service](network-map.html) using PostgreSQL on AWS.
4. Deploy the [Zone Service](zone-service.html) using PostgreSQL on AWS.
5. Deploy the [Signing Service](signing-service.html#signing-service) (it does not use a database).
