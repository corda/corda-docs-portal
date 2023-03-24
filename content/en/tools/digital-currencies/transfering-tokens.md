---
date: '2023-03-21'
lastmod: '2023-03-21'
section_menu: tools
menu:
  tools:
    name: "Transfering Tokens"
    weight: 1300
    parent: digital-currencies-tokens-overview
    identifier: digital-currencies-transfering-tokens
    description: "Digital Currencies documentation describing how to transfer tokens via the GUI"
title: "Transfering Tokens"
---

Tokens can be transferred between entities (for example, wholesale banks, bank branches, retailers, retailer branches or franchises) on the network. Entities can request to send or request to receive tokens.

<!--

### Creating Transfer Requests

Currently, Bank A has made a deposit and tokens have been minted. Bank B, currently has not made a deposit and therefore holds no tokens. There are two methods which can be used to transfer tokens between entities:

* [Creating Requests to Send](#creating-requests-to-send)
* [Creating Requests to Receive](#creating-requests-to-receive)

#### Creating Requests to Send

The following shows how to create a 'Request to Send' on behalf of Bank A to request a transfer of tokens *to* Bank B:

1. Select the role of **Bank A** from the dropdown menu at the top-right of the **Home** page:

   {{< figure src="select-bank-a.png" width=28% figcaption="Selecting Bank A as Active" alt="Selecting Bank A as Active" >}}

   The header of the page now displays *Bank A*, indicating that you are now acting in that role:

   {{< figure src="bank-a-header.png" width=38% figcaption="Bank A as Active" alt="Bank A as Active"   >}}

2. Click the **Transfers** button:

   {{< figure src="transfers-button.png" width=18% figcaption="Transfers Button" alt="Transfers Button"   >}}
   
   A page including the **Request Transfer pane** is displayed:
   
   {{< figure src="request-transfer-pane.png" width=38% figcaption="Request Transfer Pane" alt="Request Transfer Pane"   >}}

3. Specify the following values:

   * **Select Network:** Select *R3 Token Network*.
   * **Transfer Type:** Can be either REQUEST_TO_RECEIVE or REQUEST_TO_SEND. For this example, select REQUEST_TO_SEND.
   * **To/From:** Since REQUEST_TO_SEND is selected, this field is labeled **To** (otherwise **From**). For this example, select *Bank B*.
   * **Token Type:** Select our token type *dUSD*. Only token types on this network can be specified. Once you select the token type, your current balance of that type is displayed below this field:
        {{< figure src="token_balance.png" width=38% figcaption="Token Balance" alt="Token Balance"   >}}
   * **Amount:** Enter *50*.
   
4. Click the **Request Transfer** button.

   The message *Successfully requested transfer* is displayed:

   {{< figure src="successfully-requested-transfer-message.png" width=38% figcaption="'Successfully requested transfer' Message" alt="'Successfully requested transfer' Message"   >}}

   {{< note >}}You can cancel the transfer at this point by selecting the transfer and clicking on the **Cancel Transfer** button.{{< /note >}}
   
The **Outgoing Transfer Requests** pane lists the new request:

{{< figure src="bank-a-outgoing-transfer-requests-req-to-send.png" width=80% figcaption="Outgoing Transfer Request Pane" alt="Outgoing Transfer Request Pane"   >}}

#### Creating Requests to Receive

The following shows how to create a 'Request to Receive' on behalf of Bank A to request a transfer of tokens *from* Bank B:

1. Select the role of **Bank A** from the dropdown menu at the top-right of the **Home** page: 

   {{< figure src="select-bank-a.png" width=28% figcaption="Selecting Bank A as Active" alt="Selecting Bank A as Active" >}}

   The header of the page now displays *Bank A*, indicating that you are now acting in that role:

   {{< figure src="bank-a-header.png" width=58% figcaption="Bank A as Active" alt="Bank A as Active"   >}}

2. Click the **Transfers** button:

   {{< figure src="transfers-button.png" width=18% figcaption="Transfers Button" alt="Transfers Button"   >}}
   
   A page including the **Request Transfer pane** is displayed:
   
   {{< figure src="request-transfer-pane.png" width=38% figcaption="Request Transfer Pane" alt="Request Transfer Pane"   >}}

3. Specify the following values:

   * **Select Network:** Select *R3 Token Network*.
   * **Transfer Type:** Select REQUEST_TO_RECEIVE.
   * **To/From:** Since REQUEST_TO_RECEIVE is selected, this field is labeled **From**. For this example, select *Bank B*.
   * **Token Type:** Select our token type *dUSD*.  Only token types on this network can be specified. Once you select the token type, your current balance of that type is displayed below this field:
        {{< figure src="token_balance.png" width=38% figcaption="Token Balance" alt="Token Balance"   >}}
   * **Amount:** Enter *50*.
   
4. Click the **Request Transfer** button.

   The message *Successfully requested transfer* is displayed:

   {{< figure src="successfully-requested-transfer-message.png" width=38% figcaption="'Successfully requested transfer' Message" alt="'Successfully requested transfer' Message"   >}}  

   {{< note >}}You can cancel the transfer at this point by selecting the transfer and clicking on the **Cancel Transfer** button.{{< /note >}}
   
The **Outgoing Transfer Requests** pane lists the new request:

{{< figure src="bank-a-outgoing-transfer-requests-req-to-rec.png" width=80% figcaption="'Outgoing Transfer Request' Pane" alt="'Outgoing Transfer Request' Pane"   >}}
### Accepting Transfer Requests

In this example, as Bank B, we accept the 'Request to Send' transfer request from Bank A:

1. Select the role of **Bank B** from the dropdown menu at the top-right of the **Home** page:

   {{< figure src="select-bank-b.png" width=28% figcaption="Selecting Bank B as Active" alt="Selecting Bank B as Active" >}}

   The header of the page now displays *Bank B*, indicating that you are now acting in that role:

   {{< figure src="bank-b-header.png" width=58% figcaption="Bank B as Active" alt="Bank B as Active"   >}}

2. Click the **Transfers** button:

   {{< figure src="transfers-button.png" width=18% figcaption="Transfers Button" alt="Transfers Button"   >}}
   
   A page including the **Incoming Requests** tabbed pane is displayed:

   {{< figure src="bank-b-incoming-transfers-pane.png" width=80% figcaption="Bank B: Incoming Transfer Requests" alt="Bank B: Incoming Transfer Requests"   >}}

3. Click on the relevant request with a status of *Requested*.

   The **Transfer Request** dialog box is displayed with details of the request:
   
   {{< figure src="bank-b-transfer-request.png" width=38% figcaption="Bank B: Transfer Request Dialog Box" alt="Bank B: Transfer Request Dialog Box"   >}}

4. Click **Accept Transfer**.

   The message *Successfully accepted transfer* is displayed:
   
   {{< figure src="successfully-requested-transfer-message.png" width=38% figcaption="'Successfully requested transfer' Message" alt="'Successfully requested transfer' Message" >}}

   The status of the request now appears as *Accepted*:
   
   {{< figure src="bank-b-incoming-transfers-pane-accepted.png" width=38% figcaption="Bank B: Incoming Transfer Request Accepted" alt="Bank B: Incoming Transfer Request Accepted"   >}}

Alternatively, you can click **Reject Transfer** to reject the transfer.

### Completing Transfer Requests

If Bank B accepted the transfer request, Bank A must now complete the transfer to send the tokens to Bank B:

1. Select the role of **Bank A** from the dropdown menu at the top-right of the **Home** page:

   {{< figure src="select-bank-a.png" width=28% figcaption="Selecting Bank A as active" alt="Selecting Bank A as active" >}}
   
2. Select **R3 Token Network** from the dropdown list at the top-left of the page:

   {{< figure src="select-r3-network.png" width=38% figcaption="Select R3 Token Network" alt="Select R3 Token Network" >}}
   
   The header of the page now displays *Bank A*, indicating that you are now acting in that role:

   {{< figure src="bank-a-header.png" width=58% figcaption="Bank A as Active" alt="Bank A as Active"   >}}
   
3. Click the **Transfers** button:

   {{< figure src="transfers-button.png" width=18% figcaption="Transfers Button" alt="Transfers Button"   >}}
   
   The **Transfers** page is displayed including the **Outgoing Transfer Requests** pane:
   
   {{< figure src="bank-a-outgoing-transfer-requests.png" width=38% figcaption="Bank A: Outgoing Transfer Requests Pane" alt="Bank A: Outgoing Transfer Requests Pane" >}}

   The pane displays the transfer request with a status of *Accepted*.
   
4. Click the transfer request.

   The **Transfer Request** dialog box is displayed:
   
   {{< figure src="bank-a-transfer-request.png" width=38% figcaption="Bank A: Transfer Request Dialog Box" alt="Bank A: Transfer Request Dialog Box"   >}}

5. Click the **Complete Transfer** button.

   The message *Successfully completed transfer* is displayed:
   
   {{< figure src="successfully-completed-transfer-message.png" width=38% figcaption="'Successfully completed transfer' Message" alt="'Successfully completed transfer' Message" >}}
   
   The **Outgoing Transfer Requests** pane now displays the request with a status of *Completed*:
   
   {{< figure src="bank-a-outgoing-transfer-requests-completed.png" width=38% figcaption="Bank A: Outgoing Transfer Requests Pane (Completed)" alt="Bank A: Outgoing Transfer Requests Pane (Completed)" >}}
   
The tokens are transferred from Bank A to Bank B. The banks' balances are updated accordingly to reflect this movement. The smart contract will acknowledge the change in ownership.   
  
## Redeeming Tokens

The last stage of the Stablecoin life cycle is *redemption*. A bank on the network can send a request to redeem their tokens for collateral at any time.


