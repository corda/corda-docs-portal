+++
date = "2020-01-08T09:59:25Z"
title = "DB Configuration Validation"
aliases = [ "/releases/release-1.0/tool-db-validation.html",]
menu = [ "cenm-1-0",]
tags = [ "tool", "db", "validation",]
+++


# DB Configuration Validation

To test the credentials within the Doorman’s database configuration and to thus ensure
            the database server is still contactable by the Doorman, the database validator can be found in the utilities package.

This will make a connection using the credentials specified in the configuration file to the database
            instance and validate the data access.

```shell
java -jar utilities-<version>.jar db-validate --config-file <config file>
```

## Results

On successful connection and validation the tool will print this affirmation to the console and
                set errno to 0.

On encountering any error the tool will print out the cause and set errno appropriately.

Exit codes are as follows

> 
> 0 - Success
>                     1 - Unknown Error
>                     2 - Missing driver error
>                     3 - Outstanding migrations


