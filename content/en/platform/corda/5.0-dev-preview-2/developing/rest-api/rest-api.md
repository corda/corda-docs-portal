---
title: "REST API"
menu:
  corda-5-dev-preview2:
    identifier: corda-5-dev-preview-rest-api
    parent: corda-5-dev-preview-develop
    weight: 2500
section_menu: corda-5-dev-preview2
---
The Corda REST API enables operators to interact with a running version of Corda.
To access and invoke the REST API:

1. To access the RPC endpoint of a Corda cluster, forward the port by running the following command in a terminal window:

   ```sh
   kubectl port-forward -n corda deploy/corda-rpc-worker 8888
   ```

   You can then access the Swagger documentation for the RPC endpoint at [https://localhost:8888/api/v1/swagger](https://localhost:8888/api/v1/swagger).
Note that the RPC endpoint is protected by a self-signed certificate.

2. To invoke the RPC endpoint from the Swagger UI, use the user name `admin` and password `admin`. Alternatively, you can use curl. For example:

   ```sh
   curl -u admin:admin -k https://localhost:8888/api/v1/hello
   ```

You can also view the REST API documentation [here](C5_OpenAPI.html).
