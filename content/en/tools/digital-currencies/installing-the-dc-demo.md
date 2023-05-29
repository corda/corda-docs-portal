---
date: '2023-03-21'
section_menu: tools
menu:
  tools:
    name: Installing the Digital Currencies Demo
    weight: 100
    parent: digital-currencies
    identifier: digital-currencies-installing-demo
    description: "Digital Currencies documentation describing how to install the Digital Currencies demo"
title: Installing the Digital Currencies Demo
---

This topic describes how to install the Digital Currencies demo, enabling you to trigger flow actions via a web-enabled GUI.

## Summary

1. [Install the prerequisites](#install-the-prerequisites)
2. [Configure Artifactory authentication](#configure-artifactory-authentication)
2. [Clone the Digital Currencies repositories](#clone-the-digital-currencies-repositories)
3. [Run a clean version of corda](#run-corda)
4. [Deploy the Digital Currencies CorDapp](#deploy-the-digital-currencies-cordapp) 
6. [Specify Virtual Nodes for Digital Currencies UI](#specify-virtual-nodes-for-digital-currencies-ui)
7. [Run the Digital Currencies UI](#run-the-digital-currencies-ui)

## Install the Prerequisites

The following guide assumes you have the following prerequisites installed.

* Operating systems
* Java Azul Zulu JDK 11
* Git
* npm
* node (version 16.18.0)
* gradle
* Docker Engine ~v20.X.Y or Docker Desktop ~v3.5.X
* Intellij
* [Corda CLI]({{< relref "../../platform/corda/5.0-beta/developing/getting-started/installing-corda-cli.md" >}}) 

  {{< attention >}}
  Ensure that you have the latest version of Corda CLI ("Gecko").
  {{</ attention >}}

## Configure Artifactory Authentication

This section describes how to specify the environment variables CORDA_ARTIFACTORY_USERNAME and CORDA_ARTIFACTORY_PASSWORD which are required to access internal Maven repositories. 

1. Navigate to https://software.r3.com/ui/user_profile.

2. If required, log in with your usual credentials.

3. Click on your email address at the top-right, then select **Edit Profile** from the menu displayed.

   The User Profile page is displayed.

4. Scroll down and click on **Generate API Key**.

   The message *Successfully generated API key* is displayed.
   
5. Copy the value in the **API Key** field.

6. In the Windows search box, search for *environment variables*.

7. Click **Edit the system environment variables**.

   The **System Properties** dialog box is displayed.

8. Click **Environment Variables**.

9. Add the following system variables:

   * `CORDA_ARTIFACTORY_USERNAME`: Set this to your email address.
   * `CORDA_ARTIFACTORY_PASSWORD`: Set this to the value of the **API Key** field from step 5.

## Clone the Digital Currencies Repositories

You need a local copy of both the following repositories:

* https://github.com/corda/digital-currencies
* https://github.com/corda/digital-currencies-ui

1. Navigate to a suitable directory; for example, C:\Repos.
2. Run the following commands:

  ```
  git clone https://github.com/corda/digital-currencies
  git clone https://github.com/corda/digital-currencies-ie
  ```

  {{<
  figure
	 src="images/cloned-repos.png"
   width=40%
	 figcaption="Cloned Repositories"
	 alt="Cloned Repositories"
   >}}

3. If necessary, initialise the git repos and change the remotes so you do not inadvertently push your work back.

4. Run IntelliJ.

5. Select **File > Open**, select the *digital-currencies* directory and click **OK**. Allow the import process complete.

   When complete, the project structure looks as follows:

   {{<
     figure
	 src="images/dc-open-in-intellij.png"
   width=80%
	 figcaption="Digital Currencies Project in IntelliJ"
	 alt="Digital Currencies Project in IntelliJ"
   >}}

The project includes Gradle tasks to manage a local deployment of Corda and DC.

Configure Gradle to use the correct version of Java:

6. Select **File > Settings**

   The **Settings** dialog box is displayed.

7. In the **Settings** dialog box, select **Build, Execution, Deployment > Build Tools > Gradle**.

8. In the  **Gradle VM** field, ensure that *Project SDK zulu-11* is selected, then click **OK**

## Run Corda

First, ensure that any current version of Corda running is stopped and cleaned:

1. In the *Gradle* panel, double-click the **stopAndCleanCorda** Gradle task.

   The log panel at the bottom of the screen should show output ending with *BUILD SUCCESSFUL*:

   ```
   BUILD SUCCESSFUL in 6s
   11 actionable tasks: 2 executed, 9 up-to-date
   17:29:16: Execution finished 'stopAndCleanCorda'.
   ```

2. In the *Gradle* panel, double-click the **startCorda** Gradle task.

    The log panel at the bottom of the screen should show output ending with *BUILD SUCCESSFUL*:

    ```
        ______               __      
       / ____/     _________/ /___ _ 
     / /     __  / ___/ __  / __ `/ 
    / /___  /_/ / /  / /_/ / /_/ /  
    \____/     /_/   \__,_/\__,_/ 
    --- Combined Worker (5.0.0.0-Hawk101) ---
    Running Changeset: net/corda/db/schema/config/migration/cpx-creation-v1.0.xml::cpx-creation-v1.0::R3.Corda
    Running Changeset: net/corda/db/schema/config/migration/config-creation-v1.0.xml::config-creation-v1.0::R3.Corda
    Running Changeset: net/corda/db/schema/config/migration/chunking-creation-v1.0.xml::chunks-creation-v1.0::R3.Corda
    Running Changeset: net/corda/db/schema/config/migration/static-network-creation-v1.0.xml::static-network-creation-v1.0::R3.Corda
    Running Changeset: net/corda/db/schema/messagebus/migration/db-message-bus-tables-v1.0.xml::db-message-bus-tables::R3.Corda
    Running Changeset: net/corda/db/schema/rbac/migration/rbac-creation-v1.0.xml::rbac-creation-v1.0::R3.Corda
    Running Changeset: net/corda/db/schema/crypto/migration/crypto-creation-v1.0.xml::crypto-creation-v1.0::R3.Corda

    ```

3. Wait up to one minute for Corda to finish its start-up routine.

###  Test Corda Using Swagger

Test that Corda is live by accessing and testing its Swagger UI.

1. In a browser, open the URL:

    [https://localhost:8888/api/v1/swagger#/](https://localhost:8888/api/v1/swagger#/)

    If Corda has started, the following page is displayed:

    {{<
      figure
	  src="images/swagger.png"
      width=80%
	  figcaption="Corda Swagger UI"
	  alt="Corda Swagger UI"
    >}}

To access Corda, you must authorize Swagger:

2. Click the **Authorize** button.

    {{<
      figure
	  src="images/swagger_auth_button.png"
      width=20%
	  figcaption="Swagger Authorize Button"
	  alt="Swagger Authorize Button"
    >}}


   The **Available Authorizations** dialog box is displayed:

    {{<
      figure
	  src="images/available_auth_dialog.png"
      width=60%
	  figcaption="Swagger Authorize Button"
	  alt="Swagger Authorize Button"
    >}}

3. Enter the username and password *admin* and *admin* and click **Authorize**.

   You are now authorized:

   {{<
      figure
	  src="images/swagger_authorized.png"
      width=60%
	  figcaption="Swagger Authorized"
	  alt="Swagger Authorized"
    >}}

4. Click **Close**.

For the purposes of testing Corda, we will use the CPI endpoint.

5. Click the CPI GET method to expand it:

    {{<
      figure
	  src="images/cpi-get-method.png"
      width=80%
	  figcaption="cpi GET method"
	  alt="cpi GET method"
    >}}

6. Click **Try it out**, followed by **Execute**.

   If Corda is running correctly, you should see a response similar to this:

   {{<
      figure
	  src="images/cpi-get-response.png"
      width=100%
	  figcaption="cpi GET response"
	  alt="cpi GET method"
   >}}

   As we have not uploaded any CPIs yet, the returned list of CPIs is empty. If Corda has not started yet, Swagger will return a *TypeError: Load failed* error.

   {{< note >}}
   If you get any errors, first try the following: run the *stopAndCleanCorda* Gradle task, run the *startCorda* Gradle task, wait one minute, then try and access Swagger again.

   If you still get errors, check the topic on [Resetting the CSDE]({{< relref "/content/en/platform/corda/5.0-beta/developing/getting-started/reset-csde.md" >}}).
   {{</ note >}}

## Deploy the Digital Currencies CorDapp

1. In IntelliJ, double-click the **digital-currencies/Tasks/csde-cordapp/5-vNodeSetup** Gradle task.

   The task will run tasks 1 to 5 in turn:
   
   ```
   15:34:12: Executing '5-vNodesSetup'...

   Starting Gradle Daemon...
   Gradle Daemon started in 1 s 342 ms
   > Task :projInit
   
   > Task :1-createGroupPolicy
   createGroupPolicy: Creating a GroupPolicy

   > Task :2-createKeystore
   Creating a keystore and signing certificate.
   Certificate was added to keystore
   Certificate was added to keystore
   Certificate stored in file <workspace/signingkey1.pem>
   
   ...
   
   > Task :3-buildCpis
   Creating digital-currencies Cpi.
   Creating Digital Currencies Notary Server Cpi.

   ...
 
   > Task :4-deployCpis
   Certificate 'gradle-plugin-default-key' uploaded.
   Certificate 'my-signing-key' uploaded.
   Certificate 'beta-ca-root' uploaded.
   
   ....
   
   > Task :5-vNodesSetup
   Creating virtual node for: CN=Alice, OU=Test Dept, O=R3, L=London, C=GB
   Creating virtual node for: CN=Bob, OU=Test Dept, O=R3, L=London, C=GB
   Creating virtual node for: CN=Charlie, OU=Test Dept, O=R3, L=London, C=GB
   Creating virtual node for: CN=Dave, OU=Test Dept, O=R3, L=London, C=GB
   Creating virtual node for: CN=NotaryRep1, OU=Test Dept, O=R3, L=London, C=GB
   Creating virtual node for: CN=Goku, OU=Test Dept, O=R3, L=London, C=GB
   ```
   
   The log panel at the bottom of the screen should show output ending with *BUILD SUCCESSFUL*:

   ```
   BUILD SUCCESSFUL in 2m 19s
   24 actionable tasks: 24 executed
   15:36:32: Execution finished '5-vNodesSetup'.
   ```
 
## Specify Virtual Nodes for Digital Currencies UI

{{< note >}}
This section can normally be skipped as appConfig.json is automatically configured with the correct nodes; you can skip to [Run the Digital Currencies UI](#run-the-digital-currencies-ui) It remains included if you understand how appConfig.json can be configured manually. 
{{</ note >}}


1. Open the Swagger UI:

   [https://localhost:8888/api/v1/swagger#/](https://localhost:8888/api/v1/swagger#/)

2. Scroll down to the Virtual Node API:

   {{<
      figure
	  src="images/virtual-node-api.png"
      width=100%
	  figcaption="Virtual Node API"
	  alt="Virtual Node API"
   >}}

3. Expand the GET method:

   {{<
      figure
	  src="images/virtual-node-api-get.png"
      width=100%
	  figcaption="Virtual Node API Get Method"
	  alt="Virtual Node API Get Method"
   >}}

4. Click **Try it out**, then **Execute**.

   (You may need to enter your credentials - *admin/admin* - again.)

   The response body will include a list of five nodes:

   {{< 
      figure
	  src="images/virtual-node-api-get-response.png"
      width=100%
	  figcaption="Virtual Node API Get Method Response"
	  alt="Virtual Node API Get Method Response"
   >}}

5. Take a note of the *x500Name* for four nodes.

6. Navigate to the *digital-currencies-ui/public/appConfig* directory.

7. Edit the file *appConfig.json*.

   The file contains both configuration details for multiple nodes: 
   
   * one of appType "CENTRAL_BANK",
   * one of appType "COMMERCIAL_BANK",

   Each has a *holdingIdHash* parameter and a *x500* parameter:

   ```json 
   {
    "appType": "CENTRAL_BANK",
    "apiUrl": "http://localhost:10055",
    "holdingIdHash": "BA0AE88BD184",
    "x500": "CN=Charlie, OU=Test Dept, O=R3, L=London, C=GB",
    
    ...
    
    "appType": "COMMERCIAL_BANK",
    "apiUrl": "https://localhost:8888",
    "holdingIdHash": "11BD540F9730",
    "x500": "CN=Bob, OU=Test Dept, O=R3, L=London, C=GB",
    ```

For each bank:

8. Replace the value of *holdingIdHash* with the *shortHash* value noted in step 5.

9. Replace the value of *x500* with the *x500Name* value noted in step 5.

10. Save and close the file.

## Run the Digital Currencies UI

1. Open a command prompt and navigate to the *digital-currencies-ui* directory, where you cloned that repository.

2. Run the command:

   ```
   npm ci
   ```

   This command downloads the dependencies required by the web server front-end.

3. Run the command:

   ```
   npm run dev
   ```

   The following output is displayed:

   ```
   VITE v3.1.3  ready in 417 ms

   ➜  Local:   http://127.0.0.1:5173/
   ➜  Network: use --host to expose
   ```

The Digital Currencies UI is now available. See [Launching the Digital Currencies GUI]({{< relref "launching-the-dc-demo.md" >}}).