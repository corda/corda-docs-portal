---
date: '2023-03-21'
lastmod: '2023-03-21'
section_menu: digitalcurrencies
menu:
  digitalcurrencies:
    name: "Viewing Issuance Requests"
    weight: 400
    parent: digital-currencies-token-issuance
    identifier: digital-currencies-viewing-transfer-requests
    description: "Digital Currencies documentation describing how to view transfer requests via the GUI"
title: "Viewing Issuance Requests"
---

To view the list of existing issuance requests for the current participant:

1. In the left-hand menu, click on **Issuances**.

   The **Issuances** page is displayed. This page contains the **Issuance Requests** panel, which lists existing issuance requests and their status:

   {{<
      figure
	  src="images/issuance-requests-panel-issuer.png"
      width=100%
	  figcaption="Issuance Requests Panel"
	  alt="Issuance Requests Panel"
   >}}

   For each issuance request, the following information is displayed:

   * **Issuer Status:** Whether or not the issuer has approved the issuance request.
   * **Custodian Status:** Whether or not the custodian has approved the issuance request.
   * **Token name:** The name of the token definition; normally the full name of the currency; for example, Canadian Dollar.
   * **Token symbol:** A symbol for the token definition; normally the [three-letter ISO-4217 code](https://en.wikipedia.org/wiki/ISO_4217) for the currency; for example, *CAD*.
   * **Amount:** The number of tokens requested.
   * **Requester:** The entity making the issuance request.
   * **Last Updated:** The date and time at which the request was last updated.

You can change the GUI settings using the following buttons:

* **Columns**: Enables you to hide some or all columns in the list
* **Filters**: Enables you to filter items in the list
* **Density**: Enables you to change the vertical spacing between rows in the list
* **Export**: Enables you to export the list as a CSV (Comma Separated Value) file, or to print the list

From this panel, you can perform the following actions:

* [Approve or reject issuance requests]({{< relref "approving-or-rejecting-issuance-requests.md" >}})