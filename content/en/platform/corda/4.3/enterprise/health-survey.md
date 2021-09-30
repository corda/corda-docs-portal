---
aliases:
- /releases/4.3/health-survey.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-3:
    identifier: corda-enterprise-4-3-health-survey
    parent: corda-enterprise-4-3-tools-index-enterprise
    weight: 1050
tags:
- health
- survey
title: Health Survey Tool
---





# Health Survey Tool

The Health Survey Tool is a command line utility that can be used to collect information about a node,
which can be used by the R3 support Team as an aid to diagnose support issues. It works by scanning through a provided
node base directory and archiving some of the important files. Furthermore, it does a deployment status check by connecting to the node and probing
it and the firewall (if deployed externally) for information on configuration, service status, connections map and more.


## Running

```kotlin
java -jar corda-tools-health-survey-4.3.jar --base-directory DIRECTORY [--node-configuration DIRECTORY]
```


Usage:



* `-c`, `--node-configuration` <arg>:   Path to the Corda node configuration file, optional
* `-d`, `--base-directory` <arg>:       Path to the Corda node base directory
* `-l`, `--local`:                      Verify local node configuration only without checking bridge/firewall, by default verifies all
* `-e`, `--exclude-logs`:               Exclude node’s log files from ZIP report, by default logs are included in ZIP report
* `-t`, `--text-format`:                Create report as a single .txt file without node’s log files, default is ZIP format
* `-i`, `--timeout`:                    Override default timeout for sending health request messages
* `-v`, `--config-validate`:            Validate configuration files
* `-b`, `--bridge-configuration`        Path to bridge configuration when used in conjunction with *config-validate*
* `-f`, `--float-configuration`         Path to float configuration when used in conjunction with *config-validate*


Running the tool with no arguments assumes that the base-directory argument is the current working directory.


## Output

The tool generates the archive of the collected files in the same directory it is ran in. The names are in the format: `report-date-time.zip`

![health survey photo](/en/images/health-survey-photo.png "health survey photo")

## Deployment health check

The Corda Health Survey is designed to perform connectivity and configuration checks on a Corda Enterprise Node. The tool supports the following deployment configurations:



* Node with internal Artemis broker
* Node with internal Artemis broker, external Bridge
* Node with internal Artemis broker, Bridge, Float (full Corda Enterprise Firewall architecture)


{{< note >}}
HA Corda Node deployments are not currently supported (the required checks should run but the results will be incomplete or inconsistent).

{{< /note >}}
{{< note >}}
The Corda Health Survey is designed to help operators with initial setup of a Node; it is not meant to be used as an ongoing monitoring tool.

{{< /note >}}

## Report format

After each run, the Corda Health Survey collects and packages up into a .zip file information that R3 Support can use to help a customer with a support request, including:


* An obfuscated version of the config files (i.e., without passwords, etc.)
* Node logs from the last 3 days (if the user is happy to share)
* The version of Corda, Java virtual machine and operating system, networking information with DNS lookups to various endpoints (database, network map, doorman, external addresses)
* A copy of the network parameters file
* A list of installed CorDapps (including file sizes and checksums)
* A list of the files in the drivers directory
* A copy of the Node information file and a list of the ones in the additional-node-infos directory, etc.

Instead of zipping the reports, operators can print them to a text file using the command line option -t.


## Disabling the Corda Health Survey in production

The tool relies on dedicated Artemis queues to relay configuration and runtime information from the Corda Firewall components. This functionality is enabled by default.
After verifying a production deployment, operators are advised to disable the health checking functionality (in order to use the standard Artemis setup for Corda Enterprise) by adding the following entry in the Node configuration file:

```none
enterpriseConfiguration { healthCheck = false }
```

And the following entry in the Bridge configuration file:

```none
healthCheck = false
```
