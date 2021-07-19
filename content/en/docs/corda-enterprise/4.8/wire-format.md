---
date: '2021-07-12'
menu:
  corda-enterprise-4-8:
    parent: corda-enterprise-4-8-node-serialization
tags:
- wire
- format
title: Wire format
weight: 4
---


# Wire format

This document describes the Corda wire format. Use these instructions with an implementation of the AMQP/1.0
specification to read serialized binary messages. AMQP/1.0 implementations include Apache
Qpid Proton and Microsoft AMQP.NET Lite.


## Header

All messages start with the 5-byte sequence `corda` followed by three versioning bytes: major, minor, and encoding.
That means you can’t directly feed a Corda message into an AMQP library. You must check the header string and
then skip it. This is deliberate, to enable other message formats in the future.

The first version byte is set to 1 by default. This indicates the major version of the format. Any other version byte indicates a serialization format that isn't backwards compatible, and you should abort.
The second byte is the minor version. Your code will tolerate this incrementing if it is robust
to unknown data (for example, new schema elements). 
The third byte is an encoding byte. This indicates that new features, such as
compression, are active. You should abort if this isn’t zero.


## AMQP

AMQP/1.0 is a protocol that contains a standardized binary encoding scheme. The scheme is comparable to, but
more advanced than, Google protocol buffers. See the [AMQP specification](https://docs.oasis-open.org/amqp/core/v1.0/os/amqp-core-types-v1.0-os.html)
for a full description of this protocol and encoded examples you can use to understand each byte of a message.

The format specifies encodings for several "primitive" types: numbers, strings, UUIDs, timestamps,
and symbols. You can think of these as enum entries. It also defines the process to encode maps, lists, and arrays. Arrays always contain a single type of element, while lists can contain multiple element types.
An AMQP byte stream is a repeated series of elements.

AMQP goes further than most tagged binary encodings by including the concept of
*described types*. This lets you impose an application-level type system on top of the basic groups of elements
that low-level AMQP gives you. Any element in the stream can be prefixed with a *descriptor*, which is either a string
or a 64-bit value. Both types of label have a defined namespacing mechanism. This labeling scheme allows sophisticated
layering on top of the simple, interoperable core.

AMQP defines a type system and schema representation which allows you to create app-level type layers.
Standard AMQP defines an XML-based schema language as part of the specification, but doesn’t define a way to represent
schemas using AMQP itself.

You can group fields together using *composite types*. A composite type is a
described list in which each list entry is one field of the composite. Use composites to encode language-level
classes, records, structs, and more.

You can also define a *restricted type*. These define a type that is a specialization or subset of
an existing one. For enumerations, you can list the choices in the schema.

You can interpret a serialized message at several levels of detail. If you parse it using the basic AMQP type system, you will get nested lists and maps containing a few basic
types (similar to JSON). If you use descriptors and map those containers to a higher level, you will get more strongly-typed structures.


## Extended AMQP

Standard AMQP contains collections made up of primitives or additional collections, and any element can be labeled with a
string or numeric code. However, it is not self-describing like JSON or XML. Classes map to a list of field contents, but you would need access to the original class code that generated the message to understand the fields.

AMQP’s type system can solve this. However, it has two problems:

* Messages don’t include their own schemas.
* AMQP only defines an XML-based representation for schemas.

It is not best practice to embed XML inside binary formats designed to be digitally signed, so Corda defines a
mapping from the schema notation directly to the AMQP encoding. This makes AMQP messages on Corda self-describing by embedding a
schema for each application or platform-level type that is serialized. The schema provides information such as field names,
annotations, and variables for generic types. You can ignore the schema in many interoperability cases. Its primary function is
to enable version evolution of persisted data structures over time.

## Descriptors

Serialized messages use described types extensively. There are two types of descriptor:

* 64-bit code. In Corda, the top 32 bits are always equal to `0x0000c562`, which is R3’s IANA-assigned enterprise number. The
low bits define elements in our meta-schema—essentially, the way we describe the schemas of other messages.
* Strings. These always start with `net.corda`, followed by either a well-known type name or
a Base64 encoded fingerprint of the underlying schema that was generated from the original class. Strings are
encoded using the AMQP symbol type.

You can use the fingerprint to determine if the serialized message maps precisely to a holder type (class) you already
have in your environment. If you don’t recognize the fingerprint, you may need to examine the schema data to figure out
a reasonable approximate mapping to a type you do have.

The numeric codes are:

* `ENVELOPE`
* `SCHEMA`
* `OBJECT_DESCRIPTOR`
* `FIELD`
* `COMPOSITE_TYPE`
* `RESTRICTED_TYPE`
* `CHOICE`
* `REFERENCED_OBJECT`
* `TRANSFORM_SCHEMA`
* `TRANSFORM_ELEMENT`
* `TRANSFORM_ELEMENT_KEY`

Remember to mask out the top 16 bits first.

In this document, the term “record” means an AMQP list described with one of these numeric codes. A record may represent a logical list of variable length, or a fixed-length list of fields. The term “object” means a list
described by a string or symbolic descriptor that references a schema entry.


## High level format

Every Corda message is, at the top level, an `ENVELOPE` record containing three elements:


* The top-level message, described using a string (symbolic) descriptor.
* A `TRANSFORM_SCHEMA` record. This describes how a data structure has evolved over time,
    making it easier to map to old or new code.
* A `SCHEMA` record. This always contains a single element: a list containing `COMPOSITE_TYPE` records.

Each `COMPOSITE_TYPE` record describes a single app-level type, and contains the members:

* `Name`: A string.
* `Label`: A nullable string. This field is usually null—it exists to match the AMQP specification.
* `Provides`: A list of strings naming Java interfaces that the original type implements. Use it for safe, strongly-typed work with messages generically. Rather than guessing whether a type is meant to be a Foo or Bar based on matching
  with the field names, the schema itself declares what contracts it is intended to meet.
* `Descriptor`: An `OBJECT_DESCRIPTOR` record. It has two elements: a string/symbol and an unsigned long code. Typically, only one is set. This record corresponds to the descriptor that appears in the main message stream.
* `Fields`: A list of `FIELD` records.

 Each *FIELD* record has the following members:

* `Name`: A string.
* `Type`: A Java class name with generic parameters.
* `Requires`: A list of strings.
* `Default`: A nullable string.
* `Label`: A nullable string.
* `Mandatory`: A boolean.
* `Multiple`: A boolean.

See the [AMQP specification](https://docs.oasis-open.org/amqp/core/v1.0/os/amqp-core-types-v1.0-os.html) for a full description of these types.


## Mapping JVM classes to composite types

Corda does not use a separate schema definition language. The source code defines schemas
using regular class definitions in any statically-typed, JVM-bytecode-targeting language. As a result, you may come across types that are only definied in the Corda source code. These definitions are canonical and not
derived from any other kind of schema. Any class annotated as `@CordaSerializable` could appear in an AMQP message.
You don’t need access to the original class files to decode the typed structure of a Corda message, because of the embedded AMQP
schema. You may find it more convenient to work with the original structures using JVM reflection. This is useful for code generators.

Optionally, you can parse the Java `.class` file format using a variety of libraries. It uses a tagged
union-style format and [can be parsed in about 300 lines of C](https://github.com/atcol/cfr/blob/master/src/class.c). The only
part of the class file that is relevant for type information is the parameters for the constructor. Those parameters define which fields
are stored to the wire.

The source code does not have a deterministic field ordering. Developers may re-arrange fields in their classes as they refactor
their code, which in a conventional serialization scheme would break the wire format. When mapping classes to AMQP schemas,
fields are sorted alphabetically. If a new field is added, it will not necessarily appear at the end of the list.


{{< warning >}}
You cannot skip fields when handling format evolution. You must notice if the descriptors have changed from what you expect, and consult the schema to determine how to map the new message
to a schema that you can work with.
{{< /warning >}}



## Containers

AMQP defines encodings for maps and lists, which are mapped to/from `java.util.Map` and `java.util.List` in JVM code. You don’t need
any special support to read these, unless you are interested in the higher-level type system.

In the binary schemas, containers are represented as follows. A field in a composite-type list would look like this:


* `Name`: `“livingIn”`
* `Type`: `“*”`
* `Requires`: `[ “java.util.List<net.corda.tools.serialization.City>” ]`
* `Default`: `NULL`
* `Label`: `NULL`
* `Mandatory`: `true`
* `Multiple`: `false`

The `requires` field is a list of *archetypes*. These are uninterpreted strings that refer to other schema elements that
list the same string in their `provides` field. This implements a form of intersection typing. We use Java-type names
with generics to link the field to the definition of a restricted type.

The list type is defined as a restricted type, like this:

* `Name`: `“java.util.List<net.corda.tools.serialization.City>”`
* `Label`: `NULL`
* `Provides`: `[]`
* `Source`: `“list”`
* `Symbol`: `net.corda:2A8U5kaXW/lD5ns+l0xPFg==`
* `Numeric`: `NULL`
* `Choices`: `[]`


## Signed data

A common pattern in Corda is that an outer wrapper serialized message contains signatures and certificates for an inner
serialized message. The inner message is represented as ‘binary’, requiring two passes to deserialize fully. This works as a security firebreak, because it means you can avoid processing any serialized
data until the signatures have been checked and provenance established. It also helps ensure everyone calculates a
signature over the same binary data without roundtripping.

These types are used for the protocol:

* `net.corda.core.internal.SignedDataWithCert`, descriptor `net.corda:VywzVs/TR8ztvQBpYFpnlQ==`. Fields:
    * raw: `net.corda.core.serialization.SerializedBytes<?>`
    * sig: `net.corda.core.internal.DigitalSignatureWithCert`


* `net.corda.core.internal.DigitalSignatureWithCert`, descriptor `net.corda:AJin3eE1QDfCwTiDWC5hJA==`. Fields:
    * by: `java.security.cert.X509Certificate`
    * bytes: binary



The signature bytes are opaque—their format depends on the cryptographic scheme identified in the X.509 certificate.
For example, elliptic curve signatures use a standardised (non-AMQP) binary format that encodes the coordinates of the
point on the curve. The type `java.security.cert.X509Certificate` does not appear in the schema, it is parsed as a
special case and has the descriptor `net.corda:java.security.cert.X509Certificate`. A field with this descriptor is
of type ‘binary’ and contains a certificate in the standard X.509 binary format (again, not AMQP).


## Examples

The following sample shows how a few lines of Kotlin code defining some sophisticated data structures maps to an AMQP message.

```kotlin
@CordaSerializable
data class Employee(val names: Pair<String, String>)

@CordaSerializable
data class Department(val name: String, val employees: List<Employee>)

@CordaSerializable
data class Company(
        val name: String,
        val createdInYear: Short,
        val logo: OpaqueBytes,
        val departments: List<Department>,
        val historicalEvents: Map<String, Instant>
)
```

Here is an ad-hoc textual representation of what it turns into on the wire. This format is not stable or meaningful.

```kotlin
envelope [
    0. net.corda:XIBlQ9Yl/RlKGLjCMY1/Kg== [
           0. 2014: short
                  0. net.corda:J6fOfvKOUIhpLqSmzN2ecw== [
           1. net.corda:mCdn5Q/6wPrRd120wfv5og== [
                         0. net.corda:KwaBqNRsTDOaXBrYdtDZpw== [
                                       0. net.corda:c0Lkwk4E63sshTPr2G60aQ== [
                                0. net.corda:zjQ3JQXiArQUxXuCcaWANw== [
                                              0. "John"
                                          ]
                                              1. "Doe"
                                   ]
                                       0. net.corda:c0Lkwk4E63sshTPr2G60aQ== [
                                1. net.corda:zjQ3JQXiArQUxXuCcaWANw== [
                                              0. "Jane"
                                          ]
                                              1. "Doe"
                                   ]
                                       0. net.corda:c0Lkwk4E63sshTPr2G60aQ== [
                                2. net.corda:zjQ3JQXiArQUxXuCcaWANw== [
                                              0. "Alice"
                                          ]
                                              1. "Doe"
                                   ]
                            ]
                         1. "Platform"
                     ]
              ]
           2. net.corda:QXkG3ayKZNvF8dIEKbOTSw== {
                  "First lab project proposal email" -> net.corda:java.time.Instant [
                      0. 1411596660: long
                      1. 0: int
                  ]
                  "Hired John" -> net.corda:java.time.Instant [
                      0. 1446552000: long
                      1. 0: int
                  ]
              }
           3. net.corda:pgT0Kc3t/bvnzmgu/nb4Cg== [
                  0. <binary of 1 bytes>
              ]
           4. "R3"
       ]
    1. schema [
           0. [
                  0. composite type [
                         0. "net.corda.tools.serialization.Company"
                         1. NULL
                         2. []
                         3. object descriptor [
                                0. net.corda:XIBlQ9Yl/RlKGLjCMY1/Kg==: symbol
                                1. NULL
                            ]
                         4. [
                                0. field [
                                       0. "createdInYear"
                                       1. "short"
                                       2. []
                                       3. "0"
                                       4. NULL
                                       5. true
                                       6. false
                                   ]
                                1. field [
                                       0. "departments"
                                       1. "*"
                                       2. [
                                              0. "java.util.List<net.corda.tools.serialization.Department>"
                                          ]
                                       3. NULL
                                       4. NULL
                                       5. true
                                       6. false
                                   ]
                                2. field [
                                       0. "historicalEvents"
                                       1. "*"
                                       2. [
                                              0. "java.util.Map<string, java.time.Instant>"
                                          ]
                                       3. NULL
                                       4. NULL
                                       5. true
                                       6. false
                                   ]
                                3. field [
                                       0. "logo"
                                       1. "net.corda.core.utilities.OpaqueBytes"
                                       2. []
                                       3. NULL
                                       4. NULL
                                       5. true
                                       6. false
                                   ]
                                4. field [
                                       0. "name"
                                       1. "string"
                                       2. []
                                       3. NULL
                                       4. NULL
                                       5. true
                                       6. false
                                   ]
                            ]
                     ]
                  1. restricted type [
                         0. "java.util.List<net.corda.tools.serialization.Department>"
                         1. NULL
                         2. []
                         3. "list"
                         4. object descriptor [
                                0. net.corda:mCdn5Q/6wPrRd120wfv5og==: symbol
                                1. NULL
                            ]
                         5. []
                     ]
                  2. composite type [
                         0. "net.corda.tools.serialization.Department"
                         1. NULL
                         2. []
                         3. object descriptor [
                                0. net.corda:J6fOfvKOUIhpLqSmzN2ecw==: symbol
                                1. NULL
                            ]
                         4. [
                                0. field [
                                       0. "employees"
                                       1. "*"
                                       2. [
                                              0. "java.util.List<net.corda.tools.serialization.Employee>"
                                          ]
                                       3. NULL
                                       4. NULL
                                       5. true
                                       6. false
                                   ]
                                1. field [
                                       0. "name"
                                       1. "string"
                                       2. []
                                       3. NULL
                                       4. NULL
                                       5. true
                                       6. false
                                   ]
                            ]
                     ]
                  3. restricted type [
                         0. "java.util.List<net.corda.tools.serialization.Employee>"
                         1. NULL
                         2. []
                         3. "list"
                         4. object descriptor [
                                0. net.corda:KwaBqNRsTDOaXBrYdtDZpw==: symbol
                                1. NULL
                            ]
                         5. []
                     ]
                  4. composite type [
                         0. "net.corda.tools.serialization.Employee"
                         1. NULL
                         2. []
                         3. object descriptor [
                                0. net.corda:zjQ3JQXiArQUxXuCcaWANw==: symbol
                                1. NULL
                            ]
                         4. [
                                0. field [
                                       0. "names"
                                       1. "kotlin.Pair<string, string>"
                                       2. []
                                       3. NULL
                                       4. NULL
                                       5. true
                                       6. false
                                   ]
                            ]
                     ]
                  5. composite type [
                         0. "kotlin.Pair<string, string>"
                         1. NULL
                         2. []
                         3. object descriptor [
                                0. net.corda:c0Lkwk4E63sshTPr2G60aQ==: symbol
                                1. NULL
                            ]
                         4. [
                                0. field [
                                       0. "first"
                                       1. "string"
                                       2. []
                                       3. NULL
                                       4. NULL
                                       5. true
                                       6. false
                                   ]
                                1. field [
                                       0. "second"
                                       1. "string"
                                       2. []
                                       3. NULL
                                       4. NULL
                                       5. true
                                       6. false
                                   ]
                            ]
                     ]
                  6. restricted type [
                         0. "java.util.Map<string, java.time.Instant>"
                         1. NULL
                         2. []
                         3. "map"
                         4. object descriptor [
                                0. net.corda:QXkG3ayKZNvF8dIEKbOTSw==: symbol
                                1. NULL
                            ]
                         5. []
                     ]
                  7. composite type [
                         0. "net.corda.core.utilities.OpaqueBytes"
                         1. NULL
                         2. []
                         3. object descriptor [
                                0. net.corda:pgT0Kc3t/bvnzmgu/nb4Cg==: symbol
                                1. NULL
                            ]
                         4. [
                                0. field [
                                       0. "bytes"
                                       1. "binary"
                                       2. []
                                       3. NULL
                                       4. NULL
                                       5. true
                                       6. false
                                   ]
                            ]
                     ]
              ]
       ]
    2. transform schema {
       }
]
```
