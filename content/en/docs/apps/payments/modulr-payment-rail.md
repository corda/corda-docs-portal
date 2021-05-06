---
date: '2020-01-08T09:59:25Z'
menu:
  apps:
    parent: "payments"
    identifier: modulr-payment-rail
tags:
- Payments
- Payments SDK
title: Modulr Payment Rail CorDapp Alpha
weight: 200
---
# Modulr Payment Rail CorDapp Alpha

Modulr is a payments-as-a-service platform which automates payment flows through one API. You can use the Modulr Payment Rail CorDapp, along with [Payments-core](payments-core-cordapp) to make payments using Modulr as a Payment Service Provider (PSP).

{{< warning >}}
This version of the Modulr Payment Rail CorDapp is fully operational, but is at a very early stage in its development. If you are interested in using this solution at a commercial scale, contact a Corda specialist to explore how the development of this feature is set to accelerate and change in future versions.
{{< /warning >}}

## How this works with the Payments-core CorDapp

This payment uses the Payments-core CorDapp to make payments and retrieve payment data.

A typical payment looks like this:  

1. The Modulr Payment Rail CorDapp connects to the Modulr API.

2. The Modulr CorDapp extracts the necessary information from the provided ISO20022 formatted message and constructs a JSON payload as specified by Modulr.

3. The ISO 20022 payload sent to Modulr is stored.

4. The Modulr Payment Rail CorDapp sends an HTTP request containing the specified payment initiation payload to the Modulr API. Modulr provides different environment URLs which we specify in the node's configuration.

5. The Modulr Payment Rail CorDapp polls the status of the payment through the Modulr API until Modulr returns a final state of either `PROCESSED` or `CANCELLED`.

6. The response received from the Modulr API is converted from JSON to the equivalent ISO XML message.

## Project structure

Use this documentation to explore the `modulr-rail` module. You should also be familiar with the [Payments-core CorDapp](payments-core-cordapp) before using this rail.

In the Modulr Payment Rail main submodule, there are two packages:

* Client - which contains the `ModulrClient` class - a proxy to the Modulr API.
* Rail - which contains sub-projects with the actions, flows, and services required to make payments from a Corda node via the Modulr PSP.

### Client module

The `com.r3.payments.modulr.client` package contains the `ModulrClient` class, a wrapper class which acts as a proxy to the Modulr API. The `client` obtains data from the Modulr API via HTTP calls to REST endpoints.

This package contains Java Object representations of JSON entities which may be serialized to JSON to be sent via HTTP to the Modulr API.  

Additionally, there are `Utils` and `Exceptions` classes as well as a class for the Modulr API REST paths.

### Rail

Rail contains two subprojects:

* `actions`.
* `flows`.  

It also contains classes for:

* `Utils`.
* `Exceptions`.
* A `CordaService` called `ModulrService`.  

### ModulrService

`ModulrService`, an implementation of `PaymentRailServiceInterface` from [Payments-core CorDapp](payments-core-cordapp), provides access to a `ModulrClient` that will be shared across flows - executing actions that require interaction with the Modulr API. This abstraction provides a safe and resource-efficient way for a Corda node to communicate with the Modulr API.

This service is initialized during node startup with environment variables retrieved through the configuration of the `payments-core` CorDapp. This includes generic information concerning the amount and currency types in which payments may be made using this rail, as well as specific information required for communicating with the Modulr API - including the API key and API secret.

## Actions

Learn more about `Actions`/`IdempotentAction` and `external-action-manager` in the [Payments-core documentation](payments-core-cordapp).

The actions package contains idempotent and non-idempotent actions to communicate with the Modulr API using the `ModulrClient`. The following is a list of all the classes that contain actions used in this CorDapp followed by the abstract class which is extended:

`external-action-manager`.

`ModulrAccountActions`
- `GetModulrAccounts` extends `Action`.
- `CreateModulrAccountByCustomer` extends `IdempotentAction`.

`ModulrCustomerActions`
- `GetModulrCustomers` extends `Action`.

`ModulrPaymentAction`
- `InitiateModulrPayment` extends `IdempotentAction`.
- `GetModulrPaymentByDeduplicationId` extends `Action`.
- `GetModulrPaymentByID` extends `Action`.


## Flows

The flows package contains flows that allow a node to send a payment to another node, an external destination (not a Corda node), and a flow to retrieve the status of a payment - all using the Modulr API.

Respective flows trigger an action which in turn communicate with the Modulr API through the `ModulrClient`.  The following is a list of flows used by modulr-rails-cordapp.

{{< note >}}
These are not to be used directly by the developer, they are only accessible through the Payments-core CorDapp.  
{{< /note >}}

### ModulrISOPaymentFlow

Makes a payment using the Modulr API and client to a destination not represented by a Corda node. This flow executes an `InitiateModulrPayment` after constructing a `PaymentInitiationPayload` from a received `isoMessage`. It will then continue to poll for the results of the initiated payment and return the payment entity once it has been processed.

#### Parameters

* `isoMessage` - A XML message formatted in ISO20022.
* `clientDeduplicationId` - An ID submitted by the invoking client for the purposes of deduplication.

#### Return type

* `String` - This flow will return a `String` representing an ISO20022 status report message regarding the Modulr payment.

### ModulrPaymentInitiationFlow

This flow initiates a payment using the Modulr payment rail.  It will construct and execute an `InitiateModulrPayment` action using the provided `Destination` to create a Modulr-specific `PaymentInitiationPayload` as required input.

#### Parameters

* `paymentAmount` - The amount of the payment to be initiated, denominated in a specific currency.
* `destination` - Information surrounding the destination (beneficiary) of the payment.
* `clientDeduplicationId` - An ID submitted by the invoking client for the purposes of deduplication.

#### Return type

* `PaymentResult<ModulrPaymentEntity>` - This flow will return a `PaymentResult` object with type argument `ModulrPaymentEntity`, representing the result of running a `ModulrPaymentPollingFlow` as a subflow.

#### Exceptions

* `PaymentExecutionException` - This exception will be thrown if the currency specified is not one of the two accepted currencies: `GBP` or `EUR`.
* `IdempotentActionExecutionException` - This exception will be thrown if the action triggered to initiate a Modulr payment is unsuccesful.
* `ModulrPaymentExecutionException` - This exception is thrown if no other exceptions are thrown and the initiated Modulr payment is still unsuccesful.

### ModulrISOGetAccountFlow

This flow gets the account balance for the specified account.

#### Parameters

* `isoMessage` - An XML message formatted in ISO20022.

#### Return type

* `String` - This flow will return an XML `String` representing the balance of the specified account.

### ModulrPaymentPollingFlow

This flow executes a `GetModulrPaymentByID` action and is used as a subflow by several other initiating flows to determine when a specific Modulr payment has been successfully processed.

#### Parameters

* `paymentId` - The ID of the payment that has been submitted for processing by the Modulr Payment Rail CorDapp.

#### Return type

* `PaymentResult<ModulrPaymentEntity>` - This flow will return a `PaymentResult` object with type argument `ModulrPaymentEntity`, representing the result of running a `ModulrPaymentPollingFlow` as a subflow.

#### Exceptions

* `ModulrPaymentException` - This exception will be thrown if the status of the polled payment is `CANCELLED`.
* `IdempotentActionExecutionException` - This exception will be thrown if the action triggered to initiate a Modulr payment is unsuccesful.
* `ModulrPaymentTimeoutException` - This exception is thrown if an `ExponentialBackOffException` is caught.  An `ExponentialBackOffException` is thrown if exponential backoff used to validate the Modulr payment has reached a maximum threshold.

## Frontend Demo

To see how a payments solution might be presented to users on your network, you can use this demo console for the Modulr Payment Rail on Corda.

Please follow these instructions carefully as this is an experimental web application, and you may encounter bugs:

### Set up the demo

To set up a demo payment with  UI:

1. Open the project in IntelliJ and then open the Gradle tab on the right side of the window.
2. Open a terminal and navigate to the root of `payments-cordapp`.
3. Run `./gradlew clean deployNodes` to deploy the two nodes.
4. Run `build/nodes/runnodes`.  The following nodes should have started `Party A` and `Party B`  If the nodes don't start properly, you can manually run the `jar` for each node, located within the `build` directory.
5. Open two new terminal tabs (make sure you are in the root of `payments-cordapp`).  Run `./gradlew runPartyA` in one tab and `./gradlew runPartyB` in the other.  These commands will start the server for the frontend.
6. In a new terminal window, navigate to `payments-cordap/modulr-rail-frontend`.
7. Run `npm install -l` to install all npm dependencies
8. Run `npm start` to start the frontend server.

### Use the demo console

The frontend currently allows you to do two things:

* Make a payment.
* Get the status of a payment.

You must log in as a Party to make a payment or get the status of a payment.  After logging in, you must make a payment before using `GetPayment`. The payment will take 1.9 minutes, almost exactly. The only supported currency is EUR.

To use the console to make a payment:

1. Open [http://localhost:4006](http://localhost:4006) to view it in the browser.

2. Log in as either Party A or Party B.

3. Make a payment with the provided fields.
The result of the payment will be seen: A XML payload representing a payment status report.

You can now use the value of `<MsgId>` (a field in the XML payload) to get the status of the payment with `GetPayment`.

## Creating and installing the CorDapp `.jar` file

Once your dependencies are set correctly, you can build your CorDapp `.jar` file(s) using the Gradle `jar` task:

Unix/Mac OSX: `./gradlew jar`

Windows: `gradlew.bat jar`

Each of the project’s modules will be compiled into its own CorDapp `.jar` file. You can find these CorDapp `.jar` files in the `build/libs` folders of each of the project’s modules.

{{< note >}}
The hash of the generated CorDapp `.jar` file is not deterministic, as it depends on variables such as the timestamp at creation. Nodes running the same CorDapp must therefore ensure they are using the exact same CorDapp `.jar` file, and not different versions of the `.jar` file created from identical sources.

The file name of the `.jar` file must include a unique identifier to deduplicate it from other releases of the same CorDapp. This is typically done by appending the version string to the CorDapp’s name. This unique identifier should not change once the `.jar` file has been deployed on a node. If it does change, make sure no one is relying on `FlowContext.appName` in their flows (see Versioning).
{{< /note >}}

At start-up, nodes will load any CorDapps present in their `cordapps` folder. In order to install a CorDapp on a node, the CorDapp `.jar` file must be added to the `<node_dir>/cordapps/` folder (where `node_dir` is the folder in which the node’s `.jar` file and configuration files are stored) and the node must be restarted.
