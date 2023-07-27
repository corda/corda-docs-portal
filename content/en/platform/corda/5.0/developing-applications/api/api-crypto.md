---
date: '2023-06-21'
version: 'Corda 5.0'
title: "net.corda.v5.crypto"
menu:
  corda5:
    identifier: corda5-api-crypto
    parent: corda5-api
    weight: 5000
section_menu: corda5
draft: true
---
# net.corda.v5.crypto

The `corda-crypto` module 

## Implementing Signature Schemes

Corda supports the following `SignatureSpecs` (signature schemes) for creating the following objects:

* SHA256withRSA
* SHA384withRSA
* SHA512withRSA
* RSASSA-PSS with SHA256
* RSASSA-PSS with SHA384
* RSASSA-PSS with SHA512
* RSASSA-PSS with SHA256 and MGF1
* RSASSA-PSS with SHA384 and MGF1
* RSASSA-PSS with SHA512 and MGF1
* SHA256withECDSA
* SHA384withECDSA
* SHA512withECDSA
* EdDSA
* SHA512withSPHINCS256
* SM3withSM2
* SHA256withSM2
* GOST3411withGOST3410

Use `SignatureSpecService` to retrieve the `SignatureSpec`.

Initially the above list of signature spec was available to users. However, they could be passing the wrong signature spec for a signing key type (e.g. an RSA key with an SHA256withECDSA), which would lead to an error when attempting to generate the signature.

Instead SignatureSpecService was introduced which takes in a key (and a digest algorithm optionally) and returns a default signature spec for those.

## CompositeKey.java

```kotlin

package net.corda.v5.crypto;

import org.jetbrains.annotations.NotNull;

import java.security.PublicKey;
import java.util.Set;

/**
 * A tree data structure that enables the representation of composite public keys, which are used to represent
 * the signing requirements for multi-signature scenarios. A composite key is a list
 * of leaf keys and their contributing weight, and each leaf can be a conventional single key or a composite key.
 * Keys contribute their weight to the total if they are matched by the signature.
 * <p>
 * For complex scenarios, such as <em>"Both Alice and Bob need to sign to consume a state S"</em>, we can represent
 * the requirement by creating a tree with a root {@link CompositeKey}, and <code>Alice</code> and <code>Bob</code> as children.
 * The root node would specify <strong>weights</strong> for each of its children and a <strong>threshold</strong> –
 * the minimum total weight required (for example, the minimum number of child signatures required) to satisfy the
 * tree signature requirement.
 * <p>
 * Using these constructs we can express, for example, 1 of N (OR) or N of N (AND) signature requirements. By nesting we can
 * create multi-level requirements such as <em>"either the CEO or three of five of his assistants need to sign"</em>.
 * <p>
 * Composite key implementations will track the minimum total weight required (in the simple case – the minimum number of child
 * signatures required) to satisfy the subtree rooted at this node.
 */

public interface CompositeKey extends PublicKey {
    /**
     * This method will detect graph cycles in the full composite key structure to protect against infinite loops when
     * traversing the graph and key duplicates in each layer. It also checks if the threshold and weight constraint
     * requirements are met, while it tests for aggregated-weight integer overflow.
     * In practice, this method should be always invoked on the root {@link CompositeKey}, as it inherently
     * validates the child nodes (all the way till the leaves).
     */
    void checkValidity();

    /**
     * Takes single {@link PublicKey} and checks if {@link CompositeKey} requirements hold for that key.
     *
     * @param key The public key.
     * @return true if the public key is a composite key, false otherwise.
     */
    boolean isFulfilledBy(@NotNull PublicKey key);

    /**
     * Checks if the public keys corresponding to the signatures are matched against the leaves of the composite
     * key tree in question, and the total combined weight of all children is calculated for every intermediary node.
     * If all thresholds are satisfied, the composite key requirement is considered to be met.
     */
    boolean isFulfilledBy(@NotNull Set<PublicKey> keysToCheck);

    /**
     * Set of all leaf keys of that {@link CompositeKey}.
     *
     * @return a {@link Set} of the {@link PublicKey}.
     */
    @NotNull
    Set<PublicKey> getLeafKeys();
}
```

## CompositeKeyNodeAndWeight.java

```kotlin

package net.corda.v5.crypto;

import org.jetbrains.annotations.NotNull;

import java.security.PublicKey;

/**
 * A simple data class for passing keys and weights into <code>CompositeKeyGenerator</code>.
 */
 
public final class CompositeKeyNodeAndWeight {
    private final PublicKey node;
    private final int weight;

    /**
     * Creates a new {@code CompositeKeyNodeAndWeight} for
     * the specified key and weight for the key.
     *
     * @param node   A public key.
     * @param weight The weight for that key, must be greater than zero.
     */
    public CompositeKeyNodeAndWeight(@NotNull PublicKey node, int weight) {
        if (weight <= 0)
            throw new IllegalArgumentException("A non-positive weight was detected. Member info: " + this);
        this.node = node;
        this.weight = weight;
    }

    /**
     * Creates a new {@code CompositeKeyNodeAndWeight} for
     * the specified key, defaulting the key's weight to 1.
     *
     * @param node  A public key.
     */
    public CompositeKeyNodeAndWeight(@NotNull PublicKey node) {
        this(node, 1);
    }

    /**
     * @return The key of the {@code CompositeKeyNodeAndWeight}.
     */
    @NotNull
    public PublicKey getNode() {
        return this.node;
    }

    /**
     * @return The weight of the key.
     */
    public int getWeight() {
        return this.weight;
    }

    @NotNull
    public String toString() {
        return String.format("[%s, %d]", this.node, weight);
    }

    public int hashCode() {
        return node.hashCode() + 31 * weight;
    }

    public boolean equals(Object other) {
        if (this == other) return true;
        if (!(other instanceof CompositeKeyNodeAndWeight)) return false;
        CompositeKeyNodeAndWeight otherKey = (CompositeKeyNodeAndWeight) other;
        if (!otherKey.node.equals(node)) return false;
        return otherKey.weight == weight;
    }
}

```

## CordaOID.java

{{< tabs name="CordaOID">}}
{{% tab name="Kotlin" %}}

```kotlin

package net.corda.v5.crypto;

import org.jetbrains.annotations.NotNull;

/**
 * OIDs used for the Corda platform. All entries MUST be defined in this file only and they MUST NOT be removed.
 * If an OID is incorrectly assigned, it should be marked deprecated and NEVER be reused again.
 */

public final class CordaOID {
    private CordaOID() {}

    /**
     * An OID root assigned to R3, see
     * <a HREF="http://www.oid-info.com/cgi-bin/display?oid=1.3.6.1.4.1.50530&action=display">
     * http://www.oid-info.com/cgi-bin/display?oid=1.3.6.1.4.1.50530&action=display </a>
     */
    @NotNull
    public static final String OID_R3_ROOT = "1.3.6.1.4.1.50530";

    /**
     * OIDs issued for the Corda platform.
     */
    @NotNull
    public static final String OID_CORDA_PLATFORM = OID_R3_ROOT + ".1";

    /**
     * Identifier for the X.509 certificate extension specifying the Corda role.
     */
    @NotNull
    public static final String OID_X509_EXTENSION_CORDA_ROLE = OID_CORDA_PLATFORM + ".1";

    /**
     * OID for alias private keys.
     */
    @NotNull
    public static final String OID_ALIAS_PRIVATE_KEY = OID_CORDA_PLATFORM + ".2";

    /**
     * OID for {@link CompositeKey}.
     */
    @NotNull
    public static final String OID_COMPOSITE_KEY = OID_CORDA_PLATFORM + ".3";

    /**
     * OID for composite signatures.
     */
    @NotNull
    public static final String OID_COMPOSITE_SIGNATURE = OID_CORDA_PLATFORM + ".4";
}
```

## DigestAlgorithmName.java

```kotlin
package net.corda.v5.crypto;

import net.corda.v5.base.annotations.CordaSerializable;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

/**
 * The digest algorithm name. This class is to be used in Corda hashing API.
 */
@CordaSerializable
public final class DigestAlgorithmName {
    private final String name;

    /**
     * Construct a digest algorithm name.
     * <p>
     *
     * @param name The name of the digest algorithm to be used for the instance.
     */
    public DigestAlgorithmName(@NotNull String name) {
        if (name == null || name.isBlank()) throw new IllegalArgumentException("Hash algorithm name unavailable or not specified");
        this.name = name;
    }

    /**
     * Instance of SHA-256.
     */
    @NotNull
    public static final DigestAlgorithmName SHA2_256 = new DigestAlgorithmName("SHA-256");

    /**
     * Instance of Double SHA-256.
     */
    @NotNull
    public static final DigestAlgorithmName SHA2_256D = new DigestAlgorithmName("SHA-256D");

    /**
     * Instance of SHA-384.
     */
    @NotNull
    public static final DigestAlgorithmName SHA2_384 = new DigestAlgorithmName("SHA-384");

    /**
     * Instance of SHA-512.
     */
    @NotNull
    public static final DigestAlgorithmName SHA2_512 = new DigestAlgorithmName("SHA-512");

    /**
     * Converts a {@link DigestAlgorithmName} object to a string representation.
     */
    @NotNull
    public String toString() {
        return this.name;
    }

    /**
     * Returns a hash code value for the object.
     */
    public int hashCode() {
        return this.name.toUpperCase().hashCode();
    }

    /**
     * Check if two specified instances of the {@link DigestAlgorithmName} are the same based on their content.
     *
     * @return true if they are equal.
     */
    public boolean equals(@Nullable Object other) {
        if (other == null) return false;
        if (this == other) return true;
        if (!(other instanceof DigestAlgorithmName)) return false;
        DigestAlgorithmName otherDigest = (DigestAlgorithmName) other;
        return this.name.equalsIgnoreCase(otherDigest.name);
    }

    @NotNull
    public String getName() {
        return this.name;
    }
}

```

## DigitalSignature.java

```kotlin

package net.corda.v5.crypto;

import net.corda.v5.base.annotations.CordaSerializable;
import net.corda.v5.base.annotations.DoNotImplement;
import org.jetbrains.annotations.NotNull;

/**
 * A wrapper around a digital signature.
 */
@DoNotImplement
@CordaSerializable
public interface DigitalSignature {

    /**
     * @return The digital signature bytes.
     */
    @NotNull
    byte[] getBytes();

    /**
     * A digital signature that identifies who is the owner of the signing key used to create this signature.
     */
    @DoNotImplement
    interface WithKeyId extends DigitalSignature {

        /**
         * Gets the key ID of the public key (public key hash) whose private key pair was used to sign the data. If the
         * original key passed in to the sign operation is a {@link CompositeKey} then the key ID, is the ID of the
         * composite key leaf used to sign.
         */
        @NotNull
        SecureHash getBy();
    }
}

```

## KeySchemeCodes.java

```kotlin

package net.corda.v5.crypto;

import org.jetbrains.annotations.NotNull;

/**
 * Key schemes used in Corda for signing and key derivation.
 */
public final class KeySchemeCodes {
    private KeySchemeCodes() {}

    /**
     * RSA key scheme code name.
     * The key scheme can be used for signing only.
     */
    @NotNull
    public static final String RSA_CODE_NAME = "CORDA.RSA";

    /**
     * ECDSA with SECP256K1 curve key scheme code name.
     * The key scheme can be used for signing and key derivation such as ECDH.
     */
    @NotNull
    public static final String ECDSA_SECP256K1_CODE_NAME = "CORDA.ECDSA.SECP256K1";

    /**
     * ECDSA with SECP256R1 curve key scheme code name.
     * The key scheme can be used for signing and key derivation such as ECDH.
     */
    @NotNull
    public static final String ECDSA_SECP256R1_CODE_NAME = "CORDA.ECDSA.SECP256R1";

    /**
     * EdDSA with 25519PH curve key scheme code name.
     * The key scheme can be used for signing only.
     */
    @NotNull
    public static final String EDDSA_ED25519_CODE_NAME = "CORDA.EDDSA.ED25519";

    /**
     * EdDSA with X25519 curve key scheme code name.
     * The key scheme can be used for key derivation such as ECDH only.
     */
    @NotNull
    public static final String X25519_CODE_NAME = "CORDA.X25519";

    /**
     * SM2 key scheme code name.
     * As the key scheme is variant of ECDSA, it can be used for signing and key derivation such as ECDH.
     */
    @NotNull
    public static final String SM2_CODE_NAME = "CORDA.SM2";

    /**
     * GOST3410 with GOST3411 key scheme code name.
     * The key scheme can be used for signing only.
     */
    @NotNull
    public static final String GOST3410_GOST3411_CODE_NAME = "CORDA.GOST3410.GOST3411";

    /**
     * SPHINCS post quantum key scheme code name.
     * The key scheme can be used for signing only.
     */
    @NotNull
    public static final String SPHINCS256_CODE_NAME = "CORDA.SPHINCS-256";

    /**
     * Composite Key, see [CompositeKey] for details.
     * The scheme cannot be directly used for signing or key derivation.
     */
    @NotNull
    public static final String COMPOSITE_KEY_CODE_NAME = "COMPOSITE";
}

```

## KeyUtils.java

```kotlin

package net.corda.v5.crypto;

import org.jetbrains.annotations.NotNull;

import java.security.PublicKey;
import java.util.Collections;
import java.util.Set;

/**
 * Helper functions for key look up in a set of keys. These functions also work when the key to look up in the
 * set of keys is {@link CompositeKey}.
 */
public final class KeyUtils {
    private KeyUtils() {}

    /**
     * Checks whether <code>key</code> has any intersection with the keys in <code>otherKeys</code>, 
     * recursing into <code>key</code> (the first argument) if it is a composite key. Does not match
     * any composite keys in <code>otherKeys</code>.
     * <p/>
     * For simple non-compound public keys, this operation simply checks if the first argument occurs in the
     * second argument. If <code>key</code> is a compound key, the outcome is whether any of its leaf keys
     * are in <code>otherKeys</code>.
     * {@link PublicKey}.
     * <p/>
     * This function checks against compound key tree leaves, which by definition are not {@link CompositeKey}.
     * That is why if any of the <code>otherKeys</code> is a {@link CompositeKey}, this function will not 
     * find a match, though composite keys in the <code>otherKeys</code> set is not regarded as an error; they
     * are silently ignored.
     * <p/>
     * The notion of a key being in a set is about equality, which is not the same as whether one key is 
     * fulfilled by another key. For example, a {@link CompositeKey} C could be defined to have threshold 2 and:
     * <p/>
     * <ul>
     *     <li> Public key X with weight 1 </li>
     *     <li> Public key Y with weight 1 </li>
     *     <li> Public key Z with weight 2 </li>
     * </ul>
     * Then we would find that <code>isKeyInSet(C, X)</code> is true, but X would not fulfill C since C is fulfilled by
     * X and Y together but not X on its. However, <code>isKeyInSet(C, Z)</code> is true, and Z fulfills C by itself.
     * 
     * @param key       The key being looked for.
     * @param otherKeys The keys searched for the {@code key}.
     * @return True if <code>key</code> is in otherKeys.
     */
    public static boolean isKeyInSet(@NotNull PublicKey key, @NotNull Set<PublicKey> otherKeys) {
        if (key instanceof CompositeKey) {
            CompositeKey compositeKey = (CompositeKey) key;
            Set<PublicKey> leafKeys = compositeKey.getLeafKeys();
            leafKeys.retainAll(otherKeys);
            return !leafKeys.isEmpty();
        } else {
            return otherKeys.contains(key);
        }
    }

    /**
     * Return true if a set of keys fulfil the requirements of a specific key.
     * <p/>
     * Fulfilment of a {@link CompositeKey} as <code>firstKey</code> key is checked by delegating to the <code>isFulfilledBy</code> method of that
     * compound key. It is a question of whether all the keys which match the compound keys in total have enough weight
     * to reach the threshold of the primary key. 
     * <p/>
     * In contrast, if this is called with <code>firstKey</code> being a simple public key, the test is whether
     * <code>firstKey</code> is equal to any of the keys in <code>otherKeys</code>. Since a simple public key
     * is never considered equal to a {@link CompositeKey} we know if <code>firstKey</code> is not composite, then
     * it will not be considered fulfilled by any {@link CompositeKey} in <code>otherKeys</code>. Such cases are
     * not considered errors, so we silently ignore {@link CompositeKey}s in <code>otherKeys</code>.
     *<p/>
     * If you know you have a {@link CompositeKey} in your hand, it would be simpler to call its <code>isFulfilledBy()</code>
     * method directly. This function is intended as a utility for when you have some kind of public key, and which to 
     * check fulfilment against a set of keys, without having to handle simple and composite keys separately (that is, this is
     * polymorphic).
     * 
     * @param key  The key to be checked whether it is being fulfilled by {@code otherKeys}.
     * @param otherKeys The keys against which the {@code key} is being checked for fulfilment.
     */
    public static boolean isKeyFulfilledBy(@NotNull PublicKey key, @NotNull Set<PublicKey> otherKeys) {
        if (key instanceof CompositeKey) {
            CompositeKey firstKeyComposite = (CompositeKey) key;
            return firstKeyComposite.isFulfilledBy(otherKeys);
        }
        return otherKeys.contains(key);
    }

    /**
     * Return true if one key fulfills the requirements of another key. See the previous variant; this overload
     * is the same as calling as the variant that takes an iterable set of other keys with <code>otherKey<code>
     * as a single element iterable. 
     * <p>
     * Since we do not define composite keys as acceptable on the second argument of this function, this relation
     * is not reflexive, not symmetric and not transitive. 
     *
     * @param key The key to be checked whether it is being fulfilled by {@code otherKey}.
     * @param otherKey The key against which the {@code key} is being checked for fulfilment.
     */
    public static boolean isKeyFulfilledBy(@NotNull PublicKey key, @NotNull PublicKey otherKey) {
        return isKeyFulfilledBy(key,
                Collections.singleton(otherKey));
    }
}

```

## MessageAuthenticationCode.java

```kotlin

package net.corda.v5.crypto;

import org.jetbrains.annotations.NotNull;

public final class MessageAuthenticationCode {
    private MessageAuthenticationCode() {}

    /**
     * Constant specifying the HMAC SHA-256 algorithm.
     */
    @NotNull
    public static final String HMAC_SHA256_ALGORITHM = "HmacSHA256";

    /**
     * Constant specifying the HMAC SHA-512 algorithm.
     */
    @NotNull
    public final static String HMAC_SHA512_ALGORITHM = "HmacSHA512";
}

```

## SecureHash.java

```kotlin

package net.corda.v5.crypto;

import net.corda.v5.base.annotations.CordaSerializable;
import net.corda.v5.base.annotations.DoNotImplement;
import org.jetbrains.annotations.NotNull;

/**
 * A cryptographically secure hash value, computed by a specified digest algorithm ({@link DigestAlgorithmName}).
 * A {@link SecureHash} can be computed and acquired through the {@link net.corda.v5.application.crypto.DigestService}.
 */
@DoNotImplement
@CordaSerializable
public interface SecureHash {
    /**
     * Hashing algorithm which was used to generate the hash.
     */
    @NotNull
    String getAlgorithm();

    /**
     * Returns hexadecimal representation of the hash value.
     */
    @NotNull
    String toHexString();

    /**
     * The delimiter used in the string form of a secure hash to separate the algorithm name from the hexadecimal
     * string of the hash.
     * <p>
     * NOTE: Algorithm name may only match the regex [a-zA-Z_][a-zA-Z_0-9\-/]* so delimiter ':' is a safe separator.
     */
    char DELIMITER = ':';

    /**
     * Converts a {@link SecureHash} object to a string representation containing the <code>algorithm</code> and hexadecimal
     * representation of the <code>bytes</code> separated by the colon character ({@link net.corda.v5.crypto.SecureHash.DELIMITER}).
     * <p>
     * Example outcome of toString(): SHA-256:98AF8725385586B41FEFF205B4E05A000823F78B5F8F5C02439CE8F67A781D90
     */
    @NotNull
    String toString();
}

```

## SignatureSpec.java

```kotlin

package net.corda.v5.crypto;

import net.corda.v5.base.annotations.CordaSerializable;
import net.corda.v5.base.annotations.DoNotImplement;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

/**
 * A digital signature scheme.
 */
@CordaSerializable
@DoNotImplement
public interface SignatureSpec {

    /**
     * Gets the signature-scheme name as required to create {@link java.security.Signature} objects
     * (for example, <code>SHA256withECDSA</code>).
     *
     * @return A string containing the signature name.
     */
    @NotNull
    String getSignatureName();
}

```

## package-info.java

```kotlin

@Export
package net.corda.v5.crypto;

import org.osgi.annotation.bundle.Export;

```
