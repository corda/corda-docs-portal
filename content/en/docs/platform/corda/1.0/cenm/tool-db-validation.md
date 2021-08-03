---
aliases:
- /releases/release-1.0/tool-db-validation.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-0:
    identifier: cenm-1-0-tool-db-validation
    parent: cenm-1-0-tools-index
    weight: 1050
tags:
- tool
- db
- validation
title: DB Configuration Validation
---


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


0 - Success
1 - Unknown Error
2 - Missing driver error
3 - Outstanding migrations


