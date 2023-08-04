---
date: '2023-08-02'
title: "Façade Definition"
project: corda
version: 'Corda 5.2'
menu:
  corda5:
    identifier: corda5-interop-facade-definition
    parent: corda5-interop-cordapp-api
    weight: 3000
section_menu: corda5
---

# Façade Definition

Façade definition is a text file with minimal semantics consisting of a list of methods with parameters and return
values. The definition is an Interface Definition Language (IDL) oriented for the request/response paradigm with a
common set of data types. The definition of methods/operations in IDL allows abstracting away any programming language
details or ledger details.
Systems wishing to communicate via Façade with each other need to implement its definition. The implementation can be
based on Façade text definition only, with implied simple semantics.
The Façade definition is represented as a JSON document, offering a lightweight way to describe the methods
and their associated parameters and return values. Below we have a simple Façade definition:

```json
{
  "id": "org.corda.interop/platform/tokens/v1.0",
  "aliases": {
    "denomination": "string (org.corda.interop/platform/tokens/types/denomination/1.0)"
  },
  "queries": {
    "getBalance": {
      "in": {
        "denomination": "denomination"
      },
      "out": {
        "balance": "decimal"
      }
    }
  },
  "commands": {
    "reserve-tokens": {
      "in": {
        "denomination": "denomination",
        "amount": "decimal"
      },
      "out": {
        "reservation-ref": "uuid"
      }
    }
  }
}
```

The JSON document consists of the following elements:

- `"id"`: This field represents the fully-qualified name of the Façade and its version. For example,
- "org.example.facade: v1.0" uniquely identifies the Façade.
- `"aliases"`: This section allows defining custom data types with descriptive names. The map consists of keys with
  custom type name, and values which have format of basic type and qualifier name in brackets. In this example a custom type called
  `denomination` is of `string`type and have qualifier `org.corda.interop/platform/tokens/types/denomination/1.0)`.
- `"commands"`: The "commands" section lists the methods supported by the Façade. In this example,
  there's one command named `reserve-tokens`.
- `"in"`: The "in" section of a command or a query lists its input parameters, where each parameter has a descriptive
  name and a type. The type can be a primitive data type like `string`, `decimal`, or `UUID`, or it can refer to a custom
  type defined in the `aliases` section. This allows for a flexible yet expressive way to define the data expected by the
  command. In the example above `reserve-tokens` has to input parameters `denomination`and `amount` of types (respectively)
  `demonomination` and `decimal`. The first type, as non-basic one, is defined in the `aliases` section.
- `"out"`: The "out" section defines the output or return values of a command or a query. Similar to the "in" section,
  the output types can also be primitive or custom types.
- `"queries"`: This section has the same structure as "commands", it defines operations which semantic doesn't mutate
  the state as opposed to "commands". The example contains a single query `getBalance` returning a value as opposed to
  `reserve-tokens` which should also change a state.

Overall, this JSON representation of the Façade definition provides a clear and concise way to specify the interface
that systems can use to communicate with each other.
Implementations of a Façade can be solely based on a JSON definition.
