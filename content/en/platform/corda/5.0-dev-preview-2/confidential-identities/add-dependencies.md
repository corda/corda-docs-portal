---
date: '2020-09-10'
title: "Add dependencies to a CorDapp"
menu:
  corda-5-dev-preview:
    identifier: corda-5-dev-preview-1-confidential-identities-dependencies
    weight: 300
    parent: corda-5-dev-preview-1-confidential-identities
section_menu: corda-5-dev-preview

---

1. Add a variable for the confidential identities release group and the version you wish to use. Set the Corda version to the one you have installed locally:

    ```
      buildscript {
          ext {
              confidential_id_release_version = '2.0.0-DevPreview-RC05'
              confidential_id_release_group = 'com.r3.corda.lib.ci'
            }
          }
    ```

2.  Add the confidential identities' development artifactory repository to the list of repositories for your project:

    ```
      repositories {
          maven { url 'https://software.r3.com/artifactory/corda-os-maven-stable' }
        }
    ```

3. Add the confidential identities SDK dependency to the `dependencies` block in your CorDapp module (where applicable).

    cordapp "$confidential_id_release_group:ci-workflows:$confidential_id_release_version"

4. Deploy your corDapp CPKs along with the following CPKs:
    * ci-workflows

    You have installed the Confidential Identities SDK.
