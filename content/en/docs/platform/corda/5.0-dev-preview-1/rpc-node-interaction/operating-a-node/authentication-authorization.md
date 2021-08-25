---
title: "Configure authorization and authentication"
date: '2021-08-25'
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-operate-node
    identifier: corda-5-dev-preview-1-operate-node-authentication-authorization
    weight: 500
project: corda-5
section_menu: corda-5-dev-preview
description: >
  Instructions on how to configure authentication and authorization for HTTP-RPC.
---

## Authorization

Authorization in Corda 5 uses the same Apache Shiro-based solution that was available in Corda 4. For details on how to configure this, see the guide on [managing RPC security](https://docs.corda.net/docs/corda-os/4.8/clientrpc.html#managing-rpc-security) in Corda 4.

## Authentication

Most endpoints exposed via HTTP-RPC require authentication.
There is one internal endpoint which does not require authentication: `getProtocolVersion`.

You can test this functionality using Swagger UI (if enabled):

![Authenticate on Swagger UI](swagger_auth.PNG "Authenticate on SwaggerUI")

{{< attention >}}

Unauthorized responses will return the configured authentication types and their parameters via [WWW-Authenticate](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/WWW-Authenticate) headers.

{{< /attention >}}

### Supported authentication types
Basic authentication.
---

As in Corda 4, you can use authenticated HTTP-RPC endpoints with [basic HTTP authentication](https://en.wikipedia.org/wiki/Basic_access_authentication) using the username/password combinations set up for RPC use. To configure user credentials in the `node.conf` file or through the use of an external database, see the guide on [managing RPC security](https://docs.corda.net/docs/corda-os/4.8/clientrpc.html#managing-rpc-security) in Corda 4.

This feature is enabled by default and cannot be disabled.

## Testing basic authentication

You can test this functionality using Swagger UI:

![Basic authentication on Swagger UI](swagger_basic.PNG "Basic authentication on SwaggerUI")

AzureAD SSO setup.
---

You can set up your Corda 5 node to use Azure Active Directory (Azure AD) for single sign-on (SSO). Authorized users who can access HTTP-RPC functions on the node can use their Azure AD credentials to stay logged in to any applications that use the HTTP-RPC API.

You need to configure the Azure AD tenant serving as an identity provider and the node to enable HTTP-RPC endpoints to support Azure AD-based authentication.

This authentication type requires an Azure AD **ID token** or **access token** to be passed with the HTTP-RPC requests as a [Bearer Token](https://datatracker.ietf.org/doc/html/rfc6750). The node verifies the following properties/claims of the token:

* Expiration date.
* Issuer (should be a valid Microsoft Identity Platform value).
* Audience (should be the `clientId` of the node).

You can test this functionality using Swagger UI. The data flow should look like this:

![Example flow](example_flow.png "Example flow")

{{< attention >}}
You can generate tokens using any method that is supported by the Microsoft Identity Platform, as long as it can be verified using the parameters above. This may mean different flows are used than those shown in the diagram above.
{{< /attention >}}

## Configuring Azure

{{< attention >}}
This describes a basic setup. Configuring a production setup may include further steps, such as for user access management and permission sets (scopes).
{{< /attention >}}

To complete the configuration of your node using the [Azure Portal](https://portal.azure.com/):

1. Navigate to the *register an application* screen (Manage > App registration > New registration).

2. Complete the online form to represent your node:

![Add new app registration](step2.png "Add new app registration")

3. Make a note of the "Application (client) ID" and "Directory (tenant) ID". You need these to configure your node.

![Record app details](step3.png "Record app details")

4. Set authentication to ensure only accounts in this directory can use the app:

![Set authentication](step4.png "Set authentication")

5. Make the following menu selections: Manage > Authentication, Platform configuration > Add a platform, Configure platforms > Single-page application.

{{< attention >}}

You may need to use different configuration depending on the types of application that need to access the HTTP-RPC. This setup is for testing with the Swagger UI.

Applications accessing the HTTP-RPC should use a different app registration and the [On-Behalf-Of flow](https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-on-behalf-of-flow).

You can register an application without implicit flows. You'll need to create a [**client secret**](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app#add-a-client-secret) and include it in the application authenticating. If you're using the Swagger UI, it can be entered there.

{{< /attention >}}

6. Set the **redirect URI** to `http(s)://<host>:<port>/webjars/swagger-ui/3.44.0/oauth2-redirect.html`, and select implicit grant as `ìd_tokens`.

7. Under **Manage**, select **API permissions**, and add user permissions. You must apply `User.Read` as a minimum, but you can select scopes with wider permissions to suit your requirements.

![Add user permissions](step8.png "Add user permissions")

You have finished configuring Azure.

## Node configuration

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

| Field              | Required? | Value |
| ---------------- | --------- | ----- |
| `clientSecret`     | Optional | Autofills the client-secret field on the Swagger UI authentication page when a non-public client flow is configured on Azure. *This field will be exposed on the Swagger UI*. |
| `principalNameClaims` | Optional | A prioritized list of [**claims**](https://docs.microsoft.com/en-us/azure/active-directory/develop/active-directory-optional-claims) that the node retrieves from the Azure AD-generated JSON web token (JWT) to then identify the user and fetch their permissions. Defaults to `["upn", "preferred_username", "email", "appid", "azp"]`.|

### Authorization

Permissions are retrieved using the Apache Shiro solution, the same as for basic authentication. This means permissions can be set up in the same way. However, the actual name of the user will be derived from Azure `claims`. For Azure AD SSO authentication, JWT tokens are used to verify a user's identity. Therefore, users listed in the Shiro database should *not* specify a password:

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

Username matching uses the extracted principal name claim, which can change depending on the type of JWT provided and the `principalNameClaims` configuration item.

## Testing the configuration

You can test this functionality using the Swagger UI:

![AzureAD authentication on Swagger UI](swagger_azure.PNG "AzureAD authentication on SwaggerUI")
