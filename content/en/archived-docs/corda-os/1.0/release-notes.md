---
aliases:
- /releases/release-V1.0/release-notes.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-os-1-0:
    identifier: corda-os-1-0-release-notes
    parent: corda-os-1-0-release-process-index
    weight: 1010
tags:
- release
- notes
title: Release notes
---


# Release notes

Here are release notes for each snapshot release from M9 onwards.


## Unreleased


## Release 1.0

Corda 1.0 is finally here!

This critical step in the Corda journey enables the developer community, clients, and partners to build on Corda with confidence.
Corda 1.0 is the first released version to provide API stability for Corda application (CorDapp) developers.
Corda applications will continue to work against this API with each subsequent release of Corda. The public API for Corda
will only evolve to include new features.

As of Corda 1.0, the following modules export public APIs for which we guarantee to maintain backwards compatibility,
unless an incompatible change is required for security reasons:



* core
Contains the bulk of the APIs to be used for building CorDapps: contracts, transactions, flows, identity, node services,
cryptographic libraries, and general utility functions.
* client-rpc
An RPC client interface to Corda, for use by both UI facing clients and integration with external systems.
* client-jackson
Utilities and serialisers for working with JSON representations of basic types.


Our extensive testing frameworks will continue to evolve alongside future Corda APIs. As part of our commitment to ease of use and modularity
we have introduced a new test node driver module to encapsulate all test functionality in support of building standalone node integration
tests using our DSL driver.

Please read [API](api-index.md) for complete details.

{{< note >}}
it may be necessary to recompile applications against future versions of the API until we begin offering
[ABI (Application Binary Interface)](https://en.wikipedia.org/wiki/Application_binary_interface) stability as well.
We plan to do this soon after this release of Corda.

{{< /note >}}
Significant changes implemented in reaching Corda API stability include:


* **Flow framework**:
The Flow framework communications API has been redesigned around session based communication with the introduction of a new
`FlowSession` to encapsulate the counterparty information associated with a flow.
All shipped Corda flows have been upgraded to use the new *FlowSession*. Please read [API: Flows](api-flows.md) for complete details.
* **Complete API cleanup**:
Across the board, all our public interfaces have been thoroughly revised and updated to ensure a productive and intuitive developer experience.
Methods and flow naming conventions have been aligned with their semantic use to ease the understanding of CorDapps.
In addition, we provide ever more powerful re-usable flows (such as *CollectSignaturesFlow*) to minimize the boiler-plate code developers need to write.
* 
{{< warning >}}**{{< /warning >}}

Simplified annotation driven scanning 
{{< warning >}}**{{< /warning >}}

:
CorDapp configuration has been made simpler through the removal of explicit configuration items in favour of annotations
and classpath scanning. As an example, we have now completely removed the *CordaPluginRegistry* configuration.
Contract definitions are no longer required to explicitly define a legal contract reference hash. In their place an
optional *LegalProseReference* annotation to specify a URI is used.
* **Java usability**:
All code has been updated to enable simple access to static API parameters. Developers no longer need to
call getter methods, and can reference static API variables directly.

In addition to API stability this release encompasses a number of major functional improvements, including:


* **Contract constraints**:
Provides a means with which to enforce a specific implementation of a State’s verify method during transaction verification.
When loading an attachment via the attachment classloader, constraints of a transaction state are checked against the
list of attachment hashes provided, and the attachment is rejected if the constraints are not matched.
* **Signature Metadata support**:
Signers now have the ability to add metadata to their digital signatures. Whereas previously a user could only sign the Merkle root of a
transaction, it is now possible for extra information to be attached to a signature, such as a platform version
and the signature-scheme used.![signatureMetadata](/en/images/signatureMetadata.png "signatureMetadata")

* **Backwards compatibility and improvements to core transaction data structures**:
A new Merkle tree model has been introduced that utilises sub-Merkle trees per component type. Components of the
same type, such as inputs or commands, are grouped together and form their own Merkle tree. Then, the roots of
each group are used as leaves in the top-level Merkle tree. This model enables backwards compatibility, in the
sense that if new component types are added in the future, old clients will still be able to compute the Merkle root
and relay transactions even if they cannot read (deserialise) the new component types. Due to the above,
*FilterTransaction* has been made simpler with a structure closer to *WireTransaction*. This has the effect of making the API
more user friendly and intuitive for both filtered and unfiltered transactions.
* **Enhanced component privacy**:
Corda 1.0 is equipped with a scalable component visibility design based on the above sophisticated
sub-tree model and the introduction of nonces per component. Roughly, an initial base-nonce, the “privacy-salt”,
is used to deterministically generate nonces based on the path of each component in the tree. Because each component
is accompanied by a nonce, we protect against brute force attacks, even against low-entropy components. In addition,
a new privacy feature is provided that allows non-validating notaries to ensure they see all inputs and if there was a
*TimeWindow* in the original transaction. Due to the above, a malicious user cannot selectively hide one or more
input states from the notary that would enable her to bypass the double-spending check. The aforementioned
functionality could also be applied to Oracles so as to ensure all of the commands are visible to them.![subTreesPrivacy](/en/images/subTreesPrivacy.png "subTreesPrivacy")

* **Full support for confidential identities**:
This includes rework and improvements to the identity service to handle both *well known* and *confidential* identities.
This work ships in an experimental module in Corda 1.0, called *confidential-identities*. API stabilisation of confidential
identities will occur as we make the integration of this privacy feature into applications even easier for developers.
* **Re-designed network map service**:
The foundations for a completely redesigned network map service have been implemented to enable future increased network
scalability and redundancy, support for multiple notaries, and administration of network compatibility zones and business networks.

Finally, please note that the 1.0 release has not yet been security audited.

We have provided a comprehensive [Upgrade notes](upgrade-notes.md) to ease the transition of migrating CorDapps to Corda 1.0

Upgrading to this release is strongly recommended, and you will be safe in the knowledge that core APIs will no longer break.

Thank you to all contributors for this release!


## Milestone 14

This release continues with the goal to improve API stability and developer friendliness. There have also been more
bug fixes and other improvements across the board.

The CorDapp template repository has been replaced with a specific repository for
[Java](https://github.com/corda/cordapp-template-java) and [Kotlin](https://github.com/corda/cordapp-template-kotlin)
to improve the experience of starting a new project and to simplify the build system.

It is now possible to specify multiple IP addresses and legal identities for a single node, allowing node operators
more flexibility in setting up nodes.

A format has been introduced for CorDapp JARs that standardises the contents of CorDapps across nodes. This new format
now requires CorDapps to contain their own external dependencies. This paves the way for significantly improved
dependency management for CorDapps with the release of [Jigsaw (Java Modules)](http://openjdk.java.net/projects/jigsaw/). For those using non-gradle build systems it is important
to read [CorDapp Build Systems](cordapp-build-systems.md) to learn more. Those using our `cordformation` plugin simply need to update
to the latest version (`0.14.0`) to get the fixes.

We’ve now begun the process of demarcating which classes are part of our public API and which ones are internal.
Everything found in `net.corda.core.internal` and other packages in the `net.corda` namespace which has `.internal` in it are
considered internal and not for public use. In a future release any CorDapp using these packages will fail to load, and
when we migrate to Jigsaw these will not be exported.

The transaction finalisation flow (`FinalityFlow`) has had hooks added for alternative implementations, for example in
scenarios where no single participant in a transaction is aware of the well known identities of all parties.

DemoBench has a fix for a rare but inconvenient crash that can occur when sharing your display across multiple devices,
e.g. a projector while performing demonstrations in front of an audience.

Guava types are being removed because Guava does not have backwards compatibility across versions, which has serious
issues when multiple libraries depend on different versions of the library.

The identity service API has been tweaked, primarily so anonymous identity registration now takes in
AnonymousPartyAndPath rather than the individual components of the identity, as typically the caller will have
an AnonymousPartyAndPath instance. See change log for further detail.

Upgrading to this release is strongly recommended in order to keep up with the API changes, removal and additions.


## Milestone 13

Following our first public beta in M12, this release continues the work on API stability and user friendliness. Apart
from bug fixes and code refactoring, there are also significant improvements in the Vault Query and the
Identity Service (for more detailed information about what has changed, see [Changelog](changelog.md)).
More specifically:

The long awaited new **Vault Query** service makes its debut in this release and provides advanced vault query
capabilities using criteria specifications (see `QueryCriteria`), sorting, and pagination. Criteria specifications
enable selective filtering with and/or composition using multiple operator primitives on standard attributes stored in
Corda internal vault tables (eg. vault_states, vault_fungible_states, vault_linear_states), and also on custom contract
state schemas defined by CorDapp developers when modelling new contract types. Custom queries are specifiable using a
simple but sophisticated builder DSL (see `QueryCriteriaUtils`). The new Vault Query service is usable by flows and by
RPC clients alike via two simple API functions: `queryBy()` and `trackBy()`. The former provides point-in-time
snapshot queries whilst the later supplements the snapshot with dynamic streaming of updates.
See [API: Vault Query](api-vault-query.md) for full details.

We have written a comprehensive Hello, World! tutorial, showing developers how to build a CorDapp from start
to finish. The tutorial shows how the core elements of a CorDapp - states, contracts and flows - fit together
to allow your node to handle new business processes. It also explains how you can use our contract and
flow testing frameworks to massively reduce CorDapp development time.

Certificate checks have been enabled for much of the identity service. These are part of the confidential (anonymous)
identities work, and ensure that parties are actually who they claim to be by checking their certificate path back to
the network trust root (certificate authority).

To deal with anonymized keys, we’ve also implemented a deterministic key derivation function that combines logic
from the HMAC-based Extract-and-Expand Key Derivation Function (HKDF) protocol and the BIP32 hardened
parent-private-key -> child-private-key scheme. This function currently supports the following algorithms:
ECDSA secp256K1, ECDSA secpR1 (NIST P-256) and EdDSA ed25519. We are now very close to fully supporting anonymous
identities so as to increase privacy even against validating notaries.

We have further tightened the set of objects which Corda will attempt to serialise from the stack during flow
checkpointing. As flows are arbitrary code in which it is convenient to do many things, we ended up pulling in a lot of
objects that didn’t make sense to put in a checkpoint, such as `Thread` and `Connection`. To minimize serialization
cost and increase security by not allowing certain classes to be serialized, we now support class blacklisting
that will return an `IllegalStateException` if such a class is encountered during a checkpoint. Blacklisting supports
superclass and superinterface inheritance and always precedes `@CordaSerializable` annotation checking.

We’ve also started working on improving user experience when searching, by adding a new RPC to support fuzzy matching
of X.500 names.


## Milestone 12 - First Public Beta

One of our busiest releases, lots of changes that take us closer to API stability (for more detailed information about
what has changed, see [Changelog](changelog.md)). In this release we focused mainly on making developers’ lives easier. Taking
into account feedback from numerous training courses and meet-ups, we decided to add `CollectSignaturesFlow` which
factors out a lot of code which CorDapp developers needed to write to get their transactions signed.
The improvement is up to 150 fewer lines of code in each flow! To have your transaction signed by different parties, you
need only now call a subflow which collects the parties’ signatures for you.

Additionally we introduced classpath scanning to wire-up flows automatically. Writing CorDapps has been made simpler by
removing boiler-plate code that was previously required when registering flows. Writing services such as oracles has also been simplified.

We made substantial RPC performance improvements (please note that this is separate to node performance, we are focusing
on that area in future milestones):


* 15-30k requests per second for a single client/server RPC connection.
* 1Kb requests, 1Kb responses, server and client on same machine, parallelism 8, measured on a Dell XPS 17(i7-6700HQ, 16Gb RAM)
* The framework is now multithreaded on both client and server side.
* All remaining bottlenecks are in the messaging layer.

Security of the key management service has been improved by removing support for extracting private keys, in order that
it can support use of a hardware security module (HSM) for key storage. Instead it exposes functionality for signing data
(typically transactions). The service now also supports multiple signature schemes (not just EdDSA).

We’ve added the beginnings of flow versioning. Nodes now reject flow requests if the initiating side is not using the same
flow version. In a future milestone release will add the ability to support backwards compatibility.

As with the previous few releases we have continued work extending identity support. There are major changes to the `Party`
class as part of confidential identities, and how parties and keys are stored in transaction state objects.
See [Changelog](changelog.md) for full details.

Added new Byzantine fault tolerant (BFT) decentralised notary demo, based on the [BFT-SMaRT protocol](https://bft-smart.github.io/library/)
For how to run the demo see: [Notary demo](running-the-demos.md#notary-demo)

We continued to work on tools that enable diagnostics on the node. The newest addition to Corda Shell is `flow watch` command which
lets the administrator see all flows currently running with result or error information as well as who is the flow initiator.
Here is the view from DemoBench:

![flowWatchCmd](/en/images/flowWatchCmd.png "flowWatchCmd")
We also started work on the strategic wire format (not integrated).


## Milestone 11

Special thank you to [Gary Rowe](https://github.com/gary-rowe) for his contribution to Corda’s Contracts DSL in M11.

Work has continued on confidential identities, introducing code to enable the Java standard libraries to work with
composite key signatures. This will form the underlying basis of future work to standardise the public key and signature
formats to enable interoperability with other systems, as well as enabling the use of composite signatures on X.509
certificates to prove association between transaction keys and identity keys.

The identity work will require changes to existing code and configurations, to replace party names with full X.500
distinguished names (see RFC 1779 for details on the construction of distinguished names). Currently this is not
enforced, however it will be in a later milestone.


* “myLegalName” in node configurations will need to be replaced, for example “Bank A” is replaced with
“CN=Bank A,O=Bank A,L=London,C=GB”. Obviously organisation, location and country (“O”, “L” and “C” respectively)
must be given values which are appropriate to the node, do not just use these example values.
* “networkMap” in node configurations must be updated to match any change to the legal name of the network map.
* If you are using mock parties for testing, try to standardise on the `DUMMY_NOTARY`, `DUMMY_BANK_A`, etc. provided
in order to ensure consistency.

We anticipate enforcing the use of distinguished names in node configurations from M12, and across the network from M13.

We have increased the maximum message size that we can send to Corda over RPC from 100 KB to 10 MB.

The Corda node now disables any use of ObjectInputStream to prevent Java deserialisation within flows. This is a security fix,
and prevents the node from deserialising arbitrary objects.

We’ve introduced the concept of platform version which is a single integer value which increments by 1 if a release changes
any of the public APIs of the entire Corda platform. This includes the node’s public APIs, the messaging protocol,
serialisation, etc. The node exposes the platform version it’s on and we envision CorDapps will use this to be able to
run on older versions of the platform to the one they were compiled against. Platform version borrows heavily from Android’s
API Level.

We have revamped the DemoBench user interface. DemoBench will now also be installed as “Corda DemoBench” for both Windows
and MacOSX. The original version was installed as just “DemoBench”, and so will not be overwritten automatically by the
new version.


## Milestone 10

Special thank you to [Qian Hong](https://github.com/fracting), [Marek Skocovsky](https://github.com/marekdapps),
[Karel Hajek](https://github.com/polybioz), and [Jonny Chiu](https://github.com/johnnyychiu) for their contributions
to Corda in M10.

A new interactive **Corda Shell** has been added to the node. The shell lets developers and node administrators
easily command the node by running flows, RPCs and SQL queries. It also provides a variety of commands to monitor
the node. The Corda Shell is based on the popular [CRaSH project](http://www.crashub.org/) and new commands can
be easily added to the node by simply dropping Groovy or Java files into the node’s `shell-commands` directory.
We have many enhancements planned over time including SSH access, more commands and better tab completion.

The new “DemoBench” makes it easy to configure and launch local Corda nodes. It is a standalone desktop app that can be
bundled with its own JRE and packaged as either EXE (Windows), DMG (MacOS) or RPM (Linux-based). It has the following
features:



* New nodes can be added at the click of a button. Clicking “Add node” creates a new tab that lets you edit the most
important configuration properties of the node before launch, such as its legal name and which CorDapps will be loaded.
* Each tab contains a terminal emulator, attached to the pseudoterminal of the node. This lets you see console output.
* You can launch an Corda Explorer instance for each node at the click of a button. Credentials are handed to the Corda
Explorer so it starts out logged in already.
* Some basic statistics are shown about each node, informed via the RPC connection.
* Another button launches a database viewer in the system browser.
* The configurations of all running nodes can be saved into a single `.profile` file that can be reloaded later.


Soft Locking is a new feature implemented in the vault to prevent a node constructing transactions that attempt to use the
same input(s) simultaneously. Such transactions would result in naturally wasted effort when the notary rejects them as
double spend attempts. Soft locks are automatically applied to coin selection (eg. cash spending) to ensure that no two
transactions attempt to spend the same fungible states.

The basic Amount API has been upgraded to have support for advanced financial use cases and to better integrate with
currency reference data.

We have added optional out-of-process transaction verification. Any number of external verifier processes may be attached
to the node which can handle loadbalanced verification requests.

We have also delivered the long waited Kotlin 1.1 upgrade in M10! The new features in Kotlin allow us to write even more
clean and easy to manage code, which greatly increases our productivity.

This release contains a large number of improvements, new features, library upgrades and bug fixes. For a full list of
changes please see [Changelog](changelog.md).


## Milestone 9

This release focuses on improvements to resiliency of the core infrastructure, with highlights including a Byzantine
fault tolerant (BFT) decentralised notary, based on the BFT-SMaRT protocol and isolating the web server from the
Corda node.

With thanks to open source contributor Thomas Schroeter for providing the BFT notary prototype, Corda can now resist
malicious attacks by members of a distributed notary service. If your notary service cluster has seven members, two can
become hacked or malicious simultaneously and the system continues unaffected! This work is still in development stage,
and more features are coming in the next snapshot!

The web server has been split out of the Corda node as part of our ongoing hardening of the node. We now provide a Jetty
servlet container pre-configured to contact a Corda node as a backend service out of the box, which means individual
webapps can have their REST APIs configured for the specific security environment of that app without affecting the
others, and without exposing the sensitive core of the node to malicious Javascript.

We have launched a global training programme, with two days of classes from the R3 team being hosted in London, New York
and Singapore. R3 members get 5 free places and seats are going fast, so sign up today.

We’ve started on support for confidential identities, based on the key randomisation techniques pioneered by the Bitcoin
and Ethereum communities. Identities may be either anonymous when a transaction is a part of a chain of custody, or fully
legally verified when a transaction is with a counterparty. Type safety is used to ensure the verification level of a
party is always clear and avoid mistakes. Future work will add support for generating new identity keys and providing a
certificate path to show ownership by the well known identity.

There are even more privacy improvements when a non-validating notary is used; the Merkle tree algorithm is used to hide
parts of the transaction that a non-validating notary doesn’t need to see, whilst still allowing the decentralised
notary service to sign the entire transaction.

The serialisation API has been simplified and improved. Developers now only need to tag types that will be placed in
smart contracts or sent between parties with a single annotation… and sometimes even that isn’t necessary!

Better permissioning in the cash CorDapp, to allow node users to be granted different permissions depending on whether
they manage the issuance, movement or ledger exit of cash tokens.

We’ve continued to improve error handling in flows, with information about errors being fed through to observing RPC
clients.

There have also been dozens of bug fixes, performance improvements and usability tweaks. Upgrading is definitely
worthwhile and will only take a few minutes for most apps.

For a full list of changes please see [Changelog](changelog.md).

