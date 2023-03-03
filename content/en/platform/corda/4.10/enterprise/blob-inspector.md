---
date: '2021-07-15'
menu:
  corda-enterprise-4-10:
    parent: corda-enterprise-4-10-corda-nodes-operating
tags:
- blob
- inspector
title: Blob Inspector
weight: 100
---


# Blob inspector

The Corda blob inspector tool gives you a human-readable view of content stored in a [custom binary serialization format](serialization.md).
The blob inspector shows you the output of binary blob files (or URL end-points) in YAML or JSON using `JacksonSupport` (see [JSON](json.md) for more on Jackson serialization).

The tool is distributed as a `.jar.` file - `corda-tools-blob-inspector-4.10.jar`. To run it, pass in the file or URL as the first parameter:

```kotlin
java -jar corda-tools-blob-inspector-4.10.jar <file or URL>
```


Use the `--help` flag for a full list of command line options.

The serialization framework can synthesize any classes found in the blob that are not on the classpath. That means you don't need to include the JARs containing the class definitions when inspecting your custom data structures.


## Supported formats

The inspector can read **input data** in three formats: raw binary, hex encoded text, and Base64 encoded text. The tool will try each format until one works.

You may find it useful to know that Corda’s format always starts with the word “corda” in binary. Try
hex decoding 636f726461 using the [online hex decoder tool](https://convertstring.com/EncodeDecode/HexDecode)
to see for yourself.

**Output data** can be in either a slightly extended form of YAML or JSON. YAML (Yet another Markup Language) is
easier for humans to read, and is the default. JSON can be parsed by any JSON library in any language.

{{< note >}}
The binary blob may contain embedded `SerializedBytes` objects. Rather than printing these
out as a Base64 string, the blob inspector first materializes them into Java objects, then outputs those. You will
see this when dealing with classes such as `SignedData` or other structures that attach a signature, such as the
`nodeInfo-*` files or the `network-parameters` file in the node’s directory.

{{< /note >}}

## Example

Here’s what a `node-info` file from the node’s data directory may look like:


* YAML:

```none
net.corda.nodeapi.internal.SignedNodeInfo
---
raw:
  class: "net.corda.core.node.NodeInfo"
  deserialized:
    addresses:
    - "localhost:10005"
    legalIdentitiesAndCerts:
    - "O=BankOfCorda, L=London, C=GB"
    platformVersion: 4
    serial: 1527851068715
signatures:
- !!binary |-
  VFRy4frbgRDbCpK1Vo88PyUoj01vbRnMR3ROR2abTFk7yJ14901aeScX/CiEP+CDGiMRsdw01cXt\nhKSobAY7Dw==
```


* JSON:

```none
net.corda.nodeapi.internal.SignedNodeInfo
{
  "raw" : {
    "class" : "net.corda.core.node.NodeInfo",
    "deserialized" : {
      "addresses" : [ "localhost:10005" ],
      "legalIdentitiesAndCerts" : [ "O=BankOfCorda, L=London, C=GB" ],
      "platformVersion" : 4,
      "serial" : 1527851068715
    }
  },
  "signatures" : [ "VFRy4frbgRDbCpK1Vo88PyUoj01vbRnMR3ROR2abTFk7yJ14901aeScX/CiEP+CDGiMRsdw01cXthKSobAY7Dw==" ]
}
```

Notice the file is actually a serialized `SignedNodeInfo` object, which has a `raw` property of type `SerializedBytes<NodeInfo>`.
This property is materialized into `NodeInfo` and is output under the `deserialized` field.


## Classpath

If you run the blob inspector without any JAR files on the classpath, then it will deserialize objects using the class carpenter, (see [Object serialization](serialization.md)).
This happens because the types are not available, so the serialization framework has to synthesize them.

{{< note >}}
If the serialized blob contains an `enum`, you will get this exception `java.lang.NoClassDefFoundError: Could not initialize class _YourEnum_`.
To solve this known issue, add the JAR file that contains the `enum` to the classpath of the blob inspector.

{{< /note >}}

## Command-line options

You can start the blob inspector with the following command line options:

```shell
blob-inspector [-hvV] [--full-parties] [--schema] [--format=type]
               [--input-format=type] [--logging-level=<loggingLevel>] SOURCE
               [COMMAND]
```


* `--format=type`: Output format. Possible values: [YAML, JSON]. Default: YAML.
* `--input-format=type`: Input format. If the file can’t be decoded with the given value it’s auto-detected, so you should
never normally need to specify this. Possible values [BINARY, HEX, BASE64]. Default: BINARY.
* `--full-parties`: Display the owningKey and certPath properties of Party and PartyAndReference objects respectively.
* `--schema`: Print the blob’s schema first.
* `--verbose`, `--log-to-console`, `-v`: If set, prints logging to the console as well as to a file.
* `--logging-level=<loggingLevel>`: Enable logging at this level and higher. Possible values: ERROR, WARN, INFO, DEBUG, TRACE. Default: INFO.
* `--help`, `-h`: Show this help message and exit.
* `--version`, `-V`: Print version information and exit.


### Sub-commands

`install-shell-extensions`: Install `blob-inspector` alias and auto-completion for bash and zsh. See [Shell extensions for CLI Applications](node/operating/cli-application-shell-extensions.md).
