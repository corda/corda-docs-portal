---
date: '2026-02-25T00:00:00Z'
menu:
  corda-enterprise-4-14:
    identifier: corda-enterprise-4-14-solana-notary
    parent: corda-enterprise-4-14-notaries
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

The notary program (`notary95bwkGXj74HV2CXeCn4CgBzRVv5nmEVfqonVY`) runs on Solana and is administered by R3 Ltd.
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
The Solana notary program is administered exclusively by R3 Ltd. Contact R3 to have your notary key authorized for
both mainnet and devnet.
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
2. **Notary authorization**: Your notary's Solana public key must be authorized by R3 Ltd in the Solana notary program.
3. **Solana RPC access**: The notary node requires HTTP and WebSocket access to a [Solana RPC endpoint](https://solana.com/rpc).
4. **Program whitelist agreement**: Agree with your network participants which Solana programs may be invoked via
notary instructions. By default, the SPL Token and Token-2022 programs are whitelisted.

## Configuration

The Solana notary is configured with the `notary.solana` block.

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

### Configuration reference

#### `rpcUrl`

*Required*

HTTP RPC URL of the Solana cluster.

*Example:* `https://api.mainnet-beta.solana.com`

#### `websocketUrl`

*Required*

WebSocket URL of the Solana cluster.

*Example:* `wss://api.mainnet-beta.solana.com`

#### `notaryKeypairFile`

*Required*

Path to the Solana keypair file for the notary account. This account must be pre-authorized by R3 and must hold
sufficient SOL to cover transaction fees and account rent.

#### `custodiedKeysDir`

*Optional*

Path to a directory containing Solana keypair files for accounts whose signatures the notary will provide on behalf
of participants. Changes to the directory are picked up automatically. Must not contain the notary keypair itself.

*Default:* not set

#### `programWhitelist`

*Optional*

List of Solana program IDs (base58-encoded) permitted to appear in notary instructions. If omitted, defaults to the
SPL Token and Token-2022 programs. Provide an empty list to disallow all programs (any notary instructions will be
rejected).

*Default:* SPL Token (`TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA`) and Token-2022
(`TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb`)

#### `trustedCordaSigners`

*Optional*

List of Corda X.500 party names whose signatures are accepted as authorization for transactions containing Solana
instructions. When this list is non-empty, the notary verifies that any transaction carrying a `SolanaInstruction`
is signed by at least one of the listed parties. If the list is empty, no such check is performed.

*Default:* empty (no restriction)

#### `defaultRpcRateLimit`

*Optional*

Default rate limit in requests per second applied to each RPC method. Used when no method-specific limit is
configured in `rpcSpecificRateLimits`.

*Default:* derived from `threadPoolSize`

#### `rpcSpecificRateLimits`

*Optional*

Per-method rate limits (requests per second) that override `defaultRpcRateLimit`. Keys are Solana RPC method names.
The `sendTransaction` method is the bottleneck in the notarisation flow; its rate limit determines the maximum
notarisation throughput.

*Default:* not set

#### `threadPoolSize`

*Optional*

Number of threads used to process notarisation requests and make Solana RPC calls. If omitted, the value is derived
in order from: the `sendTransaction` rate limit, `defaultRpcRateLimit`, or a fallback of 10.

*Default:* derived from `sendTransaction` rate limit, then `defaultRpcRateLimit`, then 10

### Program whitelist

The program whitelist is a security control that restricts which Solana programs can be invoked through notary
instructions. Any `SolanaInstruction` referencing a program ID not in the whitelist is rejected before the Solana
transaction is submitted.

Configure the whitelist to include only the programs that your network participants have agreed to use. Accepting
instructions for unknown programs could allow malicious actors to execute arbitrary Solana operations as a side
effect of notarisation.

### Trusted Corda signers

When `trustedCordaSigners` is configured, the notary requires that any Corda transaction containing
`SolanaInstruction`s carries a valid signature from at least one of the listed parties. This provides an additional
layer of authorization: only transactions approved by a recognized party trigger Solana-side execution.

If `trustedCordaSigners` is empty (the default), any Corda transaction may include Solana instructions, subject only
to the program whitelist check.

### Rate limiting and thread pool sizing

Solana RPC providers impose rate limits on their endpoints. Configure `defaultRpcRateLimit` and
`rpcSpecificRateLimits` to match your RPC provider's limits. The `sendTransaction` method is particularly important:
if its rate limit is lower than other methods, Solana transactions may expire while waiting to be sent, leading to
retries and reduced throughput.

The `threadPoolSize` setting controls concurrency — higher values allow more notarisation requests to be processed
in parallel, but should not exceed the rate limits of the RPC provider.

## Solana account costs

Each notarised Corda transaction creates one or more `CordaTxAccount` PDAs on Solana. These accounts require
[deposit or "rent"](https://docs.solana.com/developing/programming-model/accounts#rent) to be paid in SOL by the notary
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

## Limitations

* **Maximum of 128 output states**: The Solana notary program supports a maximum `StateRef` index of 127 (indices 0–127).
  Output states at index 128 or greater cannot be consumed. Do not notarise Corda transactions with more than 128 output
  states. This limit is not currently enforced in the platform.
* **Solana finality**: Notarisation is confirmed when the Solana transaction reaches `CONFIRMED` commitment level.
  Network disruptions affecting the Solana cluster will delay or prevent notarisation.

## Sample CorDapps

The following sample CorDapps demonstrate how to use the Solana notary in practice. Both use the
[Corda Token SDK](https://github.com/corda/token-sdk) to represent Corda assets as fungible tokens.

* **[Delivery-versus-payment](https://github.com/corda/samples-kotlin/tree/release/ent/4.14/Solana/delivery-vs-payment)**:
  A seller transfers Corda stock tokens to a buyer, while the buyer's Solana stablecoin payment is transferred to the
  seller — atomically, in a single notarisation.

* **[Bridge token](https://github.com/corda/samples-kotlin/tree/release/ent/4.14/Solana/bridge-token)**:
  Demonstrates bridging Corda Token SDK fungible tokens to a Solana SPL token representation and back. A Bridge
  Authority node orchestrates the process: the Corda tokens are transferred to the Bridge Authority (which holds
  them in a pool), and the Solana notary atomically mints the equivalent SPL tokens on Solana. Redemption works in
  reverse — the holder burns the Solana tokens, and the Bridge Authority releases the corresponding Corda tokens.

## Further reading

* [Solana documentation](https://docs.solana.com/)
* [SPL Token program](https://spl.solana.com/token)
* [Token-2022 program](https://spl.solana.com/token-2022)
* [Solana Program Derived Addresses](https://solana.com/docs/core/pda)
* [Solana account rent](https://docs.solana.com/developing/programming-model/accounts#rent)
