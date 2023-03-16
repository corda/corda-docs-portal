---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-9:
    identifier: corda-enterprise-4-9-corda-nodes-deploying-node-generating-dockerform
    parent: generating-a-node
tags:
- generating
- node
title: Dockerform task
weight: 1
---

# Tasks using Dockerform

You need both `Docker` and `docker-compose` installed and enabled to use this method. Docker CE
(Community Edition) is sufficient. Please refer to [Docker CE documentation](https://www.docker.com/community-edition)
and [Docker Compose documentation](https://docs.docker.com/compose/install/) for installation instructions for all
major operating systems.

Dockerform supports the following configuration options for each node:

* `name`
* `notary`
* `cordapps`
* `rpcUsers`
* `useTestClock`

You do not need to specify the node ports because every node has a separate container so no ports conflicts will occur. Every node will expose port `10003` for RPC connections. Docker will then map these to available ports on your host machine.

You should interact with each node via its shell over SSH - see the [node configuration options]({{< relref "../../../../../../../en/platform/corda/4.9/enterprise/node/setup/corda-configuration-file.md" >}}) for more information.

To enable the shell, you need to set the `sshdPort` number for each node in the gradle task - this is explained in the section [run the Dockerform task](#run-the-dockerform-task) further below. For example:

```groovy
node {
    name "O=PartyA,L=London,C=GB"
    p2pPort 10002
    rpcSettings {
        address("localhost:10003")
        adminAddress("localhost:10023")
    }
    rpcUsers = [[user: "user1", "password": "test", "permissions": ["ALL"]]]
    sshdPort 2223
}
```

{{< note >}}
Make sure to use Corda Gradle plugin version 5.0.10 or above. If you do not specify the `sshd` port number for a node, it will use the default value `2222`. Please run the `docker ps` command to check the allocated port on your host that maps to this port.
{{< /note >}}

The Docker image associated with each node can be configured in the `Dockerform` task. This will initialise *every* node in the `Dockerform` task with the specified Docker image. If you need nodes with different Docker images, you can edit the `docker-compose.yml` file with your preferred image.

{{< note >}}
Before running any Corda Enterprise Docker images, you must accept the license agreement and indicate that you have done this by setting the environment variable `ACCEPT_LICENSE` to `YES` or `Y` on your machine. If you do not do this, none of the Docker containers will start.

As an alternative, you can specify this parameter when running the `docker-compose up` command, for example:
`ACCEPT_LICENSE=Y docker-compose up`
{{< /note >}}

## Specify an external database

You can configure `Dockerform` to use a standalone database to test with non-H2 databases. For example, to use PostgresSQL, you need to make the following changes to your CorDapp project:

1. Create a file called `postgres.gradle` in your Cordapp directory, and insert the following code block:

```groovy
ext {
    postgresql_version     = '42.2.12'
    postgres_image_version = '11'
    dbUser                 = 'myuser'
    dbPassword             = 'mypassword'
    dbSchema               = 'myschema'
    dbName                 = 'mydb'
    dbPort                 = 5432
    dbHostName             = 'localhost'
    dbDockerfile           = 'Postgres_Dockerfile'
    dbInit                 = 'Postgres_init.sh'
    dbDataVolume           =  [
            hostPath      : 'data',
            containerPath : '/var/lib/postgresql/data:\${SUFFIX}',
            containerPathArgs   : [
                    SUFFIX : "rw"
            ]
    ]
    postgres = [
            dataSourceProperties: [
                    dataSourceClassName: 'org.postgresql.ds.PGSimpleDataSource',
                    dataSource: [
                            user    : dbUser,
                            password: dbPassword,
                            url     : "jdbc:postgresql://\${DBHOSTNAME}:\${DBPORT}/\${DBNAME}?currentSchema=\${DBSCHEMA}",
                            urlArgs : [
                                    DBHOSTNAME  : dbHostName,
                                    DBPORT      : dbPort,
                                    DBNAME      : dbName,
                                    DBSCHEMA    : dbSchema
                            ]
                    ]
            ],
            database: [
                    schema                   : dbSchema
            ],
            dockerConfig: [
                    dbDockerfile    : dbDockerfile,
                    dbDockerfileArgs: [
                         DBNAME         : dbName,
                         DBSCHEMA       : dbSchema,
                         DBUSER         : dbUser,
                         DBPASSWORD     : dbPassword,
                         DBPORT         : dbPort
                    ],
                    dbUser          : dbUser,
                    dbPassword      : dbPassword,
                    dbSchema        : dbSchema,
                    dbName          : dbName,
                    dbPort          : dbPort,
                    dbHostName      : dbHostName,
                    dbDatabase      : dbName,
                    dbDataVolume    : dbDataVolume
            ]
    ]
}

apply plugin: 'net.corda.plugins.cordformation'

dependencies {
    cordaDriver "org.postgresql:postgresql:$postgresql_version"
}

def generateInitScripts = tasks.register('generateInitScripts') { Task task ->
    def initialDockerfile = file("$buildDir/$dbDockerfile")
    def initialScript = file( "$buildDir/$dbInit")
    task.inputs.properties(project['postgres'])
    task.outputs.files(initialDockerfile, initialScript)
    /*
     * Dockerfile to initialise the PostgreSQL database.
     */
    task.doLast {
        initialDockerfile.withPrintWriter('UTF-8') { writer ->
            writer << """\
# Derive from postgres image
FROM postgres:$postgres_image_version

ARG DBNAME=$dbName
ARG DBSCHEMA=$dbSchema
ARG DBUSER=$dbUser
ARG DBPASSWORD=$dbPassword
ARG DBPORT=$dbPort

ENV POSTGRES_DB=\$DBNAME
ENV POSTGRES_DB_SCHEMA=\$DBSCHEMA
ENV POSTGRES_USER=\$DBUSER
ENV POSTGRES_PASSWORD=\$DBPASSWORD
ENV PGPORT=\$DBPORT

# Copy all postgres init file to the docker entrypoint
COPY ./$dbInit /docker-entrypoint-initdb.d/$dbInit

# Allow postgres user to run init script
RUN chmod 0755 /docker-entrypoint-initdb.d/$dbInit
"""
        }

        /**
         * Append the persistence configuration if persistence is required (i.e., persistence=true)
         */
        if (project.hasProperty("dbDataVolume")) {

            initialDockerfile.withWriterAppend('UTF-8') { writer ->
                writer << """\

# Associate the volume with the host user
USER 1000:1000

# Initialise environment variable with database directory
ENV PGDATA=/var/lib/postgresql/data/pgdata
"""
            }
        }

        /*
         * A UNIX script to generate the init.sql file that
         * PostgreSQL needs. This must use UNIX line endings,
         * even when generated on Windows.
         */
        initialScript.withPrintWriter('UTF-8') { writer ->
            writer << """\
#!/usr/bin/env bash
# Postgres database initialisation script when using Docker images

dbUser=\${POSTGRES_USER:-"$dbUser"}
dbPassword=\${POSTGRES_PASSWORD:-"$dbPassword"}
dbSchema=\${POSTGRES_DB_SCHEMA:-"$dbSchema"}
dbName=\${POSTGRES_DB:-"$dbName"}

psql -v ON_ERROR_STOP=1 --username "\$dbUser"  --dbname "\$dbName" <<-EOSQL
        CREATE SCHEMA \$dbSchema;
        GRANT USAGE, CREATE ON SCHEMA \$dbSchema TO \$dbUser;
        GRANT SELECT, INSERT, UPDATE, DELETE, REFERENCES ON ALL tables IN SCHEMA \$dbSchema TO \$dbUser;
        ALTER DEFAULT privileges IN SCHEMA \$dbSchema GRANT SELECT, INSERT, UPDATE, DELETE, REFERENCES ON tables TO \$dbUser;
        GRANT USAGE, SELECT ON ALL sequences IN SCHEMA \$dbSchema TO \$dbUser;
        ALTER DEFAULT privileges IN SCHEMA \$dbSchema GRANT USAGE, SELECT ON sequences TO \$dbUser;
        ALTER ROLE \$dbUser SET search_path = \$dbSchema;
EOSQL
""".replaceAll("\r\n", "\n")
        }
        initialScript.executable = true
    }
}
```

2. In the `build.gradle` file, add the gradle task `generateInitScripts` to the `dependsOn` list of the `prepareDockerNodes` task, add the `dockerConfig` element, and initialise it with the `postgres` block. An example is shown below:

```groovy
task prepareDockerNodes(type: net.corda.plugins.Dockerform, dependsOn: ['jar',  'generateInitScripts']) {

    [...]

    node {
        [...]
    }

    // The postgres block from the postgres.gradle file
    dockerConfig = postgres
}
```

The `postgres.gradle` file includes the following:
* A gradle task called `generateInitScripts` used to generate the Postgres Docker image files.
* A set of variables used to initialise the Postgres Docker image.

To set up the external database, you must place the following two files in the `build` directory:
* `Postgres_Dockerfile` -  a wrapper for the base Postgres Docker image.
* `Postgres_init.sh` -  a shell script to initialise the database.

The `Postgres_Dockerfile` is referenced in the `docker-compose.yml` file and allows for a number of arguments for configuring the Docker image.

You can use the following configuration parameters in the `postgres.gradle` file:

| Parameter              | Description                                       |
|------------------------|---------------------------------------------------|
| postgresql_version     | Version of JDBC driver to connect to the database |
| postgres_image_version | Version of Postgres Docker image                  |
| dbUser                 | Database user                                     |
| dbPassword             | Database password                                 |
| dbSchema               | Postgres schema                                   |
| dbName                 | Database name                                     |
| dbPort                 | Database port (default: 5432)                     |
| dbHostName             | Database host (default: localhost)                |
| dbInit                 | Initialisation script for Postgres Docker image   |
| dbDockerfile           | Wrapper of base Postgres Docker image             |
| dbDataVolume           | Path to database files for Postgres Docker image  |

To make the database files persistent across multiple `docker-compose` runs, you must set the `dbDataVolume` parameter. If this variable is commented out, the database files will be removed after every `docker-compose` run.

## Run the Dockerform task

To run the Dockerform task, follow the steps below.

{{< note >}}
The node configuration described here is just an example. `Dockerform` allows you specify any number of nodes and you can define their configurations and names as needed.
{{< /note >}}

1. Open the `build.gradle` file of your CorDapp project and add a new gradle task, as shown in the example below.

{{< note >}}
Make sure to use Corda Gradle plugin version 5.0.10 or above.
{{< /note >}}

{{% warning %}}
The Docker image name must be specified by using the `dockerImage` property.
{{% /warning %}}

```groovy
task prepareDockerNodes(type: net.corda.plugins.Dockerform, dependsOn: ['jar']) {
    // set docker image for each node
    dockerImage = "corda/corda-zulu-java1.8-4.4"

    nodeDefaults {
        cordapp project(":contracts-java")
    }
    node {
        name "O=Notary,L=London,C=GB"
        notary = [validating : false]
        p2pPort 10002
        rpcSettings {
            address("localhost:10003")
            adminAddress("localhost:10023")
        }
        projectCordapp {
            deploy = false
        }
        cordapps.clear()
        sshdPort 2222
    }
    node {
        name "O=PartyA,L=London,C=GB"
        p2pPort 10002
        rpcSettings {
            address("localhost:10003")
            adminAddress("localhost:10023")
        }
        rpcUsers = [[user: "user1", "password": "test", "permissions": ["ALL"]]]
        sshdPort 2223
    }
    node {
        name "O=PartyB,L=New York,C=US"
        p2pPort 10002
        rpcSettings {
            address("localhost:10003")
            adminAddress("localhost:10023")
        }
        rpcUsers = [[user: "user1", "password": "test", "permissions": ["ALL"]]]
        sshdPort 2224
    }

    // This property needs to be outside the node {...} elements
    dockerImage = "corda/corda-zulu-java1.8-4.8"
}
```

{{< note >}}
If you do not specify the sshd port number for a node, it will use the default value `2222`.
{{< /note >}}

2. To create the nodes defined in the `prepareDockerNodes` gradle task added in the first step, run the following command in a command prompt or a terminal window, from the root of the project where the `prepareDockerNodes` task is defined:

* Linux/macOS: `./gradlew prepareDockerNodes`
* Windows: `gradlew.bat prepareDockerNodes`

This command creates the nodes in the `build/nodes` directory. A node directory is generated for each node defined in the `prepareDockerNodes` task. The task also creates a `docker-compose.yml` file in the `build/nodes` directory.


## External database configuration

If you configure an external database, a `Postgres_Dockerfile` file and `Postgres_init.sh` file are also generated in the `build` directory. If you make any changes to your CorDapp source or `prepareDockerNodes` task, you will need to re-run the task to see the changes take effect.

If the external database is not defined and configured properly, as described in [specifying an external database](#specify-an-external-database), the files `Postgres_Dockerfile` and `Postgres_init.sh` will not be generated.

In this case, each Corda node is associated with a Postgres database. Only one Corda node can connect to the same database. While there is no maximum number of nodes you can deploy with `Dockerform`, you are constrained by the maximum available resources on the machine running this task, as well as the overhead introduced by every Docker container that is started. All the started nodes run in the same Docker overlay network.

The connection settings to the Postgres database are provided to each node through the `postgres.gradle` file. The Postgres JDBC driver is provided via Maven as part of the `cordaDrive` gradle configuration, which is also specified in the dependencies block of the `postgres.gradle` file.

Note that this feature is not designed for users to access the database via elevated or admin rights - you must only use such configuration changes for testing/development purposes.
