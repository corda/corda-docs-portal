---
aliases:
- /head/tutorial-attachments.html
- /HEAD/tutorial-attachments.html
- /tutorial-attachments.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-os-4-7:
    identifier: corda-os-4-7-tutorial-attachments
    parent: corda-os-4-7-supplementary-tutorials-index
    weight: 1080
tags:
- tutorial
- attachments
title: Working with attachments
---




# Working with attachments

This tutorial outlines how to work with attachments, also known as contract attachments.

## Introduction

Attachments are ZIP/JAR files referenced from transaction by hash, but not included in the transaction
itself. These files are automatically requested from the node sending the transaction when needed and cached
locally so they are not re-requested if encountered again. Attachments typically contain:

* Contract code
* Metadata about a transaction, such as PDF version of an invoice being settled
* Shared information to be permanently recorded on the ledger

## Uploading and downloading attachments

To add attachments, the file must first be uploaded to the node, which returns a unique ID that can be added
using `TransactionBuilder.addAttachment()`.

It is encouraged that, where possible, attachments are reusable data, so that nodes can meaningfully cache them.

### Uploading an attachment

To upload an attachment to the node, you need to first connect to the relevant node. You can do this via the Corda RPC Client, as described in [Interacting with a node](clientrpc.md) or you can upload your attachment via the [Node shell](shell.md).

To upload an attachment, run the following command:

```
run uploadAttachment jar: <insert path-to-the-file>.jar
```

Alternatively, if you want to include the metadata with the attachment which can be used to find it later on, run the following command:

```
run uploadAttachmentWithMetadata jar: path/to/the/file.jar, uploader: myself, filename: original_name.jar
```

Note that currently both uploader and filename are just plain strings - there is no connection between uploader and the RPC users, for example).

The file is uploaded, checked and if successful the hash of the file is returned. This is how the attachment is
identified inside the node.

### Downloading an attachment

To download an attachment named by its hash, you need to first connect to the relevant node. You can do this via the Corda RPC Client, as described in [Interacting with a node](clientrpc.md) or you can upload your attachment via the [Node shell](shell.md).

To download an attachment, run the following command, replacing the ID with the hash of the attachment that you want to download:

```
run openAttachment id: AB7FED7663A3F195A59A0F01091932B15C22405CB727A1518418BF53C6E6663A
```

You will be prompted to provide a path to save the file to. To do the same thing programmatically, you
can pass a simple `InputStream` or `SecureHash` to the `uploadAttachment`/`openAttachment` RPCs from
a JVM client.


## Searching for attachments

Attachment metadata can be queried in a similar way to the vault (see [API: Vault Query](api-vault-query.md)).

`AttachmentQueryCriteria` can be used to build a query using the following set of column operations:

* Binary logical (`AND`, `OR`)
* Comparison (`LESS_THAN`, `LESS_THAN_OR_EQUAL`, `GREATER_THAN`, `GREATER_THAN_OR_EQUAL`)
* Equality (`EQUAL`, `NOT_EQUAL`)
* Likeness (`LIKE`, `NOT_LIKE`)
* Nullability (`IS_NULL`, `NOT_NULL`)
* Collection based (`IN`, `NOT_IN`)

The `and` and `or` operators can be used to build complex queries. For example:

{{< tabs name="tabs-1" >}}
{{% tab name="kotlin" %}}
```kotlin

attachmentStorage.queryAttachments(
    AttachmentsQueryCriteria(uploaderCondition = Builder.equal("alice"))
        .and(AttachmentsQueryCriteria(uploaderCondition = Builder.equal("bob")))
)
​
attachmentStorage.queryAttachments(
    AttachmentsQueryCriteria(uploaderCondition = Builder.equal("alice"))
        .or(AttachmentsQueryCriteria(uploaderCondition = Builder.equal("bob")))

```
{{% /tab %}}

{{% tab name="java" %}}
```java

attachmentStorage.queryAttachments(
    new AttachmentsQueryCriteria(Builder.INSTANCE.equal("alice"))
    .and(new AttachmentsQueryCriteria(Builder.INSTANCE.equal("bob")))
);
​
attachmentStorage.queryAttachments(
    new AttachmentsQueryCriteria(Builder.INSTANCE.equal("alice"))
        .or(new AttachmentsQueryCriteria(Builder.INSTANCE.equal("bob")))
);
```
{{% /tab %}}


{{< /tabs >}}




## Fetching attachments

Normally, attachments on transactions are fetched automatically via the `ReceiveTransactionFlow`. Attachments
are needed in order to validate a transaction (they include, for example, the contract code), so must be fetched
before the validation process can run.

{{< note >}}
Future versions of Corda may support non-critical attachments that are not used for transaction verification
and which are shared explicitly. These are useful for attaching and signing auditing data with a transaction
that isn’t used as part of the contract logic.
{{< /note >}}

## Example

Here is a simple example of how to attach a file to a transaction and send it to the counterparty. The full code for this demo can be found in the [Kotlin](https://github.com/corda/samples-kotlin/tree/master/Features/attachment-sendfile) and [Java](https://github.com/corda/samples-java/tree/master/Features/attachment-sendfile) sample repositories.

{{< tabs name="tabs-2" >}}
{{% tab name="kotlin" %}}

```kotlin
@InitiatingFlow
@StartableByRPC
class SendAttachment(
        private val receiver: Party,
        private val unitTest: Boolean
) : FlowLogic<SignedTransaction>() {
    companion object {
        object GENERATING_TRANSACTION : ProgressTracker.Step("Generating transaction")
        object PROCESS_TRANSACTION : ProgressTracker.Step("PROCESS transaction")
        object FINALISING_TRANSACTION : ProgressTracker.Step("Obtaining notary signature and recording transaction.")

        fun tracker() = ProgressTracker(
                GENERATING_TRANSACTION,
                PROCESS_TRANSACTION,
                FINALISING_TRANSACTION
        )
    }

    constructor(receiver: Party) : this(receiver, unitTest = false)

    override val progressTracker = tracker()
    @Suspendable
    override fun call():SignedTransaction {
        // Obtain a reference from a notary we wish to use.
        /**
         *  METHOD 1: Take first notary on network, WARNING: use for test, non-prod environments, and single-notary networks only!*
         *  METHOD 2: Explicit selection of notary by CordaX500Name - argument can by coded in flow or parsed from config (Preferred)
         *
         *  * - For production you always want to use Method 2 as it guarantees the expected notary is returned.
         */
        val notary = serviceHub.networkMapCache.notaryIdentities.single() // METHOD 1
        // val notary = serviceHub.networkMapCache.getNotary(CordaX500Name.parse("O=Notary,L=London,C=GB")) // METHOD 2

        //Initiate transaction builder
        val transactionBuilder = TransactionBuilder(notary)

        //upload attachment via private method
        val path = System.getProperty("user.dir")
        println("Working Directory = $path")

        val zipPath = if (unitTest!!) "../test.zip" else "../../../../test.zip"

        //Change the path to "../test.zip" for passing the unit test.
        //because the unit test are in a different working directory than the running node.
        val attachmenthash = SecureHash.parse(uploadAttachment(zipPath,
                serviceHub,
                ourIdentity,
                "testzip"))

        progressTracker.currentStep = GENERATING_TRANSACTION
        //build transaction
        val ouput = InvoiceState(attachmenthash.toString(), participants = listOf(ourIdentity, receiver))
        val commandData = InvoiceContract.Commands.Issue()
        transactionBuilder.addCommand(commandData,ourIdentity.owningKey,receiver.owningKey)
        transactionBuilder.addOutputState(ouput, InvoiceContract.ID)
        transactionBuilder.addAttachment(attachmenthash)
        transactionBuilder.verify(serviceHub)

        //self signing
        progressTracker.currentStep = PROCESS_TRANSACTION
        val signedTransaction = serviceHub.signInitialTransaction(transactionBuilder)


        //conter parties signing
        progressTracker.currentStep = FINALISING_TRANSACTION

        val session = initiateFlow(receiver)
        val fullySignedTransaction = subFlow(CollectSignaturesFlow(signedTransaction, listOf(session)))

        return subFlow(FinalityFlow(fullySignedTransaction, listOf(session)))
    }
}


//private helper method
private fun uploadAttachment(
        path: String,
        service: ServiceHub,
        whoAmI: Party,
        filename: String
): String {
    val attachmenthash = service.attachments.importAttachment(
            File(path).inputStream(),
            whoAmI.toString(),
            filename)

    return attachmenthash.toString();
}
```
{{% /tab %}}

{{% tab name="java" %}}

@InitiatingFlow
@StartableByRPC
public class SendAttachment extends FlowLogic<SignedTransaction> {
    private final ProgressTracker.Step GENERATING_TRANSACTION = new ProgressTracker.Step("Generating transaction");
    private final ProgressTracker.Step PROCESSING_TRANSACTION = new ProgressTracker.Step("PROCESS transaction");
    private final ProgressTracker.Step FINALISING_TRANSACTION = new ProgressTracker.Step("Obtaining notary signature and recording transaction.");

    private final ProgressTracker progressTracker =
            new ProgressTracker(GENERATING_TRANSACTION, PROCESSING_TRANSACTION, FINALISING_TRANSACTION);

    private final Party receiver;
    private boolean unitTest = false;

    public SendAttachment(Party receiver) {
        this.receiver = receiver;
    }

    public SendAttachment(Party receiver, boolean unitTest) {
        this.receiver = receiver;
        this.unitTest = unitTest;
    }

    @Nullable
    @Override
    public ProgressTracker getProgressTracker() {
        return progressTracker;
    }

    @Suspendable
    @Override
    public SignedTransaction call() throws FlowException {

        // Obtain a reference to a notary we wish to use
        final Party notary = getServiceHub().getNetworkMapCache().getNotaryIdentities().get(0); // METHOD 1

        // Initiate transaction Builder
        TransactionBuilder transactionBuilder = new TransactionBuilder(notary);

        // upload attachment via private method
        String path = System.getProperty("user.dir");
        System.out.println("Working Directory = " + path);

        //Change the path to "../test.zip" for passing the unit test.
        //because the unit test are in a different working directory than the running node.
        String zipPath = unitTest ? "../test.zip" : "../../../../test.zip";

        SecureHash attachmentHash = null;
        try {
            attachmentHash = SecureHash.parse(uploadAttachment(
                    zipPath,
                    getServiceHub(),
                    getOurIdentity(),
                    "testzip")
            );
        } catch (IOException e) {
            e.printStackTrace();
        }

        progressTracker.setCurrentStep(GENERATING_TRANSACTION);
        // build transaction
        InvoiceState output = new InvoiceState(attachmentHash.toString(), ImmutableList.of(getOurIdentity(), receiver));
        InvoiceContract.Commands.Issue commandData = new InvoiceContract.Commands.Issue();
        transactionBuilder.addCommand(commandData, getOurIdentity().getOwningKey(), receiver.getOwningKey());
        transactionBuilder.addOutputState(output, InvoiceContract.ID);
        transactionBuilder.addAttachment(attachmentHash);
        transactionBuilder.verify(getServiceHub());

        // self signing
        progressTracker.setCurrentStep(PROCESSING_TRANSACTION);
        SignedTransaction signedTransaction = getServiceHub().signInitialTransaction(transactionBuilder);

        // counter parties signing
        progressTracker.setCurrentStep(FINALISING_TRANSACTION);

        FlowSession session = initiateFlow(receiver);
        SignedTransaction fullySignedTransaction = subFlow(new CollectSignaturesFlow(signedTransaction, ImmutableList.of(session)));

        return subFlow(new FinalityFlow(fullySignedTransaction, ImmutableList.of(session)));
    }

    private String uploadAttachment(String path, ServiceHub service, Party whoami, String filename) throws IOException {
        SecureHash attachmentHash = service.getAttachments().importAttachment(
                new FileInputStream(new File(path)),
                whoami.toString(),
                filename
        );

        return attachmentHash.toString();
    }
}

{{% /tab %}}

{{< /tabs >}}
