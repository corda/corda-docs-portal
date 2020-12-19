---
date: '2020-05-28T17:40:25Z'
menu:
  cenm-1-5:
    identifier: cenm-1-5-management-console
    parent: cenm-1-5-tools-index
    weight: 1020
tags:
- CENM management console
title: CENM Management Console
---

# CENM management console

The CENM management console is a web interface that allows you to perform key CENM tasks using a visual UI.

You can use the CENM management console to perform key CENM tasks and access CENM services and network information. With the CENM management console, you can:

* Access the network map.
* Update Network Parameters.
* Review Identity Manager progress for Onboarding and Removing members.

{{< note >}}
Your ability to perform certain tasks using the CENM management console depends on your user permissions. Permissions for each CENM service can be allocated and managed by an administrator in the [User Admin tool](user-admin.md). You will not be able to self-allocate the required permissions - they must be granted by an administrator.
{{< /note >}}

To use the CENM management console, you must install it as a *plug-in* to your Gateway Service. Once you have installed the plug-in, anyone with the required permissions can access and use the management console from any web browser.

## Installation

### Requirements

- [Auth Service](auth-service.md) that has been set up with at least one user (ideally an admin user) and running.
- [Zone Service](zone-service.md) running.

### Install the CENM management console

The CENM management console is accessed via the [Gateway service](gateway-service.md). Once you have added the plugin binaries to the correct directory on the machine that hosts your Gateway Service, you can access the web service from any browser.

To install the CENM management console:

1. Download the latest Gateway Service binaries from [Artifactory](https://software.r3.com).
2. Download the CENM management console Gateway Plugin binaries from Artifactory.
3. Create a directory called `plugins` in the same directory as the Gateway Service `.jar` file (if you do not already have this directory for other plug-ins).
4. Copy the CENM Gateway Plugin `.jar` file to the `plugins` directory.
5. Configure the Gateway Service using the `auth { }` and `cenm { }` properties.
   Example configuration:
   ```
   auth {
        serverUrl = "https://auth-service:8081/"
        sslConfig = {
            trustStore = "/etc/corda/trust-stores/corda-ssl-trust-store.jks"
            trustStorePassword = "trustpass"
        }
        clientCredentials = {
            clientId = "farm1"
            clientSecret = "secret1"
        }
    }
    cenm {
        zoneHost: "zone-service"
        zonePort: 5063
        ssl = {
            keyStore = {
               keyPassword = "password"
             location = "/etc/corda/key-stores/farm-ssl-keys.jks"
               password = "password"
            }
            trustStore = {
               location = "/etc/corda/trust-stores/corda-ssl-trust-store.jks"
               password = "trustpass"
            }
           }
    }
    server {
        port = 8081
    }
   ```
6. Launch the Gateway Service.
7. Open your browser and use the Gateway Service's host and the `port` property from the configuration (`localhost:8081` in the example above).
8. The login page is displayed. Log in using the initial user credentials.
9. You can either open the **USER ADMINISTRATION** page to manage users, groups, and roles (please note that this requires admin rights), or open the CENM management console to manage your CENM instance.

{{< note >}}
See the [CENM User Admin tool](user-admin.md) documentation for more information. This tool is accessed in the same way as the CENM management console.
{{< /note >}}

## User guide

### Access the CENM management console

The CENM management console is located in a directory within the machine that hosts your Gateway Service, followed by `/cenm`.

For example: `http://10.230.41.12:8080/cenm`

To access the CENM management console:

1. Navigate to the URL address for your CENM management console instance.

2. On the login screen, enter your user login credentials:

{{% figure zoom="/en/images/cenm-management-console-login-screen.png" alt="CENM management console login screen" %}}

3. Select **CENM CONSOLE**.

{{% figure zoom="/en/images/cenm-management-console-launcher.png" alt="CENM management console launcher screen" %}}

The CENM management console loads on the **NETWORK MAP** Service screen.

{{% figure zoom="/en/images/cenm-management-console-network-map-list-screen.png" alt="CENM management console Network Map Service screen" %}}

### Explore the Network Map Service

You can access network member details, filter information, and search using the Network Map Service screen.

#### Switch between Layout View and Map View of the Network Map

The default Network Map view is called **LAYOUT VIEW** - this is what you see when you log in to the CENM management console (as shown above).

There is also a **MAP VIEW**, which shows the Network Map as an actual map grid:

{{% figure zoom="/en/images/cenm-management-console-map-view.png" alt="CENM management console - Map View" %}}

You can switch between the two views by selecting **MAP VIEW**/**LAYOUT VIEW** respectively from the drop-down menu that opens when you click on your username in the top right corner of the screen:

{{% figure src="/en/images/cenm-management-console-map-layout-view-switch.png" alt="CENM management console - switching between Map View and Layout View" width=200 %}}

### View and update Network Parameters

To view the status and any pending changes to the Network Parameters, or to make new updates, click **NETWORK PARAMETERS** in the top navigation area of the screen. The Network Parameters view shows the current network parameters in the **CURRENT PARAMETERS** tab:

{{% figure zoom="/en/images/cenm-management-console-net-params-current-only.png" alt="CENM management console - Network Parameters" %}}

If there are pending updates, you will see them in the **PENDING UPDATE** tab:

{{% figure zoom="/en/images/cenm-management-console-net-params.png" alt="CENM management console - Network Parameters" %}}

To update the Network Parameters:

1. On the **NETWORK PARAMETERS** screen, scroll to the bottom and click **START UPDATE PROCESS** to open the **Network Parameters Update** form view:

{{% figure zoom="/en/images/cenm-management-console-net-params-update-started.png" alt="CENM management console - Network Parameters" %}}

2. Give a name to the update in the **ABOUT THE UPDATE** field.

3. Use the calendar picker to schedule the time and date of the **Flag Day** - this is the period during which the network parameters will update.

4. Make the required changes in the **BASIC PARAMETERS** fields. Alternatively, to make the changes in a command-line interface within the console, select the **CODE VIEW** in the top right corner of the screen:

{{% figure zoom="/en/images/cenm-management-console-net-params-code-view.png" alt="CENM management console - Network Parameters" %}}

5. If required, add a Notary to the update in the **NOTARIES** section.

6. Click **SET PARAMETERS**.

    Now that the update has been scheduled, click **ADVERTISE UPDATE** to advertise the update:

{{% figure zoom="/en/images/cenm-management-console-net-params-advertise.png" alt="CENM management console - Network Parameters - advertise update" %}}

7. Once you have updated the parameters, scroll down and click **ADVERTISE UPDATE** again to advertise the parameters update:

{{% figure zoom="/en/images/cenm-management-console-net-params-advertise-params.png" alt="CENM management console - Network Parameters - advertise parameters update" %}}

8. You can now see the nodes that have accepted the update, and those that are still pending.

    Once you have advertised the update, and the scheduled time has been reached, you can execute the flag day.

9. Scroll down and click **Execute Flag Day**:

{{% figure zoom="/en/images/cenm-management-console-net-params-acceptance.png" alt="CENM management console - Network Parameters - execute Flag Day" %}}

### Check Identity Manager Service status and progress

To access the Identity Manager Service, click **IDENTITY MANAGER** in the top navigation area of the screen. A list of CSR requests and their statuses is shown in the **CSR STATUS** tab:

{{% figure zoom="/en/images/cenm-management-console-identity-manager-csr-status.png" alt="CENM management console - Identity Manager Service" %}}

#### Check CSR (onboarding) and CRL (removal) status

To check the status of members being onboarded to the network, click the **CSR STATUS** tab. You can see the status tag, and details of the request like the Request ID and legal name of the prospective member:

{{% figure zoom="/en/images/cenm-management-console-identity-manager-csr-status-open.png" alt="CENM management console - Identity Manager Service" %}}

To check the status of members being removed from the network, click the **CRR/CRL STATUS** tab. You can view the status tag for the removal progress, and details of the membership:

{{% figure zoom="/en/images/cenm-management-console-identity-manager-crr-crl-status-open.png" alt="CENM management console - Identity Manager Service" %}}

### Update services configuration files

You can access and edit the configuration files of the Identity Manager Service, the Signing Service, and the Network Map Service.

#### Identity Manager Service configuration

To access and edit the configuration files of the Identity Manager Service, click **CONFIGURATION** in the top navigation area of the screen, and then the **IDENTITY MANAGER** tab:

{{% figure zoom="/en/images/cenm-management-console-configuration-identity-manager.png" alt="CENM management console - Identity Manager Service configuration" %}}

#### Signing Service configuration

To access and edit the configuration files of the Identity Manager Service, click **CONFIGURATION** in the top navigation area of the screen, and then the **SIGNER** tab:

{{% figure zoom="/en/images/cenm-management-console-configuration-signer.png" alt="CENM management console - Signing Service configuration" %}}

#### Network Map Service configuration

To access and edit the configuration files of the Identity Manager Service, click **CONFIGURATION** in the top navigation area of the screen, and then the **NETWORK MAP** tab:

{{% figure zoom="/en/images/cenm-management-console-configuration-network-map.png" alt="CENM management console - Network Map configuration" %}}
