---
date: '2022-14-11'
title: "REST API"
menu:
  corda-5-beta:
    identifier: corda-5-beta-rest-api
    parent: corda-5-beta-develop
    weight: 2500
section_menu: corda-5-beta
---
The Corda REST API enables operators to interact with a running version of Corda.
To access and invoke the REST API:

1. If the REST API has not been exposed externally to the cluster via a load balancer, forward the port by running the following command in a terminal window, replacing `<NAMESPACE>` with the Kubernetes namespace that Corda is installed in:

   ```sh
   kubectl port-forward -n <NAMESPACE> deploy/corda-rpc-worker 8888
   ```


   If you did not explicitly specify the username for the initial admin user at install time, the default is `admin`.
If you did not explicitly specify the password for the initial admin user at install time, you can retrieve it using the following command:

   ```sh
   kubectl get secret -n <NAMESPACE> corda-initial-admin-user -o go-template="{{ .data.password | base64decode }}"
   ```

4. The REST API is at the path `/api/v1`. An example invocation using `curl` when the API endpoint is exposed via port forwarding is as follows:

   ```sh
   API_ENDPOINT=https://localhost:8888
   USERNAME=admin
   PASSWORD=$(kubectl get secret -n <NAMESPACE> corda-initial-admin-user -o go-template="{{ .data.password | base64decode }}")
   curl -u $USERNAME:$PASSWORD -k $API_ENDPOINT/api/v1/hello
   ```

   {{< note >}}
   The REST API is protected by a self-signed certificate.
   {{< /note >}}

You can access the Swagger documentation for the REST API at the path `/api/v1/swagger`. For example, when using port forwarding the documentation is available at [https://localhost:8888/api/v1/swagger](https://localhost:8888/api/v1/swagger).

You can also view the REST API documentation [here](C5_OpenAPI.html).
