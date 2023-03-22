---
date: '2023-03-21'
section_menu: tools
menu:
  tools:
    name: Installing the Digital Currencies Demo
    weight: 100
    parent: digital-currencies
    identifier: digital-currencies-installing
title: Installing the Digital Currencies Demo
---

# Setting up Digital Currencies

## Summary

1. [Install the prerequisites](#prerequisites)
2. [Clone the Digital Currencies repositories](#clone-the-digital-currencies-repositories)
3. [Run a clean version of corda](#run-corda)
4. [Deploy the Digital Currencies CorDapp](#deploy-the-digital-currencies-cordapp)

   (Temporary) switch to CDC-247/POC-external-apis-with-flow-tracking branch.
   
5. [Run the External API Service using the runExternalApiServer Gradle task](#run-the-external-api-service-using-the-runexternalapiserver-gradle-task)
6. [Specify Virtual Node for Digital Currencies UI](#specify-virtual-node-for-digital-currencies-ui)
7. [Run the Digital Currencies UI](#run-the-digital-currencies-ui)

## Prerequisites

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
   width=80%
	 figcaption="Cloned Repositories"
	 alt="Cloned Repositories"
   >}}

{{< note >}}
For digital-currencies-ie, switch to the POC-DEMO branch.
{{</ note >}}

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

The project includes Gradle tasks to manage a local deployment of Corda and DC:

   {{<
     figure
	 src="images/gradle-tasks.png"
   width=80%
	 figcaption="Digital Currencies Project Gradle Tasks"
	 alt="Digital Currencies Project Gradle Tasks"
   >}}

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
    BUILD SUCCESSFUL in 10s
    12 actionable tasks: 2 executed, 10 up-to-date
    17:31:26: Execution finished 'startCorda'.
    ```

3. Wait up to one minute for Corda to finish its start-up routine.

###  Test Corda Using Swagger

Test that Corda is live by accessing and testing its Swagger UI.

1. In a browser, open the URL:

    https://localhost:8888/api/v1/swagger#/

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
      width=30%
	  figcaption="Swagger Authorize Button"
	  alt="Swagger Authorize Button"
    >}}


   The **Available Authorizations** dialog box is displayed:

    {{<
      figure
	  src="images/available_auth_dialog.png"
      width=80%
	  figcaption="Swagger Authorize Button"
	  alt="Swagger Authorize Button"
    >}}

3. Enter the username and password admin/admin and click **Authorize**.

   You are now authorized:

   {{<
      figure
	  src="images/swagger_authorized.png"
      width=80%
	  figcaption="Swagger Authorized"
	  alt="Swagger Authorized"
    >}}

4. Click **Close**.

For the purposes of testing Corda, we will use the cpi endpoint.

5. Click on the cpi GET method to expand it:

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
      width=80%
	  figcaption="cpi GET response"
	  alt="cpi GET method"
   >}}

   As we have not uploaded any CPIs yet, the returned list of CPIs is empty. If Corda has not started yet, Swagger will return a *TypeError: Load failed* error.

   {{< note >}}
   If you get any errors, first try the following: run the *stopAndCleanCorda* Gradle task, run the *startCorda* Gradle task, wait one minute, then try and access Swagger again.

   If you still get errors, check the topic on [Resetting the CSDE]({{< relref "/content/en/platform/corda/5.0-beta/developing/getting-started/reset-csde.md" >}}).
   {{</ note >}}

## Deploy the Digital Currencies CorDapp

1. In IntelliJ, double-click the **digital-currencies/Tasks/csde-cordapp/quickDeployCorDapp** Gradle task.

   The log panel at the bottom of the screen should show output ending with *BUILD SUCCESSFUL*:

   ```
   BUILD SUCCESSFUL in 1m 15s
   40 actionable tasks: 12 executed, 28 up-to-date
   19:38:37: Execution finished 'quickDeployCorDapp'.
   ```
 {{< note >}}
Temporary step: Need to check out the branch origin/CDC-247/POC-external-apis-with-flow-tracking
 {{</ note >}}
 
## Run the External API Service using the runExternalApiServer Gradle task

*  In IntelliJ, double-click the **digital-currencies/external-api/Tasks/other/runExternalApiServer** Gradle task.

   The log panel at the bottom of the screen should show output ending with *BUILD SUCCESSFUL*:

## Specify Virtual Node for Digital Currencies UI

1. Open the Swagger UI.

2. Scroll down to the Virtual Node API:

   {{<
      figure
	  src="images/virtual-node-api.png"
      width=80%
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

   The response body will include a list of one or more nodes:

   {{< 
      figure
	  src="images/virtual-node-api-get-response.png"
      width=100%
	  figcaption="Virtual Node API Get Method Response"
	  alt="Virtual Node API Get Method Response"
   >}}

5. Take a note of the *shortHash* value and *x500Name* for any node.

6. Navigate to the *digital-currencies-ui/public/appConfig* directory.

7. Edit the file *appConfig.json*.

   The file contains both a *holdingIdHash* parameter and a *x500* parameter:

   ```
   {
    "appType": "CENTRAL_BANK",
    "apiUrl": "http://localhost:10055",
    "holdingIdHash": "BA0AE88BD184",
    "x500": "CN=Charlie, OU=Test Dept, O=R3, L=London, C=GB",
    ```

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

The Digital Currencies UI is now available.

In a browser access the URL http://localhost:5173/ (rather than the above URL).