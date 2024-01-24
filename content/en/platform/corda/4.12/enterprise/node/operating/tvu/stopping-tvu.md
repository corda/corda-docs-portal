---
description: "Learn how to stop Transaction Validator Utility in a correct way."
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

As the utility writes its runtime progress and registers transaction processing errors to the underlying resources, if needed, you can stop it in one of the following ways so the progress and errors are reliably registered:
* Press `Ctrl+C`
* Send `SIGTERM`

Do not try to stop the utility using `kill -9` or `SIGKILL`. Since `kill -9` and `SIGKILL` terminate the utility immediately, the progress and the errors will not be reliably registered. This does not harm the utility’s working in anyways with regard to transaction processing but only disrupt the functionality wherein it registers progress for progress reloading and registers errors for debugging.
