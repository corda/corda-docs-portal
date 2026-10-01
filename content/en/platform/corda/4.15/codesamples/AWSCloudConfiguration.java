package com.r3.corda.hsm.sample.aws;

import com.r3.corda.utils.cryptoservice.CryptoServiceCredentials;
import net.corda.nodeapi.internal.config.CustomConfigParser;

@CustomConfigParser(parser = AWSCloudConfigurationParser.class)
public class AWSCloudConfiguration implements CryptoServiceCredentials<AWSCloudConfiguration> {
    private String username;
    private String password;
    private String partition;

    public AWSCloudConfiguration(
            String username,
            String password,
            String partition) {
        this.username = username;
        this.password = password;
        this.partition = partition;
    }

    public boolean samePartition(AWSCloudConfiguration other) {
        // Public keys are shared between multiple HSM users, so we have to use different aliases within the same HSM instance.
        return partition.equals(other.partition);
    }

    public String getUsername() {
        return username;
    }

    public String getPassword() {
        return password;
    }

    public String getPartition() {
        return partition;
    }
}