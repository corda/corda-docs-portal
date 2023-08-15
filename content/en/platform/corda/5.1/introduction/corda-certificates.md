---
title: "Certificates Keys and Certificates in Corda 5.1"
date: 2023-04-21
version: 'Corda 5.1'
menu:
  corda51:
    identifier: corda51-certficates
    parent: corda51-intro
    weight: 5000
section_menu: corda51
---

This page is to document different types of keys and certificates in Corda 5 and their purpose.

|Key name |Is it used with Certificate| Description                                                                        | Key type|
| --------------------------------------- | ---------------------------------------------------------------------------------- |
| P2P TLS key                                    | Yes| Part of TLS encryption at Corda cluster gateway level.                                       ||
| Session initiation key                |Yes| Used during end-to-end session handshake between 2 clusters, used to sign group parameters.          ||
| ECDH (MGM)                        | The path to write the generated DML files to.                                      |
| -s, \-\-schemas                         | The file of schema files to generate. If not specified, all schemas are generated. |