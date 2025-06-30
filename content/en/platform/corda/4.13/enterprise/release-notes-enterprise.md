---
title: Corda Enterprise Edition 4.13 release notes
date: '2025-06-30'

menu:
  corda-enterprise-4-13:
    identifier: corda-enterprise-4-13-release-notes
    parent: about-corda-landing-4-13-enterprise
    name: "Release notes"
tags:
- release
- notes
- enterprise

weight: 10
---

# Corda Enterprise Edition 4.13 release notes

The Corda Enterprise Edition 4.13 release introduces .... In this release, Java has been upgraded to Java x from Java x and Kotlin has been upgraded to Kotlin x from x.

When a CorDapp(s) and a node are successfully upgraded to 4.13, you are able to seamlessly interoperate 4.12 and 4.11 (or earlier) nodes on the same network, including the existing transactions on the ledger.

Supporting new Java and Kotlin versions is a major feature, as we must also handle legacy contracts from existing backchains. The upgraded Java and Kotlin versions also have implications for CorDapp developers. Simply replacing the Corda JAR without introducing other changes is not possible.

### Upgrade recommendation

{{< important >}}
When upgrading a node to Corda 4.13, it is extremely important that you run the Transaction Validator Utility on your node database to verify that the transactions in the old node are compatible with 4.12 nodes.

To ensure compatibility of the transactions, you must also run the Transaction Validator Utility on any older nodes that are not being upgraded and will likely interact with any upgraded nodes.

For more information, see [Transaction Validator Utility]({{< relref "node/operating/tvu/_index.md" >}}).
{{< /important >}}

As a developer or node operator, you should upgrade to the [latest released version of Corda]({{< relref "../enterprise/_index.md" >}}) as soon as possible. The latest Corda Enterprise release notes are on this page, and for the latest upgrade guide, refer to [Corda Enterprise Edition 4.12 to 4.13 upgrade guide]({{< relref "upgrade-guide.md" >}}).

The steps from this guide only work for direct upgrades from Corda 4.12 to 4.13. If you have any nodes on versions 4.11 and below, you must upgrade them to 4.12 first. To do that, consult the relevant release upgrade documentation.

### Platform version change

Corda 4.13 uses platform version xxxx.

For more information about platform versions, see [Versioning]({{< relref "cordapps/versioning.md" >}}).

### New features, enhancements and restrictions

* [Multiple thread pools can now be defined and have flows assigned to them]({{< relref "cordapps/thread-pools.md" >}}). Thread pools enable operators to prioritize particular flows and to segregate them from other flows.

### Fixed issues



### Known issues

 
### Third party component upgrades

**Following table needs to be updated for 4.13**

The following table lists the dependency version changes between 4.11 and 4.12 Enterprise Editions:

| Dependency                                     | Name                   | Version 4.11 Enterprise   | Version 4.12 Enterprise  |
|------------------------------------------------|------------------------|---------------------------|------------------------- |
| com.google.guava:guava                         | Guava                  | 28.0-jre                  | 33.1.0-jre               |
| co.paralleluniverse:quasar-core	               | Quasar	                | 0.7.16_r3	                | 0.9.0_r3                 |
| org.bouncycastle	                             | Bouncy Castle	        | jdk18on:1.75	            | lts8on:2.73.6            |
| pro com.guardsquare:proguard-gradle	           | ProGuard	              | 6.1.1	                    | 7.3.1                    |
| org.yaml:snakeyaml	                           | SnakeYAML	            | 1.33	                    | 2.2                      |
| com.github.ben-manes.caffeine:caffeine         | Caffeine	              | 2.9.3	                    | 3.1.8                    |
| io.netty:netty-tcnative-boringssl-static	     | TC Native	            | 2.0.48.Final	            | 2.0.65.Final             |
| org.apache.commons:commons-configuration2      | Commons Configuration2	| 2.10.0	                  | 2.10.1                   |
| co.paralleluniverse:capsule	                   | Capsule	              | 1.0.3	                    | 1.0.4_r3                 |
| org.ow2.asm:asm	                               | ASM	                  | 7.1	                      | 9.5                      |
| org.apache.activemq:*	                         | Artemis	              | 2.19.1	                  | 2.32.0                   |
| com.fasterxml.jackson.*	                       | Jackson XML	          | 2.13.5	                  | 2.17.0                   |
| org.eclipse.jetty.ee10:jetty-ee10-*	           | Jetty	                | 9.4.53.v20231009	        | 12.0.7                   |
| org.glassfish.jersey.*	                       | Jersey	                | 2.25	                    | 3.1.6                    |
| javax.validation:validation-api	               | Validation	            | -	                        | 2.0.1.Final              |
| org.slf4j:*	Simpe                              | Log4J	                | 1.7.30	                  | 2.0.12                   |
| org.apache.logging.log4j:*	                   | Log4j	                | 2.17.1	                  | 2.23.1                   |
| com.squareup.okhttp3:okhttp	                   | OK HTTP	              | 3.14.9	                  | 4.12.0                   |
| io.netty:*	                                   | Netty                	| 4.1.77.Final	            | 4.1.109.Final            |
| org.apache.commons:commons-fileupload2-jakarta | File Upload	          | 1.4	                      | 2.0.0-M1                 |
| com.esotericsoftware:kryo	                     | Kryo	                  | 4.0.2	                    | 5.5.0                    |
| org.mockito:mockito-core	                     | Mockito	              | 2.28.2	                  | 5.5.0                    |
| org.mockito.kotlin:mockito-kotlin	             | Mockito for Kotlin	    | 1.6.0	                    | 5.2.1                    |
| org.jetbrains.dokka:dokka-gradle-plugin	       | Dokka for Gradle       | 0.10.1	                  | 1.8.20                   |
| net.i2p.crypto:eddsa	                         | EddSA	                | 0.3.0	                    | -                        |
| com.zaxxer:HikariCP	                           | Hikari	                | 3.3.1	                    | 5.1.0                    |
| org.iq80.snappy:snappy	                       | Snappy	                | 0.4	                      | 0.5                      |
| commons-io:commons-io	                         | Commons I/O	          | 2.6	                      | 2.7                      |
| org.javassist:javassist	                       | Java Assist	          | 3.27.0-GA	                | 3.29.2-GA                |
| org.jooq:joor	                                 | Joor	                  | -	                        | 0.9.15                   |
| org.apache.curator:*	                         | Apache Curator	        | 5.1.0	                    | 5.6.0                    |
| org.apache.zookeeper:zookeeper	               | Apache Zookeeper	      | -	                        | 3.8.3                    |
| org.apache.commons:commons-dbcp2	             | Apache Commons	        | -	                        | 2.12.0                   |
