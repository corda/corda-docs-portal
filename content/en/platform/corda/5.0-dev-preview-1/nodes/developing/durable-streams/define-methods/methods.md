---
title: "Defining durable stream methods"
date: '2021-09-16'
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-nodes-developing-durable-streams
    identifier: corda-5-dev-preview-1-nodes-developing-durable-streams-methods
    weight: 3200
section_menu: corda-5-dev-preview
description: >
  How to define durable stream methods.
---

The durable stream method is a special type of `RPCOps` method and returns either:
* `DurableCursorBuilder` for infinite streams (streams that have no end).
* `FiniteDurableCursorBuilder` for finite streams (streams which end). For example, a chronologically ordered set of transactions for a given business day in the past.

## Define infinite durable streams

Use `NumberSequencesRPCOps` in your durable query polling requests for infinite streams.

Here is an `RPCOps` interface definition for a simple durable stream operation which will produce an infinite
stream of: `"Two"`, `"Four"`, `"Six"`, `...` if `NumberTypeEnum.EVEN` is passed as an input parameter:

```kotlin
@CordaSerializable
enum class NumberTypeEnum {
    EVEN, ODD
}

@HttpRpcResource("...")
interface NumberSequencesRPCOps : RPCOps {
    @HttpRpcPOST
    fun retrieve(type: NumberTypeEnum): DurableCursorBuilder<String>
}
```

{{< note >}}
As shown in the example, you don't need to include any HTTP-RPC annotations specific to durable streams.
{{< /note >}}

The OpenAPI definition generated from this method shows the POST HTTP method `/numberseq/retrieve` takes in the request
body of type `NumberseqRetrieveRequest` and (for successful requests) replies with the JSON construct
`DurableReturnResult_of_String`:

```json
{
  "openapi" : "3.0.1",
  "paths" : {
    "/numberseq/retrieve" : {
      "post" : {
        "tags" : [ "net.corda.extensions.node.rpc.NumberSequencesRPCOps" ],
        "description" : "",
        "operationId" : "post_numberseq_retrieve",
        "parameters" : [ ],
        "requestBody" : {
          "description" : "requestBody",
          "content" : {
            "application/json" : {
              "schema" : {
                "$ref" : "#/components/schemas/NumberseqRetrieveRequest"
              }
            }
          },
          "required" : true
        },
        "responses" : {
          "200" : {
            "description" : "Success.",
            "content" : {
              "application/json" : {
                "schema" : {
                  "$ref" : "#/components/schemas/DurableReturnResult_of_String"
                }
              }
            }
          }
        }
      }
    }
  },
  "components" : {
    "schemas" : {
      "DurableReturnResult_of_String" : {
        "required" : [ "positionedValues" ],
        "type" : "object",
        "properties" : {
          "positionedValues" : {
            "uniqueItems" : false,
            "type" : "array",
            "nullable" : false,
            "items" : {
              "type" : "object",
              "properties" : {
                "position" : {
                  "type" : "integer",
                  "format" : "int64",
                  "nullable" : false,
                  "example" : 0
                },
                "value" : {
                  "type" : "string",
                  "nullable" : false,
                  "example" : "string"
                }
              },
              "nullable" : false,
              "example" : "No example available for this type"
            }
          },
          "remainingElementsCountEstimate" : {
            "type" : "integer",
            "format" : "int64",
            "nullable" : true,
            "example" : 0
          }
        },
        "nullable" : false
      },
      "DurableStreamContext" : {
        "required" : [ "awaitForResultTimeout", "currentPosition", "maxCount" ],
        "type" : "object",
        "properties" : {
          "awaitForResultTimeout" : {
            "type" : "string",
            "format" : "duration",
            "nullable" : false,
            "example" : "PT15M"
          },
          "currentPosition" : {
            "type" : "integer",
            "format" : "int64",
            "nullable" : false,
            "example" : 0
          },
          "maxCount" : {
            "type" : "integer",
            "format" : "int32",
            "nullable" : false,
            "example" : 0
          }
        },
        "description" : "",
        "nullable" : false
      },
      "NumberseqRetrieveRequest" : {
        "required" : [ "context", "type" ],
        "properties" : {
          "type" : {
            "description" : "",
            "nullable" : false,
            "example" : "ODD",
            "enum" : [ "EVEN", "ODD" ]
          },
          "context" : {
            "$ref" : "#/components/schemas/DurableStreamContext"
          }
        },
        "description" : "NumberseqRetrieveRequest",
        "nullable" : false
      }
    }
  }
}
```

The OpenAPI definition of `NumberseqRetrieveRequest` includes `DurableStreamContext`:

```json
      {
        "required" : [ "context", "type" ],
        "properties" : {
          "type" : {
            "description" : "",
            "nullable" : false,
            "example" : "ODD",
            "enum" : [ "EVEN", "ODD" ]
          },
          "context" : {
            "$ref" : "#/components/schemas/DurableStreamContext"
          }
        },
        "description" : "NumberseqRetrieveRequest",
        "nullable" : false
      }
```

`DurableStreamContext` specifies:
* From which position elements should be served.
* How many elements the client should receive.
* How long the call may wait (block) on the server side for elements to become available.

{{< note >}}
`DurableStreamContext` is not specific to this method. It is a mandatory, complex parameter which HTTP-RPC clients
**must** pass with every call.

Read [how to implement durable streams on the server](../../../../../../../../en/platform/corda/5.0-dev-preview-1/nodes/developing/durable-streams/implement-server/implement-server.md) for more information on using `DurableStreamContext`.
{{< /note >}}

If the request is successful, the HTTP-RPC server will reply with `DurableReturnResult_of_String`,
which is an array of pairs where every `String` element (representing the payload: `"Two"`, `"Four"`, `"Six"`, `...`)
is coupled with its `int64` position value.

The server also provides `remainingElementsCountEstimate`, which tells the client if it should continue polling and how
frequently.

## Define finite durable streams

Finite durable streams have all the characteristics of [infinite durable streams](#define-infinite-durable-streams), however,
they have an extended ability to tell the HTTP-RPC client that the end of the stream has been reached and it can stop
[polling](../../../../../../../../en/platform/corda/5.0-dev-preview-1/nodes/developing/durable-streams/durable-streams-homepage.html#polling-requests).

Here is an `RPCOps` interface definition for a finite durable stream:

```kotlin
@HttpRpcResource("...")
interface CalendarRPCOps : RPCOps {

    @CordaSerializable
    data class CalendarDay(val dayOfWeek: DayOfWeek, val dayOfYear: String)

    @HttpRpcPOST
    fun daysOfTheYear(year: Int): FiniteDurableCursorBuilder<CalendarDay>
}
```

In this example, the value for `dayOfYear` could be `29-Jul-2021`.

The OpenAPI definition generated from this method is very similar to that for an [infinite durable stream method](#define-infinite-durable-streams).
However, `isLastResult` is now present for `FiniteDurableReturnResult_of_CalendarDay`:

```json
{
  "openapi" : "3.0.1",
  "paths" : {
    "/calendar/daysoftheyear" : {
      "post" : {
        "tags" : [ "net.corda.extensions.node.rpc.CalendarRPCOps" ],
        "description" : "",
        "operationId" : "post_calendar_daysoftheyear",
        "parameters" : [ ],
        "requestBody" : {
          "description" : "requestBody",
          "content" : {
            "application/json" : {
              "schema" : {
                "$ref" : "#/components/schemas/CalendarDaysoftheyearRequest"
              }
            }
          },
          "required" : true
        },
        "responses" : {
          "200" : {
            "description" : "Success.",
            "content" : {
              "application/json" : {
                "schema" : {
                  "$ref" : "#/components/schemas/FiniteDurableReturnResult_of_CalendarDay"
                }
              }
            }
          }
        }
      }
    }
  },
  "components" : {
    "schemas" : {
      "CalendarDay" : {
        "required" : [ "dayOfWeek", "dayOfYear" ],
        "type" : "object",
        "properties" : {
          "dayOfWeek" : {
            "nullable" : false,
            "example" : "TUESDAY",
            "enum" : [ "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY" ]
          },
          "dayOfYear" : {
            "type" : "string",
            "nullable" : false,
            "example" : "string"
          }
        },
        "nullable" : false
      },
      "FiniteDurableReturnResult_of_CalendarDay" : {
        "required" : [ "isLastResult", "positionedValues" ],
        "type" : "object",
        "properties" : {
          "isLastResult" : {
            "type" : "boolean",
            "nullable" : false,
            "example" : true
          },
          "positionedValues" : {
            "uniqueItems" : false,
            "type" : "array",
            "nullable" : false,
            "items" : {
              "type" : "object",
              "properties" : {
                "position" : {
                  "type" : "integer",
                  "format" : "int64",
                  "nullable" : false,
                  "example" : 0
                },
                "value" : {
                  "$ref" : "#/components/schemas/CalendarDay"
                }
              },
              "nullable" : false,
              "example" : "No example available for this type"
            }
          },
          "remainingElementsCountEstimate" : {
            "type" : "integer",
            "format" : "int64",
            "nullable" : true,
            "example" : 0
          }
        },
        "nullable" : false
      },
      "DurableStreamContext" : {
        "required" : [ "awaitForResultTimeout", "currentPosition", "maxCount" ],
        "type" : "object",
        "properties" : {
          "awaitForResultTimeout" : {
            "type" : "string",
            "format" : "duration",
            "nullable" : false,
            "example" : "PT15M"
          },
          "currentPosition" : {
            "type" : "integer",
            "format" : "int64",
            "nullable" : false,
            "example" : 0
          },
          "maxCount" : {
            "type" : "integer",
            "format" : "int32",
            "nullable" : false,
            "example" : 0
          }
        },
        "description" : "",
        "nullable" : false
      },
      "CalendarDaysoftheyearRequest" : {
        "required" : [ "context", "year" ],
        "properties" : {
          "year" : {
            "type" : "integer",
            "description" : "",
            "format" : "int32",
            "nullable" : false,
            "example" : 0
          },
          "context" : {
            "$ref" : "#/components/schemas/DurableStreamContext"
          }
        },
        "description" : "CalendarDaysoftheyearRequest",
        "nullable" : false
      }
    },
    "securitySchemes" : {
      "basicAuth" : {
        "type" : "http",
        "scheme" : "basic"
      }
    }
  }
}
```
