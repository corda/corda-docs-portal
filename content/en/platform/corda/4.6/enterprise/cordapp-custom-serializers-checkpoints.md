---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-6:
    parent: corda-enterprise-4-6-node-serialization
tags:
- cordapp
- custom
- serializers
title: Pluggable serializers for CorDapp checkpoints
weight: 20
---


# Pluggable serializers for CorDapp checkpoints


If a CorDapp encounters an exception during the checkpoint process, it may need a custom serializer to make a class serializable.

{{< warning >}}

**IMPORTANT**

* This is an unsupported advanced feature for use when a class cannot be serialized and cannot be avoided. It should be avoided unless there is no choice.

* Care needs to be taken when modifying CorDapps when custom checkpoint serializers are present. Avoid removing or renaming a custom serializer needed to deserialize a checkpoint. It is best to modify CorDapps containing custom checkpoint serializers when no checkpoints are present.

{{< /warning >}}

{{< note >}}
Please read [Pluggable serializers for CorDapps](cordapp-custom-serializers.md) before you start.
{{< /note >}}


## Writing a custom checkpoint serializer

Checkpoint serializers follow the same rules as [normal pluggable serializers](cordapp-custom-serializers.md).

In addition they need to implement `net.corda.core.serialization.CheckpointCustomSerializer`.

## Example

Create a class that claims to implement the Map interface, but does not behave correctly:

```java
@CordaSerializable
public final class BrokenMapImpl<K,V> extends HashMap<K,V> {
    @Override
    public V put(K key, V value) {
        throw new RuntimeException("Broken on purpose");
    }
}
```

This class will not checkpoint correctly because the `put` method is broken.

Here is a flow for testing the behaviour of this map:

```java
@InitiatingFlow
@StartableByRPC
public class BrokenMapFlow extends FlowLogic<Integer> {

    @Suspendable
    @Override
    public Integer call() throws FlowException {

        // Something to store in our map
        HashMap<String, Integer> inputValues = new HashMap<>();
        inputValues.put("Key", 5);

        // This map won't serialize correctly
        BrokenMapImpl<String, Integer> brokenMap = new BrokenMapImpl<>();
        brokenMap.putAll(inputValues);

        // Force a checkpoint
        sleep(Duration.ofMinutes(5));

        // Output a value from the map
        getLogger().info("Flow completed successfully");
        getLogger().info("Result is " + brokenMap.get("Key"));
        return brokenMap.get("Key");
    }
}
```

At this point, there is a flow that will not deserialize from checkpoint correctly. It will throw an exception when trying to rebuild `BrokenMapImpl`.

Adding this implementation of `CheckpointCustomSerializer` will fix the issue. It will be found at startup and registered with the system. When the test flow reaches a checkpoint, this will transform `BrokenMapImpl` into a `HashMap` for storage and then convert back to `BrokenMapImpl` when the flow resumes.

```java
public class BrokenMapSerializer implements CheckpointCustomSerializer<BrokenMapImpl, HashMap> {

    // Convert to a HashMap for storage
    @Override
    public HashMap toProxy(BrokenMapImpl brokenMap) {
        return new HashMap(brokenMap);
    }

    // Convert back to BrokenMapImpl on resume
    @Override
    public BrokenMapImpl fromProxy(HashMap hashMap) {
        BrokenMapImpl brokenMap = new BrokenMapImpl();
        brokenMap.putAll(hashMap);
        return brokenMap;
    }
}
```
