---
date: '2023-02-23'
title: "Managing Virtual Nodes"
project: corda
version: 'Corda 5.0'
menu:
  corda5:
    identifier: corda5-cluster-nodes
    parent: corda5-cluster
    weight: 5000
section_menu: corda5
---
# Managing Virtual Nodes
This section **. It contains the following:
* 

## Rules for X.500 Member Names

Each virtual node within an application network is uniquely identified by its X.500 distinguished name. The rules for a valid X.500 name in Corda are the following:

* The string specified must use the grammar defined in RFC 1779 or RFC 2253.
* The only supported attributes are CN, OU, O, L, ST, C.
* Attributes cannot be duplicated and must have a single value.
* The attributes O, L, C are mandatory.
* The Organization attribute (O) cannot be blank and must be less than 128 characters.
* The Locality attribute (L) cannot be blank and must be less than 64 characters.
* The Country attribute (C) cannot be blank and must be an ISO 3166-1 2-letter country code or "ZZ" to indicate unspecified country.
* If specified, the State attribute (ST) cannot be blank and must be less than 64 characters.
* If specified, the Organization unit attribute (OU) cannot be blank and must be less than 64 characters.
* If specified, the Common Name attribute (CN) cannot be blank and must be less than 64 characters.
