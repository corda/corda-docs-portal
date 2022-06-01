---
title: "Configuring node.conf"
date: '2021-08-25'
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-nodes-operating
    identifier: corda-5-dev-preview-1-nodes-operating-configure-nodeconf
    weight: 4000
section_menu: corda-5-dev-preview
description: >
  How to configure a node's `node.conf` file for HTTP-RPC.
---

Use this guide to configure a node's `node.conf` file for HTTP-RPC.

When a node starts up, the `corda.jar` file defaults to reading the node's configuration from a `node.conf` file.
To use HTTP-RPC, you need to configure your node's `node.conf` by:

1. <a href="#add-httprpcsettings-fields-and-configuration">Adding `httpRpcSettings` fields and configuration</a>.
2. [Verifying HTTP-RPC setup](#verify-http-rpc-setup)

## Add `httpRpcSettings` fields and configuration
`httpRpcSettings` is a top-level object that you need to include in the `node.conf` file. Here is a template that you can adapt:
```
{
    ...
    "httpRpcSettings": {
        "address": "mynode:8888",
        "context": {
            "description": "Exposing RPCOps interfaces as webservices",
            "title": "HTTP RPC demo",
        },
        "ssl": {
            "keyStorePath": "/home/corda/certificates/https.keystore",
            "keyStorePassword": "password"
        },
        maxContentLength=100000
    },
    ...
}
```

Configuration options available in the `httpRpcSettings` object:

{{<table>}}

| Field     | Required? | Value |
| ------- | --------- | ----- |
| `address` | Required  | The endpoint the node is listening to (`host:port` format). This is a local setting, so if you're using a hostname rather than `localhost` or `0.0.0.0`, you need to make sure the hostname resolves to the host the node is running on). The API will be available at `http[s]://{address}/api/v1/` |
| `context` | Required  | See [API configuration](#api-configuration). |
| `ssl`     | Required (unless node is in developer mode)  | See [SSL configuration](#ssl-configuration). |
| `sso`     | Optional | See [single sign-on (SSO) configuration](../../../../../../en/platform/corda/5.0-dev-preview-1/nodes/operating/authentication/authentication.html#set-up-azure-ad-sso). |
| `maxContentLength`     | Optional | The maximum content length accepted for `POST` requests (in bytes). The default value is 1 MiB.|

{{</table>}}

### API configuration

{{<table>}}

| Field         | Required? | Value |
| ----------- | --------- | ----- |
| `title`       | Required  | Name of the exposed API. |
| `description` | Required  | Human-friendly description of the API.|

{{</table>}}


### SSL configuration

{{<table>}}

| Field              | Required? | Value |
| ---------------- | --------- | ----- |
| `keyStorePath`     | Required | Path to the key store, relative to the current working directory. |
| `keyStorePassword` | Required | Password to the key store.|

{{</table>}}

To configure your node to use SSL encryption for HTTP-RPC, see the [SSL setup](../../../../../../en/platform/corda/5.0-dev-preview-1/nodes/operating/setup-ssl-encryption.md) guide.

## Verify HTTP-RPC setup
Start the node to verify that you have set up HTTP-RPC correctly. You should see:

```Console
[INFO] 2021-05-28T16:20:25,572Z [net.corda.node.OSGiNodeActivator.start] BasicInfo.printBasicNodeInfo - HTTP RPC address                        : https://mynode:8888 {}
[INFO] 2021-05-28T16:20:25,573Z [net.corda.node.OSGiNodeActivator.start] BasicInfo.printBasicNodeInfo - Swagger UI available at                 : https://mynode:8888/api/v1/swagger
[...]
[INFO] 2021-05-28T16:20:27,907Z [NodeLifecycleEventsDistributor-0] rpc.CordaRPCOpsImpl.update - After start {}
[INFO] 2021-05-28T16:20:27,931Z [NodeLifecycleEventsDistributor-0] flow.StartableFlowsRetriever.get - Rpc startable flows: {}
[INFO] 2021-05-28T16:20:27,931Z [NodeLifecycleEventsDistributor-0] flow.StartableFlowsRetriever.get - net.corda.httprpcdemo.workflows.MessageStateIssue {}
```

A Swagger UI address is included in the output. Use this address to test the various endpoints. As a simple smoke test, you can use any of the `getProtocolVersion` calls. If the test is successful and HTTP-RPC is configured correctly, it will return a `200 OK` status and an integer in the response body (the actual value depends on which Corda version the node is running).

### Common errors

* If the specified SSL certificate isn't accepted by the computer you're using to access the Swagger UI, the browser will treat the connection as insecure. However, this may not be an issue if the API is used from other sources that validate the certificate in a different way compared to the browser.

* When running a node in Docker you may get the error `HTTP Error 404 - site not accessible`. If the port specified in `node.conf` is not exposed, the API will be inaccessible. To make sure the port is available from outside the container, check the Dockerfile and command you're using to start the container. Read about [published ports](https://docs.docker.com/config/containers/container-networking/#published-ports) for more information.
