---
date: '2023-12-15'
section_menu: corda-enterprise-4-12
menu:
  corda-enterprise-4-12:
    identifier: corda-enterprise-4-12-stopping-tvu
    parent: corda-enterprise-4-12-tvu
tags:
- stopping tvu
- tvu
- transaction validator utility
title: Stopping Transaction Validator Utility
weight: 400
---

# Stopping Transaction Validator Utility

As the utility writes progress and errors to the underlying resources, if needed, you must stop it in one of the following ways:
* Press `Ctrl+C`
* Send `SIGTERM`

Do not try to stop the utility using a `kill -9` or `SIGKILL`.
