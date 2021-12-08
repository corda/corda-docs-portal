---
date: '2020-01-08T09:59:25Z'
menu:
  apps:
    parent: "payments"
    name: Deploy a local payments network
title: Deploy a local payments network
weight: 200
---

You can use the Corda Payments Technical Preview to locally replicate payments in a live environment. the fastest way to do this is to use the Corda Payments sample CorDapps.

By following this guide, you can:

1. Deploy a local network that includes the required nodes to sent and receive payments, and a node to act as the Payments Agent.
2. Set up the Payments Agent locally.
3. Add the details of two Modulr accounts to the payer and payee nodes on your local network.
4. Make a payment by initiating a payment flow.
5. Set triggers for call back listeners that can trigger flows at specific points in the payments process.

## Requirements

You must have :

* Access to the Corda Enterprise Customer Hub.
* A Corda Payments-enabled CorDapp.
* Modulr sandbox credentials.

## Set up Modulr Sandbox for Payments Agent

Corda Payments is dependent on integration with a Payment Service Provider (PSP). In this technical preview, you can only use Modulr as the PSP. Your payments are simulated using the Modulr Sandbox environment. This is a mock environment, so no real money is paid to anyone.

To run the Payments Agent, you must have a **Partner Account** for your Modulr Sandbox. This involves contacting Modulr by email. You can follow the Modulr instructions to do this here: https://secure-sandbox.modulrfinance.com/sandbox/onboarding.

Once you have registered, Modulr will communicate your API key and secret. The Payments Agent holds these keys. Customers of the Payments Agent (anyone on the network who wants to use Corda Payments) do not require Modulr accounts with API key or secret.

With these, you can set the following environment variables:

```
MODULR_API_KEY = {enter-your-api-key}
MODULR_SECRET = {enter-your-secret}

```
## About Modulr accounts and payment accounts

Payments can only be triggered by a member of a network if one of the following is true:

* They have an account with the PSP that has been set up by the Payments Agent.
* They have an existing **Direct account** with Modulr that they have set up directly, and has been recorded with the Payments Agent. In this technical preview, you can do this on behalf of the nodes on your local network to test this kind of payment account. 


##  Download files from CustomerHub

The CorDapps that make up the Corda Payments solution are made available to Corda Enterprise customers by agreement. Once your Corda account manager has arranged access, you can download the Corda Payments files via the Corda Enterprise Customer Hub.

To install Corda Payments Technical Preview, go to:

https://customerhub.r3.com/s/

## Get access to the Modulr Sandbox for individual nodes

For the quickest set up, sign up to use the sandbox https://secure-sandbox.modulrfinance.com/sandbox/onboarding and create two accounts on the sandbox to run the sample commands.

## Update the `payments.properties`

Set the following properties:

* `payments-jar-location` = Location of the files downloaded from CustomerHub
* `account-id-1` = First Modulr account ID
* `account-id-2` = Second Modulr account ID

Example:
```
payments-jar-location=/Users/Bob/Downloads/corda-payments-1.0.0-TechPreview-1.0

account-id-1=A120NXXX
account-id-2=A120NXXX
```

## Set environmental variables

```
MODULR_API_KEY = Your Modulr api key
MODULR_SECRET = Your Modulr secret
```

## Running Corda Payments

### Deploy Corda Nodes

```
./gradlew deployNodes
```
### Run Corda Nodes

```
./gradlew runNodes
```
### Run Corda Nodes (Windows only)

```
./gradlew runNodesWindows
```

### Run Payment Gateway

```
./gradlew runGateway
```

##  Running Sample Commands

The following list are Gradle commands that trigger flows in the sample CorDapps.

* Add an account to PartyA
```
./gradlew AddAccountPartyA
```
* Add an account to PartyB
```
./gradlew AddAccountPartyB
```
* Get accounts from PartyA
```
./gradlew GetAccountsPartyA
```
* Get accounts from PartyB
```
./gradlew GetAccountsPartyB
```
* Remove account from PartyA
```
./gradlew RemoveAccountPartyA
```
* Remove account from PartyB
```
./gradlew RemoveAccountPartyB
```
* Get available PSPs from PartyA
```
./gradlew GetAvailablePSPsPartyA
```
* Get available PSPs from PartyB
```
./gradlew GetAvailablePSPsPartyB
```
* Get balance from PartyA
```
./gradlew GetBalancePartyA
```
* Get balance from PartyB
```
./gradlew GetBalancePartyB
```
* Make payment to PartyA
```
./gradlew MakePaymentToPartyA
```
* Make payment to PartyB
```
./gradlew MakePaymentToPartyB
```
* Get payments from PartyA's PSP
```
./gradlew GetTransactionsPartyA
```
* Get payments from PartyB's PSP
```
./gradlew GetTransactionsPartyB
```
* Get payments from PartyA's vault
```
./gradlew GetPaymentsPartyA
```
* Get payments from PartyB's vault
```
./gradlew GetPaymentsPartyB
```
Making a payment for an amount greater than the available balance to make it stall
* Get stalled payments from PartyA
```
./gradlew GetStalledPaymentsPartyA
```
* Get stalled payments from PartyB
```
./gradlew GetStalledPaymentsPartyB
```


## Running Sample GUIs

The Corda Payments sample includes some basic user interfaces that you can use to trigger API calls and flows from the perspective of a node making payments, or the Payments Agent.

{{< note >}}
These GUIs and web servers are for demonstration purposes only, and are not supported as part of Corda Payments Technical Preview.
{{< /note >}}


1. In a new terminal, run the sample agent web server

```
./gradlew runSampleAgentWebserver
```
2. In a new terminal, run the sample agent GUI
  * URL = http://localhost:3002/
  * Username = agent
  * Password = test
```
./gradlew runSampleAgentGUI
```
3.  In a new terminal, run the sample client web server
```
./gradlew runSampleClientWebserver
```
4. In a new terminal, run the sample client GUI
    * URL = http://localhost:3001/
    * Username = user
    * Password = admin
```
./gradlew runSampleClientGUI
```
