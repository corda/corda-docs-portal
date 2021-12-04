---
date: '2020-01-08T09:59:25Z'
menu:
  apps:
    parent: "payments"
    name: Send payments locally
title: Send and receive payments with the demo CorDapps
weight: 300
---

You can use the Corda Payments Technical Preview to locally replicate payments in a live environment.   

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

## About Modulr accounts and payment accounts

Payments can only be triggered by a member of a network if they have an existing account with the PSP, and these details are reflected in the Payments Agent CorDapp.

When using the Corda Payments API method `createPaymentAccount`, one required parameter is the `accountName` - this is the name for the account that is registered with Modulr.

## Run the Payments Agent infrastructure locally

The Payments Agent CorDapp is hosted in a live environment by a trusted member of the network, such as the Business Network Operator (BNO). In this technical preview, you can assign the role of Payments Agent to a local node.

To add the Payment Agent infrastructure locally:

1. Use the `deployNodes` Gradle task - which automates the deployment of CorDapps to specified nodes - by adding the following dependencies to your root `build.gradle` file:

```
    cordapp "$corda_payments_release_group:payments-cordapp:$corda_payments_release_version"
    cordapp "$corda_payments_release_group:payments-contracts:$corda_payments_release_version"
    cordapp "$corda_payments_release_group:payments-agent:$corda_payments_release_version"
```

2. Add the following to the `deployNodes` task with the following syntax:

```
nodeDefaults {
    projectCordapp {
        deploy = false
    }
        cordapp "$corda_payments_release_group:payments-cordapp:$corda_payments_release_version"
        cordapp "$corda_payments_release_group:payments-contracts:$corda_payments_release_version"
        cordapp "$corda_payments_release_group:payments-agent:$corda_payments_release_version"
}
```

3. Add this agent node to your `deployNodes` task using the following configuration:

```
task deployNodes(type: net.corda.plugins.Cordform, dependsOn: ['jar']) {
    directory "./build/nodes"
    nodeDefaults {
        projectCordapp {
            deploy = false
        }

        cordapp("$corda_payments_release_group:payments-cordapp:$corda_payments_release_version")
        cordapp("$corda_payments_release_group:payments-contracts:$corda_payments_release_version")

        runSchemaMigration = true
    }
    node {
        name "O=Notary,L=London,C=GB"
        notary = [validating: false]
        p2pPort 10002
        rpcSettings {
            address("localhost:10003")
            adminAddress("localhost:10043")
        }
    }
    node {
        name "O=PartyA,L=London,C=GB"
        p2pPort 10005
        rpcSettings {
            address("localhost:10006")
            adminAddress("localhost:10046")
        }
        rpcUsers = [[user: "user1", "password": "test", "permissions": ["ALL"]]]
        cordapp("$corda_payments_release_group:payments-cordapp:$corda_payments_release_version") {
            config """
            {
                "payments" : {
                    "agent" : "O=Agent,L=New York,C=US"
                }
            }
                """
        }
    }
    node {
        name "O=PartyB,L=New York,C=US"
        p2pPort 10008
        rpcSettings {
            address("localhost:10009")
            adminAddress("localhost:10049")
        }
        cordapp project(":iou-workflows")
        cordapp project(":iou-contracts")
        rpcUsers = [[user: "user1", "password": "test", "permissions": ["ALL"]]]
        cordapp("$corda_payments_release_group:payments-cordapp:$corda_payments_release_version") {
            config """
            {
                "payments" : {
                    "agent" : "O=Agent,L=New York,C=US"
                }
            }
                """
        }
    }
    node {
        name "O=Agent,L=New York,C=US"
        p2pPort 10000
        rpcSettings {
            address("localhost:10001")
            adminAddress("localhost:10044")
        }
        cordapp("$corda_payments_release_group:payments-agent:$corda_payments_release_version") {
            config """
        {
            "workflow" : {
                "polling" : "1000",
                "shutdown" : "true"
                "timeout" : {
                    "delay" : 50000
                }
            }
        }
            """
        }
        rpcUsers = [[user: "user1", "password": "test", "permissions": ["ALL"]]]
    }
}
```

4. From your project, run:

  * `./gradlew clean deployNodes`

  * `./build/nodes/runnodes`

6. From directory where the downloaded `payments-spring-service` .jar files are located, run the following commands:

```
java -jar payments-spring-service-0.2.jar
```

You can now register payment accounts with the Payments Agent, using Modulr account details and use them to make payments against the Modulr PSP, from Corda.

## Create a payment account

You need to first create your payer and payee accounts on the Modulr sandbox. Once they have been created then you
need to store the account details on the system. The details required for making a payment on Modulr from a GBP account
to another GBP account are `Account ID` and `Account Number`.

From the payer node and payee nodes you can add the account details as follows.

Flow:
````
    val agent = paymentService.getPaymentAgent()
    val accountName = "{your-account-alias}"
    val currency = GBP
    val psp = "MODULR"
    val details = mutableMapOf(
        "id" to "{your-account-id}",
        "accountNumber" to "{your-account-number}"
    )

    paymentService.createAccount(accountName, currency, psp, details, agent)
````
RPC:
```
    rpc.startFlow(::CreatePaymentAccount, accountName, psp, details, agent)
```

When a payment account is registered on the system it returns a `PaymentAccount` object. The `PaymentAccount.accountId`
is the parameter you will use to make a payment.

## Make a payment

Once the payer and payee have both registered their payment account details on the system then a payment can be made
between the two of them. The payment will be made in the currency associated with the payment accounts.

The `PaymentAccount` objects can be accessed by using the `PaymentService.paymentAccounts` or `PaymentService.paymentAccount` API. You can filter the results of `paymentAccounts` based on the account name, currency, or PSP the account is held with.

Flow:
```
    val amount = 100
    val payer = payerAccount.accountId
    val payee = payeeAccount.accountId
    val transactionRef = "{your-transaction-ref}"

    paymentService.makePayment(amount, payer, payee, transactionRef)
```
RPC:
```
    rpc.startFlow(::MakePayment, amount, payer, payee, transactionRef)
```

Once the payment has been sent - you should receive the payment state object confirming that the payment has been initiated. The state object has the status `unprocessed`.

## Trigger flows on completion of a payment

Making payments requires calls to the external PSP, so there may be a small delay between initiating the payment and
it being successful or failing. You can therefore trigger flows when a payment transitions to a specific status.

The recommended annotations are:

* `@OnPaymentSucceed` - for payment success.
* `@OnPaymentFailure` - for payment failure.

If desired, you can trigger flows at a more granular level by specifying a `PaymentStatus`.

```
package com.r3.payments.callbacks

@StartableByService
@OnPaymentSucceed
class PostPaymentFlow(private val paymentState: PaymentState) : FlowLogic<Unit>() {
    override fun call() {
        // some process
    }
}

@StartableByService
@OnPaymentFailure
class FailedPaymentFlow(private val paymentState: PaymentState) : FlowLogic<Unit>() {
    override fun call() {
        // some process
    }
}

@StartableByService
@OnPaymentStatus(PaymentStatus.RESPONSE_PENDING)
class WaitingForPaymentResponseFlow(private val paymentState: PaymentState) : FlowLogic<Unit>() {
    override fun call() {
        // some process
    }
}
```

You will need to add the packages that these flows live in to your node CorDapp config as follows.

```
 "payments" : {
    "packages" : "com.r3.payments.callbacks"
  }
```
