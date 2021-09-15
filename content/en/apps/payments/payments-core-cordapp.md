---
date: '2020-01-08T09:59:25Z'
menu:
  apps:
    parent: "payments"
    identifier: payments-core-alpha-cordapp
tags:
- Payments
- Payments SDK
title: Payments-core Alpha
weight: 100
---
# Payments-core Alpha

The Payments-core CorDapp contains all the flows and actions that are required to make payments between nodes, and between nodes and external parties. This means you can write CorDapps that use these flows to facilitate payments, via a Payment Service Provider (PSP), on a Corda network.

With this version of the Payments-core CorDapp, you can theoretically create payments via integration with any desired PSP. This is made possible using the ISO 20022 messaging standard, which is marshalled from raw XML by the Payments-core CorDapp as the API connection is made to the PSP. The best way to see this in action is to make use of the Mock Payment Rail feature, included in the project.

A typical payment flow using this CorDapp looks like this:

1. A payment flow is initiated from a node on your network.
2. The initiated payment triggers a flow to determine which PSP will be used to make the payment.
3. The PSP is contacted via the Payments API.
4. Raw XML messaging containing the required authorization and payment protocols is converted to and from ISO 20022 messaging as the node communicates with the PSP.
5. Payment is completed.
6. A flow is initiated to confirm the status of the payment, via the same API.

{{< warning >}}
This early version of the CorDapp is to be used in an experimental capacity. Before investing in commercial development based on this feature, you should get in touch with your Corda team to discuss future changes as the architecture and functionality is developed.
{{< /warning >}}

### What you can do with the Alpha version of this feature

In trial conditions, you can create a CorDapp to:

* Initiate payments - either from one node to another on your network, or to an external destination.
* Get the status of a payment.
* Receive payments - either from a node on your network or an external source.
* Test sample ISO payloads using a mock PSP.

This functionality frees you from considering the specifics of every PSP/payment rail that your customers may want to use.

To use this Alpha feature:

1. Install the Payments-core CorDapp project.
2. Use the Mock Payment Client project to create a CorDapp.
3. Integrate a mock PSP with your Payments-core CorDapp.

## Integrating a PSP with the Payments-core CorDapp

Use these steps to get an overview of how you can integrate a PSP with your network. You can choose to create your own solution with a PSP of your choice, or follow these steps using the [Mock Payment Rail](#mock-payment-rail) which includes a mock PSP that acts in a similar way to most commercial PSPs, but will not incur costs. For early and experimental purposes, the Mock Payment Rail gives you a fast, easy to set up experience of making payments on Corda.

To integrate a PSP with the Payments-core CorDapp:

1. Create a new module with the following `build.gradle`

```
apply plugin: 'net.corda.plugins.cordapp'
apply plugin: 'net.corda.plugins.quasar-utils'
apply plugin: "kotlin-noarg"

cordapp {
    targetPlatformVersion 6
    minimumPlatformVersion 6

    workflow {
        name "<PSP Integration Layer Name>"
        vendor "com.r3"
        licence "Corda Enterprise Evaluation License"
        versionId 1
    }

    signing {
        enabled false
    }
}

sourceSets {
    main {
        resources {
            srcDir rootProject.file("config/dev")
        }
    }
    test {
        resources {
            srcDir rootProject.file("config/test")
        }
    }
    integrationTest {
        kotlin {
            compileClasspath += main.output + test.output
            runtimeClasspath += main.output + test.output
            srcDir file('src/integrationTest/kotlin')
        }
    }
}

configurations {
    integrationTestCompile.extendsFrom testCompile
    integrationTestRuntime.extendsFrom testRuntime
}

noArg {
    annotation("javax.persistence.Entity")
}

dependencies {
    compile "org.jetbrains.kotlin:kotlin-stdlib-jdk8:$kotlin_version"
    testCompile "org.jetbrains.kotlin:kotlin-test:$kotlin_version"
    testCompile "junit:junit:$junit_version"

    // HTTP Client Dependencies
    implementation "com.squareup.okhttp3:okhttp:$okhttp_version"

    // Corda dependencies.
    cordaCompile "$corda_core_release_group:corda-core:$corda_core_release_version"
    cordaRuntime "$corda_release_group:corda:$corda_release_version"
    testCompile "$corda_release_group:corda-node-driver:$corda_release_version"

    // Project dependencies
    cordapp project(":payments-core")

    // Logging dependencies
    implementation "org.apache.logging.log4j:log4j-api:$log4j2_version"
    implementation "org.apache.logging.log4j:log4j-core:$log4j2_version"
}

task integrationTest(type: Test, dependsOn: []) {
    testClassesDirs = sourceSets.integrationTest.output.classesDirs
    classpath = sourceSets.integrationTest.runtimeClasspath
}
```
2. Write a client for the PSP.  In the case of `mock-payment-rail`, this is `MockRailClient`.

3. Write an implementation of `PaymentRailServiceInterface` for the respective PSP; this is `MockRailService` in `mock-payment-rail`.  This will subsequently require implementing flows for initiating, polling, and making payments between parties.

4. Build an idempotent action for initiating a payment and a non-idempotent action for querying a payment, all through the PSP.  This can be done by extending the abstract classes discussed in the External Action Manager section below. These actions are triggered during a flow when a node needs to communicate with the client that you built in step 1.

5. Navigate to the `build.gradle` for the `payments-cordapp`, in the root of the project.  Set the extra property `nodeConfig` to the following string:

```
'''
{

  "paymentRails" : {

      "<PSP>" : {

          "associatedService" : "<classpath to PSP service from step 3>",

          "config" : {
              <config details for PSP>
          },

          "details" : {

              "acceptedCurrencies" : [

                  "<accepted currencies>"
              ],

              "maxAmount" : <max amount>,

              "minAmount" : <min amount>,

              "timeWindow" : <time window>
          },

          "enabled" : true
      }
  }   
}
'''
```

6.  In order to generate this config for testing purposes, you can edit the `generateMockRailConfig` function in `TestUtils` within `mock-payment-rail` to model the required config for the associated PSP.


## Project structure - what's inside the Payments-core CorDapp

The project contains five modules:

* `payments-core` - provides the standard API and deals with messages in the ISO 20022 messaging standard, and Integration layer (cordapp that communicates with PSP), which converts the standard ISO messages into PSP specific formats and handle communication and authorization with the specific PSP.  
* `external-action-manager` - used to manage and store asynchronous operations that occur outside of your network - like initiating payment via a PSP.
* `iso-xml-utils` - used to marshall and unmarshall raw XML into ISO 20022. ISO 20022 is the international messaging standard used by PSPs globally.
* `mock-payment-rail` - a test payment rail that allows you to quickly build and deploy a trial payment solution.
* `mock-payment-service-provider` - a test PSP that allows payments to be made in the mock environment.

### External Action Manager

The `external-action-manager` is used to manage and store external asynchronous operations that a node may need to execute, such as initiating a payment for a particular PSP.

Actions that can be performed using the `external-action-manager` are either **idempotent** or **non-idempotent**.  An action is idempotent when you want a specific operation to be executed once, no matter how many times the action is triggered.  For example, the `InitiateModulrPayment` action in `ModulrPaymentActions` is idempotent because you cannot allow a payment with a deduplication ID to initiate twice.

These actions are triggered during a flow when a node needs to make an HTTP request via the client for the PSP's API.  In the case of `MockPaymentRail`, the actions are triggered when a flow needs to make an asynchronous request using `MockRailClient`.  When an action is being executed during a flow, the flow is check-pointed and serialized to disk.

The `external-action-manager` module contains three important packages:

* `actions` contains two abstract classes, `Action` and `IdempotentAction` which allow for repeatable non-idempotent actions and idempotent actions, respectively.  Both abstract classes ensure that the client provided deduplication ID will be available at runtime.
* `persistence` contains a schema as well as classes to persist and flush `ProofOfAction` objects to/from the node database.  
* `services` contains an `ActionExecutionService`.  This service is designed to manage all external asynchronous operations that a node may need to execute.  These operations include idempotent and non-idempotent actions.

The module also contains an `Exceptions` class, to handle `ActionExcution` exceptions as well as a `Utilities` class, for helper functions in use throughout the module.

### ISO XML Utils

The `iso-xml-utils` module contains various utilities that marshall a raw XML to an ISO 20022 and unmarshall:

Unmarshalling (XML -> ISO POJO)

1. The raw XML is converted into a POJO using JAXB, this includes a syntactic validation of the XML using xsd schemes distributed by the ISO 20022 Registration Authority (RA)
2. The POJO representing the ISO message under goes syntactic, semantic, and scope validations.

Marshalling (ISO POJO -> XML)

- The POJO gets converted into XML using JAXB. As part of the conversion the syntax of the generated XML ISO message is checked.

The ISO 20022 message formats are described in a set of .xsd files published by the ISO 20022 Registration Authority (RA).

The JAXB Library provides functionality to generate the POJO classes from the ISO xsd files.  The classes for each of the message types are provided upfront.

Given the xsds, the marshalling/unmarshalling of the ISO XML from/to POJOs is handled by the JAXB library.

As part of the marshalling/ unmarshalling processes the XMLs are checked to make sure they are syntactically correct per the xsds. This ensures that all XML elements included are valid components of the overarching message set.

### Payments Core

The `payments-core` module contains three subpackages:

* `configuration` contains the interface to be implemented in order to configure a PSP/rail.
* `flows` contains flows that enable you to send payments between nodes, node to an external destination, obtain payment records, and send ISO 20022 formatted payments.
* `persistence` contains services/schemas to store `IsoMessageRecord` objects.

## Flows

Below are all the flows that enable you to:

* Send a payment from a node to an external destination.
* Send payments between nodes.
* Obtain payment records.
* Send ISO 20022 formatted payments.

### `ExternalDestinationPaymentFlow`

This flow will be used by Corda nodes to initiate payment to external destinations not represented by another Corda node with an associated network identity.

This flow is available to the node operator.

#### Parameters

* `designatedPaymentRail` - The payment rail that should be used to initiate the payment.
* `paymentAmount` - The amount of the payment denominated in the specified currency.
* `destination` - The details of the destination for the payment, the type of which is determined by the specified `designatedPaymentRail`.
* `clientDeduplicationId` - An optional ID that will be used to deduplicate payments initiated by the client.

#### Return type

* `PaymentRecord` - This flow returns the `PaymentRecord` which is persisted to the DB.

#### Command Line Interface

`flow start ExternalDestinationPaymentFlow designatedPaymentRail: <Payment Rail>, paymentAmount: <Payment Amount>, destination: <UUID of destination account>, clientDeduplicationId: <provided clientDeduplicationId>`




### `GetPaymentRecordsFlow`

This flow returns all payment records in the database associated with the provided initiator or beneficiary parties. It is available to the node operator.

#### Parameters

* `initiatingParty` - The legal identity of the node that initiated the payments being queried.
* `beneficiaryParty` - The legal identity of the node that received the payments being queried.

#### Command Line Interface

`flow start GetPaymentRecordsFlow initiatingParty: <X500 Name of initiatingParty>, beneficiaryParty: <X500 Name of beneficiary>`

Example: `flow start GetPaymentRecordsFlow initiatingParty: "O=partyA,L=New York,C=US", beneficiaryParty: "O=partyB,L=London,C=GB"`

#### Return type

`List<PaymentRecord>` - This flow will return a list of type `PaymentRecord`.

### PaymentFlow

This is the primary flow that will be used by participating nodes to initiate payment. An acceptable payment rails will first be negotiated between the nodes based on their respective configuration files. Once a mutually accepted payment rails is determined, the payment will be routed using the appropriate subflow.

This flow is available to the node operator.

#### Parameters

* `isoMessage` - An XML message formatted in ISO20022.
* `selectedPaymentRail` - A supported payment rail.
* `clientDeduplicationId` - An optional ID that will be used to deduplicate payments initiated by the client.

#### Return type

`PaymentRecord` - This flow will return the persisted `IsoMessageRecord` object.

#### Command Line Interface

`flow start PaymentFlow isoMessage: <XML formatted in ISO20022>, clientDeduplicationId: <provided clientDeduplicationId>`

Example: `flow start PaymentFlow isoMessage: <XML formatted in ISO20022>, clientDeduplicationId: "4"`

#### Exceptions

`PaymentExecutionException` - This exception will be thrown if the `selectedPaymentRail` is not supported.

### GetAccountFlow

A flow used to retrieve an ISO20022 ReturnAccount message with information concerning a specific account and its balance.

#### Parameters

* `accountIdentifier` - A data class which contains the information required to create an ISO20022 message.
* `isoMessage` - An ISO formatted GetAccount message with all necessary query information.
* `paymentRail` - A string indicating with payment rail should be queried.

#### Return type

`String` - This flow will return an ISO20022 formatted ReturnAccount message.

### RetrievePaymentByIdFlow

A flow that retrieves an ISO20022 message containing information about a payment with the specified ID.

#### Parameters

* `paymentId` - The ID associated with the payment that was previously initiated.
* `selectedPaymentRail` - The payment rail through which the payment was made.

#### Return type

`String` - This flow will return an ISO20022 formatted message with information about the specified payment.
### NegotiatePaymentRailFlow

Facilitates negotiation between two nodes to determine the appropriate payment rail through which the initiated payment should be routed.

#### Parameters

* `counterParty` - The legal identity of the counter-party with whom you should be negotiating payment details.
* `amount` - An amount representing the amount of the payment to be initiated.

#### Return type

`String` - This flow will request a list of enabled payment rails from the counterparty, filter the list to determine which payment rails are viable, and return the negotiated rail.

#### Exceptions

`PaymentRailNegotiationException` - This exception will be thrown if the `selectedPaymentRail` is not supported.

### `NegotiatePaymentRailFlowResponder`

A counter flow in which the responding node analyzes the payments rails suggested by the initiating party to determine if there is an acceptable payment rail as configured by both parties. This flow returns a simple `String` value representing the selected payment rail.

#### Parameters

`counterpartySession` - A communication session provide by the counter party.

#### Return type

`Unit / Void` - None.


#### Exceptions

`PaymentRailNegotiationException` - This exception will be thrown if the `selectedPaymentRail` is not supported.

### `NotifyCounterpartyFlow`

This flows sends a completed payment ID to the counter party.

#### Parameters

* `beneficiaryParty` - The legal identity of the party receiving the payment.
* `paymentRecord` - A record of a previously completed payment.

#### Return type

`Unit / Void` - None.

#### Exceptions

`PaymentRailNegotiationException` - This exception will be thrown if there is no shared acceptable methods of payment.

### `NotifyCounterpartyFlowResponder`

This flows receives a completed payment record from the counter party and persists it for tracking and reconciliation purposes.

#### Parameters

`session` - The flow session provided by Corda, which we will use to respond to the initiating party.

#### Return type

`Unit / Void` - None.

### `PaymentFlow`

This is the primary flow that will be used by participating nodes to initiate payment.  An acceptable payment rails will first be negotiated between the nodes based on their respective configuration files.  Once a mutually accepted payment rails is determined, the payment will be routed using the appropriate subflow.

This flow is available to the node operator.

#### Parameters

* `beneficiaryParty` - The legal identity of the Corda node that will act as the beneficiary of the payment.
* `paymentAmount` - The amount of the payment denominated in the specified currency.
* `clientDeduplicationId` - An optional ID that will be used to deduplicate payments initiated by the client.

#### Return type

`PaymentRecord` - This flow will return the persisted `PaymentRecord` object.

#### Command Line Interface

`flow start PaymentFlow beneficiaryParty: <X500 Name of beneficiary>, paymentAmount: <Payment Amount>, clientDeduplicationId: <provided clientDeduplicationId>`

Example: `flow start PaymentFlow beneficiaryParty: "O=partyB,L=New York,C=US", paymentAmount: 12 GBP, clientDeduplicationId: "4"`

## API

The API endpoints are conceptually split into three categories:

* **Outgoing** - where an ISO message is sent from `payments-core`.
* **Incoming** - where an ISO message is received by the `payments-core`.
* **Admin** - which provides the functionality to query the stored message records.

The ISO messages in scope are:

| type  | message | message name |
|---|---|---|
| Outbound | Pain.001.001.10 | CustomerCreditTransferInitiationV10 |
| Inbound | Pain.002.001.11 | CustomerPaymentStatusReportV11 |
| Outbound | camt.003.001.07 | GetAccountV07 |
| Inbound | camt.004.001.08 | ReturnAccountV08 |

### XML <-> POJO conversions

The ISO 20022 message formats are described in a set of `.xsd` files published by the ISO 20022 Registration Authority (RA).

The JAXB Library provides functionality to generate the POJO classes from the ISO xsd files.  Given the xsds, the marshalling/ unmarshalling of the ISO XML from/to POJOs is handled by the JAXB library.

As part of the marshalling/ unmarshalling processes the XMLs are checked to make sure they are syntactically correct per the xsds. This ensures that all XML elements included are valid components of the overarching message set. It also enforces rules about order, required fields, duplicated elements, and other more nuanced payment details.

### Validations

There are 3 types of validations:

* **Code Set validations**
  * For some elements in the XML, the xsd does not define the allowed values, instead this is delegated to a separately defined set of allowed codes published by Swift.
  * The Code set valdations ensure that the codes in the XML/ POJO exist in the Swift Code set
* **Scope Validations** - Scope validation limits the number of optional fields / elements inside of the message that can be filled in.
* **Semantic validations**  - The ISO 20022 Registration Authority (RA) publish a set of semantic rules for each message type. This might take the form of: if element A is populated
then element B must also be populated.

Validations are implemented as Kotlin classes which implement one of the Validator interfaces:

* `SemanticValidator` -> defines `validateSemantics()` function.
* `CodeSetValidator` -> defines `validateCodeSets()` function.
* `ScopeValidator` -> defines `validateScope()` function.

There will be one of each type of validator for every ISO message type. Each validator will list the set of validation rules that must be applied for that type of validation for that type of ISO message.

The validation rules are Kotlin classes which will implement one of the following interfaces:

* `SemanticRule` -> defines `validateSemanticRule()` function
* `ScopeRestriction` -> defines `validateScopeRestrition()` function
* `CodeSetCheck` -> defines `validateCodeSet()` function

The rules are expressed as Kotlin code operating on the POJO representation of the message which throws an exception if the validation fails.


## Mock payment rail

The `mock-payment-rail` module contains two sub-packages: `actions` and `flows`.

- `actions` contains two actions: `InitiateMockRailPayment` and `GetMockRailPaymentByPaymentId`, each triggered when a node needs to make a request to the MockRail API during a flow.

The module also contains a `MockRailClient`, a wrapper class providing access to the MockPaymentRail API as well as a `MockRailService`, an implementation of `PaymentRailServiceInterface`.  This service allows `payments-core` to make payments using the MockPaymentRail API.

### Mock payment rail service provider

The `mock-payment-rail-service-provider` module is comprised of a SpringBoot Web Server acting as Mock PSP for testing purposes.  The web server endpoints allow you to create an account, make a payment, and get a payment record.

The `Controller` class contains all the endpoints and implementations.

### Mock payment rail flows

Below are all the flows for nodes to make a payment from a node to an external destination (an account in Mock Rail, denoted by its `UniqueIdentifier`), from one node to another node, and to poll a processed payment.

{{< note >}}
These are not to be used directly by the developer, they are only accessible through the Payments-core CorDapp.
{{< /note >}}

### MockRailExternalDestinationFlow

This flow makes a payment using the MockRail API and client to a destination not represented by a Corda node.  It executes an `InitiateMockRailPayment` action using the constructed `PaymentInitiationPayload`. It will then continue to poll for the results of the initiated payment and return the payment entity once it has been processed.

#### Parameters

* `paymentAmount` - The amount of the payment to be made denominated in the specified currency.
* `destination` - The destination of the payment to be initiated.

#### Return type

* `PaymentResult<String>` - This flow returns a `PaymentResult` object.

### MockRailPaymentFlow

This flow facilitates the complete process of making a payment to another Corda node using the Mock Payment rail.  It first retrieves a payment destination from the provided `party`. This `destination` will inform the payment to be initiated. The flow will then initiate said payment using the Mock payment rail and poll for completion.

#### Parameters

* `party` - The party that will be the beneficiary of the payment.
* `paymentAmount` - The amount of the payment to be made denominated in the specified currency.
* `clientDeduplicationId` - An ID submitted by the invoking client for the purposes of deduplication.

#### Return type

* `PaymentResult<String>` - This flow returns a `PaymentResult` object.

### ExecuteMockRailPaymentFlowResponder

This flows responds to an initiated `MockRailPaymentFlow` with an appropriate `destination` to receive a payment. This `destination` is retrieved from the CorDapp configuration.

#### Parameters

* `session` - The flow session provided by Corda which you will use to respond to the initiating party.

#### Return type

* `Unit / Void` - None.

### MockRailPaymentInitiationFlow

#### Overview

This flow initiates a payment using the MockRail payment rail.  It will construct and execute an `InitiateMockRailPayment` action using the provided `destination` to create a MockRail specific `PaymentInitiationPayload` as required input.

#### Parameters

* `paymentAmount` - The amount of the payment to be initiated, denominated in a specific currency.
* `destination` - UniqueIdentifier of beneficiary.

#### Return type

* `String` - JSON representing a record of the initiated payment.

#### Exceptions

* `IdempotentActionExecutionException` - This exception will be thrown if the action triggered to initiate a MockRail payment is unsuccesful.
* `MockRailPaymentExecutionException` - This exception is thrown if no other exceptions are thrown and the initiated MockRail payment is still unsuccesful.

### MockRailPaymentPollingFlow

#### Overview

This flow executes a `GetMockRailPaymentByPaymentId` action and is used as a subflow by several other initiating flows to determine when a specific MockRail payment has been successfully processed.

#### Parameters

    * `paymentId` - The ID of the payment that has been submitted for processing by the MockRail payment rail.

#### Return type

    * `String` - JSON representing a record of the processed payment.

#### Exceptions

    * `MockRailTimeoutException` - This exception is thrown if an `ExponentialBackOffException` is caught.  An `ExponentialBackOffException` is thrown if exponential backoff used to validate the MockRail payment has reached a maximum threshold.


## Create and Install the CorDapp Jar

Once your dependencies are set correctly, you can build your CorDapp `.jar`s using the Gradle jar task:

Unix/Mac OSX: `./gradlew jar`

Windows: `gradlew.bat jar`

Each of the project’s modules will be compiled into its own CorDapp JAR. You can find these CorDapp JARs in the build/libs folders of each of the project’s modules.

The hash of the generated CorDapp JAR is not deterministic, as it depends on variables such as the timestamp at creation. Nodes running the same CorDapp must therefore ensure they are using the exact same CorDapp JAR, and not different versions of the JAR created from identical sources.

The filename of the JAR must include a unique identifier to deduplicate it from other releases of the same CorDapp. This is typically done by appending the version string to the CorDapp’s name. This unique identifier should not change once the JAR has been deployed on a node. If it does, make sure no one is relying on `FlowContext.appName` in their flows (see Versioning).

At start-up, nodes will load any CorDapps present in their cordapps folder. In order to install a CorDapp on a node, the CorDapp JAR must be added to the `<node_dir>/cordapps/` folder (where `node_dir` is the folder in which the node’s JAR and configuration files are stored) and the node restarted.

## Run the CorDapp

1. Open up a terminal and navigate to the root of the `payments-cordapp` directory.
2. Run the following command: `./gradlew clean deployNodes`.
3. After the project has been built succesfully, run the following command to run the nodes: `build/nodes/runnodes`.
4. For testing purposes, you can run `./gradlew test` to run all the tests that come with the `payments-cordapp`.
