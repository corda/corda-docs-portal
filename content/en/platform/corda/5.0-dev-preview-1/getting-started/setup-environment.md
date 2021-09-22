---
date: '2021-09-06'
title: "Setting up your development environment"
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-gettingstarted
    weight: 200
project: corda-5
section_menu: corda-5-dev-preview
---

Before you deploy a local network and start working with Corda 5 developer preview, you must perform all the following steps to set up your development environment:

1.	Install the Corda CLI tool by following the steps from the [Installing Corda CLI](XXX) procedure.

2. You need Zulu OpenJDK 11 to compile CorDapps. Use the `java -version` command from a shell to verify if you have Zulu OpenJDK and which version.

   If you do not have Zulu OpenJDK installed or your version is lower than 11, install Zulu OpenJDK 11.

3. Install Docker. You will use it to run a local Corda network.

   After installing Docker, open Docker Desktop and perform one of the following steps:

    * If you are a Mac user, go to **Preferences** and configure Docker Desktop to have at least 6GB of RAM and use 6 cores.
    * If you are a Windows user, go to **Settings > General** and select the following options: **Expose daemon on tcp://localhost:2375 without TLS** and **Use the WSL 2 based engine**.

4. Install Docker Compose using a shell such as Bash, or Git Bash for Windows.
