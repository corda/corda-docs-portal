---
description: "Learn how to invoke the Corda 5.3 REST API."
title: "Accessing the REST API"
date: 2023-05-08
menu:
  corda53:
    parent: corda53-rest-api-reference
    identifier: corda53-rest-api-accessing
    weight: 1000
---
# Accessing the REST API

To access and invoke the REST API:

1. If the REST API has not been exposed externally to the {{< tooltip >}}cluster{{< /tooltip >}} via a load balancer, forward the port by running the following command in a terminal window, replacing `<NAMESPACE>` with the Kubernetes namespace that Corda is installed in:

   ```sh
   kubectl port-forward -n <NAMESPACE> deploy/corda-rest-worker 8888
   ```

   If you did not explicitly specify the username for the initial admin user at install time, the default is `admin`. If you did not explicitly specify the password for the initial admin user at install time, you can retrieve it using the following command:

   ```sh
   kubectl get secret -n <NAMESPACE> corda-rest-api-admin -o go-template="{{ .data.password | base64decode }}"
   ```

4. The REST API is at the path `/api/v5_3`. The following is an example invocation using `curl` when the API endpoint is exposed via port forwarding:

   ```sh
   REST_API_URL=https://localhost:8888/api/v5_3
   REST_API_USER=admin
   REST_API_PASSWORD=$(kubectl get secret -n <NAMESPACE> corda-rest-api-admin -o go-template="{{ .data.password | base64decode }}")
   curl -k -u $REST_API_USER:$REST_API_PASSWORD $REST_API_URL/hello
   ```

   {{< note >}}
   The REST API is protected by a self-signed certificate.
   {{< /note >}}

You can access the Swagger documentation for the REST API at the path `/api/v5_3/swagger`. For example, when using port forwarding, the documentation is available at `<REST_API_URL>/swagger`.

You can also view the REST API documentation [here](./openapi.html).
