---
date: '2023-03-21'
lastmod: '2023-03-21'
section_menu: tools
menu:
  tools:
    name: "Querying Token Balances"
    weight: 1500
    parent: digital-currencies-tokens-overview
    identifier: digital-currencies-querying-token-balances
    description: "Digital Currencies documentation describing how to query token balances via the GUI"
title: "Querying Token Balances"
---

Once a token type has been defined, tokens of that type can be issued. 

<!-- Wholesale banks and financial institutions can deposit assets in exchange for tokens minted on the network. This process involves:

* A bank or financial institution requests a deposit in exchange for tokens, as described in *[Requesting Deposits](#requesting-deposits)*.
* A custodian approves the deposit request, as described in *[Accepting or Rejecting Deposit Requests](#accepting-or-rejecting-deposit-requests)*.
* The bank issues a payment to transfer collateral (off-ledger assets) to the custodian in exchange for the issuance of tokens, as described in *[Issuing Payments](#issuing-payments)*.
* The custodian accepts the payment, as described in *[Accepting or Rejecting Payments](#accepting-or-rejecting-payments)*.

-->

1. Click **Create Tokens** in the left-hand sidebar.

   The 

   {{< figure src="deposits-button.png" width=18% figcaption="Deposits Button" alt="Deposits Button" >}}   
   
   The **Home** page now displays a **Request Deposit** pane:
   
   {{< figure src="request-deposit-pane.png" width=38% figcaption="'Request Deposit' Pane" alt="'Request Deposit' Pane" >}}
   
4. Specify the following values:

   * **Select Network:** Select the network associated with the relevant token; for example, *R3 Token Network*.
   * **Token Type:** Select the token type you want to request; for example, *dUSD*. Only token types on the selected network can be specified.
   * **Custodian:** Select the custodian that will be responsible for this token type; for this example, select *Custodian A*.
   * **Amount:** Enter the amount you want; for example *100*.
  
5. Click the **Deposit Request** button.

   The *Successfully requested deposit* message is displayed:
   
   {{< figure src="successfully-requested-deposit-message.png" width=58% figcaption="'Successfully requested deposit' Message" alt="'Successfully requested deposit' Message" >}}

   The deposit request is sent and is displayed in the **Outgoing Deposit Requests** pane:
   
   {{< figure src="outgoing-deposit-requests.png" width=80% figcaption="Outgoing Deposit Requests Pane" alt="Outgoing Deposit Requests Pane" >}}
   
   The specified custodian can then either accept or reject the request as described in the next section.

### Accepting or Rejecting Deposit Requests

A custodian can either accept or reject a request for tokens:

1. Select the role of **Custodian A** from the dropdown menu at the top-right of the **Home** page:

   {{< figure src="select-custodian-a.png" width=28% figcaption="Selecting Custodian A as Active" alt="Selecting Custodian A as Active" >}}

   The header of the page now displays *Custodian A*, indicating that you are now acting in that role:
   
   {{< figure src="custodian-a-header.png" width=38% figcaption="Custodian A Active" alt="Custodian A Active" >}}

2. Click the **Deposits** tab.

   The **Incoming Deposit Requests** pane is displayed:
   
   {{< figure src="incoming-deposit-requests-pane.png" width=80% figcaption="Incoming Deposit Requests pane" alt="Incoming Deposit Requests pane" >}}
   
   The pane lists all incoming deposit requests; new requests will appear at the top of the list.
   
3. Optionally, you can filter the deposit requests listed:

   * **Status Filter:** Filter requests by status; for example, only show requests of status *REQUESTED*.
   * **Network Filter** Filter requests by their network; for example, only show requests for the R3 Token Network. Note that only networks selected in the network filter, described in *[Handling Multiple Networks](#handling-multiple-networks)*, are displayed here.   

4. Select the request from Bank A.

   The **Deposit Request** dialog box is displayed:
   
   {{< figure src="deposit-request-popup.png" width=48% figcaption="Deposit Request" alt="Deposit Requests" >}}

5. Click **Accept Deposit Request**. 

   The message *Successfully accepted deposit* is displayed:
   
   {{< figure src="successfully-accepted-deposit-message.png" width=48% figcaption="'Successfully accepted deposit' Message" alt="'Successfully accepted deposit' Message" >}}

Alternatively, you could select **Reject Deposit Request** to reject the collateral and end the request process.

### Issuing Payments

Once the custodian has accepted the deposit request, Bank A can issue a payment to transfer collateral (off-ledger assets) to the custodian in exchange for the transfer of tokens:

1. Select the role of **Bank A** from the dropdown menu at the top-right of the **Home** page:

   {{< figure src="select-bank-a.png" width=28% figcaption="Selecting Bank A as active" alt="Selecting Bank A as active" >}}
   
2. Select **R3 Token Network** from the dropdown list at the top-left of the page:

   {{< figure src="select-r3-network.png" width=38% figcaption="Select R3 Token Network" alt="Select R3 Token Network" >}}
   
   The header of the page now displays *Bank A*, indicating that you are now acting in that role:

   {{< figure src="bank-a-header.png" width=58% figcaption="Bank A as Active" alt="Bank A as Active"   >}}
   
3. Click the **Deposits** button at the top of the page:

   {{< figure src="deposits-button.png" width=18% figcaption="Deposits Button" alt="Deposits Button" >}}   
   
   The **Home** page now displays a **Outgoing Deposit Requests** pane:
   
   {{< figure src="bank-a-outgoing-deposit-requests.png" width=80% figcaption="'Outgoing Deposit Requests' Pane" alt="Request Deposit Pane" >}}

4. Click the deposit request with a status of *Accepted*.

   The **Deposit Request** dialog box is displayed:
   
   {{< figure src="deposit-request-popup-issue-payment.png" width=38% figcaption="Deposit Request" alt="Deposit Requests" >}}

4. Click **Issue Payment**

   The message *Successfully issued payment against deposit* is displayed:
   
   {{< figure src="successfully-issued-payment-against-deposit-message.png" width=38% figcaption="'Successfully issued payment against deposit' Message" alt="Successfully issued payment against deposit' Message" >}}

The payment will be made off-ledger via traditional payment rails; for example, RTGS or SWIFT.

{{< note >}}
Bank A can use the unique reference ID provided at this stage in the off-ledger payment to aid the custodian in their reference of the payment.
{{< /note >}}

### Accepting or Rejecting Payments

The custodian will inspect their off-ledger banking account to ensure that the payment made has been received and for the said amount agreed against the deposit requested. Once satisfied, they can accept the payment.

To accept or reject the payment:

1. Select the role of **Custodian A** from the dropdown menu at the top-right of the **Home** page:

   {{< figure src="select-custodian-a.png" width=28% figcaption="Selecting Custodian A as Active" alt="Selecting Custodian A as Active" >}}

   The header of the page now displays *Custodian A*, indicating that you are now acting in that role:
   
   {{< figure src="custodian-a-header.png" width=48% figcaption="Custodian A Active" alt="Custodian A Active" >}}

2. Scroll down and click on the **Deposits** tab.

   The **Incoming Deposit Requests** pane is displayed:
   
   {{< figure src="custodian-a-incoming-deposit-requests.png" width=80% figcaption="Incoming Deposit Requests" alt="Incoming Deposit Requests" >}}

3. Click the relevant deposit request from Bank A.

   The **Deposit Request** dialog box is displayed:
   
   {{< figure src="deposit-request-popup-accept-payment.png" width=38% figcaption="Deposit Request" alt="Deposit Request" >}}
   
4. Review the details of the deposit payment request. 

5. If the payment aligns with the agreed amount in the request, click **Accept Payment**. 

   The *Successfully accepted payment* message is displayed:
   
   {{< figure src="successfully-accepted-payment-message.png" width=38% figcaption="'Successfully accepted payment' message" alt="'Successfully accepted payment' message" >}}

If not, click **Reject Payment**.

Upon acceptance of the payment, the tokens are minted together with the TIE. The token balance against the custodian will be updated to reflect the newly accepted deposit in the custodian’s home tab. This ensures that the custodian always has view of the collateral they need to back. If you navigate to the TIE node, the TIE’s token balance will also be updated to reflect the position of the tokens in balance against the token type. 

In addition, Bank A’s token balance is also updated in the home tab to reflect the amount deposited:

{{< figure src="bank-a-token-balances.png" width=80% figcaption="Token Balances for Bank A" alt="Token Balances for Bank A" >}}

## Transferring Tokens

Tokens can be transferred between entities (for example, wholesale banks, bank branches, retailers, retailer branches or franchises) on the network. Entities can request to send or request to receive tokens.

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

### Sending Redemption Requests

Send a redemption request from Bank B to exchange tokens for collateral:

1. Select the role of **Bank B** from the dropdown menu at the top-right of the **Home** page:

   {{< figure src="select-bank-b.png" width=28% figcaption="Selecting Bank B as Active" alt="Selecting Bank B as Active" >}}

   The header of the page now displays *Bank B*, indicating that you are now acting in that role:

   {{< figure src="bank-b-header.png" width=38% figcaption="Bank B as Active" alt="Bank B as Active"   >}}

2. Click the **Redemptions** button:

   {{< figure src="redemptions-button.png" width=18% figcaption="Redemptions Button" alt="Redemptions Button"   >}}
   
   The **Redemptions** page is displayed, including a **Request Redemption** pane:
   
   {{< figure src="request-redemption-pane.png" width=38% figcaption="Request Redemption Pane" alt="Request Redemption Pane"   >}}

3. In the **Request Redemption** pane, specify the following values:

   * **Select Network:** Select our example network *R3 Token Network*.
   * **Token Type:** Select our token type *dUSD*. Only token types on this network can be specified. Once you select the token type, your current balance of that type is displayed below this field:
        {{< figure src="request-membership-token-balance.png" width=38% figcaption="Token Balance" alt="Token Balance"   >}}
   * **Custodian:** Select the custodian that will be responsible for this token type; in this example, *Custodian A*.
   * **Amount:** Enter the amount; in this example, *50*. 
   
7.	Click **Request Redemption**.

    The message *Successfully requested redemption* is displayed:
         
    {{< figure src="successfully-requested-redemption-message.png" width=38% figcaption="'Successfully requested redemption' Message" alt="'Successfully requested redemption' Message" >}}

    The redemption request is sent to Custodian A. The **Redemption Requests** pane on the **Redemptions** page now lists this request:
    
    {{< figure src="bank-b-redemption-requests-pane.png" width=80% figcaption="Bank A: Redemption Requests Pane" alt="Bank A: Redemption Requests Pane" >}}    

    Your tokens will be burned upon request for redemption. This is to avoid double-spending.

    If you check Bank B’s token balance on the Home page, you can now see that the balance has been lowered by the redemption request amount; in this example it now displays as zero:
   
    {{< figure src="bank-b-home-zero-tokens.png" width=100% figcaption="Bank B: Token Balance After Redemption Request" alt="Bank B: Token Balance After Redemption Request" >}}

    If the request is rejected, Bank B will be reissued with the requested tokens that were redeemed.

### Accepting or Rejecting Redemption Requests

Once a bank has created a request to redeem tokens, the relevant custodian can accept or reject the request.

1. Select the role of **Custodian A** from the dropdown menu at the top-right of the **Home** page:

   {{< figure src="select-custodian-a.png" width=28% figcaption="Selecting Custodian A as Active" alt="Selecting Custodian A as Active" >}}

   The header of the page now displays *Custodian A*, indicating that you are now acting in that role:
   
   {{< figure src="custodian-a-header.png" width=38% figcaption="Custodian A Active" alt="Custodian A Active" >}}

2. On the **Home** page, scroll down and click on the **Redemptions** tab.

   The **Incoming Redemption Requests** pane is displayed, listing the redemption request from Bank B:
   
   {{< figure src="custodian-a-incoming-redemption-requests.png" width=80% figcaption="Custodian A: Incoming Redemption Requests Pane" alt="Custodian A: Incoming Redemption Requests Pane" >}}

3. Click on the redemption request.

   The **Redemption Request** dialog box is displayed, showing details of the request:
   
   {{< figure src="custodian-a-redemption-request-requested.png" width=48% figcaption="Custodian A: Redemption Request Dialog Box" alt="Custodian A: Redemption Request Dialog Box" >}}

5. The custodian should now check their balance before proceeding. They will need to make an off-ledger payment for the amount requested to be redeemed via traditional payment rails. Once they have moved the funds to Bank A's banking account, they can proceed.

4.	Click **Complete Redemption** to accept Bank A’s request to redeem their tokens.

   The message *Successfully completed redemption* is displayed:
   
   {{< figure src="successfully-completed-redemption-message.png" width=38% figcaption="'Successfully completed redemption' Message" alt="'Successfully completed redemption' Message" >}}

Otherwise you could click **Reject Redemption** to reject their request. Upon rejection the custodian, together with the TIE, will reissue the said tokens back to Bank A and Bank A’s token balance will be updated to reflect their position.

### Viewing Tokens in Circulation

The **TIE** can view the tokens that are in circulation in an aggregated graph view at any time:

1. Select the role of **Token Issuing Entity** from the dropdown menu at the top-right of the **Home** page:

   {{< figure src="select-tie.png" width=28% figcaption="Selecting TIE as active" alt="Selecting TIE as active" >}}
   
2. Select **R3 Token Network** from the dropdown list at the top-left of the page:

   {{< figure src="select-r3-network.png" width=38% figcaption="Select R3 Token Network" alt="Select R3 Token Network" >}}
   
   Alternatively, to include tokens from multiple networks in the graph view, select multiple networks from the dropdown.

   The **Tokens in Circulation** pane on the TIE **Home** page displays the total number of tokens in circulation for the networks selected.
   
   {{< figure src="tokens-in-circulation.png" width=38% figcaption="'Tokens in Circulation' Pane" alt="'Tokens in Circulation' Pane" >}}

   The up-to-date tokens are now displayed on the donut charts of the **Custodian**, the **TIE** and **Bank B**.

{{< note >}}
Currently an aggregated view, a total of all bank's assets is shown on screen for demo purposes.
{{< /note >}}
