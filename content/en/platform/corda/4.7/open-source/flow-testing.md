---
aliases:
- /head/flow-testing.html
- /HEAD/flow-testing.html
- /flow-testing.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-os-4-7:
    identifier: corda-os-4-7-flow-testing
    parent: corda-os-4-7-core-tutorials-index
    weight: 1140
tags:
- flow
- testing
title: Writing flow tests
---




# Writing flow tests

This tutorial will take you through the steps required to write a flow test.

## Introduction

A flow can be a fairly complex thing that interacts with many services and other parties over the network. This
means that unit testing a flow requires some infrastructure to provide lightweight mock implementations.

 ## Creating a mock network

The `MockNetwork` class provides this testing infrastructure layer; you can find this class in the `test-utils` module.

The `IOUTransferFlowTests` tests provide a good example for learning how to unit test flows. This test file sits in our sample repositories under `Advanced/obligation-cordapp` and is available in both [Kotlin](https://github.com/corda/samples-kotlin/tree/master/Advanced/obligation-cordapp) and [Java](https://github.com/corda/samples-java/tree/master/Advanced/obligation-cordapp) versions.

Setup codes for both versions are shown here:

{{< tabs name="tabs-1" >}}
{{% tab name="kotlin" %}}
```kotlin

class IOUTransferFlowTests {
    lateinit var mockNetwork: MockNetwork
    lateinit var a: StartedMockNode
    lateinit var b: StartedMockNode
    lateinit var c: StartedMockNode

    @Before
    fun setup() {
        mockNetwork = MockNetwork(listOf("net.corda.training"),
                notarySpecs = listOf(MockNetworkNotarySpec(CordaX500Name("Notary","London","GB"))))
        a = mockNetwork.createNode(MockNodeParameters())
        b = mockNetwork.createNode(MockNodeParameters())
        c = mockNetwork.createNode(MockNodeParameters())
        val startedNodes = arrayListOf(a, b, c)
        // For real nodes this happens automatically, but we have to manually register the flow for tests
        startedNodes.forEach { it.registerInitiatedFlow(IOUIssueFlowResponder::class.java) }
        startedNodes.forEach { it.registerInitiatedFlow(IOUTransferFlowResponder::class.java) }
        mockNetwork.runNetwork()
    }

    @After
    fun tearDown() {
        mockNetwork.stopNodes()
    }

```
{{% /tab %}}

{{% tab name="java" %}}
```java

public class IOUTransferFlowTests {

    private MockNetwork mockNetwork;
    private StartedMockNode a, b, c;

    @Before
    public void setup() {
        MockNetworkParameters mockNetworkParameters = new MockNetworkParameters().withCordappsForAllNodes(
                Arrays.asList(
                        TestCordapp.findCordapp("net.corda.samples.contracts")
                )
        ).withNotarySpecs(Arrays.asList(new MockNetworkNotarySpec(new CordaX500Name("Notary", "London", "GB"))));
        mockNetwork = new MockNetwork(mockNetworkParameters);
        System.out.println(mockNetwork);

        a = mockNetwork.createNode(new MockNodeParameters());
        b = mockNetwork.createNode(new MockNodeParameters());
        c = mockNetwork.createNode(new MockNodeParameters());

        ArrayList<StartedMockNode> startedNodes = new ArrayList<>();
        startedNodes.add(a);
        startedNodes.add(b);
        startedNodes.add(c);

        // For real nodes this happens automatically, but we have to manually register the flow for tests
        startedNodes.forEach(el -> el.registerInitiatedFlow(IOUTransferFlow.Responder.class));
        startedNodes.forEach(el -> el.registerInitiatedFlow(IOUIssueFlow.ResponderFlow.class));
        mockNetwork.runNetwork();
    }

    @After
    public void tearDown() {
        mockNetwork.stopNodes();
    }

```
{{% /tab %}}

{{< /tabs >}}

We create a mock network in our `@Before` setup method and create a couple of nodes. We also record the identity
of the notary in our test network, which will come in handy later. We also tidy up when we’re done.

## Writing a test case

Next, we write a test case:

{{< tabs name="tabs-2" >}}
{{% tab name="kotlin" %}}
```kotlin

@Test
fun flowReturnsCorrectlyFormedPartiallySignedTransaction() {
    val lender = a.info.chooseIdentityAndCert().party
    val borrower = b.info.chooseIdentityAndCert().party
    val stx = issueIou(IOUState(10.POUNDS, lender, borrower))
    val inputIou = stx.tx.outputs.single().data as IOUState
    val flow = IOUTransferFlow(inputIou.linearId, c.info.chooseIdentityAndCert().party)
    val future = a.startFlow(flow)
    mockNetwork.runNetwork()
    val ptx = future.getOrThrow()
    // Check the transaction is well formed...
    // One output IOUState, one input state reference and a Transfer command with the right properties.
    assert(ptx.tx.inputs.size == 1)
    assert(ptx.tx.outputs.size == 1)
    assert(ptx.tx.inputs.single() == StateRef(stx.id, 0))
    println("Input state ref: ${ptx.tx.inputs.single()} == ${StateRef(stx.id, 0)}")
    val outputIou = ptx.tx.outputs.single().data as IOUState
    println("Output state: $outputIou")
    val command = ptx.tx.commands.single()
    assert(command.value == IOUContract.Commands.Transfer())
    ptx.verifySignaturesExcept(b.info.chooseIdentityAndCert().party.owningKey, c.info.chooseIdentityAndCert().party.owningKey,
            mockNetwork.defaultNotaryNode.info.legalIdentitiesAndCerts.first().owningKey)
}

```
{{% /tab %}}

{{% tab name="java" %}}
```java

@Test
    public void flowReturnsCorrectlyFormedPartiallySignedTransaction() throws Exception {
        Party lender = a.getInfo().getLegalIdentitiesAndCerts().get(0).getParty();
        Party borrower = b.getInfo().getLegalIdentitiesAndCerts().get(0).getParty();
        SignedTransaction stx = issueIOU(new IOUState(Currencies.DOLLARS(10), lender, borrower));
        IOUState inputIou = (IOUState) stx.getTx().getOutputs().get(0).getData();
        IOUTransferFlow.InitiatorFlow flow = new IOUTransferFlow.InitiatorFlow(inputIou.getLinearId(), c.getInfo().getLegalIdentities().get(0));
        Future<SignedTransaction> future = a.startFlow(flow);

        mockNetwork.runNetwork();

        SignedTransaction ptx = future.get();

        // Check the transaction is well formed...
        // One output IOUState, one input state reference and a Transfer command with the right properties.
        assert (ptx.getTx().getInputs().size() == 1);
        assert (ptx.getTx().getOutputs().size() == 1);
        assert (ptx.getTx().getOutputs().get(0).getData() instanceof IOUState);
        assert (ptx.getTx().getInputs().get(0).equals(new StateRef(stx.getId(), 0)));

        IOUState outputIOU = (IOUState) ptx.getTx().getOutput(0);
        Command command = ptx.getTx().getCommands().get(0);

        assert (command.getValue().equals(new IOUContract.Commands.Transfer()));
        ptx.verifySignaturesExcept(b.getInfo().getLegalIdentities().get(0).getOwningKey(), c.getInfo().getLegalIdentities().get(0).getOwningKey(), mockNetwork.getDefaultNotaryIdentity().getOwningKey());
    }

```
{{% /tab %}}

{{< /tabs >}}

Writing a test is an intuitive process. You are essentially mimicking what the flow does, composing the transaction, and collecting required signatures. In our example above, we first create the state attributes and package them into a state. Then we start the flow with a mock node. For the verification process, we take the obtained signed transaction and assert the required fields of the transaction as well as that of the input/output states.
