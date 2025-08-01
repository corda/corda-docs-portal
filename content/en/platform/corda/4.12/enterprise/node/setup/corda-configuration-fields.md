---
date: '2021-11-24T18:55:00Z'
menu:
  corda-enterprise-4-12:
    parent: corda-enterprise-4-12-corda-nodes-configuring
tags:
- corda
- configuration
- file
title: Configuration fields
weight: 4
---

# Configuration fields

{{< note >}}
The available configuration fields are listed below in alphabetic order.
{{< /note >}}

## `additionalP2PAddresses`

An array of additional host:port values, which will be included in the advertised NodeInfo in the network map in addition to the `p2pAddress`.
Nodes can use this configuration option to advertise HA endpoints and aliases to external parties.
0.0.0.0 is not a valid host setting since each additionalP2PAddress must be an external client address.

*Default:* empty list

## `attachmentContentCacheSizeMegaBytes`

Optionally specify how much memory should be used to cache attachment contents in memory.

*Default:* 8 MB plus 5% of all heap memory above 300MB.

## `blacklistedAttachmentSigningKeys`

List of SHA-256 hashes of public keys. Attachments signed by any of these public keys will not be considered as trust roots for any attachments received over the network.
This property is similar to `cordappSignerKeyFingerprintBlacklist` but only restricts CorDapps that were
included as attachments in a transaction and received over the network from a peer.

This property requires retrieving the hashes of public keys that need to be blacklisted.

  *Default:* not defined

## `compatibilityZoneURL`

{{< important >}}
Deprecated. Use `networkServices` instead.
{{< /important >}}

The root address of the Corda compatibility zone network management services, it is used by the Corda node to register with the network and obtain a Corda node certificate, and also is used by the node to obtain network map information.
Cannot be set at the same time as the `networkServices` option.

*Default:* not defined

## `cordappSignerKeyFingerprintBlacklist`

List of the public keys fingerprints (SHA-256 of public key hash) not allowed as Cordapp JARs signers.
The node will not load Cordapps signed by those keys.
The option takes effect only in production mode and defaults to Corda development keys (`["56CA54E803CB87C8472EBD3FBC6A2F1876E814CEEBF74860BD46997F40729367", "83088052AF16700457AE2C978A7D8AC38DD6A7C713539D00B897CD03A5E5D31D"]`), in development mode any key is allowed to sign Cordpapp JARs.

This property requires retrieving the hashes of public keys that need to be blacklisted.

*Default:* not defined

## `crlCheckArtemisServer`

Set this configuration field to `true` to enable CRL checking of TLS certificates for inbound P2P connections into the embedded Artemis messaging server. The CRL checking mode is defined by `crlCheckSoftFail` option.

This setting is only relevant for node configurations with no Corda Firewall enabled. If you set this field to `true`, ensure that the connection links to the CRL distribution endpoints are reliable and operational (for example, not behind a firewall), otherwise these connections may be dropped.

*Default:* `false`

## `crlCheckSoftFail`

This is a boolean flag that when enabled (that is, `true` value is set) causes certificate revocation list (CRL) checking to use soft fail mode.
Soft fail mode allows the revocation check to succeed if the revocation status cannot be determined because of a network error.
If this parameter is set to `false` rigorous CRL checking takes place. This involves each certificate in the certificate path being checked for a CRL distribution point extension, and that this extension points to a URL serving a valid CRL.
This means that if any CRL URL in the certificate path is inaccessible, the connection with the other party will fail and be marked as bad.
Additionally, if any certificate in the hierarchy, including the self-generated node SSL certificate, is missing a valid CRL URL, then the certificate path will be marked as invalid.

By default, CRL checking is applicable only for outbound P2P connections. To enable it also for inbound P2P connections, set `crlCheckArtemisServer=true`.

If a proxy is configured for HTTP connections to network services, you can optionally use it for CRL checking. To do so, specify the following Java system properties:

* `http.proxyHost` and `http.proxyPort` for HTTP proxy
* `socksProxyHost` and `socksProxyPort` for SOCKS proxy

To use proxy with authentication, you must also configure:
* Java system properties
* proxy parameters in the `networkServices` section

For example:
  ```json
    custom.jvmArgs = ["-Dhttp.proxyHost=198.51.100.5", "-Dhttp.proxyPort=3128"]
    crlCheckSoftFail = true
    crlCheckArtemisServer = true
    networkServices {
        doormanURL = "https://cz.example.com"
        networkMapURL = "https://cz.example.com"
        proxyType = HTTP
        proxyAddress = "198.51.100.5:3128"
        proxyUser = my-user
        proxyPassword = my-password
    }
  ```

*Default:* true

## `cryptoServiceName`

Optional name of the CryptoService implementation. This only needs to be set if you intend to use a different provider than the default one.

## `cryptoServiceConf`

Optional path to the configuration file for the CryptoService provider. This may have to be present if you use a different CryptoService provider than the default one.

## `cryptoServiceFlowRetryCount`

`cryptoServiceFlowRetryCount` is used to specify which actions should be taken in the event of a flow suffering a CryptoServiceException due to a timeout.

The *absolute value* of `cryptoServiceFlowRetryCount` determines the number of times that the flow is retried. The *sign* of the value determines what happens when all retries are exhausted:

* If a *negative* value is specified, a `CryptoServiceException` is propagated back to the calling code and the flow fails; this was the default behaviour in versions of Corda before 4.10.
* If a *positive* value is specified, then the flow is held in the flow hospital paused until either:
  * the node is restarted
  * a node operator manually restarts the flow
  * a node operator manually kills the flow off

For example, if `cryptoServiceFlowRetryCount` is set to `-2`, then the flow is retried a maximum of two times. If it still fails, then the exception is propagated back to the code that invoked the flow and the flow failed.

*Default:* -2

## `cryptoServiceTimeout`

Optional time-out value of actions sent to the CryptoService (HSM). If the HSM takes longer than this duration to respond, then a `TimedCryptoServiceException` will be thrown and handled by the Flow Hospital. You can increase it to mitigate the time-out error.

*Default:* 10000 milliseconds

## `custom`

Set custom command line attributes (for example, Java system properties) on the node process via the capsule launcher or on the external verifier process.

* `jvmArgs`
  * A list of JVM arguments to apply to the node process. This removes any defaults specified from `corda.jar`, but can be overridden from the command line.
  * *Default:* not defined
* `externalVerifierJvmArgs`
  {{< important >}}
  This configuration field is only available from Corda 4.12.5 onwards. For more information, see the [4.12.5 release notes]({{< relref "../../release-notes-enterprise.md#fixed-issues" >}}).
  {{< /important >}}
  * A list of JVM arguments to apply to the external verifier process.
  * *Default:* not defined

## `database`

Database configuration

* `exportHibernateJMXStatistics`:
  * Whether to export Hibernate JMX statistics.  **Caution: enabling this option causes expensive run-time overhead**
  * *Default:* false
* `schema`
  * Some database providers require a schema name when generating DDL and SQL statements. The value is passed to the Hibernate    property 'hibernate.default_schema'. This is optional.
* `hibernateDialect`
  * Optional property for testing/development against an unsupported database. The value is passed to Hibernate `hibernate.dialect` option.     All supported databases don't require this option, as Hibernate sets the correct dialect value out of box.

## `dataSourceProperties`

This section is used to configure the JDBC connection and database driver used for the node's persistence.
To add additional data source properties (for a specific JDBC driver) use the `dataSource.` prefix with the property name (e.g. `dataSource.customProperty = value`).

* `dataSourceClassName`
  * JDBC Data Source class name.
* `dataSource.url`
  * JDBC database URL.
* `dataSource.user`
  * Database user.
* `dataSource.password`
  * Database password.

*Default:*

```
dataSourceClassName = org.h2.jdbcx.JdbcDataSource
dataSource.url = "jdbc:h2:file:"${baseDirectory}"/persistence;DB_CLOSE_ON_EXIT=FALSE;WRITE_DELAY=0;LOCK_TIMEOUT=10000"
dataSource.user = sa
dataSource.password = ""
```

## `detectPublicIp`

This flag toggles the auto IP detection behaviour.
If enabled, on startup the node will attempt to discover its externally visible IP address first by looking for any public addresses on its network interfaces, and then by sending an IP discovery request to the network map service.
Set to `true` to enable.

*Default:* false

## `devMode`

This flag sets the node to run in development mode.
On startup, if the keystore `<workspace>/certificates/sslkeystore.jks`
does not exist, a developer keystore will be used if `devMode` is true.
The node will exit if `devMode` is false and the keystore does not exist.
`devMode` also turns on background checking of flow checkpoints to shake out any bugs in the checkpointing process.
Also, if `devMode` is true, Hibernate will try to automatically create the schema required by Corda or update an existing schema in the SQL database; if `devMode` is false, Hibernate will simply validate the existing schema, failing on node start if the schema is either not present or not compatible.
If no value is specified in the node configuration file, the node will attempt to detect if it's running on a developer machine and set `devMode=true` in that case.
This value can be overridden from the command line using the `--dev-mode` option.

This flag affects the default value for Java heap size.

*Default:* Corda will try to establish based on OS environment

## `devModeOptions`

Allows modification of certain `devMode` features

{{< important >}}
This is an unsupported configuration.
{{< /important >}}

## `allowCompatibilityZone`

  Allows a node configured to operate in development mode to connect to a compatibility zone.

  *Default:* not defined

## `emailAddress`

The email address responsible for node administration, used by the Compatibility Zone administrator.

*Default:* company@example.com

## `enterpriseConfiguration`

Allows fine-grained controls of various features only available in the enterprise version of Corda.

* `mutualExclusionConfiguration`
  * Enable the protective heartbeat logic so that only one node instance is ever running (hot-cold deployment).
* `on`
  * Enables the logic. Values can be either true or false.
  * *Default:* false
* `updateInterval`
  * Interval in milliseconds used by the node to update the lock on the database.
  * *Default:* not defined
* `waitInterval`
  * Interval in milliseconds used by the node to try and acquire the lock on the database.
  * *Default:* not defined
* `healthCheck`
  * Enables the health check feature.
  * *Default:* true
* `externalBridge`
  * Enables P2P communication to pass through the Corda Firewall.
  * *Default:* false
* `identityKeyAlias`
  * The alias of the identity key. Allowed are up to 100 lower case alphanumeric characters and the hyphen (-).
  * *Default:* identity-private-key
* `clientCaKeyAlias`
  * The alias of the CA key. Allowed are up to 100 lower case alphanumeric characters and the hyphen (-).
  * *Default:* cordaclientca
* `distributedNotaryKeyAlias`
  * The alias of the distributed notary signing key alias (used if this node is a notary). Allowed are up to 100 lower case alphanumeric    characters and the hyphen (-).
  * *Default:* distributed-notary-private-key
* `messagingServerSslConfiguration`
  * TLS configuration used to connect to external P2P Artemis message server. Required when `messagingServerExternal` = `true`. Also, it can be used optionally with embedded Artemis when external Bridge is configured. For more information, see [Storing node TLS keys in HSM]({{< relref "tls-keys-in-hsm.md" >}}).
  * `sslKeystore`
    * The path to the KeyStore file to use in Artemis connections.
    * *Default:* not defined
  * `keyStorePassword`
    * The password for the TLS KeyStore.
    * *Default:* not defined
  * `trustStoreFile`
    * The path to the TrustStore file to use in Artemis connections.
    * *Default:* not defined
  * `trustStorePassword`
    * The password for TLS TrustStore.
    * *Default:* not defined
* `messagingServerConnectionConfiguration`
  * Mode used when setting up the Artemis client. Supported modes are:
    * **DEFAULT:** Five initial connect attempts, five reconnect attempts in case of failure, starting retry interval of five seconds with an exponential back-off multiplier of one and a half for up to three minutes retry interval.
    * **FAIL_FAST**: No initial attempts, no reconnect attempts.
    * **CONTINUOUS_RETRY**: Infinite initial and reconnect attempts, starting retry interval of five seconds with an exponential back-of multiplier of one and a half up for up to five minutes retry interval. Using 'CONTINUOUS_RETRY' does not mean that a node will keep retrying until it connects to the destination node. Rather, this is about connections to - and only for - an external HA Artemis client. Connected to an internal Artemis client will work. Note that an embedded Artemis client runs with node's TLS key, not with a shareable key like external Artemis. Also, CONTINUOUS_RETRY does not work for other Artemis bug reasons so the node disconnects from the external Artemis client and the node dies. We do guarantee trying to connect to an external Artemis client repeatedly on a fresh start.
* `messagingServerBackupAddresses`
  * List of Artemis Server back-up addresses. If any back-ups are specified, the client will be configured to automatically failover to the first server it can connect to.
  * *Default:* empty list
* `artemisCryptoServiceConfig`
  * This is an optional crypto service configuration which will be used for HSM TLS signing when interacting with the Artemis message server.
  * This option only makes sense when `messagingServerSslConfiguration` is specified: either to connect to a standalone Artemis messaging server, or when external Bridge is configured. If this option is missing, the local file system will be used to store private keys inside JKS key stores, as defined by `messagingServerSslConfiguration`.
  * `cryptoServiceName`
    * The name of HSM provider to be used. E.g.: `UTIMACO`, `GEMALTO_LUNA`, etc.
  * `cryptoServiceConf`
    * Absolute path to HSM provider specific configuration which will contain everything necessary to establish connection with HSM.
    * *Default:* Not present so local file system is used.
* `attachmentClassLoaderCacheSize`
  * This field can be used to configure the attachments class loader cache size - this is the number of attachment class loaders per cache. This cache caches the class loaders used to store the transaction attachments.
  * *Default:* The default value is `32` attachment class loaders per cache.
  * **IMPORTANT: The default value must not be changed unless explicitly advised by R3 support!**
* `auditService`
  * Allows for configuration of audit services within the node
    * `eventsToRecord` defines which types of events will be recorded by the audit service - currently supported types are `{NONE, RPC, ALL}`
    * *Default:* `NONE`
* `maintenanceMode`
  * An optional field used by [Node Maintenance Mode]({{< relref "../operating/maintenance-mode.md#configuration-of-node-maintenance-mode" >}}), which enables you to run certain house-keeping events automatically within Corda at specific times of the day or week, using a "_cron-like_" scheduling algorithm.
  * *Default:* Not present. By default, no maintenance activities will be performed if the `maintenanceMode` section is not provided. Without the new parameter, Corda will behave as if maintenance mode is not available.
  * If the `maintenanceMode` sub-section is provided, then **ALL** `maintenanceMode` parameters (as described below) must be supplied and must also pass configuration validation at start-up.
  * Parameters:
    * `schedule` is a *“cron-like”* expression, which is used to control at what time(s) the maintenance tasks are run. The format follows the existing cron standards using a 6-part time specification but omits the command line part of the expression as would be present in a Unix cron expression. Times are in **UTC**. See an example in [Node Maintenance Mode]({{< relref "../operating/maintenance-mode.md#configuration-of-node-maintenance-mode" >}}). For more information on *cron* (with examples) please see [cron-wiki](https://en.wikipedia.org/wiki/Cron) and note that the examples shown will include the *<command to execute>* part which is not present in the Corda `schedule`. The tasks that get run are not dependent on this configuration item and are determined *within* Corda. The following example will run maintenance at 14:30 and 15:30 (UTC) on Fridays (‘5’ in final column): `schedule = "00 30 14,15 * * 5"`.
    * `duration` is the maximum time that a maintenance window is expected to take to run all tasks. At start-up, Corda will check for all maintenance events that occur within the following week. If there is an overlap (due the specified duration being longer than the interval between any two adjacent maintenance windows), Corda Enterprise will emit a *warning* to the log which will precisely specify the overlap scenario but no further action will be taken. Additionally, if the time that the maintenance tasks *actually* take to run exceeds the specified duration, a warning will be emitted to the log but the maintenance tasks will not be interrupted. The purpose of the duration parameter is to allow the user to check that there are no overlaps and to allow monitoring of overrunning activities via log messaging and monitoring. The duration is specified in HOCON *duration* format with suffixes of `‘h’ (hours), ‘m’ (minutes) and ‘s’ (seconds)` - for example, `‘1h’` to mean one hour. For additional information on HOCON duration format parsing, see [HOCON-duration-format](https://github.com/lightbend/config/blob/master/HOCON.md#duration-format).
    * `rpcAuditDataRetentionPeriod` is a parameter to the RPC table maintenance task and specifies how long records should be kept for within the table for. The parameter is in HOCON *period* format - for example, `‘365d’, ‘1w’`. In general, the following suffixes should be sufficient: `‘d’ (days), ‘w’ (weeks), ‘m’ (months), ‘y’ (years)`. For more information on the HOCON period format see [HOCON-period-format](https://github.com/lightbend/config/blob/master/HOCON.md#period-format). The end of the retention period will be the current time (in UTC) minus the duration.
  * [Node Maintenance Mode]({{< relref "../operating/maintenance-mode.md#configuration-of-node-maintenance-mode" >}}) uses the `processedMessageCleanup` parameters (see below).
* `processedMessageCleanup`
  * An optional field that allows you to run the message ID cleanup task at shutdown. The same rules will apply for calculation of default values as when the activity runs at shutdown.
  * This field and its parameters are also used by the [Node Maintenance Mode]({{< relref "../operating/maintenance-mode.md#configuration-of-node-maintenance-mode" >}}) (`maintenanceMode` just above) functionality.
  * Parameters:
    * `generalRetentionPeriodInDays` indicates the number of days a message (sent during recovery) will be retained. If not specified, it will default to the specified `senderRetentionPeriodInDays` value plus the event horizon duration (or 365 days, if the event horizon is larger than 365 days).
    * `senderRetentionPeriodInDays` indicates the number of days a message (sent during normal operation) will be retained. If not specified, it will default to 7 days.
    * In both of these cases, these are sensible defaults and **you should only update them after serious consideration and when advised to do so by R3 support**. Reducing the value of these periods means the node will clean up records more eagerly, so storage from the table will be reclaimed more quickly. However, this also means there is a higher risk of processing some messages more than once.
  * Example:
  ```
  {
      enterpriseConfiguration {
          processedMessageCleanup {
              generalRetentionPeriodInDays = 365
              senderRetentionPeriodInDays = 7
          }
      }
  }
  ```
* `tlsCryptoServiceConfig`
  * Optional crypto service configuration to store node's TLS private key in HSM. If this option is missing, the TLS private key will be stored in the file-based `sslkeystore.jks`.
  * Parameters:
    * `cryptoServiceName`: the name of the CryptoService provider to be used.
    * `cryptoServiceConf`: the path to the configuration file for the CryptoService provider.
* `tlsKeyAlias`
  * The alias of the TLS key. It can consist of up to 100 lowercase alphanumeric characters and the hyphen (-).
  * *Default:* `cordaclienttls`
* `previousIdentityKeyAliases`
  * List of previous node identity key aliases after key rotation. For more information about this feature, contact your R3 account manager.
  * Default value: An empty list.
* `enableURLConnectionCache`
  * Enables URL connection caching. It is set to `false` by default and it is highly recommended to keep it that way.
  * When caching is enabled (set to `true`), JAR files will be cached, which can cause leaking of file handles. This is caused by the way the `ServiceLoader` handles JAR files that are children of the `URLClassLoader`. For more information, see [here](https://bugs.java.com/bugdatabase/view_bug.do?bug_id=8156014).
    * *Default:* `false`
* `metricsConfiguration`
  * Optional configuration section that controls metric configuration.
  * Parameters:
    * `reservoirType`: Sets the reservoir type. Valid values are `EDR` (default) and `TIME_WINDOW`. For more information, see the [metrics documentation]({{< relref "../operating/monitoring-and-logging/node-metrics.md" >}}).
    * `timeWindow`: Sets the data gathering duration for `TIME_WINDOW` data reservoirs. If not set, the default is five minutes.

* `tuning`

    * The Corda node configuration file section that contains performance tuning parameters for Corda Enterprise Nodes.

    - `backchainFetchBatchSize`

        * This is an optimization for sharing transaction backchains. Corda Enterprise nodes can request backchain items in bulk instead of one at a time. This field specifies the size of the batch. The value is just an integer indicating the maximum number of states that can be requested at a time during backchain resolution.
        * *Default:* 50

    - `brokerConnectionTtlCheckIntervalMs`

        * The interval at which acknowledgements of completed commands are to be sent in case `p2pConfirmationWindowSize` is not exhausted in time.
        * *Default:* 1 millisecond

    - `flowThreadPoolSize`

      The number of threads available to handle flows in parallel. This is the number of flows
  that can run in parallel doing something and/or holding resources like database connections.
    A larger number of flows can be suspended, for example, waiting for reply from a counterparty.
  When a response arrives, a suspended flow will be woken up if there are any available threads in the thread pool.

      Otherwise, a currently active flow must be finished or suspended before the suspended flow can be woken
  up to handle the event. This can have serious performance implications if the flow thread pool is too small, as a flow cannot be suspended while in a database transaction, or without checkpointing its state first.

      Corda Enterprise allows the node operators to configure the number of threads the state machine manager can use to execute flows in parallel, allowing more than one flow to be active and/or use resources at the same time.

      The ideal value for this parameter depends on a number of factors. These include the hardware the node is running on, the performance profile of the flows, and the database instance backing the node as datastore. Every thread will open a database connection, so for n threads, the database system must have at least n+1 connections available. Also, the database
  must be able to actually cope with the level of parallelism to make the number of threads worthwhile - if
  using for example H2, any number beyond eight does not add any substantial benefit due to limitations with its internal
  architecture. For these reasons, the default size for the flow framework thread pool is the lower number between either the available number of processors times two, and 30. Overriding this value in the configuration allows you to specify any number.

    - `rpcThreadPoolSize`

      * The number of threads handling RPC calls - this defines how many RPC requests can be handled
  in parallel without queueing. The default value is set to the number of available processor cores.
      * Incoming RPC calls are queued until a thread from this
  pool is available to handle the connection, prepare any required data and start the requested flow. As  this
  might be a non-trivial amount of work, the size of this pool can be configured in Corda Enterprise.
      * On a multicore machine with a large `flowThreadPoolSize`, this might need to be increased, to avoid flow threads being idle while the payload is being deserialized and the flow invocation run.
      * If there are idling flow threads while RPC calls are queued, it might be worthwhile increasing this * number slightly.
      * Valid values for this property are between 4 (that is the number used for the single threaded state * machine in open source) and the number of flow threads.

    - `journalBufferTimeout`
      * The interval (in nanoseconds) at which Artemis messages that are buffered in-memory will be flushed to disk, if the buffer hasn't been filled yet. Setting this to 0 will disable the internal buffer and writes will be written directly to the journal file.
      * *Default:* 1 000 000 nanoseconds

    - `journalBufferSize`

      - The size of the in-memory Artemis buffer for messages, in bytes. Note that there is a lower bound to the buffer size, which is calculated based on the maximum message size of the network parameters to ensure messages of any allowed size can be stored successfully. As a result, any value lower than this bound will be ignored with the appropriate logging. This bound is also used as the default, if no value is specified.

* `ledgerRecoveryConfiguration`

    * This configuration allows you to tailor Ledger Recovery behavior for your Corda node. It offers flexibility in defining parameters related to key pair pre-generation, backup intervals, and confidential identity backup options. For a detailed description of Ledger Recovery that uses this configuration, see [Ledger Recovery]({{< relref "../ledger-recovery/ledger-recovery.md" >}}).

    - `noOfPreGeneratedKeys`

        * This property specifies the number of pre-generated keys used for confidential identities, indicating the count
        of keys that will be backed up in the database. It represents the pre-generated count of so-called new
        confidential identities; that is, those that don’t have a certificate.
        * The default for this property is 0, which means that:
           * if you have not changed it
           * if you are using new confidential identities, and
           * if you have not changed `canProvideNonBackedUpKeyPair` from its default value,
           then you receive a confidential identity created on the fly, not a pre-generated one. If you have changed `canProvideNonBackedUpKeyPair` to `false` and if there are no backed-up keys to return, then an exception is raised.
        * *Default:* 0

    - `noOfPreGeneratedKeysWithCerts`

        * This property specifies the number of pre-generated keys with certificates used for confidential identities,
        indicating the count of keys that will be backed up in the database. It represents the pre-generated count
        of so-called old confidential identities, that is, those that have a certificate.
        * The default for this property is 0, which means that:
          * if you have not changed it,
          * if you are using new confidential identities, and
          * if you have not changed `canProvideNonBackedUpKeyPair` from its default value,
          then you receive a confidential identity created on the fly, not a pre-generated one. If you have changed `canProvideNonBackedUpKeyPair` to `false` and if there are no backed-up keys to return, then an exception is raised.
        * *Default:* 0

    - `preGeneratedKeysTopUpInterval`

        * Defines the time interval (in seconds) at which the pre-generated keys are topped up or refreshed.
        * *Default:* 300 seconds

    - `recoveryMaximumBackupInterval`

        * Specifies the maximum time duration for which ledger recovery can be done. This parameter can be specified in
        three different ways:
          * Network parameters (if node is on a network using CENM 1.6 or later)
          * Configuration parameter (this parameter)
          * Directly as a parameter on the recovery flow

        * If the parameter is specified in more than one place, then the recovery flow parameter overrides the configuration
        parameter which overrides the network parameter. If the node is on a network not using CENM 1.6 and the parameter
        is not specified in either configuration or directly on the ledger recovery flow, then an exception is raised
        when starting the recovery flow.
        * There is no default for this parameter. If it is not specified in any of the above
        ways, an exception is raised.
        * The duration is specified in the Human-Optimized Config Object Notation (HOCON) format with suffixes of `h` (hours),
        `m` (minutes) and `s` (seconds); for example, `1h` means one hour. For additional information on the HOCON duration
        format parsing, see the [HOCON duration format file](https://github.com/lightbend/config/blob/master/HOCON.md) on GitHub.
        * *Default:* If the recovery flow is run, you must set `recoveryMaximumBackupInterval` using one of the ways described above.

    - `confidentialIdentityMinimumBackupInterval`

        * Defines the time interval (duration) within which automatic database backups occur, ensuring that all pre-generated
        keys created before the backup are marked as backed-up according to this interval. This parameter can be specified
        in two different ways:
          * Network parameters (if node is on a network using CENM 1.6 or later)
          * Configuration parameter (this parameter)

        * If the parameter is specified in more than one place, then the configuration parameter overrides the network parameter.
        * If the node is on a network not using CENM 1.6 and the parameter is not specified in configuration, then an exception
        is raised if either `noOfPreGeneratedKeys` or `noOfPreGeneratedKeysWithCerts` is greater than 0. In other words, if
        you want to regenerate keys, then you must have the `confidentialIdentityMinimumBackupInterval` defined. There is
        no default for this parameter.
        * The duration is specified in the Human-Optimized Config Object Notation (HOCON) format with suffixes of `h` (hours),
        `m` (minutes) and `s` (seconds); for example, `1h` means one hour. For additional information on the HOCON duration
        format parsing, see the [HOCON duration format file](https://github.com/lightbend/config/blob/master/HOCON.md) on GitHub.
        * *Default:* If either `noOfPreGeneratedKeys` or `noOfPreGeneratedKeysWithCerts` is greater than zero, you must set
        `confidentialIdentityMinimumBackupInterval` using one of the ways described above.

    - `canProvideNonBackedUpKeyPair`

        * Determines whether the node can provide non-backed-up key pairs if backed-up keys pairs are exhausted, or if CIs
        are used and both `noOfPreGeneratedKeys` and `noOfPreGeneratedKeysWithCerts` are zero.
        * *Default:* true

    - `bufferSizeForKeys`

        * By configuring this property, you can control the number of pre-generated keys that are readily available in memory.
        * *Default:* 0

    - `bufferSizeForKeys` with certificates

        * By configuring this property, you can control the number of pre-generated keys with certificates that are readily available in memory.
        * *Default:* 0

    * To configure the `ledgerRecoveryConfiguration` for your Corda Enterprise node, modify the properties according to the
    requirements in your node's configuration file; for example:

        ```
        enterpriseConfiguration = {
        # Ledger Recovery Configuration
            ledgerRecoveryConfiguration {
                noOfPreGeneratedKeys= 100
                noOfPreGeneratedKeysWithCerts = 0
                preGeneratedKeysTopUpInterval = 10 # 10 seconds
                recoveryMaximumBackupInterval = "24h"
                confidentialIdentityMinimumBackupInterval = "12h"
                canProvideNonBackedUpKeyPair = false
                bufferSizeForKeys = 100
                bufferSizeForKeysWithCerts = 100
            }
        }
        ```

## `extraNetworkMapKeys`

An optional list of private network map UUIDs. Your node will fetch the public network and private network maps based on these keys.
Private network UUID should be provided by network operator and lets you see nodes not visible on public network.

{{< important >}}This is a temporary feature for onboarding network participants that limits their visibility for privacy reasons.{{< /important >}}

*Default:* not defined

## `flowExternalOperationThreadPoolSize`

The number of threads available to execute external operations that have been called from flows.

*Default:* Set to the lower value between the maximum number of cores allocated to the node, or 10 cores if the maximum exceeds 10.

## `flowMonitorPeriodMillis`

Duration of the period suspended flows waiting for IO are logged.

*Default:* 60 seconds

## `flowMonitorSuspensionLoggingThresholdMillis`

Threshold duration suspended flows waiting for IO need to exceed before they are logged.

*Default:* 60 seconds

## `flowTimeout`

When a flow implementing the `TimedFlow` interface and setting the `isTimeoutEnabled` flag does not complete within a defined elapsed time, it is restarted from the initial checkpoint.
Currently only used for notarisation requests with clustered notaries: if a notary cluster member dies while processing a notarisation request, the client flow eventually times out and gets restarted.
On restart the request is resent to a different notary cluster member in a round-robin fashion. Note that the flow will keep retrying forever. The calculation of the retry timer is as follows:

```
Timeout = Base timeout * Backoff base ^ Retry count * Jitter factor
```

The jitter factor is set to a random number between 1 and 1.5, and is intended to introduce a degree of randomness to the calculation, helping to protect the notary against sudden increases in notarisation requests causing a subsequent increase in retry attempts.

* `timeout`
  * The initial flow timeout period.
  * Default: 30 seconds
* `maxRestartCount`
  * The number of retries the back-off time keeps growing for. For subsequent retries, the timeout value will remain constant.
  * Default: 6
* `backoffBase`
  * The base of the exponential backoff, `t_{wait} = timeout * backoffBase^{retryCount}`
  * Default: 1.8

## `graphiteOptions`

Optionally export metrics to a Graphite server. When specified, the node will push out all JMX metrics to the specified Graphite server at regular intervals.

* `server`
  * Server name or IP address of the Graphite instance.
* `port`
  * Port the Graphite instance is listening at.  This must be the pickle receiver port.
* `prefix`
  * Optional prefix string to identify metrics from this node, will default to a string made up from Organisation Name and IP address.
* `sampleIntervalSeconds`
  * Optional wait time between pushing metrics. This will default to 60 seconds.

## `h2Port`

{{< important >}}
Deprecated. Use `h2Setting` instead
{{< /important >}}

Defines port for h2 DB.

## `h2Settings`

Sets the H2 JDBC server host and port.
For non-localhost address the database password needs to be set in `dataSourceProperties`.

*Default:* NULL

## `jarDirs`

An optional list of file system directories containing JARs to include in the classpath when launching via `corda.jar` only.
Each should be a string.
Only the JARs in the directories are added, not the directories themselves.
This is useful for including JDBC drivers and the like. e.g. `jarDirs = [ ${baseDirectory}"/libs" ]`.
(Note that you have to use the `baseDirectory` substitution value when pointing to a relative path).

{{< warning >}}
If an item in a list is overridden via an environment variable/system property, the whole list will be overridden. This mechanism should not be used for CorDapps directory.
{{< /warning >}}

*Default:* not defined

This property is only available for Corda distributed with Capsule. For the Corda tarball distribution this option is unavailable.
It's advisable to copy any required JAR files to the 'drivers' subdirectory of the node base directory.

## `jmxMonitoringHttpPort`

If set, will enable JMX metrics reporting via the Jolokia HTTP/JSON agent on the corresponding port.
Default Jolokia access url is `http://127.0.0.1:port/jolokia/`.

*Default:* not defined

## `jmxReporterType`

Provides an option for registering an alternative JMX reporter.
Available options are `JOLOKIA` and `NEW_RELIC`.

The Jolokia configuration is provided by default.
The New Relic configuration leverages the Dropwizard NewRelicReporter solution.

*Default:* `JOLOKIA`

## `keyStorePassword`

The password to unlock the keystore files `<workspace>/certificates/sslkeystore.jks` and `<workspace>/certificates/nodestore.jks` containing the node certificate and private key.

{{< important >}}This is the non-secret value for the development certificates automatically generated during the first node run.
Alternatively, these keys can be managed in secure hardware devices.{{< /important >}}

*Default:* cordacadevpass

## `lazyBridgeStart`

Internal option.

{{< important >}}Please do not change.{{< /important >}}

*Default:* true

## `manAllowed`

Enables the usage of the shell 'man' command. Please note it makes use of insecure APIs and should be enabled with caution.

*Default:* false

## `messagingServerAddress`

The address of the ArtemisMQ broker instance.
If not provided the node will run one locally.

0.0.0.0 should not be specified since this needs to be a valid client address.

*Default:* not defined

## `messagingServerExternal`

If `messagingServerAddress` is specified the default assumption is that the artemis broker is running externally.
Setting this to `false` overrides this behaviour and runs the artemis internally to the node, but bound to the address specified in `messagingServerAddress`.
This allows the address and port advertised in `p2pAddress` to differ from the local binding, especially if there is external remapping by firewalls, load balancers , or routing rules. Note that `detectPublicIp` should be set to `false` to ensure that no translation of the `p2pAddress` occurs before it is sent to the network map.

0.0.0.0 is not a valid host setting since p2pAddress must be an external client address.

{{< note >}}
When `messagingServerExternal` = `true`, `messagingServerSslConfiguration` is required for TLS configuration used to connect to external P2P Artemis message server. For more information, see [Storing node TLS keys in HSM]({{< relref "tls-keys-in-hsm.md" >}}).
{{< /note >}}

*Default:* not defined

## `myLegalName`

The legal identity of the node.
This acts as a human-readable alias to the node's public key and can be used with the network map to look up the node's info.
This is the name that is used in the node's certificates (either when requesting them from the doorman, or when auto-generating them in dev mode).
At runtime, Corda checks whether this name matches the name in the node's certificates.
The name must be a valid X.500 distinguished name; see [Node identity]({{< relref "node-naming.md" >}}).

*Default:* not defined

## `notary`

Include this optional configuration object in the node configuration file if you want to configure the node to run as a notary.

{{< warning >}}
If running as part of a HA notary cluster, you must specify the `serviceLegalName` and either the `mysql` (deprecated) or `jpa` configuration as described below.

For a single-node notary, you must specify the `validating` and `serviceLegalName` configuration fields.
{{< /warning >}}

{{< note >}}
Once a notary is configured with a default value, it cannot be reconfigured. To change a non-validating notary to validating
(or vice-versa), you need to create and register a new notary.
{{< /note >}}

* `validating`
  * Boolean to determine whether the notary is a validating or non-validating one.
  * *Default:* false
* `serviceLegalName`
  * Specify the legal name of the notary service. At runtime, Corda checks whether this name matches the name of the certificate of the notary.
  * *Default:* not defined
* `extraConfig`
  * Configuration for the single-node notary only. For HA notaries use either the `mysql` (deprecated) or `jpa` configuration.
  * `batchSize`
    * The maximum number of transactions processed in a single batch. Larger batches are generally processed more efficiently than smaller batches;       however, larger batches may worsen latency.
    * *Default:* 32
  * `maxInputStates`
    * The maximum combined number of input states processed in a single batch when finding conflicts.
    * *Default:* 2 000
  * `maxDBTransactionRetryCount`
    * The maximum number of retries of database operations before throwing an exception.
    * *Default:* 10
  * `backOffBaseMs`
    * The duration to wait before retrying failing DB operations. Doubled with every retry.
    * *Default:* 20
  * `batchTimeoutMs`
    * Configures the amount of time that the notary will wait before processing a batch, even if the batch is not full. Smaller values can lead to lower latency but potentially worse throughput as smaller batches might be processed.
    * *Default:* 1
* `mysql`
  * If using the MySQL notary (deprecated), specify this configuration section with the settings below.
  * `connectionRetries`
    * The number of times to retry connection to the MySQL database. This should be based on the number of database servers in the replicated        setup.
    * *Default:* 2, for a 3 server cluster.
  * `backOffIncrement`
    * Time increment between re-connection attempts.
    * The total back-off duration is calculated as: backOffIncrement * backOffBase ^ currentRetryCount
    * *Default:* 500
  * `backOffBase`
    * Exponential back-off multiplier base for use in determining time increment between reconnection attempts.
    * *Default:* 1.5
  * `maxBatchSize`
    * The maximum number of transactions processed in a single batch. Larger batches are generally processed more efficiently than smaller batches; however, larger batches may worsen latency. Monitor the `ProcessedBatchSize` metric exposed by the notary to determine batch utilisation. For more information, see [Highly-available notary metrics]({{< relref "../../notary/notary-metrics.md" >}}).
    * *Default:* 500
  * `maxBatchInputStates`
    * The maximum combined number of input states processed in a single batch. If the number of transactions in a batch is equal to `maxBatchSize`, but the number of states in the batch is greater than `maxBatchInputStates`, that batch will  be split into two smaller batches.
    * *Default:* 10 000
  * `batchTimeoutMs`
    * Configures the amount of time that the notary will wait before processing a batch, even if the batch is not full. Smaller values can lead to lower latency but potentially worse throughput as smaller batches might be processed.
    * *Default:* 200
  * `maxQueueSize`
    * The maximum number of commit requests in flight. Once the capacity is reached the service will block on further commit requests.
    * *Default:* 100 000
  * `dataSource`
    * This section is used to configure the JDBC connection to the database cluster. For example:
    * `autoCommit`
      * JDBC operation mode where every update to the database is immediately made permanent. For HA notary it has to be disabled, i.e. set to `"false"`.
      * *Default:* not defined
    * `jdbcUrl`
      * The JDBC connection string. Has to contain a comma-separated list of IPs for all database servers. For example, if we have a 3-node Percona cluster with addresses 10.18.1.1, 10.18.1.2 and 10.18.1.3, and the database name is `corda`:<br>
      `"jdbc:mysql://10.18.1.1,10.18.1.2,10.18.1.3/corda?rewriteBatchedStatements=true&useSSL=false&failOverReadOnly=false"`
      * *Default:* not defined
    * `username`
      * Database user.
      * *Default:* not defined
    * `password`
      * Database password.
      * *Default:* not defined

        Example configuration:

        ```json
          mysql {
            connectionRetries=2
            dataSource {
              autoCommit="false"
              jdbcUrl="jdbc:mysql://10.18.1.1,10.18.1.2,10.18.1.3/corda?rewriteBatchedStatements=true&useSSL=false&failOverReadOnly=false"
              username="CordaUser"
              password="myStrongPassword"
            }
          }
        ```

  * `etaMessageThresholdSeconds`
    * If the wait time estimate on the internal queue exceeds this value, the notary may send
  a wait time update to the client (implementation specific and dependent on the counter
  party version).
    * *Default:* Implementation dependent
  * `raft`
    * *(Deprecated)* If part of a distributed Raft cluster, specify this configuration object with the following settings:
    * `nodeAddress`
      * The host and port to which to bind the embedded Raft server. Note that the Raft cluster uses a  separate transport layer for communication that does not integrate with ArtemisMQ messaging services.
      * *Default:* not defined
    * `clusterAddresses`
      * Must list the addresses of all the members in the cluster. At least one of the members must be active and be able to communicate with the cluster leader for the node to join the cluster. If empty, a new cluster will be bootstrapped.
      * *Default:* not defined
  * `bftSMaRt`
    * *(Deprecated)* If part of a distributed BFT-SMaRt cluster, specify this configuration object with the following settings:
    * `replicaId`
      * The zero-based index of the current replica. All replicas must specify a unique replica id.
      * *Default:* not defined
    * `clusterAddresses`
      * Must list the addresses of all the members in the cluster. At least one of the members must be active and be able to communicate with the cluster leader for the node to join the cluster. If  empty, a new cluster will be bootstrapped.
      * *Default:* not defined
  * `jpa`
    * If using the JPA notary, specify this configuration section with the settings below. For more details refer to [Configuring the notary worker nodes]({{< relref "../../notary/installing-the-notary-service.md" >}}).
    * `connectionRetries`
      * The number of times to retry connection to the database. This should be based on the number of database servers in the replicated setup.
      * *Default:* 2
    * `backOffIncrement`
      * Time increment between re-connection attempts. The total back-off duration is calculated as: backOffIncrement * backOffBase ^ currentRetryCount
      * *Default:* 500
    * `backOffBase`
      * Exponential back-off multiplier base for use in determining time increment between reconnection attempts.
      * *Default:* 1.5
    * `maxBatchSize`
      * The maximum number of transactions processed in a single batch. Larger batches are generally processed more efficiently than smaller batches; however, larger batches may worsen latency. Monitor the `ProcessedBatchSize` metric exposed by the notary to determine batch utilisation.
      * *Default:* 500
    * `maxBatchInputStates`
      * The maximum combined number of input states processed in a single batch. If the number of transactions in a batch is equal to `maxBatchSize`, but the number of states in the batch is greater than `maxBatchInputStates`, that batch will be split into two smaller batches.
      * *Default:* 10 000
    * `maxDBTransactionRetryCount`
      * The maximum number of retries of database operations before throwing an exception.
      * *Default:* 10
    * `batchTimeoutMs`
      * Configures the amount of time that the notary will wait before processing a batch, even if the batch is not full. Smaller values can lead to lower latency but potentially worse throughput as smaller batches might be processed.
      * *Default:* 200
    * `maxQueueSize`
      * The maximum number of commit requests in flight. Once the capacity is reached the service will block on further commit requests.
      * *Default:* 100 000
    * `generateNativeSQL`
      * Boolean enabling the generation of native SQL for CockroachDB databases with multi-row insert statements. Enabling this configuration option results in better notary performance in some implementations.
      * *Default:* false
    * `database`
      * `validateSchema`
        * Sets whether to validate the database schema before allowing the notary to start. Will prevent the notary from starting if validation fails with log messages indicating the reason(s)           for the failure. The validation will ensure that the database tables match that of the entities configured in the notary. This will not check whether any migrations have been run.
        * *Default:* false
      * `schema`
        * Sets the schema to be used by Hibernate
      * `hibernateDialect`
        * Optionally sets the Hibernate dialect to use when communicating with the database.
    * `dataSourceProperties`
      * This section is used to configure the JDBC connection to the database cluster. For example:
      * `autoCommit`
        * JDBC operation mode where every update to the database is immediately made permanent. For HA notary it has to be disabled, i.e. set to `"false"`.
        * *Default:* not defined
      * `jdbcUrl`
        * The JDBC connection string. Has to contain a comma-separated list of IPs for all database servers. For example, if we have a 3-node CockroachDB cluster with addresses 10.18.1.1, 10.18.1.2 and 10.18.1.3, and the notary worker is connecting to CockroachDB via SSL using certificates created for the user `corda`:

        ```shell
        "jdbc:postgresql://10.18.1.1,10.18.1.2,10.18.1.3/corda?sslmode=require&sslrootcert=certificates/ca.crt&sslcert=certificates/client.corda.crt&sslkey=certificates/client.corda.key.pk8"
        ```

        * *Default:* not defined
      * `username`
        * Database user.
        * *Default:* not defined
      * `password`
        * Database password.
        * *Default:* not defined

        ```json
          jpa {
            connectionRetries=2
            dataSource.[VALUE] {
              autoCommit="false"
              jdbcUrl="jdbc:postgresql://10.18.1.1,10.18.1.2,10.18.1.3/corda?sslmode=require&sslrootcert=certificates/ca.crt&sslcert=certificates/client.corda.crt&sslkey=certificates/client.corda.key.pk8&user=corda"
              username="corda"
              password="myStrongPassword"
            }
          }
        ```

## `networkParameterAcceptanceSettings`

Optional settings for managing the network parameter auto-acceptance behaviour.
If not provided then the defined defaults below are used.

* `autoAcceptEnabled`
  * This flag toggles auto accepting of network parameter changes.
  If a network operator issues a network parameter change which modifies only auto-acceptable options and this behaviour is enabled then the changes will be accepted without any manual intervention from the node operator. See [Network map]({{< relref "../../network/network-map.md" >}}) for more information on the update process and current auto-acceptable parameters. Set to ``false`` to disable.
  * Default: true
* `excludedAutoAcceptableParameters`
  * List of auto-acceptable parameter names to explicitly exclude from auto-accepting. Allows a node operator to control the behaviour at a more granular level.
  * Default: empty list

## `networkServices`

If both of the Corda compatibility zone services, network map and registration (doorman), are not running on the same endpoint and thus have different URLs, use this option in place of the `compatibilityZoneURL` setting.

{{< important >}}Only one of `compatibilityZoneURL` or `networkServices` should be used.{{< /important >}}

* `doormanURL`
  * Root address of the network registration service.
  * *Default:* not defined
* `networkMapURL`
  * Root address of the network map service.
  * *Default:* not defined
* `pnm`
  * Optional UUID of the private network operating within the compatibility zone this node should be joining.
  * *Default:* not defined
* `proxyType`
  * Optional - this can be used to turn on using a proxy for the http connections to doorman and network map. Allowed    values are `DIRECT`, `HTTP` and `SOCKS`. If set to anything else than `DIRECT`, the proxyAddress must also    be set.
  * *Default:* `DIRECT` (i.e. no proxy)
* `proxyAddress`
  * Optional hostname and port of a HTTP or SOCKS proxy to be used for connections to the network map or doorman.
  * *Default:* not defined
* `proxyUser`
  * Optional user name for authentication with the proxy. Note that Corda only supports username/password based basic authentication.
* `proxyPassword`
  * Optional password for authentication with the proxy. The password can be obfuscated using the [Configuration obfuscator]({{< relref "../../tools-config-obfuscator.md" >}}).
* `csrToken`
  * Optional token to provide alongside the certificate signing request (CSR) as part of the HTTP header during node registration. The token can be used by certificate signing authority (or Identity Manager Service) to verify additional identity requirements. The maximum token length is limited by the maximum HTTP header size, which is normally 8KB, assuming that a few other internal attributes are also present in the header. Also, the token length itself may never exceed 8192, limited by the database structure. Only US-ASCII characters are allowed.
  * *Default:* not defined

## `p2pAddress`

The host and port on which the node is available for protocol operations over ArtemisMQ.

In practice the ArtemisMQ messaging services bind to **all local addresses** on the specified port.
However, note that the host is the included as the advertised entry in the network map.
As a result the value listed here must be **externally accessible when running nodes across a cluster of machines.**
If the provided host is unreachable, the node will try to auto-discover its public one.

*Default:* not defined

## `quasarExcludePackages`

A list of packages to exclude from Quasar instrumentation. Wildcards are allowed, for example `org.xml**`.

{{< important >}}Do not change unless requested by support.{{< /important >}}

*Default:* empty list

Example configuration:

```shell
quasarExcludePackages=["org.xml**", "org.yaml**"]
```

## `relay`

If provided, the node will attempt to tunnel inbound connections via an external relay. The relay's address will be
advertised to the network map service instead of the provided `p2pAddress`.

* `relayHost`
  * Hostname of the relay machine
* `remoteInboundPort`
  * A port on the relay machine that accepts incoming TCP connections. Traffic will be forwarded from this port to the local port specified in `p2pAddress`.
* `username`
  * Username for establishing an SSH connection with the relay.
* `privateKeyFile`
  * Path to the private key file for SSH authentication. The private key must not have a passphrase.
* `publicKeyFile`
  * Path to the public key file for SSH authentication.
* `sshPort`
  * Port to be used for SSH connection, default `22`.

## `rpcAddress`

{{< important >}}
Deprecated. Use `rpcSettings` instead.
{{< /important >}}

The address of the RPC system on which RPC requests can be made to the node.
If not provided then the node will run without RPC.

*Default:* not defined

## `rpcSettings`

Options for the RPC server exposed by the Node.

{{< important >}}The RPC SSL certificate is used by RPC clients to authenticate the connection.  The Node operator must provide RPC clients with a truststore containing the certificate they can trust.  We advise Node operators to not use the P2P keystore for RPC.  The node can be run with the "generate-rpc-ssl-settings" command, which generates a secure keystore and truststore that can be used to secure the RPC connection. You can use this if you have no special requirements.{{< /important >}}

* `address`
  * host and port for the RPC server binding. Specifying 0.0.0.0 (as host) is a convention allowing the host to bind all of its network interfaces when listening on a socket. By itself 0.0.0.0 is non-routable; i.e., not a proper address.
  * *Default:* not defined
* `adminAddress`
  * host and port for the RPC admin binding (this is the endpoint that the node process will connect to).  This needs to follow the same host rules as address setting (see above).
  * *Default:* not defined
* `standAloneBroker`
  * boolean, indicates whether the node will connect to a standalone broker for RPC.
  * *Default:* false
* `useSsl`
  * boolean, indicates if the node should require clients to use SSL for RPC connections.
  * *Default:* false
* `ssl`
  * (mandatory if `useSsl=true`) SSL settings for the RPC server.
  * `keyStorePath`
    * Absolute path to the key store containing the RPC SSL certificate.
    * *Default:* not defined
  * `keyStorePassword`
    * Password for the key store.
    * *Default:* not defined

## `rpcUsers`

A list of users who are authorised to access the RPC system.
Each user in the list is a configuration object with the following fields:

* `username`
  * Username consisting only of word characters (a-z, A-Z, 0-9 and _)
  * *Default:* not defined
* `password`
  * The password
  * *Default:* not defined
* `permissions`
  * A list of permissions for starting flows via RPC. To give the user the permission to start the flow `foo.bar.FlowClass`, add the string `StartFlow.foo.bar.FlowClass` to the list. If the list contains the string `ALL`, the user can start any flow via RPC. Wildcards are also allowed , for example `StartFlow.foo.bar.*` will allow the user to start any flow within the `foo.bar` package.
  This value is intended for administrator users and for development.
  * *Default:* not defined

## `security`

Contains various nested fields controlling user authentication/authorization, in particular for RPC accesses.

## `sshd`

If provided, node will start internal SSH server which will provide a management shell.
It uses the same credentials and permissions as RPC subsystem.
It has one required parameter.

`port`:
  The port to start SSH server on e.g. `sshd { port = 2222 }`.

  *Default:* not defined

## `sslHandshakeTimeout`

Internal option.

{{< important >}}Please do not change.{{< /important >}}

*Default:* 60000 milliseconds

## `systemProperties`

An optional map of additional system properties to be set when launching via `corda.jar` only.
Keys and values of the map should be strings. e.g. `systemProperties = { "visualvm.display.name" = FooBar }`

*Default:* not defined

## `telemetry`

There are new configuration fields for telemetry. See the [OpenTelemetry]({{< relref "../../../enterprise/node/operating/monitoring-and-logging/opentelemetry.md" >}}) section for more information.

* `openTelemetryEnabled`
  * Specifies if the node should generate spans to be sent to a collector. The node will only generate spans if this property is set to `true` and an OpenTelemetry SDK is on the node classpath. By default, no OpenTelemetry SDK is on the node classpath, meaning by default no spans are actually generated. To prevent spans being generated regardless of whether the OpenTelemetry SDK is on the classpath, this configuration field should be set to `false`.
  * *Default:* true
* `spanStartEndEventsEnabled`
  * When Corda generates spans for flows and certain significant operations, it has the capability to generate a span for starting the operation, ending the operation, and generating a single span to cover the whole operation. This can be useful to determine where a flow is stuck, as you will only see the start spans, and not the end spans. This is not standard OpenTelemetry behaviour, and it could also result in a lot of spans flooding the network. Setting this field to `true` will enable it.
  * *Default:* false
* `copyBaggageToTags`
  * If set to `true`, this parameter will cause baggage to be copied to tags when generating spans. Baggage are fields which can be passed around with the invocation of OpenTelemetry.
  * *Default:* false
* `simpleLogTelemetryEnabled`
  * Enables an alternative form of telemetry. If this field is set to `true`, log lines are written to logs when a flow or significant operation is started, or ended. The log line specifies a trace ID, which allows flows to be matched up across nodes.
  * *Default:* false
* Example configuration:

```kotlin
telemetry {
        openTelemetryEnabled=true
        spanStartEndEventsEnabled=false
        simpleLogTelemetryEnabled=false
      }
```

## `transactionCacheSizeMegaBytes`

Optionally specify how much memory should be used for caching of ledger transactions in memory.

*Default:* 8 MB plus 5% of all heap memory above 300MB.

## `tlsCertCrlDistPoint`

CRL distribution point (i.e. URL) for the TLS certificate.
Default value is NULL, which indicates no CRL availability for the TLS certificate.

{{< important >}}This needs to be set if crlCheckSoftFail is false (i.e. strict CRL checking is on).{{< /important >}}

*Default:* NULL

## `tlsCertCrlIssuer`

CRL issuer (given in the X500 name format) for the TLS certificate.
Default value is NULL, which indicates that the issuer of the TLS certificate is also the issuer of the CRL.

{{< important >}}If this parameter is set then `tlsCertCrlDistPoint` needs to be set as well.{{< /important >}}

*Default:* NULL

## `trustStorePassword`

The password to unlock the Trust store file (`<workspace>/certificates/truststore.jks`) containing the Corda network root certificate.
This is the non-secret value for the development certificates automatically generated during the first node run.

*Default:* trustpass

## `useOpenSsl`

If set to true, the node will use a native SSL implementation for TLS rather than the JVM SSL. The native SSL library currently shipped with
Corda Enterprise is BoringSsl. The default is to use JVM SSL, i.e. the flag being set to `false`. This configuration offers higher performance than the built-in library, but you can't use it with the Corda Firewall or an HSM—so this configuration is only recommended for private networks where there is a requirement to extract maximum performance.

## `useTestClock`

Internal option.

{{< important >}}Please do not change.{{< /important >}}

*Default:* false

## `verfierType`

Internal option.

{{< important >}}Please do not change.{{< /important >}}

*Default:* InMemory

## `reloadCheckpointAfterSuspend`

  This is an optional configuration option that enables you to detect unrestorable checkpoints when developing CorDapps and thus reduces the risk of writing flows that cannot be retried gracefully. To use this functionality, set `reloadCheckpointAfterSuspend` to `true`:

  ```
  reloadCheckpointAfterSuspend = true
  ```

  {{< note >}}
  This option is disabled by default and is independent from `devMode`.
  {{< /note >}}

  For full details, see [Automatic detection of unrestorable checkpoints]({{< relref "../operating/monitoring-and-logging/checkpoint-tooling.md#automatic-detection-of-unrestorable-checkpoints" >}}).

  *Default:* not defined
