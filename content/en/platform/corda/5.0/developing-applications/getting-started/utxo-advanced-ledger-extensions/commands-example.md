---
date: '2023-06-01'
title: "Building Basic Contract Design"
project: corda
version: 'Corda 5.0'
menu:
  corda5:
    identifier: corda5-utxo-ledger-extensions-examples
    parent: corda5-utxo-advanced-ledger-extensions
    weight: 4600
section_menu: corda5
---

# Building Basic Contract Design

The following contract defines three commands; Create, Update and Delete. The `verify` function delegates these command types to `verifyCreate`, `verifyUpdate` and `verifyDelete` functions respectively, for example:

```kotlin
    public final class ExampleContract implements Contract {
    private interface ExampleContractCommand extends Command { }
  
    public static class Create implements ExampleContractCommand { }
    public static class Update implements ExampleContractCommand { }
    public static class Delete implements ExampleContractCommand { }
    
    @Override
    public void verify(UtxoLedgerTransaction transaction) {
        
        List<? extends ExampleContractCommand> commands = transaction
                .getCommands(ExampleContractCommand.class);
        
        for (ExampleContractCommand command : commands) {
            if (command instanceof Create) verifyCreate(transaction);
            else if (command instanceof Update) verifyUpdate(transaction);
            else if (command instanceof Delete) verifyDelete(transaction);
            else throw new IllegalStateException("Unrecognised command type.");
        }
    }
    
    private void verifyCreate(UtxoLedgerTransaction transaction) {
        // Verify Create constraints
    }
    
    private void verifyUpdate(UtxoLedgerTransaction transaction) {
        // Verify Update constraints
    }
    
    private void verifyDelete(UtxoLedgerTransaction transaction) {
        // Verify Delete constraints
    }
}
  ```

Designing a contract as shown in the above example will suffice in many cases. Assuming that the constraints have been implemented correctly then, the contract functionality and design is perfectly acceptable.

{{< note >}}
There are cases where this design approach no longer fits the design goals of the system being implemented. Specifically, in regard to contract extensibility, it is currently not possible to extend a contract to support additional constraints.
{{< /note >}}

## Derivable Contract Design

The following contract refactors the above to support the ability to derive contracts, and provide additional constraints in a secure and controlled way.
The contract still provides the same three commands; `Create`, `Update` and `Delete`. The verify function delegates these command types to `verifyCreate`, `verifyUpdate` and `verifyDelete` functions respectively, which in turn call `onVerifyCreate`, `onVerifyUpdate` and `onVerifyDelete` respectively.

{{< note >}}
The verify function has been marked final. This change is necessary as it prevents derived contract implementations from circumventing the base contract rules.
{{< /note >}}

  ```kotlin
  public class ExampleContract implements Contract {
  
    private interface ExampleContractCommand extends Command { }
    public static class Create implements ExampleContractCommand { }
    public static class Update implements ExampleContractCommand { }
    public static class Delete implements ExampleContractCommand { }
    
    @Override
    
    public final void verify(UtxoLedgerTransaction transaction) {
    
        List<? extends ExampleContractCommand> commands = transaction
                .getCommands(ExampleContractCommand.class);
                
        for (ExampleContractCommand command : commands) {
            if (command instanceof Create) verifyCreate(transaction);
            else if (command instanceof Update) verifyUpdate(transaction);
            else if (command instanceof Delete) verifyDelete(transaction);
            else throw new IllegalStateException("Unrecognised command type.");
        }
    }
    
    protected void onVerifyCreate(UtxoLedgerTransaction transaction) { }
    protected void onVerifyUpdate(UtxoLedgerTransaction transaction) { }
    protected void onVerifyDelete(UtxoLedgerTransaction transaction) { }    
    private void verifyCreate(UtxoLedgerTransaction transaction) {
    
        // Verify base Create constraints
        // Then verify additional Create constraints implemented by derived contracts
        onVerifyCreate(transaction);
        
    }
    private void verifyUpdate(UtxoLedgerTransaction transaction) {
        // Verify base Update constraints
        // Then verify additional Update constraints implemented by derived contracts
        onVerifyUpdate(transaction);
    }
    
    private void verifyDelete(UtxoLedgerTransaction transaction) {
        // Verify base Delete constraints
        // Then verify additional Delete constraints implemented by derived contracts
        onVerifyDelete(transaction);
    }
}
```

Refactoring a contract as shown in the above example allows CorDapp implementors to derive from the contract, allowing additional constraints which will be verified in additional to the constraints specified by the base contract.

{{< note >}}
There are still some outstanding issues with this design, where this design approach no longer fits the design goals of the system being implemented.
{{</ note >}}

The problem really lies in the `verify` function; for example:

```kotlin
public final void verify(UtxoLedgerTransaction transaction) {
  
    List<? extends ExampleContractCommand> commands = transaction
            .getCommands(ExampleContractCommand.class);
            
    for (ExampleContractCommand command : commands) {
        if (command instanceof Create) verifyCreate(transaction);
        else if (command instanceof Update) verifyUpdate(transaction);
        else if (command instanceof Delete) verifyDelete(transaction);
        else throw new IllegalStateException("Unrecognised command type.");
    }
}
```

The `verify` function is marked final for security reasons, and therefore additional commands cannot be added to the contract. For example, the contract may wish to describe multiple ways to `Update` a state, or set of states. The contract only defines a single `Update` command: there can only be one mechanism to perform updates.

The second problem lies in the commands themselves and their names. `Create`, `Update` and `Delete` are very ambiguous names, which may not make sense depending on the context of the contract being implemented.

## Delegated Command Design

In the contracts above, the commands are nothing more than marker classes; effectively they are cases in a switch statement, which allows the contract's `verify` function to delegate responsibility of specific contract constraints to other functions, such as `verifyCreate`, `verifyUpdate` and `verifyDelete`.

We can implement the `verify` function on the command itself. Instead of being an empty marker class, this gives the command responsibility, as it becomes responsible for implementing its associated contract verification constraints.
In this case, we define a `VerifiableCommand` interface with a `verify` function; for example:

```kotlin
public interface VerifiableCommand extends Command {
    void verify(UtxoLedgerTransaction transaction);
}
```

Now that we have a command which itself can implement contract verification constraints, we can use this as the basis for the `ExampleContractCommand` class. This needs to be a class rather than an interface, because we need to be in complete control of its implementations for security.
We achieve this by making the default constructor package private, so that only commands within the same package can extend it; for example:

```kotlin
public class ExampleContractCommand implements VerifiableCommand {
    ExampleContractCommand() { }
}

Next, we can implement this interface as `Create`, `Update` and `Delete` commands; for example:

```kotlin
public class Create extends ExampleContractCommand {
    @Override
    public final void verify(UtxoLedgerTransaction transaction) {
        // Verify base Create constraints
        // Then verify additional Create constraints implemented in derived commands
        onVerify(transaction);
    }
    
    protected void onVerify(UtxoLedgerTransaction transaction) { }
}

public class Update extends ExampleContractCommand {

    @Override
    
    public final void verify(UtxoLedgerTransaction transaction) {
    
        // Verify base Update constraints
        // Then verify additional Update constraints implemented in derived commands
        onVerify(transaction);
        
    }
    protected void onVerify(UtxoLedgerTransaction transaction) { }
}

public class Delete extends ExampleContractCommand {

    @Override
    
    public final void verify(UtxoLedgerTransaction transaction) {
        // Verify base Delete constraints
        // Then verify additional Delete constraints implemented in derived commands
        onVerify(transaction);
    }
    protected void onVerify(UtxoLedgerTransaction transaction) { }
}
```

{{< note >}}
The `Create`, `Update` and `Delete` commands are not marked final. Therefore, we can extend the contract verification constraints from these points, but we cannot extend from `ExampleContractCommand`.
{{< /note >}}

## Delegated Contract Design

As we have now delegated contract verification constraint logic to the commands themselves, we must also refactor the contract to support this delegation. The contract implementation in this case becomes simpler, since it is no longer responsible for defining contract verification constraints. For example:

```kotlin
public final class ExampleContract implements Contract {
    
      @Override
      
      public void verify(UtxoLedgerTransaction transaction) {
         List<? extends ExampleContractCommand> commands = transaction
                  .getCommands(ExampleContractCommand.class);
                  
          for (ExampleContractCommand command : commands) {
              command.verify(transaction);
          }
      }
    }
```

This design addresses the outstanding issues in regard to being able to extend a contract with multiple commands, and being able to assign names to commands that make sense in the context that they're used. For example:

```kotlin

    class Mint extends Create { ... }
    class Issue extends Update { ... }
    class Transfer extends Update { ... }
    class Exchange extends Update { ... }
    class Redeem extends Update { ... }
    class Burn extends Delete { ... }
```

{{< note >}}
 The contract now supports five different command types, each of which implements different constraints and derives from `Create`, `Update`, or `Delete`.
{{< /note >}}
