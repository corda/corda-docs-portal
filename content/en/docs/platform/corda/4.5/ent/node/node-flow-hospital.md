---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-5:
    parent: corda-enterprise-4-5-corda-nodes-operating
tags:
- node
- flow
- hospital
title: Flow Hospital
weight: 150
---


# Flow Hospital


## Overview

The **flow hospital** refers to a built-in node service that manages flows that have encountered an error.

This service is responsible for recording, tracking, diagnosing, recovering and retrying flows. It determines whether errored flows should be retried
from their previous checkpoints or have their errors propagate. Flows may be recoverable under certain scenarios (eg. manual intervention
may be required to install a missing contract JAR version). For a given errored flow, the flow hospital service determines the next course of
action towards recovery and retry.

{{< note >}}
If the raised exception cannot be handled from the hospital, it will be propagated to the application code.
If the exception is not handled by the application code either, then the flow will terminate and any records of it will be removed from the hospital.
Below, you can find a list of the errors that are handled by the hospital.

{{< /note >}}
This concept is analogous to *exception management handling* associated with enterprise workflow software, or
*retry queues/stores* in enterprise messaging middleware for recovering from failure to deliver a message.


## Functionality

Flow hospital functionality is enabled by default in Corda Enterprise 4.5. No explicit configuration settings are required.

There are two aspects to the flow hospital:


* run-time behaviour in the node upon failure, including retry and recovery transitions and policies.
* visualisation of failed flows in the Explorer UI.



### Run-time behaviour

Specifically, there are two main ways a flow is hospitalized:


* A counterparty invokes a flow on your node that isn’t installed (i.e. missing CorDapp):
this will cause the flow session initialisation mechanism to trigger a `ClassNotFoundException`.
If this happens, the session initiation attempt is kept in the hospital for observation and will retry if you restart the node.
Corrective action requires installing the correct CorDapp in the node’s “cordapps” directory.
{{< warning >}}
There is currently no retry API. If you don’t want to install the cordapp, you should be able to call *killFlow* with the UUID
associated with the failing flow in the node’s log messages.{{< /warning >}}



* Once started, if a flow experiences an error, the following failure scenarios are handled:
* `SQLException` mentioning a **deadlock**:
If this happens, the flow will retry. If it retries more than once, a back off delay is applied to try and reduce contention.
Current policy means these types of failed flows will retry forever (unless explicitly killed).  No intervention required.
* **Database constraint violation** (`ConstraintViolationException`):
This scenario may occur due to natural contention between racing flows as Corda delegates handling using the database’s optimistic concurrency control.
If this exception occurs, the flow will retry. After retrying a number of times, the errored flow is kept in for observation.
* `SQLTransientConnectionException`:
Database connection pooling errors are dealt with. If this exception occurs, the flow will retry. After retrying a number of times, the errored flow is kept in for observation.
* All other instances of `SQLException`:
Any `SQLException` that is thrown and not handled by any of the scenarios detailed above, will be kept in for observation after their first failure.
* **Finality Flow handling** - Corda 3.x (old style) `FinalityFlow` and Corda 4.x `ReceiveFinalityFlow` handling:
If on the receive side of the finality flow, any error will result in the flow being kept in for observation to allow the cause of the
error to be rectified (so that the transaction isn’t lost if, for example, associated contract JARs are missing).
Intervention is expected to be “rectify error, perhaps uploading attachment, and restart node” (or alternatively reject and call *killFlow*).
* `FlowTimeoutException`:
This is used internally by the notary client flow when talking to an HA notary.  It’s used to cause the client to try and talk to a different
member of the notary cluster if it doesn’t hear back from the original member it sent the request to within a “reasonable” time.
The time is hard to document as the notary members, if actually alive, will inform the requester of the ETA of a response.
This can occur an infinite number of times.  i.e. we never give up notarising.  No intervention required.
* **HSM error handling**
    * HSM errors:
Some errors will be generated on failed HSM operations.  After retrying for a number of times the flow will be removed from
the flow hospital and the error will be allowed to propagate.
- Error type: `CryptoServiceException`
    * HSM timeouts:
These errors will be generated when the HSM takes too long to respond to an action.  The timeout value is defined in corda-configuration-file.
- Error type: `TimedCryptoServiceException`


* `HospitalizeFlowException`:
The aim of this exception is to provide user code a way to retry a flow from its last checkpoint if a known intermittent failure occurred.
Any `HospitalizeFlowException` that is thrown and not handled by any of the scenarios detailed above, will be kept in for observation.
* **Internal Corda errors**:
Flows that experience errors from inside the Corda statemachine, that are not handled by any of the scenarios details above, will be retried a number of times
and then kept in for observation if the error continues.



{{< note >}}
Flows that are kept in for observation are retried upon node restart.

{{< /note >}}
