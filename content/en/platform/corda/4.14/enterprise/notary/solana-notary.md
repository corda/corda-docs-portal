---
date: '2026-02-25T00:00:00Z'
menu:
  corda-enterprise-4-14:
    identifier: corda-enterprise-4-14-solana-notary
    parent: corda-enterprise-4-14-corda-nodes-notaries
    name: "Solana notary"
tags:
- solana
- notary
- cross-chain
- atomic
title: Solana notary
weight: 15
---

# Solana notary

The Solana notary is a Corda Enterprise notary implementation that records notarisation results on the
[Solana](https://solana.com/) blockchain rather than in a conventional database. This enables CorDapps to perform
**atomic cross-chain operations**: a Corda transaction is notarised if and only if a corresponding Solana program
instruction — such as an SPL token transfer — also executes successfully.

This enables a new category of CorDapp use cases that require coordinated finality across both networks:

* **Delivery versus payment (DvP)**: Transfer a Corda asset to a buyer at the same time as the buyer's Solana
stablecoin payment is transferred to the seller. The swap is atomic — there is no window in which delivery can occur
without payment, or vice versa.
* **Bridging**: Lock assets on the Corda network and atomically mint the corresponding amount on Solana as an SPL token.
* **Conditional token operations**: Mint, burn, or transfer a Solana token only when a specific Corda transaction is notarised.
* **Cross-chain escrow release**: Release Solana tokens held in escrow upon settlement of a Corda obligation.

In all cases, the Solana notary guarantees that if either side of the operation fails — whether due to a double-spend
attempt on Corda, or an error in the Solana instruction — the entire operation is rolled back.

## How it works

### Overview

When a Corda transaction is sent for notarisation, the Solana notary:

1. **Builds** a _Solana_ transaction containing the notary program's `commit` instruction for the input states to be
spent, and any user-provided Solana instructions.
2. **Submits** the Solana transaction on-chain. All instructions are executed atomically. If a double-spend is
detected, or any of the user-provided instructions fail, the entire Solana transaction is rolled back and nothing is
committed to the blockchain.
3. **Validates** the Corda transaction time window.
4. **Waits** for confirmation the Solana transaction was processed and is part of the blockchain. The notary will wait
until the transaction reaches **confirmed** commitment, which takes roughly 1 second.
5. **Signs** the Corda notarisation and returns it to the requesting node.

### The Solana notary program

The notary program (`notary95bwkGXj74HV2CXeCn4CgBzRVv5nmEVfqonVY`) runs on Solana and is administered by R3.
It maintains the following on-chain accounts, all implemented as Program Derived Addresses (PDAs):

* **`CordaTxAccount`**: Created for each notarised Corda transaction. Stores a 128-bit bitset in which each bit
represents a transaction output index; a cleared bit indicates that the corresponding state has been spent. This is the
mechanism by which double-spends are detected on-chain.
* **`NotaryAuthorization`**: One account per authorized notary key, linking the notary's Solana public key to a
network ID. The notary must sign every commit instruction, and the program verifies authorization before accepting it.
* **`Network`**: One account per registered Corda network. Each Corda network has a unique numeric ID assigned by the
program administrator.
* **`Administration`**: A singleton account holding the program administrator's public key and the counter used to
assign network IDs.

{{< note >}}
The Solana notary program is administered exclusively by R3. Please raise a support ticket to have your notary key
authorized.
{{< /note >}}

### State tracking

Corda transaction IDs and input state references are encoded and stored in `CordaTxAccount` PDAs as follows:

* Each Corda transaction maps to a PDA derived from a **hash of the transaction ID** and the network ID. The
hash ensures that raw Corda transaction IDs are never exposed on-chain, mitigating the risk of denial-of-state
attacks.
* Input states are tracked using a **u128 bitset** (one bit per output index). When a state is spent, its bit is cleared.

{{< warning >}}
Using a 128-bit bitset means Corda transactions cannot have more than 128 output states (indices 0–127). Output states
at index 128 or greater cannot be consumed. This is currently not enforced and so CorDapps must ensure they do not
create more than 128 output states in a transaction.
{{< /warning >}}

## Programming model

### Adding a Solana instruction to a Corda transaction

CorDapp developers attach `SolanaInstruction`s to a Corda transaction using `TransactionBuilder.addNotaryInstruction()`.
This marks the instruction for execution by the Solana notary at the point of notarisation.

{{< tabs name="tabs-3" >}}
{{% tab name="Kotlin" %}}
```kotlin
txBuilder.addNotaryInstruction(
    SplToken.transferChecked(
        sourceTokenAccount,
        tokenMint,
        destinationTokenAccount,
        signerAccount,
        amount,
        decimals
    )
)
```
{{% /tab %}}
{{% tab name="Java" %}}
```java
txBuilder.addNotaryInstruction(
    SplToken.transferChecked(
        sourceTokenAccount,
        tokenMint,
        destinationTokenAccount,
        signerAccount,
        amount,
        decimals
    )
);
```
{{% /tab %}}
{{< /tabs >}}

{{< note >}}
`SolanaInstruction` is an implementation of `NotaryInstruction`. The Solana notary however will not accept a transaction
if it has `NotaryInstruction`s which are not `SolanaInstruction`.
{{< /note >}}

The `SolanaInstruction` type mirrors the structure of a standard Solana instruction:

* **`programId`**: The base58-encoded public key of the Solana program to invoke. Must be in the notary's configured program whitelist.
* **`accounts`**: The list of accounts the instruction reads or writes, each with `isSigner` and `isWritable` flags.
* **`data`**: The serialized instruction data passed to the program.

Multiple `SolanaInstruction`s can be added to a single Corda transaction. They are executed in order within the same
Solana transaction as the notary commit.

### Verifying the Solana instruction in a contract

Corda contracts can inspect the Solana instructions attached to a transaction using
`LedgerTransaction.notaryInstructionsOfType<SolanaInstruction>()`. This allows contract code to verify the instruction
is correct for the Corda transaction that it's part of.

{{< tabs name="tabs-4" >}}
{{% tab name="Kotlin" %}}
```kotlin
override fun verify(tx: LedgerTransaction) {
    val solanaInstruction = tx.notaryInstructionsOfType<SolanaInstruction>().single()
    val expectedInstruction = SplToken.transferChecked(
        sourceTokenAccount,
        tokenMint,
        destinationTokenAccount,
        signerAccount,
        amount,
        decimals
    )
    require(solanaInstruction == expectedInstruction) {
        "Solana instruction does not match the agreed transfer"
    }
}
```
{{% /tab %}}
{{% tab name="Java" %}}
```java
@Override
public void verify(LedgerTransaction tx) {
    SolanaInstruction solanaInstruction = tx.notaryInstructionsOfType(SolanaInstruction.class).get(0);
    SolanaInstruction expectedInstruction = SplToken.transferChecked(
        sourceTokenAccount,
        tokenMint,
        destinationTokenAccount,
        signerAccount,
        amount,
        decimals
    );
    if (!solanaInstruction.equals(expectedInstruction)) {
        throw new IllegalArgumentException("Solana instruction does not match the agreed transfer");
    }
}
```
{{% /tab %}}
{{< /tabs >}}

{{< note >}}
Use of `SolanaInstruction`s in Corda transactions is entirely optional. The Solana notary can still be used to notarise
Corda transactions with no instructions. In this case the Solana blockchain is just being used for its consensus
mechanism.
{{< /note >}}

### Custodied signing keys

Some Solana instructions require a signature from an account other than the notary itself — for example, to authorize
a token transfer from a participant's account. The Solana notary supports **custodied keys**: signing keys held by the
notary on behalf of participants.

Custodied keys are stored as Solana keypair files in the directory configured by `custodiedKeysDir`. When a
`SolanaInstruction` references an account marked `isSigner = true`, the notary looks up the corresponding custodied key
and co-signs the Solana transaction.

{{< warning >}}
The notary will reject any transaction which has the notary key as a signer account to any user-provided instruction.
The notary key can only be used by the notary for signing the `commit` instruction.
{{< /warning >}}

## Prerequisites

Before configuring the Solana notary, ensure the following are in place:

1. **Notary keypair**: A Solana [keypair file](https://docs.anza.xyz/cli/wallets/file-system) for the notary. This
account must have sufficient SOL to pay for Solana transaction fees and account rent for each notarised Corda transaction.
2. **Notary authorization**: Your notary's Solana public key must be authorized by R3 in the Solana notary program.
3. **Solana RPC access**: The notary node requires HTTP and WebSocket access to a [Solana RPC endpoint](https://solana.com/rpc).
4. **Program whitelist agreement**: Agree with your network participants which Solana programs may be invoked via
notary instructions. By default, the SPL Token and Token-2022 programs are whitelisted.

## Configuration

The Solana notary is configured with the `notary.solana` block. See
[Node configuration fields]({{< relref "../node/setup/corda-configuration-fields.md#solana" >}}) for the full
configuration reference.

```hocon
notary {
    ...
    solana {
        rpcUrl = "https://api.mainnet-beta.solana.com"
        websocketUrl = "wss://api.mainnet-beta.solana.com"
        notaryKeypairFile = "/opt/corda/solana-notary-keypair.json"
    }
}
```

## Solana account costs

Each notarised Corda transaction creates one or more `CordaTxAccount` PDAs on Solana. These accounts require
[deposit or \"rent\"](https://docs.solana.com/developing/programming-model/accounts#rent) to be paid in SOL by the notary
account. Ensure the notary account is adequately funded for your expected transaction volume.

The number of accounts created per notarisation depends on how many distinct input transaction IDs appear in the
notarised transaction:

* One account for the notarised transaction itself.
* One account per distinct input transaction ID (if not already created by a previous notarisation).

Testing on devnet will give a good indication of SOL costs.

## Supported Solana networks

The Solana notary connects to whichever Solana cluster is specified in `rpcUrl` and `websocketUrl`. The notary
program is deployed on **Solana mainnet** and **devnet**. R3 maintains a devnet deployment for testing purposes.

{{< note >}}
The notary program address is the same on both mainnet and devnet: `notary95bwkGXj74HV2CXeCn4CgBzRVv5nmEVfqonVY`.
{{< /note >}}

## Testing

The Solana notary testing library provides JUnit 5 support for writing integration tests against a local Solana test
validator with the Corda notary program pre-deployed and configured. This removes the need to manage Solana
infrastructure manually in tests.

Add the following dependencies. See the
[Solana notary](https://github.com/corda/solana-notary) and
[Corda Solana libs](https://github.com/corda/corda-solana-toolkit) repositories for the latest published versions.

```groovy
testImplementation "net.corda.solana.notary:solana-notary-testing:$solanaNotaryVersion"
testImplementation "com.r3.corda.lib.solana:corda-solana-testing:$cordaSolanaLibsVersion"
```

{{< note >}}
The [Solana CLI](https://solana.com/docs/intro/installation) must be installed locally to use the testing library,
as it is used to start the local test validator.
{{< /note >}}

### SolanaNotaryExtension

`SolanaNotaryExtension` is a JUnit 5 extension that automatically starts a local Solana test validator with the
Corda notary program deployed and initialized, and shuts it down after all tests in the class have run. Apply it
with `@ExtendWith(SolanaNotaryExtension::class)` and declare the resources you need as test method parameters.

The following parameter types can be injected into test methods and lifecycle methods:

* `SolanaTestValidator` — the running local validator instance, providing `rpcUrl()`, `websocketUrl()`,
  and helpers for token and account management.
* `SolanaClient` — an RPC client already connected to the validator.
* `NotaryEnvironment` — programmatic access to notary program administration, such as creating networks and
  authorizing notary keys.
* `PublicKey`, `Signer`, or `FileSigner` annotated with `@Notary` — a generated keypair that has been funded
  with SOL and authorized on the notary program. The `@Notary` annotation accepts optional `value` (key index)
  and `network` parameters to obtain distinct notary keys or place them on different networks.

### Using SolanaNotaryExtension in a Corda Driver DSL test

The most common pattern is to use `SolanaNotaryExtension` together with the Corda Driver DSL. The injected
`@Notary FileSigner` provides the keypair file that the notary node requires for `notaryKeypairFile`, and the
`SolanaTestValidator` provides the RPC and WebSocket URLs. These are assembled into a `NotarySpec` configuration
in a `@BeforeEach` method, and then passed to `DriverParameters` when the test runs:

{{< tabs name="tabs-1" >}}
{{% tab name="Kotlin" %}}
```kotlin
@ExtendWith(SolanaNotaryExtension::class)
class DvPTest {

    @TempDir
    private lateinit var custodiedKeysDir: Path

    private lateinit var notaryConfig: Map<String, Any>

    @BeforeEach
    fun setup(validator: SolanaTestValidator, @Notary notarySigner: FileSigner) {
        notaryConfig = mapOf(
            "notary" to mapOf(
                "validating" to false,
                "solana" to mapOf(
                    "rpcUrl" to "${validator.rpcUrl()}",
                    "websocketUrl" to "${validator.websocketUrl()}",
                    "notaryKeypairFile" to "${notarySigner.file}",
                    "custodiedKeysDir" to "$custodiedKeysDir"
                )
            )
        )
    }

    @Test
    fun `atomic DvP test`() {
        driver(DriverParameters(notarySpecs = listOf(NotarySpec(solanaNotaryName, notaryConfig)))) {
            val seller = startNode(NodeParameters(providedName = sellerName)).getOrThrow()
            val buyer  = startNode(NodeParameters(providedName = buyerName)).getOrThrow()

            seller.rpc.startFlow(::SharesDvP, buyer.nodeInfo.legalIdentities[0])
                .returnValue.getOrThrow()
        }
    }
}
```
{{% /tab %}}
{{% tab name="Java" %}}
```java
@ExtendWith(SolanaNotaryExtension.class)
public class DvPTest {

    @TempDir
    private Path custodiedKeysDir;

    private Map<String, Object> notaryConfig;

    @BeforeEach
    public void setup(SolanaTestValidator validator, @Notary FileSigner notarySigner) {
        notaryConfig = Map.of(
            "notary", Map.of(
                "validating", false,
                "solana", Map.of(
                    "rpcUrl", validator.rpcUrl().toString(),
                    "websocketUrl", validator.websocketUrl().toString(),
                    "notaryKeypairFile", notarySigner.file.toString(),
                    "custodiedKeysDir", custodiedKeysDir.toString()
                )
            )
        );
    }

    @Test
    public void atomicDvPTest() {
        driver(new DriverParameters().withNotarySpecs(List.of(new NotarySpec(solanaNotaryName, notaryConfig))),
            dsl -> {
                NodeHandle seller = dsl.startNode(new NodeParameters().withProvidedName(sellerName)).get();
                NodeHandle buyer  = dsl.startNode(new NodeParameters().withProvidedName(buyerName)).get();

                seller.getRpc().startFlow(SharesDvP::new, buyer.getNodeInfo().getLegalIdentities().get(0))
                    .getReturnValue().get();
                return null;
            }
        );
    }
}
```
{{% /tab %}}
{{< /tabs >}}

### Setting up Solana accounts in tests

`SolanaTestValidator` exposes account and token management helpers that cover the most common test setup tasks.
Use `validator.accounts()` to airdrop SOL to cover transaction fees, and `validator.tokens()` to create token
mints, associated token accounts, and mint tokens to them:

{{< tabs name="tabs-2" >}}
{{% tab name="Kotlin" %}}
```kotlin
@BeforeEach
fun setupSolana(validator: SolanaTestValidator) {
    val buyerWallet = FileSigner.random(custodiedKeysDir)
    validator.accounts().airdropSol(buyerWallet.publicKey(), 10)

    val stablecoinMint = validator.tokens().createToken(mintAuthority, decimals = 6)
    val buyerTokenAccount = validator.tokens().createAssociatedTokenAccount(
        mintAuthority,
        stablecoinMint,
        buyerWallet.publicKey()
    )
    validator.tokens().mintTo(buyerTokenAccount, stablecoinMint, mintAuthority, amount = 1_000_000)
}
```
{{% /tab %}}
{{% tab name="Java" %}}
```java
@BeforeEach
public void setupSolana(SolanaTestValidator validator) {
    FileSigner buyerWallet = FileSigner.random(custodiedKeysDir);
    validator.accounts().airdropSol(buyerWallet.publicKey(), 10);

    PublicKey stablecoinMint = validator.tokens().createToken(mintAuthority, 6);
    PublicKey buyerTokenAccount = validator.tokens().createAssociatedTokenAccount(
        mintAuthority,
        stablecoinMint,
        buyerWallet.publicKey()
    );
    validator.tokens().mintTo(buyerTokenAccount, stablecoinMint, mintAuthority, 1_000_000);
}
```
{{% /tab %}}
{{< /tabs >}}

## Sample CorDapps

The following sample CorDapps demonstrate how to use the Solana notary in practice. Both use the
[Corda Token SDK](https://github.com/corda/token-sdk) to represent Corda assets as fungible tokens.

* **[Delivery-versus-payment](https://github.com/corda/samples-kotlin/tree/release/ent/4.14/Solana/delivery-vs-payment)**:
  A seller transfers Corda stock tokens to a buyer, while the buyer's Solana stablecoin payment is transferred to the
  seller — atomically, in a single notarisation.

* **[Bridge Authority](https://github.com/corda/samples-kotlin/tree/release/ent/4.14/Solana/bridge-authority)**:
  Demonstrates how Solana bridging can be added to an existing Corda network (in this case the
  [stock pay dividend sample](https://github.com/corda/samples-kotlin/tree/release/ent/4.14/Tokens/stockpaydividend))
  without modification. Only two new participants are needed: a Bridge Authority node, which orchestrates bridging
  and redemption on behalf of token holders, and a Solana notary. The Bridge Authority receives fungible tokens from
  holders, locks them in a pool, and the Solana notary atomically mints the equivalent SPL tokens on Solana.
  Redemption works in reverse — the Solana token holder transfers tokens to a designated redemption account, and the
  Bridge Authority atomically burns them and releases the corresponding Corda tokens.

## Limitations

* **Maximum of 128 output states**: The Solana notary program supports a maximum `StateRef` index of 127 (indices 0–127).
  Output states at index 128 or greater cannot be consumed. **Do not** notarise Corda transactions with more than 128 output
  states. This limit is not currently enforced in the platform.
* **Solana finality**: Notarisation is confirmed when the Solana transaction reaches `CONFIRMED` commitment level.
  Network disruptions affecting the Solana cluster will delay or prevent notarisation.

## Further reading

* [Solana documentation](https://docs.solana.com/)
* [SPL Token program](https://spl.solana.com/token)
* [Token-2022 program](https://spl.solana.com/token-2022)
* [Solana Program Derived Addresses](https://solana.com/docs/core/pda)
* [Solana account rent](https://docs.solana.com/developing/programming-model/accounts#rent)
