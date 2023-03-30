---
title: "Corda Payments SDK"
date: '2023-02-14'
menu:
  corda-community-4-9:
    parent: payments-4-9-community
    weight: 300
    name: "Payments SDK"
section_menu: corda-community-4-9
---

With the Corda Payments SDK you can build and deploy payment-enabled CorDapps on your network. Use this documentation to add all the required Payments SDK dependencies to an existing CorDapp. Once the dependencies have been added to your CorDapp, it can be configured to initiate payments, via the network's Payments Agent.

{{< note >}}
All code samples are in Kotlin.
{{< /note >}}

## Requirements

You must have access to:

* The [Corda Customer Hub](https://customerhub.r3.com/s/r3-customcommunitylogin) trial area.
* Modulr Sandbox. This is so you can [test your CorDapp on a local environment](send-payments.html#set-up-modulr-sandbox-for-payments-agent).

## Access Corda Payments on Corda Customer Hub

The CorDapps that make up the Corda Payments solution are made available to Corda Enterprise customers by agreement. Once your Corda account manager has arranged access, you can download the Corda Payments files via the Corda Enterprise Customer Hub.

To install Corda Payments Technical Preview, go to the [Corda Customer Hub](https://customerhub.r3.com/s/r3-customcommunitylogin).

## Add Corda Payments SDK dependencies to an existing CorDapp

The Corda Payments SDK dependencies can be added to an existing CorDapp, making it possible to trigger all the required flows for payments to be made and received on your network.

To add the Corda Payments SDK:

1. Add a variable for the payments release group and the version you wish to use and set the Corda version:

```
buildscript {
    ext {
        corda_release_version = '4.8.5'
        corda_payments_release_group = "com.r3.payments"
        corda_payments_release_version = "1.0.0-TechPreview-1.2"
    }
}
```

2. Add payment jars to project by replacing [payment_jar_location] with location of downloaded files

```
repositories {
    maven { url "https://software.r3.com/artifactory/r3-corda-releases"}
    flatDir { dir [payment_jar_location] }
}
```

3. In your workflows `build.gradle` add:

```
    cordaCompile "$corda_payments_release_group:payments-sdk:$corda_payments_release_version"
    cordaCompile "$corda_payments_release_group:payments-contracts:$corda_payments_release_version"
```

4. To use the `deployNodes` task, add these dependencies to your root `build.gradle` file:

```
    cordapp "$corda_payments_release_group:payments-sdk:$corda_payments_release_version"
    cordapp "$corda_payments_release_group:payments-contracts:$corda_payments_release_version"
```

5. Add the dependencies to the `deployNodes` task with the following syntax:

```
nodeDefaults {
    projectCordapp {
        deploy = false
    }
        cordapp "$corda_payments_release_group:payments-sdk:$corda_payments_release_version"
        cordapp "$corda_payments_release_group:payments-contracts:$corda_payments_release_version"
}
```

5. Specify the default agent in your node config by adding:

```
cordapp("$corda_payments_release_group:payments-sdk:$corda_payments_release_version") {
    config """
    {
        "payments" : {
            "agent" : "O=Agent,L=New York,C=US"
        }
    }
        """
}
```

You have added the Corda Payments dependencies to your existing CorDapp. You can now use a local network with a Payments Agent node to explore Corda Payments in action.
