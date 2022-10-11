---
date: '2021-10-27'
section_menu: corda-5-dev-preview
menu:
  corda-5-dev-preview:
    identifier: corda-corda-5.0-dev-preview-1-tutorial-c5-basic-cordapp-ui
    parent: corda-5-dev-preview-1-tutorials-building-cordapp
    weight: 1075
tags:
- tutorial
- cordapp
title: "Set up and test the UI"
---

## Learning objectives

After you have completed this tutorial, you will know how to set up the Mission Mars CorDapp's UI and how to use it to test the CorDapp.


## Before you start

Before you can build the Mission Mars CorDapp UI, you must:

* Copy the **Web-UI** folder into your project from the respective folder in the samples repository:

   * [Mission Mars CorDapp - Kotlin](https://github.com/corda/samples-kotlin-corda5/tree/main/Tutorial/missionmars)
   * [Mission Mars CorDapp - Java](https://github.com/corda/samples-java-corda5/tree/main/Tutorial/missionmars)

* [Deploy your CorDapp to a local Corda 5 network](../../../../../../en/platform/corda/5.0-dev-preview-1/tutorials/building-cordapp/c5-basic-cordapp-running.html#deploy-your-cordapp-to-a-local-corda-5-network).

* Download the [Node.js](https://nodejs.org/en/download/) asynchronous event-driven JavaScript runtime for your platform.


## Set up the CorDapp's UI

After you have deployed your CorDapp to a local Corda 5 network and the back-end code is running, perform the following steps:

1. Look up the RPC port for the `PartyA` node:

   `corda-cli network status -n missionmars-network`

   The default RPC port for the `PartyA` node is `12112`.

2. If the port is not `12112`, in your project, go to **Web-UI > src** and open the `setupProxy.js` file.

3. Change the default `PARTY_A_PORT` in the `setupProxy.js` file accordingly.

4. In the project directory, run `npm install`.

   This command installs all necessary [npm](https://docs.npmjs.com/) modules to run the Mission Mars CorDapp UI.

5. Run `npm start`.
   This command runs the UI in development mode.

   The Mission Mars CorDapp UI opens in your browser window.

{{<
  figure
	 src="mission-mars-ui.PNG"
	 zoom="mission-mars-ui.PNG"
   width=100%
	 figcaption="Mission Mars CorDapp UI"
	 alt="mission mars cordapp ui"
>}}


## Test your CorDapp using the UI

Once the Mission Mars CorDapp UI is up and running, you can use it to test the CorDapp's flows.

1. Check your local Corda 5 Network for the existing nodes by clicking the **CHECK** button present under the **CORDA NETWORK** tab.

   Peter's X500 name appears at the top of the page.

2. Go to the **ISSUE VOUCHER** tab to test the `CreateAndIssueMarsVoucher` flow:

   a. Provide voucher description and the voucher holder's X500 name.

   b. Click **START FLOW**.

   Voucher ID appears at the top of the page.

3. Go to the **CREATE TICKET** tab to test the `CreateBoardingTicket` flow.

   a. Provide ticket description and launch date.

   b. Click **START FLOW**.

   The **Ticket Ready!** message appears at the top of the page.

4. Go to the **REDEEM VOUCHER** tab to test the `RedeemBoardingTicketWithVoucher` flow.

   a. Provide voucher ID and the voucher holder's X500 name.

   b. Click **START FLOW**.

   The rocket goes to Mars!

5. **Optional:** You can investigate each flow you run in more detail under the **FLOW OUTCOME** tab.
