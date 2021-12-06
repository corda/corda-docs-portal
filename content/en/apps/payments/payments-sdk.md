---
date: '2020-01-08T09:59:25Z'
menu:
  apps:
    parent: "payments"
    name: Corda Payments SDK
title: Send and receive payments with the demo CorDapps
weight: 200
---

With the Corda Payments SDK you can build and deploy payment-enabled CorDapps on your network. Use this documentation to add all the required Payment SDK dependencies to an existing CorDapp. Once the dependencies have been added to your CorDapp, it can be configured to initiate payments, via the network's Payments Agent.

{{< note >}}
All code samples are in Kotlin.
{{< /note >}}

## Requirements

You must have access to:

* The Corda Enterprise Customer Hub.
* Modulr sandbox.

## Access Corda Payments on Corda Customer Hub

The CorDapps that make up the Corda Payments solution are made available to Corda Enterprise customers by agreement. Once your Corda account manager has arranged access, you can download the Corda Payments files via the Corda Enterprise Customer Hub.

To install Corda Payments Technical Preview, go to: 

https://customerhub.r3.com/s/

## Set up Modulr sandbox

Corda Payments is dependent on integration with a Payment Service Provider (PSP). In this technical preview, you can only use Modulr as the PSP. Your payments are simulated using the Modulr sandbox environment. This is a mock environment, so no real money is paid to anyone.

Once this product has reached a full commercial release, you should be able to choose from a range of compatible PSPs.

To register with the Modulr sandbox:

1. Go to https://secure-sandbox.modulrfinance.com/sandbox/onboarding.
2. Complete the registration process using the Modulr on-screen directions.
3. Once your account is set up on Modulr Sandbox, Modulr will email you with your secrets and API key. 
4. Keep your Modulr credentials available. In your Corda Payments environment, set the following environment variables:

```
CORDA_ARTIFACTORY_USERNAME = {enter-your-username}
CORDA_ARTIFACTORY_PASSWORD = {enter-your-password}
MODULR_API_KEY = {enter-your-api-key}
MODULR_SECRET = {enter-your-secret}
```

## Add Corda Payments SDK dependencies to an existing CorDapp

The Corda Payments SDK dependencies can be added to an existing CorDapp, making it possible to trigger all the required flows for payments to be made and received on your network.

To add the Corda Payments SDK:  

1. Add a variable for the payments release group and the version you wish to use and set the Corda version:

```
buildscript {
    ext {
        corda_release_version = '4.7'
        corda_payments_release_group = "com.r3.payments"
        corda_payments_release_version = "0.2"
    }
}
```

2. Add the payments Artifactory repository to the list of repositories for your project:

```
repositories {
    maven {
        url "https://software.r3.com/artifactory/r3-corda-releases"
        credentials {
            username = System.getenv('CORDA_ARTIFACTORY_USERNAME')
            password = System.getenv('CORDA_ARTIFACTORY_PASSWORD')
        }
    }
}
```

3. In your workflows `build.gradle` add:

```
    cordaCompile "$corda_payments_release_group:payments-cordapp:$corda_payments_release_version"
    cordaCompile "$corda_payments_release_group:payments-contracts:$corda_payments_release_version"
```

4. To use the `deployNodes` task, add the following dependencies to your root `build.gradle` file:

```
    cordapp "$corda_payments_release_group:payments-cordapp:$corda_payments_release_version"
    cordapp "$corda_payments_release_group:payments-contracts:$corda_payments_release_version"
```

5. Add the dependencies to the `deployNodes` task with the following syntax:

```
nodeDefaults {
    projectCordapp {
        deploy = false
    }
        cordapp "$corda_payments_release_group:payments-cordapp:$corda_payments_release_version"
        cordapp "$corda_payments_release_group:payments-contracts:$corda_payments_release_version"
}
```

5. Specify the default agent in your node config by adding the following:

```
cordapp("$corda_payments_release_group:payments-cordapp:$corda_payments_release_version") {
    config """
    {
        "payments" : {
            "agent" : "O=Agent,L=New York,C=US"
        }
    }
        """
}
```

You have added the Corda Payments dependencies to your existing CorDapp. Now you can follow the steps to trial the payments process locally.
