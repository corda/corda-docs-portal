---
title: "Hashing Service"
date: '2021-09-13'
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-cordapps-corda-services
    weight: 3000
project: corda-5
section_menu: corda-5-dev-preview
description: >
  Hashing within flows, services and internally.
---

`SecureHash` is the data class used to hold digests in Corda. This class is a wrapper around the digest's value in bytes along with the digest algorithm name used to produce the digest. `SecureHash` instances are returned by the Corda Hashing API.

Digest values in Corda are stored as byte arrays or strings. String representations must conform to the following format: [algorithm]:[digest value as a hexadecimal string]. This includes passing digests through the wire or storing them in a storage system.

`DigestAlgorithmName` is the class used in Corda Hashing API to indicate which digest algorithm is to be used for hashing.

The Corda Hashing API comprises `BasicHashingService` and `HashingService`.


## BasicHashingService

`BasicHashingService` contains a minimal set of methods to work with hashing. It offers the following utilities:


* Hashing of bytes using the specified algorithm:

  ```kotlin
  fun hash(bytes: ByteArray, digestAlgorithmName: DigestAlgorithmName): SecureHash
  ```

* Parsing of a `String` of the following format [algorithm]:[digest value as a hexadecimal string] into a `SecureHash` through:

  ```kotlin
  fun create(str: String): SecureHash
  ```

  It will throw `IllegalArgumentException` if:

  * the passed in `String` does not conform to the [algorithm]:[digest value as a hexadecimal string] format.
  * the digest value is not of the expected digest algorithm length.  

* `SecureHash` constants containing byte arrays full of zeros(0) or ones(1), of the length of the respective digest algorithm specified through:

  ```kotlin
  fun zeroHash(digestAlgorithmName: DigestAlgorithmName): SecureHash
  ```

  ```kotlin
  fun allOnesHash(digestAlgorithmName: DigestAlgorithmName): SecureHash
  ```

* Digest value computation of concatenated digests:


  ```kotlin
  fun concatenateAs(first: SecureHash, second: SecureHash, concatAlgorithmName: DigestAlgorithmName): SecureHash
  ```

  This method requires both `first` and `second` hashes to be of the same digest algorithm. Then it concatenates their `ByteArray`s and computes a digest out of the concatenated `ByteArray`, using the specified digest algorithm.


`BasicHashingService` offers digest algorithms provided by `java.security.Security`. Any of the above methods will throw an `IllegalArgumentException` if the digest algorithm is not supported.


## HashingService

`HashingService` is a wrapper around `BasicHashingService` and offers overload and helper methods that delegate to `BasicHashingService.hash`.



* The `HashingService` API can be made available to CorDapps by injecting it into flows and services.


* `DigestAlgorithmName` is the default digest algorithm name and a set of overloaded functions that use this default algorithm. These overloaded functions do not require an algorithm name as a parameter.



* `HashingService` offers computing of digest values (`SecureHash`) for the following types of objects through the `hash` overloads:


  * `ByteArray` - This is the main hashing method inherited from `BasicHashingService`.

  * `OpaqueBytes` - This class is a wrapper around a `ByteArray`. Please note that the digest value will be computed over the wrapped `ByteArray` inside of `OpaqueBytes`. The digest value will not be computed over a serialized `OpaqueBytes` object.



  * `String` - It computes the digest of a String after converting it to a `ByteArray`.


* The `HashingService` offers re-hashing of a `SecureHash` using its original digest algorithm through:



```kotlin
fun reHash(secureHash: SecureHash): SecureHash
```

* It offers computing of a random digest of the specified digest algorithm through:

```kotlin
fun randomHash(digestAlgorithmName: DigestAlgorithmName): SecureHash
```

  This method generates a `ByteArray` of the length of the specified digest algorithm with random bytes, and then it computes and returns a digest out of that `ByteArray`.

Example usages:

- Hashing a `String`:

  - Kotlin

    ```kotlin
    @StartableByRPC
    class HashingStringFlow @JsonConstructor constructor(private val params: RpcStartFlowRequestParameters) : Flow<Unit> {

        @CordaInject
        private lateinit var hashingService: HashingService

        @Suspendable
        override fun call() {
            val str = "string to hash"
            val hash0: SecureHash = hashingService.hash(str)

            val defaultDigestAlgorithmName = hashingService.defaultDigestAlgorithmName
            assert(defaultDigestAlgorithmName == DigestAlgorithmName.SHA2_256)
            val hash1: SecureHash = hashingService.hash(str, defaultDigestAlgorithmName)

            assert(hash0 == hash1)
        }
    }
    ```

  - Java

    ```java
    @StartableByRPC
    class HashingStringFlow implements Flow<Void> {

        public @JsonConstructor
        HashingStringFlow(RpcStartFlowRequestParameters params) { }

        @CordaInject
        private HashingService hashingService;

        @Override
        @Suspendable
        public Void call() {
            String str = "string to hash";
            SecureHash hash0 = hashingService.hash(str);

            DigestAlgorithmName defaultDigestAlgorithmName = hashingService.getDefaultDigestAlgorithmName();
            assert (defaultDigestAlgorithmName == DigestAlgorithmName.SHA2_256);
            SecureHash hash1 = hashingService.hash(str, defaultDigestAlgorithmName);

            assert (hash0 == hash1);
            return null;
        }
    }
    ```

- Hashing a `ByteArray`:

  - Kotlin

    ```kotlin
    @StartableByRPC
    class HashingByteArrayFlow @JsonConstructor constructor(private val params: RpcStartFlowRequestParameters) : Flow<Unit> {

        @CordaInject
        lateinit var hashingService: HashingService

        @Suspendable
        override fun call() {
            val bytes = byteArrayOf(-0x80, 0x00, 0x79)
            val hash: SecureHash = hashingService.hash(bytes, DigestAlgorithmName.SHA2_512)

            assert(hash.toHexString() == "E8448BEE6568FF8F62733E5278D63223B94231159C30024852AD5C33895D4F0C632F2DE1C69F091DDB83CEA598EE9DD177C209C189B37665FBC367D335847943")
        }
    }
    ```

  - Java

    ```java
    @StartableByRPC
    class HashingByteArrayFlow implements Flow<Void> {

        public HashingByteArrayFlow(RpcStartFlowRequestParameters params) { }

        @CordaInject
        private HashingService hashingService;

        @Override
        @Suspendable
        public Void call() {
            byte[] bytes = new byte[]{-0x80, 0x00, 0x79};
            SecureHash hash = hashingService.hash(bytes, DigestAlgorithmName.SHA2_512);

            assert (hash.toHexString().equals("E8448BEE6568FF8F62733E5278D63223B94231159C30024852AD5C33895D4F0C632F2DE1C69F091DDB83CEA598EE9DD177C209C189B37665FBC367D335847943"));
            return null;
        }
    }
    ```

- Hashing digests' concatenation:

  - Kotlin

    ```kotlin
    @StartableByRPC
    class HashingDigestsConcatenationFlow @JsonConstructor constructor(private val params: RpcStartFlowRequestParameters) : Flow<Unit> {


        @CordaInject
        lateinit var hashingService: HashingService

        @Suspendable
        override fun call() {
            val bytes = byteArrayOf(0x00, 0x01, 0x02, 0x03)
            val hash: SecureHash = hashingService.hash(bytes)
            val allOnesHash = hashingService.allOnesHash(DigestAlgorithmName.DEFAULT_ALGORITHM_NAME)
            val concatHash0 = hashingService.concatenate(hash, allOnesHash)
            val concatHash1 = hashingService.concatenateAs(hash, allOnesHash, DigestAlgorithmName.DEFAULT_ALGORITHM_NAME)

            assert(DigestAlgorithmName.DEFAULT_ALGORITHM_NAME == DigestAlgorithmName.SHA2_256)
            assert (concatHash0.toString() == "SHA-256:E76883E2B2DBD183C51B4329DF3BA30958A5CBE2DE8A65AF9509CE2BA152C302")
            assert(concatHash0 == concatHash1)
        }
    }
    ```

  - Java

    ```java
    @StartableByRPC
    class HashingDigestsConcatenationFlow implements Flow<Void> {


        public HashingDigestsConcatenationFlow(RpcStartFlowRequestParameters params) { }


        @CordaInject
        private HashingService hashingService;

        @Override
        @Suspendable
        public Void call() {
            byte[] bytes = new byte[]{0x00, 0x01, 0x02, 0x03};
            SecureHash hash = hashingService.hash(bytes);
            SecureHash allOnesHash = hashingService.allOnesHash(DigestAlgorithmName.DEFAULT_ALGORITHM_NAME);
            SecureHash concatHash0 = hashingService.concatenate(hash, allOnesHash);
            SecureHash concatHash1 = hashingService.concatenateAs(hash, allOnesHash, DigestAlgorithmName.DEFAULT_ALGORITHM_NAME);

            assert (DigestAlgorithmName.DEFAULT_ALGORITHM_NAME == DigestAlgorithmName.SHA2_256);
            assert (concatHash0.toString().equals("SHA-256:E76883E2B2DBD183C51B4329DF3BA30958A5CBE2DE8A65AF9509CE2BA152C302"));
            assert (concatHash0 == concatHash1);
            return null;
        }
    }
    ```

- Create `SecureHash` from String:

  - Kotlin

    ```kotlin
    @StartableByRPC
    class CreateSecureHashFromStringFlow @JsonConstructor constructor(private val params: RpcStartFlowRequestParameters) : Flow<Unit> {

        @CordaInject
        lateinit var hashingService: HashingService

        @Suspendable
        override fun call() {
            val validSHA256Hash = "SHA-256:E76883E2B2DBD183C51B4329DF3BA30958A5CBE2DE8A65AF9509CE2BA152C302"
            val hash = hashingService.create(validSHA256Hash)

            assert(hash.toString() == "SHA-256:E76883E2B2DBD183C51B4329DF3BA30958A5CBE2DE8A65AF9509CE2BA152C302")
        }
    }
    ```

  - Java

    ```java
    @StartableByRPC
    class CreateSecureHashFromStringFlow implements Flow<Void> {

        public CreateSecureHashFromStringFlow(RpcStartFlowRequestParameters params) {}

        @CordaInject
        private HashingService hashingService;

        @Override
        @Suspendable
        public Void call() {
            String validSHA256Hash = "SHA-256:E76883E2B2DBD183C51B4329DF3BA30958A5CBE2DE8A65AF9509CE2BA152C302";
            SecureHash hash = hashingService.create(validSHA256Hash);

            assert(hash.toString().equals("SHA-256:E76883E2B2DBD183C51B4329DF3BA30958A5CBE2DE8A65AF9509CE2BA152C302"));
            return null;
        }
    }
    ```
