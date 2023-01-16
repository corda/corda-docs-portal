---
aliases:
- /releases/3.3/serialization-index.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-3-3:
    identifier: corda-enterprise-3-3-serialization-index
    parent: corda-enterprise-3-3-building-a-cordapp-index
    weight: 1080
tags:
- serialization
title: Serialization
---


# Serialization



* [Object serialization](serialization.md)
    * [Introduction](serialization.md#introduction)
    * [Whitelisting](serialization.md#whitelisting)
    * [AMQP](serialization.md#amqp)
    * [Core Types](serialization.md#core-types)
        * [Collection Types](serialization.md#collection-types)
        * [JVM primitives](serialization.md#jvm-primitives)
        * [Arrays](serialization.md#arrays)
        * [JDK Types](serialization.md#jdk-types)
        * [Third-Party Types](serialization.md#third-party-types)
        * [Corda Types](serialization.md#corda-types)


    * [Custom Types](serialization.md#custom-types)
        * [Classes](serialization.md#classes)
            * [General Rules](serialization.md#general-rules)
            * [Constructor Instantiation](serialization.md#constructor-instantiation)
            * [Setter Instantiation](serialization.md#setter-instantiation)


        * [Inaccessible Private Properties](serialization.md#inaccessible-private-properties)
        * [Mismatched Class Properties / Constructor Parameters](serialization.md#mismatched-class-properties-constructor-parameters)
        * [Mutable Containers](serialization.md#mutable-containers)
        * [Enums](serialization.md#enums)
        * [Exceptions](serialization.md#exceptions)
        * [Kotlin Objects](serialization.md#kotlin-objects)


    * [Class synthesis](serialization.md#class-synthesis)
    * [Type Evolution](serialization.md#type-evolution)


* [Pluggable Serializers for CorDapps](cordapp-custom-serializers.md)
    * [Serializer Location](cordapp-custom-serializers.md#serializer-location)
    * [Writing a Custom Serializer](cordapp-custom-serializers.md#writing-a-custom-serializer)
    * [Example](cordapp-custom-serializers.md#example)
    * [The Proxy Object](cordapp-custom-serializers.md#the-proxy-object)
    * [Whitelisting](cordapp-custom-serializers.md#whitelisting)


* [Default Class Evolution](serialization-default-evolution.md)
    * [Adding Nullable Properties](serialization-default-evolution.md#adding-nullable-properties)
    * [Adding Non Nullable Properties](serialization-default-evolution.md#adding-non-nullable-properties)
    * [Removing Properties](serialization-default-evolution.md#removing-properties)
    * [Reordering Constructor Parameter Order](serialization-default-evolution.md#reordering-constructor-parameter-order)


* [Enum Evolution](serialization-enum-evolution.md)
    * [The Purpose of Annotating Changes](serialization-enum-evolution.md#the-purpose-of-annotating-changes)
    * [Evolution Transmission](serialization-enum-evolution.md#evolution-transmission)
    * [Evolution Precedence](serialization-enum-evolution.md#evolution-precedence)
    * [Renaming Constants](serialization-enum-evolution.md#renaming-constants)
        * [Rules](serialization-enum-evolution.md#rules)


    * [Adding Constants](serialization-enum-evolution.md#adding-constants)
        * [Rules](serialization-enum-evolution.md#id1)


    * [Combining Evolutions](serialization-enum-evolution.md#combining-evolutions)
    * [Unsupported Evolutions](serialization-enum-evolution.md#unsupported-evolutions)





