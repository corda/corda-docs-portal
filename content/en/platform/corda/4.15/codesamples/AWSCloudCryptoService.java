package com.r3.corda.hsm.sample.aws;

import com.cavium.cfm2.CFM2Exception;
import com.cavium.cfm2.LoginManager;
import com.cavium.cfm2.Util;
import com.cavium.key.CaviumKey;
import com.cavium.key.parameter.CaviumAESKeyGenParameterSpec;
import com.cavium.key.parameter.CaviumECGenParameterSpec;
import com.cavium.key.parameter.CaviumRSAKeyGenParameterSpec;
import com.r3.corda.utils.cryptoservice.AuthenticatedBlock;
import com.r3.corda.utils.cryptoservice.CryptoServiceAdmin;
import com.r3.corda.utils.cryptoservice.JCACryptoService;
import net.corda.core.crypto.Crypto;
import net.corda.core.crypto.SignatureScheme;
import net.corda.core.crypto.internal.Instances;
import net.corda.nodeapi.internal.cryptoservice.CryptoService;
import net.corda.nodeapi.internal.cryptoservice.CryptoServiceException;
import net.corda.nodeapi.internal.cryptoservice.WrappedPrivateKey;
import net.corda.nodeapi.internal.cryptoservice.WrappingMode;
import org.jetbrains.annotations.NotNull;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.security.*;
import java.security.spec.AlgorithmParameterSpec;
import java.security.spec.RSAKeyGenParameterSpec;
import java.util.UUID;
import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.security.auth.x500.X500Principal;

public class AWSCloudCryptoService extends JCACryptoService implements CryptoServiceAdmin {
    public static String NAME = "AWS_CLOUD_SAMPLE";
    private static Logger logger = LoggerFactory.getLogger(AWSCloudCryptoService.class);
    private LoginManager loginManager = LoginManager.getInstance();
    private AWSCloudConfiguration config;

    AWSCloudCryptoService(KeyStore keyStore, Provider provider, X500Principal x500Principal, AWSCloudConfiguration config) {
        super(keyStore, provider, x500Principal);
        this.config = config;
    }

    public boolean isLoggedIn() {
        try {
            return loginManager.isLoggedIn();
        } catch (Exception e) {
            logger.warn("Exception in isLoggedIn(): " + e.getMessage());
            return false;
        }
    }

    @Override
    public void logIn() throws CryptoServiceException {
        try {
            loginManager.login(config.getPartition(), config.getUsername(), config.getPassword());
        } catch (CFM2Exception e) {
            if (CFM2Exception.isClientDisconnectError(e)) {
                // Throw recoverable exception on socket disconnect
                throw new CryptoServiceException(e.getMessage(), e, true);
            }
            throw new CryptoServiceException(e.getMessage(), e, false);
        } catch (Exception e) {
            throw new CryptoServiceException(e.getMessage(), e, false);
        }
    }

    @Override
    public <T> T withAuthentication(@NotNull AuthenticatedBlock<? extends T> block) throws CryptoServiceException {
        try {
            return super.withAuthentication(block);
        } catch (CryptoServiceException e) {
            throw e;
        } catch (IllegalArgumentException e) {
            throw e;
        } catch (IllegalStateException e) {
            throw e;
        } catch (Exception e) {
            throw new CryptoServiceException(e.getMessage(), e, false);
        }
    }

    public SignatureScheme defaultIdentitySignatureScheme() {
        return Crypto.ECDSA_SECP256R1_SHA256;
    }

    public SignatureScheme defaultTLSSignatureScheme() {
        return Crypto.ECDSA_SECP256R1_SHA256;
    }

    @Override
    public PublicKey generateKeyPair(String alias, SignatureScheme scheme) throws CryptoServiceException {
        return withAuthentication(() -> {
            String publicAlias = toPublic(alias);
            String privateAlias = toPrivate(alias);
            logger.trace("CryptoService(action=generate_key_pair_start;alias='" + alias + "';scheme='" + scheme + "'");
            // Multiples keys can be stored under the same alias, so we need to check existing keys first
            Key publicKey;
            try {
                publicKey = getKeyStore().getKey(publicAlias, null);
            } catch (Exception e) {
                throw new CryptoServiceException("Exception getting public key from key store for alias '" + alias + "'", e, false);
            }

            if (publicKey != null) {
                throw new CryptoServiceException("Public key already exists in key store for alias '" + publicAlias + "'", null, false);
            }

            Key privateKey;
            try {
                privateKey = getKeyStore().getKey(privateAlias, null);
            } catch (Exception e) {
                throw new CryptoServiceException("Exception getting private key from key store for alias '" + alias + "'", e, false);
            }

            if (privateKey != null) {
                throw new CryptoServiceException("Private key already exists in key store for alias '" + publicAlias + "'", null, false);
            }

            KeyPairGenerator keyPairGenerator = keyPairGeneratorFromScheme(scheme, publicAlias, privateAlias, false, true);
            KeyPair keyPair = keyPairGenerator.generateKeyPair();
            try {
                getKeyStore().setKeyEntry(privateAlias, keyPair.getPrivate(), null, selfSign(scheme, keyPair));
            } catch (Exception e) {
                throw new CryptoServiceException("Exception setting private key in key store", e, false);
            }

            logger.trace("CryptoService(action=generate_key_pair_end;alias='" + alias + "';scheme='" + scheme + "'");
            return Crypto.toSupportedPublicKey(keyPair.getPublic());
        });
    }

    public boolean containsKey(String alias) {
        return super.containsKey(toPublic(alias)) || super.containsKey(alias);
    }

    public PublicKey getPublicKey(String alias) throws CryptoServiceException {
        return withAuthentication(() -> {
            logger.trace("CryptoService(action=key_get_start;alias='" + alias + "')");
            Key key;
            try {
                key = getKeyStore().getKey(toPublic(alias), null);
            } catch (Exception e) {
                logger.error("Exception getting key from key store: " + e.getMessage());
                throw new CryptoServiceException("Exception getting key from key store", e, false);
            }

            if (key == null) {
                return null;
            }

            if (!(key instanceof PublicKey)) {
                throw new CryptoServiceException("Key with alias '" + alias + "': Key store returned object is of type " +
                        key.getClass().getSimpleName() + ", but should be of type PublicKey", null, false);
            }

            PublicKey publicKey = (PublicKey)key;
            PublicKey supportedKey = Crypto.toSupportedPublicKey(publicKey);
            logger.trace("CryptoService(action=key_get_end;alias='" + alias + "')");
            return supportedKey;
        });
    }

    public byte[] sign(String alias, byte[] data, String signAlgorithm) throws CryptoServiceException {
        return super.sign(toPrivate(alias), data, signAlgorithm);
    }

    public void delete(String alias) throws CryptoServiceException {
        withAuthentication(() -> {
            try {
                Key k1 = getKeyStore().getKey(toPublic(alias), null);
                if (k1 != null) {
                    Util.deleteKey((CaviumKey) k1);
                }
                Key k2 = getKeyStore().getKey(toPrivate(alias), null);
                if (k2 != null) {
                    Util.deleteKey((CaviumKey) k2);
                }
                Key k3 = getKeyStore().getKey(alias, null);
                if (k3 != null) {
                    Util.deleteKey((CaviumKey) k3);
                }
            } catch (Exception e) {
                throw new CryptoServiceException("Error deleting alias '" + alias + "' from CryptoService.", e, true);
            }

            return 0; // Return type needed in withAuthentication
        });
    }

    @Override
    public synchronized void createWrappingKey(String alias, boolean failIfExists) throws CryptoServiceException {
        withAuthentication(() -> {
            try {
                boolean exists = false;
                try {
                    if (getKeyStore().getKey(alias,null) != null) {
                        exists = true;
                    }
                } catch (UnrecoverableKeyException e) {
                }

                if (exists) {
                    if (failIfExists) {
                        throw new IllegalArgumentException("There is an existing key with the alias: " + alias);
                    } else {
                        return 0;
                    }
                }
            } catch (IllegalArgumentException e) {
                throw e;
            } catch (Exception e) {
                throw new CryptoServiceException("Exception checking if keystore contains alias: '" + alias + "'", e, false);
            }

            try {
                KeyGenerator keyGenerator = KeyGenerator.getInstance("AES", getProvider());
                keyGenerator.init(new CaviumAESKeyGenParameterSpec(wrappingKeySize(), alias, false, true));
                SecretKey wrappingKey = keyGenerator.generateKey();
                getKeyStore().setKeyEntry(alias, wrappingKey, null, null);
            } catch (Exception e) {
                throw new CryptoServiceException("Exception wrapping key for alias: '" + alias + "'", e, false);
            }

            return 0; // Return type needed in withAuthentication
        });
    }

    @Override
    public kotlin.Pair<PublicKey, WrappedPrivateKey> generateWrappedKeyPair(String masterKeyAlias, SignatureScheme childKeyScheme) throws CryptoServiceException {
        return withAuthentication(() -> {
            Key key;
            try {
                key = getKeyStore().getKey(masterKeyAlias,null);
                if (key == null) {
                    throw new IllegalStateException("No master key under the alias: '" + masterKeyAlias + "'");
                }

                if (!(key instanceof SecretKey)) {
                    throw new CryptoServiceException("Master key under the alias: '" + masterKeyAlias + "': Object is of type " +
                            key.getClass().getSimpleName() + ", but should be of type SecretKey", null, false);
                }
            } catch (Exception e) {
                throw new IllegalStateException("There is no master key under the alias: " + masterKeyAlias);
            }

            SecretKey wrappingKey = (SecretKey)key;
            Cipher cipher;
            try {
                // AES Key Wrap (RFC 3394) with PKCS#5 padding
                cipher = Cipher.getInstance("AESWrap/ECB/PKCS5Padding", getProvider());
                cipher.init(Cipher.WRAP_MODE, wrappingKey);
            } catch (Exception e) {
                throw new CryptoServiceException("Unable to init cipher", e, false);
            }

            KeyPairGenerator keyPairGenerator;
            String alias = UUID.randomUUID().toString();
            try {
                keyPairGenerator = keyPairGeneratorFromScheme(childKeyScheme, toPublic(alias), toPrivate(alias), true, false);
            } catch (Exception e) {
                throw new CryptoServiceException("Unable to get keypair generator from scheme", e, false);
            }

            byte[] privateKeyMaterial;
            KeyPair keyPair;
            try {
                keyPair = keyPairGenerator.generateKeyPair();
                privateKeyMaterial = cipher.wrap(keyPair.getPrivate());
            } catch (Exception e) {
                throw new CryptoServiceException("Unable to wrap key", e, false);
            }

            try {
                Util.deleteKey((CaviumKey)keyPair.getPublic());
                Util.deleteKey((CaviumKey)keyPair.getPrivate());
            } catch (Exception e) {
                throw new CryptoServiceException("Unable to delete key", e, false);
            }

            PublicKey publicKey = Crypto.toSupportedPublicKey(keyPair.getPublic());
            return new kotlin.Pair<>(publicKey, new WrappedPrivateKey(privateKeyMaterial, childKeyScheme, null));
        });
    }

    @Override
    public byte[] sign(String masterKeyAlias, WrappedPrivateKey wrappedPrivateKey, byte[] payloadToSign) throws CryptoServiceException {
        return withAuthentication(() -> {
            try {
                Key wrappingKey = getKeyStore().getKey(masterKeyAlias, null);
                if (wrappingKey == null || !(wrappingKey instanceof SecretKey)) {
                    throw new IllegalStateException("There is no master key under the alias: " + masterKeyAlias);
                }

                Cipher cipher = Cipher.getInstance("AESWrap/ECB/PKCS5Padding", getProvider());
                cipher.init(Cipher.UNWRAP_MODE, wrappingKey);

                String algorithm = keyAlgorithmFromScheme(wrappedPrivateKey.getSignatureScheme());
                Key priKey = cipher.unwrap(wrappedPrivateKey.getKeyMaterial(), algorithm, Cipher.PRIVATE_KEY);
                if (!(priKey instanceof PrivateKey)) {
                    throw new CryptoServiceException("Key is not an instance of PrivateKey.", null, false);
                }

                PrivateKey privateKey = (PrivateKey) priKey;
                Signature signature = Instances.INSTANCE.getSignatureInstance(wrappedPrivateKey.getSignatureScheme().getSignatureName(), getProvider());
                signature.initSign(privateKey);
                signature.update(payloadToSign);
                byte[] signedData = signature.sign();
                Util.deleteKey((CaviumKey) privateKey);
                return signedData;
            } catch (CryptoServiceException e) {
                throw e;
            } catch (IllegalStateException e) {
                throw e;
            } catch (Exception e) {
                throw new CryptoServiceException("Cannot sign with alias: " + masterKeyAlias, e, false);
            }
        });
    }

    public WrappingMode getWrappingMode() {
        return WrappingMode.WRAPPED;
    }

    private String toPublic(String val) {
        return val + ":public";
    }

    private String toPrivate(String val) {
        return val + ":private";
    }

    private KeyPairGenerator keyPairGeneratorFromScheme(SignatureScheme scheme, String publicAlias, String privateAlias,
                                                        boolean extractable, boolean persistent) throws CryptoServiceException {
        String algorithm = keyAlgorithmFromScheme(scheme);
        AlgorithmParameterSpec params;
        if (scheme.getSchemeCodeName().equals(Crypto.ECDSA_SECP256R1_SHA256.getSchemeCodeName())) {
            params = new CaviumECGenParameterSpec("secp256r1", publicAlias, privateAlias, extractable, persistent);
        } else if (scheme.getSchemeCodeName().equals(Crypto.ECDSA_SECP256K1_SHA256.getSchemeCodeName())) {
            params = new CaviumECGenParameterSpec("secp256k1", publicAlias, privateAlias, extractable, persistent);
        } else if (scheme.getSchemeCodeName().equals(Crypto.RSA_SHA256.getSchemeCodeName())) {
            if (scheme.getKeySize() == null) {
                throw new CryptoServiceException("Key size must not be null for signature scheme RSA_SHA256", null, false);

            }
            params = new CaviumRSAKeyGenParameterSpec(scheme.getKeySize(), RSAKeyGenParameterSpec.F4, publicAlias, privateAlias, extractable, persistent);
        } else {
            throw new CryptoServiceException("No mapping for scheme ID '" + scheme.getSchemeNumberID() + "' [" + scheme.getSchemeCodeName() + "]", null, false);
        }

        KeyPairGenerator keyPairGenerator;
        try {
            keyPairGenerator = KeyPairGenerator.getInstance(algorithm, getProvider());
            keyPairGenerator.initialize(params);
        } catch (Exception e) {
            throw new CryptoServiceException("Cannot initialize key pair generator", e, false);
        }

        return keyPairGenerator;
    }

    private String keyAlgorithmFromScheme(SignatureScheme scheme) throws CryptoServiceException {
        if (scheme.getSchemeCodeName().equals(Crypto.ECDSA_SECP256R1_SHA256.getSchemeCodeName())) {
            return "EC";
        } else if (scheme.getSchemeCodeName().equals(Crypto.ECDSA_SECP256K1_SHA256.getSchemeCodeName())) {
            return "EC";
        } else if (scheme.getSchemeCodeName().equals(Crypto.RSA_SHA256.getSchemeCodeName())) {
            return "RSA";
        } else {
            throw new CryptoServiceException("No algorithm for scheme ID '" + scheme.getSchemeNumberID() + "'", null, false);
        }
    }

    static CryptoService fromConfiguration(X500Principal x500Principal, AWSCloudConfiguration config) throws CryptoServiceException {
        // Registered provider is required for CaviumSignature
        try {
            Provider provider = new com.cavium.provider.CaviumProvider();
            Security.addProvider(provider);
            KeyStore keyStore = KeyStore.getInstance("CloudHSM", provider);
            keyStore.load(null, null);
            return new AWSCloudCryptoService(keyStore, provider, x500Principal, config);
        } catch (Exception e) {
            throw new CryptoServiceException("Exception creating Crypto service", e, false);
        }
    }
}
