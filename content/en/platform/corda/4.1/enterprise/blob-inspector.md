---
aliases:
- /releases/4.1/blob-inspector.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-1:
    identifier: corda-enterprise-4-1-blob-inspector
    parent: corda-enterprise-4-1-serialization-index
    weight: 1050
tags:
- blob
- inspector
title: Blob Inspector
---


# Blob Inspector

There are many benefits to having a custom binary serialisation format (see [Object serialization](serialization.md) for details) but one
disadvantage is the inability to view the contents in a human-friendly manner. The Corda Blob Inspector tool alleviates
this issue by allowing the contents of a binary blob file (or URL end-point) to be output in either YAML or JSON. It
uses `JacksonSupport` to do this (see [JSON](json.md)).

The tool is distributed as part of Corda Enterprise 4.1 in the form of runnable `.jar.` file - `corda-tools-blob-inspector-4.1.jar`.

To run simply pass in the file or URL as the first parameter:

```kotlin
java -jar blob-inspector.jar <file or URL>
```

Use the `--help` flag for a full list of command line options.

When inspecting your custom data structures, there’s no need to include the jars containing the class definitions for them
in the classpath. The blob inspector (or rather the serialization framework) is able to synthesize any classes found in the
blob that aren’t on the classpath.


## Supported formats

The inspector can read **input data** in three formats: raw binary, hex encoded text and base64 encoded text. For instance
if you have retrieved your binary data and it looks like this:

```kotlin
636f7264610100000080c562000000000001d0000030720000000300a3226e65742e636f7264613a38674f537471464b414a5055...
```

then you have hex encoded data. If it looks like this it’s base64 encoded:

```kotlin
Y29yZGEBAAAAgMViAAAAAAAB0AAAMHIAAAADAKMibmV0LmNvcmRhOjhnT1N0cUZLQUpQVWVvY2Z2M1NlU1E9PdAAACc1AAAAAgCjIm5l...
```

And if it looks like something vomited over your screen it’s raw binary. You don’t normally need to care about these
differences because the tool will try every format until it works.

Something that’s useful to know about Corda’s format is that it always starts with the word “corda” in binary. Try
hex decoding 636f726461 using the [online hex decoder tool here](https://convertstring.com/EncodeDecode/HexDecode)
to see for yourself.

**Output data** can be in either a slightly extended form of YaML or JSON. YaML (Yet another markup language) is a bit
easier to read for humans and is the default. JSON can of course be parsed by any JSON library in any language.

{{< note >}}
One thing to note is that the binary blob may contain embedded `SerializedBytes` objects. Rather than printing these
out as a Base64 string, the blob inspector will first materialise them into Java objects and then output those. You will
see this when dealing with classes such as `SignedData` or other structures that attach a signature, such as the
`nodeInfo-*` files or the `network-parameters` file in the node’s directory.

{{< /note >}}

## Example

Here’s what a node-info file from the node’s data directory may look like:


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

Notice the file is actually a serialised `SignedNodeInfo` object, which has a `raw` property of type `SerializedBytes<NodeInfo>`.
This property is materialised into a `NodeInfo` and is output under the `deserialized` field.


## Command-line options

The blob inspector can be started with the following command-line options:

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

`install-shell-extensions`: Install `blob-inspector` alias and auto completion for bash and zsh. See [Shell extensions for CLI Applications](cli-application-shell-extensions.md) for more info.
