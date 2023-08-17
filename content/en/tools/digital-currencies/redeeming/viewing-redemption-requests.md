---
date: '2023-03-21'
lastmod: '2023-03-21'
section_menu: tools
menu:
  tools:
    name: "Viewing Redemption Requests"
    weight: 400
    parent: digital-currencies-token-redemption
    identifier: digital-currencies-viewing-redemption-requests
    description: "Digital Currencies documentation describing how to view redemption requests via the GUI"
title: "Viewing Redemption Requests"
---

To view the list of existing {{< tooltip >}}redemption{{< definitiondc term="redemption" >}}{{< /tooltip >}} requests for the current participant:

*. In the left-hand menu, click on **Redemptions**.

   The **Redemptions** page is displayed. This page contains the **Redemption Requests** panel, which lists existing redemption requests and their status:

   {{<
      figure
	  src="images/redemption-requests-panel-issuer.png"
      width=100%
	  figcaption="Redemption Requests Panel"
	  alt="Redemption Requests Panel"
   >}}

   For each redemption request, the following information is displayed:

   * **Issuer Status:** APPROVED or PENDING, depending on if the issuer has approved the redemption request or not.
   * **Custodian Status:** APPROVED or PENDING, depending on if the custodian has approved the redemption request or not.
   * **Token name:** The name of the token definition; normally the full name of the currency; for example, UAE Dirham.
   * **Token symbol:** A symbol for the token definition; normally the [three-letter ISO-4217 code](https://en.wikipedia.org/wiki/ISO_4217) for the currency; for example, *AED*.
   * **Amount:** The number of tokens to be redeemed.
   * **Requester:** The participant making the redemption request.
   * **Last updated:** The date and time at which the request was last updated.

You can change the GUI settings using the following buttons:

* **Columns**: Enables you to hide some or all columns in the list.
* **Filters**: Enables you to filter items in the list.
* **Density**: Enables you to change the vertical spacing between rows in the list.
* **Export**: Enables you to export the list as a CSV (Comma Separated Value) file, or to print the list.

From this panel, you can perform the following actions:

* [Approve or reject redemption requests]({{< relref "approving-or-rejecting-redemption-requests.md" >}})