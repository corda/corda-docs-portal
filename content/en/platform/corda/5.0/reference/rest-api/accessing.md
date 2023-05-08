---
title: "Accessing the REST API"
project: corda
version: 'Corda 5.0'
date: 2023-05-08
menu:
  corda5:
    parent: corda5-rest-api-reference
    identifier: corda5-rest-api-accessing
    weight: 1000
section_menu: corda5
---

To access and invoke the REST API:

1. If the REST API has not been exposed externally to the cluster via a load balancer, forward the port by running the following command in a terminal window, replacing `<NAMESPACE>` with the Kubernetes namespace that Corda is installed in:

   ```sh
   kubectl port-forward -n <NAMESPACE> deploy/corda-rest-worker 8888
   ```

   If you did not explicitly specify the username for the initial admin user at install time, the default is `admin`. If you did not explicitly specify the password for the initial admin user at install time, you can retrieve it using the following command:

   ```sh
   kubectl get secret -n <NAMESPACE> corda-initial-admin-user -o go-template="{{ .data.password | base64decode }}"
   ```

4. The REST API is at the path `/api/v1`. The following is an example invocation using `curl` when the API endpoint is exposed via port forwarding:

   ```sh
   REST_API_URL=https://localhost:8888
   REST_API_USER=admin
   REST_API_PASSWORD=$(kubectl get secret -n <NAMESPACE> corda-initial-admin-user -o go-template="{{ .data.password | base64decode }}")
   curl -u $REST_API_USER:$REST_API_PASSWORD -k $REST_API_URL/api/v1/hello
   ```

   {{< note >}}
   The REST API is protected by a self-signed certificate.
   {{< /note >}}

You can access the Swagger documentation for the REST API at the path `/api/v1/swagger`. For example, when using port forwarding the documentation is available at `<REST_API_URL>/api/v1/swagger`.

You can also view the REST API documentation [here](./C5_OpenAPI.html).