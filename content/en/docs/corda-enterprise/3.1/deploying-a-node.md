---
aliases:
- /releases/3.1/deploying-a-node.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-3-1:
    identifier: corda-enterprise-3-1-deploying-a-node
    parent: corda-enterprise-3-1-corda-nodes-index
    weight: 1040
tags:
- deploying
- node
title: Deploying a node
---
{{% important %}}
This documentation is unsupported.
Try [Corda Enterprise 3.3 documentation](/docs/corda-enterprise/3.3/_index.md) instead
{{% /important %}}


# Deploying a node


{{< note >}}
These instructions are intended for people who want to deploy a Corda node to a server,
whether they have developed and tested a CorDapp following the instructions in [Creating nodes locally](generating-a-node.md)
or are deploying a third-party CorDapp.

{{< /note >}}

## Linux: Installing and running Corda as a system service

We recommend creating system services to run a node and the optional webserver. This provides logging and service
handling, and ensures the Corda service is run at boot.

**Prerequisites**:



* Oracle Java 8. The supported versions are listed in [Getting set up](getting-set-up.md)



* Add a system user which will be used to run Corda:> 
`sudo adduser --system --no-create-home --group corda`

* Create a directory called `/opt/corda` and change its ownership to the user you want to use to run Corda:`mkdir /opt/corda; chown corda:corda /opt/corda`
* Place the Enterprise Corda JAR `corda-VERSION_NUMBER.jar` in `/opt/corda`
* (Optional) Copy the Corda webserver JAR provided to your organization
(under `/corda-webserver-VERSION_NUMBER.jar`) and place it in `/opt/corda`
* Create a directory called `cordapps` in `/opt/corda` and save your CorDapp jar file to it. Alternatively, download one of
our [sample CorDapps](https://www.corda.net/samples/) to the `cordapps` directory
* Save the below as `/opt/corda/node.conf`. See [Node configuration](corda-configuration-file.md) for a description of these options:

```kotlin
basedir : "/opt/corda"
p2pAddress : "example.com:10002"
rpcAddress : "example.com:10003"
h2port : 11000
emailAddress : "you@example.com"
myLegalName : "O=Bank of Breakfast Tea, L=London, C=GB"
keyStorePassword : "cordacadevpass"
trustStorePassword : "trustpass"
devMode : false
rpcUsers=[
    {
        user=corda
        password=portal_password
        permissions=[
            ALL
        ]
    }
]
```


* Make the following changes to `/opt/corda/node.conf`:
* Change the `p2pAddress` and `rpcAddress` values to start with your server’s hostname or external IP address.
This is the address other nodes or RPC interfaces will use to communicate with your node
* Change the ports if necessary, for example if you are running multiple nodes on one server (see below)
* Enter an email address which will be used as an administrative contact during the registration process. This is
only visible to the permissioning service
* Enter your node’s desired legal name. This will be used during the issuance of your certificate and should rarely
change as it should represent the legal identity of your node
    * Organization (`O=`) should be a unique and meaningful identifier (e.g. Bank of Breakfast Tea)
    * Location (`L=`) is your nearest city
    * Country (`C=`) is the [ISO 3166-1 alpha-2 code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)


* Change the RPC username and password



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
ExecStart=/usr/bin/java -Xmx2048m -jar /opt/corda/corda.jar
Restart=on-failure

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
exec java -Xmx2048m -jar /opt/corda/corda.jar
```




* Make the following changes to `corda.service` or `corda.conf`:> 

* Make sure the service description is informative - particularly if you plan to run multiple nodes.
* Change the username to the user account you want to use to run Corda. **We recommend that this user account is
not root**
* Set the maximum amount of memory available to the Corda process by changing the `-Xmx2048m` parameter
* **SystemD**: Make sure the `corda.service` file is owned by root with the correct permissions:> 

    * `sudo chown root:root /etc/systemd/system/corda.service`
    * `sudo chmod 644 /etc/systemd/system/corda.service`



* **Upstart**: Make sure the `corda.conf` file is owned by root with the correct permissions:> 

    * `sudo chown root:root /etc/init/corda.conf`
    * `sudo chmod 644 /etc/init/corda.conf`







{{< note >}}
The Corda webserver provides a simple interface for interacting with your installed CorDapps in a browser.
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
[Network permissioning](permissioning.md)
* Depending on the versions of Corda and of the CorDapps used, database migration scripts might need to run before a node is able to start.
For more information refer to [Database management](database-management.md)
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



* Oracle Java 8. The supported versions are listed in [Getting set up](getting-set-up.md)



* Create a Corda directory and copy the Enterprise Corda JAR `corda-VERSION_NUMBER.jar`.
Replace `VERSION_NUMBER` with the desired version. Here’s an example using PowerShell:

```kotlin
mkdir C:\Corda
copy PATH_TO_CORDA_JAR/corda-VERSION_NUMBER.jar C:\Corda\corda.jar
```


* Create a directory called `cordapps` in `C:\Corda\` and save your CorDapp jar file to it. Alternatively,
download one of our [sample CorDapps](https://www.corda.net/samples/) to the `cordapps` directory
* Save the below as `C:\Corda\node.conf`. See [Node configuration](corda-configuration-file.md) for a description of these options:

```kotlin
basedir : "C:\\Corda"
p2pAddress : "example.com:10002"
rpcAddress : "example.com:10003"
h2port : 11000
emailAddress: "you@example.com"
myLegalName : "O=Bank of Breakfast Tea, L=London, C=GB"
keyStorePassword : "cordacadevpass"
trustStorePassword : "trustpass"
extraAdvertisedServiceIds: [ "" ]
devMode : false
rpcUsers=[
    {
        user=corda
        password=portal_password
        permissions=[
            ALL
        ]
    }
]
```


* Make the following changes to `C:\Corda\node.conf`:
* Change the `p2pAddress` and `rpcAddress` values to start with your server’s hostname or external IP address.
This is the address other nodes or RPC interfaces will use to communicate with your node
* Change the ports if necessary, for example if you are running multiple nodes on one server (see below)
* Enter an email address which will be used as an administrative contact during the registration process. This is
only visible to the permissioning service
* Enter your node’s desired legal name. This will be used during the issuance of your certificate and should rarely
change as it should represent the legal identity of your node
    * Organization (`O=`) should be a unique and meaningful identifier (e.g. Bank of Breakfast Tea)
    * Location (`L=`) is your nearest city
    * Country (`C=`) is the [ISO 3166-1 alpha-2 code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)


* Change the RPC username and password


* Copy the required Java keystores to the node. See [Network permissioning](permissioning.md)
* Download the [NSSM service manager](http://nssm.cc)
* Unzip `nssm-2.24\win64\nssm.exe` to `C:\Corda`
* Save the following as `C:\Corda\nssm.bat`:

```batch
nssm install cordanode1 C:\ProgramData\Oracle\Java\javapath\java.exe
nssm set cordanode1 AppDirectory C:\Corda
nssm set cordanode1 AppParameters "-Xmx2048m -jar corda.jar --config-file=C:\corda\node.conf"
nssm set cordanode1 AppStdout C:\Corda\service.log
nssm set cordanode1 AppStderr C:\Corda\service.log
nssm set cordanode1 Description Corda Node - Bank of Breakfast Tea
nssm set cordanode1 Start SERVICE_AUTO_START
sc start cordanode1
```


* Modify the batch file:> 

* If you are installing multiple nodes, use a different service name (`cordanode1`) for each node
* Set the amount of Java heap memory available to this node by modifying the -Xmx argument
* Set an informative description



* Provision the required certificates to your node. Contact the network permissioning service or see
[Network permissioning](permissioning.md)
* Depending on the versions of Corda and of the CorDapps used, database migration scripts might need to run before a node is able to start.
For more information refer to [Database management](database-management.md)
* Run the batch file by clicking on it or from a command prompt
* Run `services.msc` and verify that a service called `cordanode1` is present and running
* Run `netstat -ano` and check for the ports you configured in `node.conf`
* You may need to open the ports on the Windows firewall




## Testing your installation

You can verify Corda is running by connecting to your RPC port from another host, e.g.:


`telnet your-hostname.example.com 10002`


If you receive the message “Escape character is ^]”, Corda is running and accessible. Press Ctrl-] and Ctrl-D to exit
telnet.

