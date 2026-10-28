package com.r3.corda.hsm.sample.aws;

import com.typesafe.config.Config;
import net.corda.nodeapi.internal.config.ConfigParser;
import org.jetbrains.annotations.NotNull;

public class AWSCloudConfigurationParser implements ConfigParser<AWSCloudConfiguration> {
    @Override
    public AWSCloudConfiguration parse(@NotNull Config config) {
        return new AWSCloudConfiguration(
                config.getString("username"),
                config.getString("password"),
                config.getString("partition")
        );
    }
}
