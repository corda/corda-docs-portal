---
aliases:
- /contract-whitelisting.html
date: '2020-01-08T09:59:25Z'
menu: []
tags:
- contract
- whitelisting
title: Contract Whitelist Generation
---


# Contract Whitelist Generation

When setting or updating the network parameters, the Network Map Service scans the `.jar` files referenced in the
configuration file (i.e. *cordappsJar* ) for the presence of any contract classes. If such a class is found then it is
added to the whitelist. It is possible to exclude certain contract classes by adding their package names to the
*exclude* section of the configuration file. A user can also define the whitelist using the contract classes and
corresponding `.jar` hashes explicitly. To do so, the `contracts` attribute holding the list of the explicitly specified
whitelisted contracts needs to be set. Following is an example of the contract whitelist generation specific
configuration:

```guess
whitelistContracts = {
    cordappsJars = [
        "/Path/To/CorDapp/JarFile1",
        "/Path/To/CorDapp/JarFile2"
    ],
    exclude = [
        "com.cordapp.contracts.ContractToExclude1",
        "com.cordapp.contracts.ContractToExclude2"
    ],
    contracts = [
        {
            className = "com.cordapp.contracts.Contract1",
            attachmentIds = [ "C9FD27992C01F4DA04F060382F52039E3B2024D46092A890BED80BB2BE58E5B9", "AAAD27992C01F4DA04F060382F52039E3B2024D46092A890BED80BB2BE58E5B9" ]
        },
        {
            className = "com.cordapp.contracts.Contract2",
            attachmentIds = [ "C9FD27992C01F4DA04F060382F52039E3B2024D46092A890BED80BB2BE58E5B9" ]
        }
    ]
}
```

{{< note >}}
The `exclude` option allows for filtering contracts during the whitelisting process. For example:
If a `.jar` file consists of multiple contracts but only some of them need to be whitelisted, then the *exclude* list
should consist of class names only of those contracts that should NOT be included in the whitelist.
If both `cordappsJars` and `contracts` are set, then the union of both is considered in the network parameters.

{{< /note >}}
