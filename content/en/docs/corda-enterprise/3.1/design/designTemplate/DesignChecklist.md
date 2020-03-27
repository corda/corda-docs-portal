---
aliases:
- /releases/3.1/design/designTemplate/DesignChecklist.html
date: '2020-01-08T09:59:25Z'
menu: []
tags:
- DesignChecklist
title: DesignChecklist
---
{{% important %}}
This documentation is unsupported.
Try [Corda Enterprise 3.3 documentation](/docs/corda-enterprise/3.3/_index.md) instead
{{% /important %}}

**Design review functionality checklist**

Does the design impact performance?

Does the design impact availability/disaster recovery?

Does the design impact operability (monitoring or management)?

Does the design impact security?

Does the design impact privacy of data on the ledger?

Does the design break API stability?

Does the design break wire stability?

Does the design break binary compatibility for OS CorDapps with Enterprise?

Does the design introduce any new dependencies on 3rd party libraries?

Does the design work with a mixed network of OS and Enterprise Corda nodes?

Does the design imply a change in deployment architecture/configuration?

Does the design introduce any potentially patentable IP?

