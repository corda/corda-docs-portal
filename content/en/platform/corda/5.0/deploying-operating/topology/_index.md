---
date: '2023-02-23'
version: 'Corda 5.0 Beta 4'
title: "Infrastructure Topology"
menu:
  corda5:
    identifier: corda5-cluster-topology
    parent: corda5-cluster
    weight: 3000
section_menu: corda5
---
# Infrastructure Topology

This topic shows topology diagrams for both Corda in Amazon Web Services (AWS) and Corda in Azure.

The size of the Kubernetes cluster required is dependent on the workload that the Corda cluster needs to handle. The [Deploying]({{< relref "../deployment/deploying/_index.md" >}}) topic gives some guidance on initial resource requests/limits to apply to the Corda workers which, when combined with the number of replicas for each worker type, can be used to estimate the total resources required in the Kubernetes cluster. The number of nodes in the cluster, and their distribution across availability zones, should take into account requirements for the availability of the solution.

Performance testing of your CorDapps under expected loads is required to determine the values that you will require in a production deployment.

The following diagram shows the topology used if hosting on AWS:

{{<
  figure
  src="aws.png"
  width=100%
  alt="AWS Example"
  figcaption="AWS Example"
>}}

The following diagram shows the topology used if hosting on Azure:

{{<
  figure
  src="azure.png"
  width=100%
  alt="Azure Example"
  figcaption="Azure Example"
>}}


1.  External Network:
    * Represents either the Internet, or a known peered network.
2.  Load Balancer Firewall:
    * Represents the network rules used to limit which networks are allowed to access the load balancer.
    * AWS resource provided by "EC2/Security Groups".
    * Azure resource provided by "Load balancing/Load Balancers", or "Network security groups".
    * Create your own, or use ones created at stage 5.
3.  Load Balancer:
    * Represents a load balancer that manages ingress traffic.
    * AWS resource provided by "EC2/Load Balancers".
    * Azure resource provided by "Load balancing/Load Balancers".
    * Create your own, or use one created at stage 5.
4.  Application Ingress Firewall:
    * Represents the network rules used to limit which networks are allowed to access the application network ingress.
    * AWS resource provided by "EC2/Security Groups".
    * Azure resource provided by "Network security groups".
    * Create your own, or use ones created at stage 5.
5.  Application Ingress:
    * Represents the Kubernetes Ingress Controller, or Kubernetes Service that exposes the cluster applications to the outside network.
    * Usually accompanied with a cloud-native load balancer with the ability to configure further.
    * Kubernetes resources provided by, but not limited to, "Ingress-Nginx", "Traefik Proxy", and the Kubernetes resource kind "Service" (type: LoadBalancer).
6.  Corda.
7.  Database Firewall:
    * Represents the network rules used to limit which networks are allowed to access the database.
    * AWS resource provided by "EC2/Security Groups".
    * Azure resource provided by "Network security groups".
8.  Database:
    * Represents the datastore used by Corda.
    * Supported database engine is "PostgreSQL" (version 14.4).
    * AWS resource provided by "RDS".
    * Azure resource provided by "Azure Database for PostgreSQL flexible servers".
9.  Egress Firewall (optional limitation):
    * Represents the network rules used to limit egress network access to external networks.
    * AWS resource provided by "EC2/Security Groups".
    * Azure resource provided by "Load balancing/Load Balancers", or "Network security groups".
10. Egress:
    * Represents the route external egress network traffic takes from the application network.
    * In AWS it is routed (from Subnet: Private) via a NAT gateway, and, if the destination is on the Internet, an Internet gateway.
    * In Azure it is routed (from Kubernetes: A) via the same Load Balancer resource, acting as a NAT gateway, from stage 2, 3 and 5.