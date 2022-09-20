---
date: '2022-09-19'
title: "Running your first CorDapp"
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-start
    identifier: corda-5-dev-preview-run-first-cordapp
    weight: 3000
section_menu: corda-5-dev-preview
---
The CSDE includes flows and tests for a very simple CorDapp, which you can run "out of the box".

The code for the flow can be found in the `src/main/kotlin.com.r3.developers.csdetemplate.MyFirstFlow.kt` file. This is also the code described in the [MyfirstFlow section](link).

## Starting the Corda combined worker
To run the flow, you must first start a local combined-worker version of Corda. CSDE includes helper gradle tasks to do this.
{{< figure src="starting-corda.png" width="50%" figcaption="CSDE startCorda task" alt="CSDE task to start the combined worker in IntelliJ" >}}

The `startCorda` task should complete relatively quickly with this message:
{{< figure src="starting-corda-complete.png" figcaption="CSDE startCorda task completed" alt="CSDE task to start the combined worker in IntelliJ completed" >}}

However, you must wait approximately one minute for Corda to finish its start-up routine.
Currently, we do not have a liveness detector for Corda in the CSDE so we check liveness by manually hitting an endpoint.

## Testing Liveness and Swagger
Corda exposes [HTTP REST API](../../developing/rest-api/rest-api.html) endpoints for interacting with itself and the CorDapps running on it. It also exposes a Swagger interface which is described in the following sections.

### Displaying the Swagger UI
To display the Swagger UI, use the following link:

https://localhost:8888/api/v1/swagger#/

{{< note >}}
* A message about certificates may be displayed. You will need to click through to the page. <** get more details here **>
* Currently the UI may not display on Chrome and we advise using a different browser.
{{< / note >}}

If Corda has started, the Swagger UI displays:
{{< figure src="starting-corda-complete.png" figcaption="Swagger UI showing Corda liveness" alt="Swagger UI showing Corda" >}}

If Corda has not started yet, the page will not load.
If the Swagger UI is already open whilst starting Corda, you must hit an endpoint to test liveness of Corda.

### Authorizing Swagger

 To access the Corda cluster, you must authorize Swagger:
 1. Click the green **Authorise** button.
{{< figure src="authorize-button.png" figcaption="Swagger Authorize button" alt="Button in Swagger UI to authorize access to the Corda cluster" >}}
   The **Available authorizations** window is displayed.
2. Enter the username and password. For the purposes of experimental development, the username for the combined worker is set to  `admin` and the password is `admin`.
{{< figure src="authorize.png" width="50%" figcaption="Swagger Authorize authorizations window" alt="Authorize authorizations window in Swagger UI to authorize access to the Corda cluster" >}}

### Hitting endpoints

Now you are authorised, you can start hitting endpoints. The easiest one to try is `/cpi`  because it is the first one on the swagger page and it requires no arguments:
1. Expand the `GET /cpi` row and click **Try it out**.
{{< figure src="get-cpi.png" figcaption="Try it out button for GET /cpi" alt="Expanded GET /cpi with Try it out button" >}}
2. Click the **Execute** button to hit the endpoint.
   If Corda has started you should see a response like this:
   {{< figure src="get-cpi-response.png" figcaption="Swagger showing a successful response to GET /cpi" alt="Swagger showing a successful response to GET /cpi" >}}
   As we have not uploaded any CPIs yet, the returned list of CPIs is empty.
   If Corda has not started yet, swagger will return an error:
   {{< figure src="get-cpi-error.png" figcaption="Swagger showing an error response to GET /cpi" alt="Swagger showing an error response to GET /cpi" >}}
   If this occurs, you either have not started Corda, Corda has not finished starting, or something has gone wrong. If something has gone wrong, you should try again or [reset the environment and start again](reference to section on resetting the environment).
   {{< note >}}
   Each time you start Corda, it is a fresh instance. There is no persistence of state between restarts.
   {{< /note >}}

## Deploying a CorDapp
You can use the `MyFirstFlow` flow to build a CorDapp, without any further work:
1. Click the `deployCorda` Gradle task:
{{< figure src="deploy-cordapp.png" width="50%" figcaption="CSDE deployCorda task" alt="CSDE task to deploy a CorDapp in IntelliJ" >}}
   This task runs a series of Gradle tasks to:
   * Build the CPB (Cordapp)
   * Create the GroupPolicy (Application Network definition)
   * Generate signing keys to sign the CPB and CPI
   * Build The CPI (Combination of CPB and Group Policy)
   * Sign the CPI
   * Upload the CPI to Corda
   * Create and register the Virtual nodes with the CPI
   {{< note >}}
   Some of these task only need to run once and will not run again if not required.
   {{< /note >}}
    You should now be able to Start the MyFirstFlow from the Swagger UI.

### Starting your first flow
To run your first flow:
1. Find the `holdingidentityshorthash` for the virtual node you want to trigger the flow on. You can do this by running the `listVnodes` gradle task which will list the VNodes set up:
   {{< figure src="list-vnodes.png" figcaption="Running the listVnodes gradle task" >}}
   The 12 digit hash is the `holdingidentityshorthash` that acts as the unique identifier for a virtual node.
2. Expand the `POST /flow/{holdingidentityshorthash}` endpoint in Swagger and click **Try it out**.
{{< figure src="post-flow.png" figcaption="Try it out button for POST /flow/{holdingidentityshorthash}" alt="Expanded POST /flow/{holdingidentityshorthash} with Try it out button" >}}  
3. Enter the hash and the `requestBody` and click **Execute**.
{{< figure src="post-flow-arguments.png" figcaption="Arguments for POST /flow/{holdingidentityshorthash}" >}}  

requestBody code:
```kotlin
{    
   "clientRequestId": "r1",    
   "flowClassName": "com.r3.developers.csdetemplate.MyFirstFlow",    
   "requestData": {
      "otherMember":"CN=Bob, OU=Test Dept, O=R3, L=London, C=GB"
   }
}
```
* `ClientRequestId` is a unique identifier for the request to start a flow.
* `flowClassName` is the fully qualified path to the flow class you want to run.
* `requestData` is the set of arguments you pass to the flow.

   You should get the following response:
   {{< figure src="post-flow-start-requested.png" figcaption="Successful response for POST /flow/{holdingidentityshorthash}" >}}  

Note, if you forget to change the `ClientRequestId` on subsequent attempts to run the flow, you will receive this error message:
{{< figure src="post-flow-already-started-error.png" figcaption="Error response for POST /flow/{holdingidentityshorthash" >}}  

Because the API is asynchronous, at this stage you only receive the confirmation `START_REQESTED`. There is no indication of  the flow has been successful. To find out the status of the flow, you must check the flow status.

### Checking the flow status
To check the flow status:
1. Expand the `GET /flow/{holdingidentityshorthash}/{clientrequestid}` endpoint in Swagger and click **Try it out**.
3. Enter the hash and the `requestid` used when [starting the flow](#starting-your-first-flow) and click **Execute**.
{{< figure src="get-flow-arguments.png" figcaption="Arguments for GET /flow/{holdingidentityshorthash}/{clientrequestid}" >}}  
   If the flow is successful, you will see the following response:
{{< figure src="get-flow-completed.png" figcaption="Successful response for GET /flow/{holdingidentityshorthash}/{clientrequestid}" >}}  
Note the flowStatus of  "COMPLETED" and flowResult of "Hello Alice best wishes from Bob".
If you receive a response with a status of "RUNNING”, wait a short time and retry the status check.
<!--
We will understand why that is the flow result in a subsequent section where we explain the flow code.

You have now run your first flow on Corda.-->
