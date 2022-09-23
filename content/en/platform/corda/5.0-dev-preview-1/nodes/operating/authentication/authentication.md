---
title: "Configuring authentication"
date: '2021-08-25'
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-nodes-operating
    identifier: corda-5-dev-preview-1-nodes-operating-authentication
    weight: 4400
section_menu: corda-5-dev-preview
description: >
  How to configure authentication and authorization for HTTP-RPC.
---

Use this guide to configure authentication and authorization for HTTP-RPC, using basic authentication or Azure Active Directory (AD) single sign-on (SSO).

Most of the endpoints exposed via HTTP-RPC require authentication. `getProtocolVersion` is the only endpoint that doesn't require authentication.

You can test the authentication functionality using Swagger UI (if enabled):

![Authenticate on Swagger UI](swagger-auth.png "Authenticate on Swagger UI")

{{< note >}}

When a client response is unauthorized, the node uses [WWW-Authenticate](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/WWW-Authenticate) response headers to provide details on supported authentication types and their parameters.

{{< /note >}}

Nodes support [Basic authentication](#set-up-basic-authentication) and [Azure Active Directory (AD) single sign-on (SSO)](#set-up-azure-ad-sso).

## Set up basic authentication

You can use authenticated HTTP-RPC endpoints with [basic HTTP authentication](https://en.wikipedia.org/wiki/Basic_access_authentication) using the username/password combinations set up for RPC use. To configure user credentials in the `node.conf` file or through the use of an external database, see the guide on [managing RPC security](../../../../../../../en/platform/corda/4.8/open-source/clientrpc.html#managing-rpc-security) in Corda 4.

This feature is enabled by default and cannot be disabled.

### Configure authorization for basic authentication

Authorization in the Corda 5 Developer Preview uses the same Apache Shiro-based solution that was available in Corda 4. For details on how to configure this, see the guide on [managing RPC security](../../../../../../../en/platform/corda/4.8/open-source/clientrpc.html#managing-rpc-security) in Corda 4.

### Test your configuration

You can test your configuration using Swagger UI:

![Basic authentication on Swagger UI](swagger_basic.png "Basic authentication on Swagger UI")

## Set up Azure AD SSO

You can set up your node to use Azure Active Directory (AD) for single sign-on (SSO). Authorized users who access HTTP-RPC functions on the node can use their Azure AD credentials to stay logged in to any applications that use the HTTP-RPC API.

1. Configure the Azure AD tenant that serves as an identity provider and the node to enable HTTP-RPC endpoints to support Azure AD-based authentication.

2. Pass an Azure AD **ID token** or **access token** as a [Bearer Token](https://datatracker.ietf.org/doc/html/rfc6750) with the HTTP-RPC requests. The node verifies these properties/claims of the token:

    * Expiration date.
    * Issuer (should be a valid Microsoft Identity Platform value).
    * Audience (should be the `clientId` of the node).

3. Test this functionality using Swagger UI. The data flow should look like this:

![Example data flow](example_flow.png "Example data flow")

{{< note >}}
You can generate tokens using any method that is supported by the Microsoft Identity Platform, as long as it can be verified using the parameters above. This may mean different flows are used than those shown in the diagram.
{{< /note >}}

### Configure Azure

These steps describe a basic setup. Configuring a production setup may include additional steps, such as those for user access management and permission sets (scopes).

To complete the configuration of your node using the [Azure Portal](https://portal.azure.com/):

{{< note >}}
To register a new application, you must be an Azure **application administrator**.
{{< /note >}}

1. Navigate to the **register an application** screen (Manage > App registration > New registration).

2. Complete the online form to represent your node:

![Register a new application](step2.png "Register a new application")

3. Make a note of the `Application (client) ID` and `Directory (tenant) ID`. You need these to configure your node.

![Record application details](step3.png "Record application details")

4. Set authentication to ensure only accounts in this directory can use the app:

![Set authentication](step4.png "Set authentication")

5. Make the menu selection: Manage > Authentication, Platform configuration > Add a platform, Configure platforms > Single-page application.

{{< note >}}

You may need to use different configuration depending on the types of application that need to access the HTTP-RPC. This setup is for testing with Swagger UI.

Applications accessing the HTTP-RPC should use a different application registration and the [On-Behalf-Of flow](https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-on-behalf-of-flow).

You can register an application without implicit flows. You'll need to create a [**client secret**](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app#add-a-client-secret) and include it in the node's `node.conf` file. If you're using the Swagger UI, it can be entered there.

{{< /note >}}

6. Set the **redirect URL** to `http(s)://<host>:<port>/webjars/swagger-ui/3.44.0/oauth2-redirect.html`, and select implicit grant as `ìd_tokens`.

7. Under **Manage**, select **API permissions**, and add user permissions. You must apply `User.Read` as a minimum, but you can select scopes with wider permissions to suit your requirements.

![Add user permissions](step8.png "Add user permissions")

You have finished configuring Azure.

### Configure your node

Azure AD SSO is configured via a top-level object named `httpRpcSettings` in `node.conf`:

```
"httpRpcSettings": {
    ...
    "sso": {
        "azureAd": {
            "clientId": "<client_id>",
            "clientSecret": "<client_secret>"
            "tenantId": "<tenant_id>",
            "principalNameClaims": ["<claim1>", "<claim2>"]
        }
    }
}
```

Configuration options include:

{{<table>}}
| Field              | Required? | Value |
| ---------------- | --------- | ----- |
| `clientSecret`     | Optional | Auto fills the client-secret field on the Swagger UI authentication page when a non-public client flow is configured on Azure. *This field will be exposed on Swagger UI*. |
| `principalNameClaims` | Optional | A prioritized list of <a href="https://docs.microsoft.com/en-us/azure/active-directory/develop/active-directory-optional-claims">**claims**</a> that the node retrieves from the Azure AD-generated JSON web token (JWT) to then identify the user and fetch their permissions. Defaults to `["upn", "preferred_username", "email", "appid", "azp"]`.|

{{</table>}}

### Configure authorization for Azure AD SSO

Permissions are retrieved using the same Apache Shiro-based solution as for [basic authentication](#configure-authorization-for-basic-authentication). However, the actual name
of the user is derived from Azure `claims`.

To specify SSO permissions, add the email address that is associated with their SSO-authenticated user profile to the `node.conf` file.

```
"rpcUsers": [
    {
        "user": "user1@company.com",
        "permissions": [
            "ALL"
        ]
    }
]
```

For Azure AD SSO authentication, **JWT tokens** are used to verify a user's identity. Therefore, users listed in the Shiro database should *not* specify a password in the `node.conf` file.

{{< note >}}

Username matching uses the extracted principal name claim, which can change depending on the type of JWT provided and the `principalNameClaims` configuration item.

{{< /note >}}

### Test your configuration

You can test your setup using the Swagger UI:

![Azure AD authentication on Swagger UI](azure-testing.png "Azure AD authentication on Swagger UI")
