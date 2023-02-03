---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-6:
    identifier: corda-enterprise-4-6-operations-guide-deployment-node-deploying
    parent: corda-enterprise-4-6-operations-guide-deployment-node
tags:
- deploying
- node
title: Deploying a node to a server
weight: 2
---


# Deploying a node to a server


{{< note >}}
These instructions are intended for people who want to deploy a Corda node to a server,
whether they have developed and tested a CorDapp following the instructions in [Creating nodes locally](generating-a-node.md)
or are deploying a third-party CorDapp.

{{< /note >}}
{{< note >}}
When deploying multiple nodes in parallel the package tool (Capsule) that Corda uses can encounter
issues retrieving dependencies. This is due to each node trying to download the dependencies in a common
location.  In these cases it is recommended to set the environment variable `CAPSULE_CACHE_DIR` which
will allow the Capsule to maintain a separate cache for each node.  This is used in the example descriptions
below. See the [Capsule documentation](http://www.capsule.io) for more details.

{{< /note >}}
{{< note >}}
Another preferable Enterprise option when deploying multiple nodes in parallel is to use the
Node Registration Tool.

{{< /note >}}

## Linux: Installing and running Corda as a system service

We recommend creating system services to run a node and the optional test webserver. This provides logging and service
handling, and ensures the Corda service is run at boot.

**Prerequisites**:



* A supported Java distribution (see [Getting set up for CorDapp development](../../cordapps/getting-set-up.md))



* As root/sys admin user - add a system user which will be used to run Corda:
`sudo adduser --system --no-create-home --group corda`

* Create a directory called `/opt/corda` and change its ownership to the user you want to use to run Corda:`mkdir /opt/corda; chown corda:corda /opt/corda`
* Place the Enterprise Corda JAR `corda-4.6.jar` in `/opt/corda`
* (Optional) Copy the Corda webserver JAR provided to your organization
(under `/corda-webserver-4.6.jar`) and place it in `/opt/corda`
* Create a directory called `cordapps` in `/opt/corda` and save your CorDapp jar file to it. Alternatively, download one of
our [sample CorDapps](https://www.corda.net/samples/) to the `cordapps` directory
* Save the below as `/opt/corda/node.conf`. See corda-configuration-file for a description of these options:

```none
p2pAddress = "example.com:10002"
rpcSettings {
    address: "example.com:10003"
    adminAddress: "example.com:10004"
}
h2port = 11000
emailAddress = "you@example.com"
myLegalName = "O=Bank of Breakfast Tea, L=London, C=GB"
keyStorePassword = "cordacadevpass"
trustStorePassword = "trustpass"
devMode = false
rpcUsers= [
    {
        user=corda
        password=portal_password
        permissions=[
            ALL
        ]
    }
]
custom { jvmArgs = [ "-Xmx2048m", "-XX:+UseG1GC" ] }
```


* Make the following changes to `/opt/corda/node.conf`:
* Change the `p2pAddress`, `rpcSettings.address` and `rpcSettings.adminAddress` values to match
your server’s hostname or external IP address. These are the addresses other nodes or RPC interfaces will use to
communicate with your node.
* Change the ports if necessary, for example if you are running multiple nodes on one server (see below).
* Enter an email address which will be used as an administrative contact during the registration process. This is
only visible to the permissioning service.
* Enter your node’s desired legal name (see node-naming for more details).
* If required, add RPC users



{{< note >}}
Ubuntu 16.04 and most current Linux distributions use SystemD, so if you are running one of these
distributions follow the steps marked **SystemD**.
If you are running Ubuntu 14.04, follow the instructions for **Upstart**.

{{< /note >}}

* **SystemD**: Create a `corda.service` file based on the example below and save it in the `/etc/systemd/system/`
directory>
```shell
[Unit]
Description=Corda Node - Bank of Breakfast Tea
Requires=network.target

[Service]
Type=simple
User=corda
WorkingDirectory=/opt/corda
ExecStart=/usr/bin/java -jar /opt/corda/corda.jar
Restart=on-failure
Environment="CAPSULE_CACHE_DIR=./capsule"

[Install]
WantedBy=multi-user.target
```






* **Upstart**: Create a `corda.conf` file based on the example below and save it in the `/etc/init/` directory>
```shell
description "Corda Node - Bank of Breakfast Tea"

start on runlevel [2345]
stop on runlevel [!2345]

respawn
setuid corda
chdir /opt/corda
exec java -jar /opt/corda/corda.jar
```




* Make the following changes to `corda.service` or `corda.conf`:

* Make sure the service description is informative - particularly if you plan to run multiple nodes.
* Change the username to the user account you want to use to run Corda. **We recommend that this user account is
not root**
* **SystemD**: Make sure the `corda.service` file is owned by root with the correct permissions:
>
    * `sudo chown root:root /etc/systemd/system/corda.service`
    * `sudo chmod 644 /etc/systemd/system/corda.service`



* **Upstart**: Make sure the `corda.conf` file is owned by root with the correct permissions:
>
    * `sudo chown root:root /etc/init/corda.conf`
    * `sudo chmod 644 /etc/init/corda.conf`







{{< note >}}
The Corda test webserver provides a simple interface for interacting with your installed CorDapps in a browser.
Running the webserver is optional.

{{< /note >}}

* **SystemD**: Create a `corda-webserver.service` file based on the example below and save it in the `/etc/systemd/system/`
directory

```shell
[Unit]
Description=Webserver for Corda Node - Bank of Breakfast Tea
Requires=network.target

[Service]
Type=simple
User=corda
WorkingDirectory=/opt/corda
ExecStart=/usr/bin/java -jar /opt/corda/corda-webserver.jar
Restart=on-failure

[Install]
WantedBy=multi-user.target
```




* **Upstart**: Create a `corda-webserver.conf` file based on the example below and save it in the `/etc/init/`
directory

```shell
description "Webserver for Corda Node - Bank of Breakfast Tea"

start on runlevel [2345]
stop on runlevel [!2345]

respawn
setuid corda
chdir /opt/corda
exec java -jar /opt/corda/corda-webserver.jar
```


* Provision the required certificates to your node. Contact the network permissioning service or see
permissioning
* Depending on the versions of Corda and of the CorDapps used, database migration scripts might need to run before a node is able to start.
For more information refer to database-management
* **SystemD**: You can now start a node and its webserver and set the services to start on boot by running the
following `systemctl` commands:



* `sudo systemctl daemon-reload`
* `sudo systemctl enable --now corda`
* `sudo systemctl enable --now corda-webserver`



* **Upstart**: You can now start a node and its webserver by running the following commands:



* `sudo start corda`
* `sudo start corda-webserver`


The Upstart configuration files created above tell Upstart to start the Corda services on boot so there is no need to explicitly enable them.

You can run multiple nodes by creating multiple directories and Corda services, modifying the `node.conf` and
SystemD or Upstart configuration files so they are unique.


## Windows: Installing and running Corda as a Windows service

We recommend running Corda as a Windows service. This provides service handling, ensures the Corda service is run
at boot, and means the Corda service stays running with no users connected to the server.

**Prerequisites**:



* A supported Java distribution (see [Getting set up for CorDapp development](../../cordapps/getting-set-up.md))



* Create a Corda directory and copy the Enterprise Corda JAR `corda-4.6.jar`.
Here’s an example using PowerShell:

```shell
mkdir C:\Corda
copy PATH_TO_CORDA_JAR/corda-4.6.jar C:\Corda\corda.jar
```


* Create a directory called `cordapps` in `C:\Corda\` and save your CorDapp jar file to it. Alternatively,
download one of our [sample CorDapps](https://www.corda.net/samples/) to the `cordapps` directory
* Save the below as `C:\Corda\node.conf`. See corda-configuration-file for a description of these options:

```none
 p2pAddress = "example.com:10002"
 rpcSettings {
     address = "example.com:10003"
     adminAddress = "example.com:10004"
 }
 h2port = 11000
 emailAddress = "you@example.com"
 myLegalName = "O=Bank of Breakfast Tea, L=London, C=GB"
 keyStorePassword = "cordacadevpass"
 trustStorePassword = "trustpass"
 devMode = false
 rpcSettings {
    useSsl = false
    standAloneBroker = false
    address = "example.com:10003"
    adminAddress = "example.com:10004"
}
custom { jvmArgs = [ '-Xmx2048m', '-XX:+UseG1GC' ] }
```


* Make the following changes to `C:\Corda\node.conf`:
* Change the `p2pAddress`, `rpcSettings.address` and `rpcSettings.adminAddress` values to match
your server’s hostname or external IP address. These are the addresses other nodes or RPC interfaces will use to
communicate with your node.
* Change the ports if necessary, for example if you are running multiple nodes on one server (see below).
* Enter an email address which will be used as an administrative contact during the registration process. This is
only visible to the permissioning service.
* Enter your node’s desired legal name (see node-naming for more details).
* If required, add RPC users


* Copy the required Java keystores to the node. See permissioning
* Download the [NSSM service manager](https://nssm.cc/)
* Unzip `nssm-2.24\win64\nssm.exe` to `C:\Corda`
* Save the following as `C:\Corda\nssm.bat`:

```batch
nssm install cordanode1 java.exe
nssm set cordanode1 AppParameters "-jar corda.jar"
nssm set cordanode1 AppDirectory C:\Corda
nssm set cordanode1 AppStdout C:\Corda\service.log
nssm set cordanode1 AppStderr C:\Corda\service.log
nssm set cordanode1 AppEnvironmentExtra CAPSULE_CACHE_DIR=./capsule
nssm set cordanode1 Description Corda Node - Bank of Breakfast Tea
nssm set cordanode1 Start SERVICE_AUTO_START
sc start cordanode1
```


* Modify the batch file:

* If you are installing multiple nodes, use a different service name (`cordanode1`), and modify
*AppDirectory*, *AppStdout* and *AppStderr* for each node accordingly
* Set an informative description



* Provision the required certificates to your node. Contact the network permissioning service or see
permissioning
* Depending on the versions of Corda and of the CorDapps used, database migration scripts might need to run before a node is able to start.
For more information refer to database-management
* Run the batch file by clicking on it or from a command prompt
* Run `services.msc` and verify that a service called `cordanode1` is present and running
* Run `netstat -ano` and check for the ports you configured in `node.conf`
* You may need to open the ports on the Windows firewall




## Testing your installation

You can verify Corda is running by connecting to your RPC port from another host, for example:


`telnet your-hostname.example.com 10002`


If you receive the message “Escape character is ^]”, Corda is running and accessible. Press Ctrl-] and Ctrl-D to exit
telnet.
