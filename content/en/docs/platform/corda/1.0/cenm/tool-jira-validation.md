---
aliases:
- /releases/release-1.0/tool-jira-validation.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-0:
    identifier: cenm-1-0-tool-jira-validation
    parent: cenm-1-0-tools-index
    weight: 1060
tags:
- tool
- jira
- validation
title: Jira Configuration Validation
---


# Jira Configuration Validation

To test the credentials within the Doorman’s Jira configuration and to thus ensure
the server is still contactable by the Doorman, the jira validator can be found in the utilities package.

This will make a connection using the credentials specified in the configuration file to the Jira
instance and validate permissions for the user.

```shell
java -jar utilities-<version>.jar jira-validate --config-file <config file>
```


## Results

On successful connection and validation the tool will print this affirmation to the console and
set errno to 0.

On encountering any error the tool will print out the cause and set errno appropriately.

Exit codes are as follows


0 - Success
1 - Unknown Error
2 - Specified configuration file is not a Doorman
3 - Specified configuration file doesn’t configure a Jira instance
4 - The Jira instance is unreachable at the specified UR
5 - Specified user is invalid
6 - Specified password is either incorrect or the user needs further validation (captcha entry)
7 - Specified project does not exist


