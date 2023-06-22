---
date: '2023-06-22'
title: "External Messaging"
project: corda
version: 'Corda 5.0 Beta 4'
menu:
  corda5:
    identifier: corda5-develop-external-messaging
    parent: corda5-develop
    weight: 7050
section_menu: corda5
---

# External Messaging

A running Corda flow can send simple messages via Kafka to external systems. 
In 5.0, this is limited to sending messages, but a future version will support both send and send-and-receive messages. 

**For CorDapp to be able to send a message there are a number of steps required by the CorDapp developer and the cluster/virtual node operator. This guide will describe each step in detail and provide a walkthrough to build a simple example app, deploy it to a cluster.**