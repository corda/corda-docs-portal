package com.r3.corda.hsm.sample.aws;

import com.r3.corda.utils.cryptoservice.CryptoServiceProvider;
import net.corda.nodeapi.internal.cryptoservice.CryptoService;
import net.corda.nodeapi.internal.cryptoservice.CryptoServiceException;
import org.jetbrains.annotations.NotNull;

import javax.security.auth.x500.X500Principal;

public class AWSCloudCryptoServiceProvider implements CryptoServiceProvider<AWSCloudConfiguration> {
    private Class configurationType = AWSCloudConfiguration.class;

    @NotNull
    @Override
    public String getName() {
        return AWSCloudCryptoService.NAME;
    }

    @NotNull
    @Override
    public Class getConfigurationType() {
        return configurationType;
    }

    public CryptoService createCryptoService(X500Principal x500Principal, AWSCloudConfiguration configuration) throws CryptoServiceException {
        return AWSCloudCryptoService.fromConfiguration(x500Principal, configuration);
    }
}
