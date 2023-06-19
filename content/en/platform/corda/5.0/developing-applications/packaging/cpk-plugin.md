---
date: '2023-06-06'
title: "CPK Gradle Plugin"
project: corda
version: 'Corda 5.0 Beta 4'
menu:
  corda5:
    parent: corda5-develop-packaging
    identifier: corda5-develop-packaging-cpk-plugin
    weight: 4000
section_menu: corda5
---
# CPK Gradle Plugin

Applying this plugin to a project declares that the project should create a CorDapp in CPK format. The CPK format
CorDapp is a ZIP file with a `.jar` extension, which is the output of the JAR task, along with the dependent JARs of that JAR.
The plugin will not include any of Corda's own JARs among these dependencies, nor any JARs that should be provided by
Corda, such as Kotlin or Quasar. The JAR should also contain sufficient OSGi metadata to be a valid OSGi bundle.

## Applying the Plugin

1. Depending on the number of modules of your Gradle project, choose one of the following options:

   * If your Gradle project contains multiple modules, perform the following actions:

     a. Include the following code at the top of the `build.gradle` file of your CorDapp Gradle project:
     ```
     plugins {
     id 'net.corda.plugins.cordapp-cpk2'
     }
     ```
     b. To configure the `cordapp-cpk2` plugin for your version of Corda, apply the `net.corda.cordapp.cordapp-configuration`
plugin to your root Gradle project:
     ```
     plugins {
     id 'net.corda.cordapp.cordapp-configuration'
     }
     ```

   * If your Gradle project contains a single module, apply both plugins together:

     ```
     plugins {
       id 'net.corda.cordapp.cordapp-configuration'
       id 'net.corda.plugins.cordapp-cpk2'
     }
     ```

2. Declare the versions of both plugins in `settings.gradle`:
```
pluginManagement {
    plugins {
        id 'net.corda.cordapp.cordapp-configuration' version cordaReleaseVersion
        id 'net.corda.plugins.cordapp-cpk2' version cpkPluginVersion
    }
}
```

Where `cpkPluginVersion` and `cordaReleaseVersion` are both Gradle properties:

```
cpkPluginVersion = '6.0.0'
cordaReleaseVersion = '5.0.0'
```

Applying the `cordapp-cpk2` plugin implicitly applies both Gradle's Java library plugin and Bnd's builder plugin,
which means that the output of the JAR task will also become an OSGi bundle. The `cordapp-cpk2` plugin assigns the
following default OSGi attributes to the bundle:

* `Bundle-SymbolicName: ${project.group}.${archiveBaseName}[-${archiveAppendix}][-${archiveClassifier}]`
* `Bundle-Version: ${project.version}`

## DSL

The plugin creates a `cordapp` DSL extension, which currently bears a strong resemblance to the legacy `cordapp` plugin's DSL extension:

{{< note >}}
This extension is likely to change as Corda 5 matures and its requirements evolve. The `name`, `licence`, and `vendor` fields
are mapped to the `Bundle-Name`, `Bundle-License`, and `Bundle-Vendor` OSGi manifest tags respectively.
{{</ note >}}


```
cordapp {
    targetPlatformVersion = '<Corda 5 Platform Version>'
    minimumPlatformVersion = '<Corda 5 Platform Version>'

    contract {
        name = 'Example CorDapp'
        versionId = 1
        licence = 'Test-Licence'
        vendor = 'R3'
    }

    workflow {
        name = 'Example CorDapp'
        versionId = 1
        licence = 'Test-Licence'
        vendor = 'R3'
    }

    signing {
        enabled = (true | false)

        // These options presumably mirror Ant's signJar task options.
        options {
            alias = '??'
            storePassword = '??'
            keyStore = file('/path/to/keystore')
            storeType= ('PKCS12' | 'JKS')
            keyPassword = '$storePassword'
            signatureFileName = '$alias'
            verbose = (true | false)
            strict = (true | false)
            internalSF = (true | false)
            sectionsOnly = (true | false)
            lazy = (true | false)
            maxMemory = '??'
            preserveLastModified = (true | false)
            tsaUrl = '??'
            tsaCert = '??'
            tsaProxyHost = '??'
            tsaProxyPort = '??'
            executable = file('/path/to/alternate/jarsigner')
            force = (true | false)
            signatureAlgorithm = '??'
            digestAlgorithm = '??'
            tsaDigestAlgorithm = '??'
        }
    }

    sealing = (true | false)

    hashAlgorithm = 'SHA-256'
}
```

## Configurations

Applying the `cordapp-cpk2` plugin creates the following new Gradle configurations:

* `cordaProvided`: This configuration declares a dependency that the CorDapp needs to compile against but should not
become part of the CPK since it will be provided by the Corda node at runtime. This effectively replaces the legacy
`cordaCompile` configuration. Any `cordaProvided` dependency is also implicitly added to Gradle's `compileOnly` and
`*Implementation` configurations. Consequently, it is not included in the `runtimeClasspath` configuration as a dependency
in the published POM file or packaged inside the CPK file. However, it will be included in the `testRuntimeClasspath`
configuration and will also become a transitive `cordaProvided` dependency of any CorDapp that depends on this CorDapp.

* `cordaPrivateProvided`: This configuration is similar to `cordaProvided`, with the difference that its contents do not
become transitive `cordaProvided` dependencies of any CorDapps that depend on this one.

* `cordapp`: This declares a compile-time dependency against the JAR of another CPK CorDapp. Similar to `cordaProvided`,
this dependency is also implicitly added to Gradle's `compileOnly` and `*Implementation` configurations. It is excluded
from the `runtimeClasspath` configuration, the published POM file, and the contents of the CPK file. The JARs of all
Cordapp dependencies are listed as lines in this JAR's `META-INF/CPKDependencies.json` file:

```json
{
    "formatVersion": "2.0",
    "dependencies": [
        {
            "name": "$BUNDLE_SYMBOLIC_NAME",
            "version": "$BUNDLE_VERSION",
            "verifySameSignerAsMe": true
        }
    ]
}
```

The `cordapp` dependencies are transitive, meaning that if CorDapp B declares a `cordapp` dependency on CorDapp A,
and then CorDapp C declares a cordapp dependency on CorDapp B, CorDapp C will acquire compile-time dependencies on the
JARs of both CorDapps A and B. Additionally, the `cordaProvided` dependencies of both A and B will be added to
CorDapp C's `cordaProvided` configuration. This mechanism is accomplished by
publishing each CPK with a "companion" POM that contains the additional dependency information. The `cordapp-cpk2`
plugin resolves these "companion" POMs transparently to the user, ensuring that CorDapps have the expected transitive relationships.

In order for everything to work as intended, the "companion" POM must be published into the same repository as its
associated JAR artifact. For a JAR with Maven coordinates:
```
 ${group}:${artifact}:${version}
```

...then the "companion's" Maven coordinates will be:
```
 ${group}.${artifact}:${artifact}.corda.cpk:${version}
```

* `cordaEmbedded`: This configuration behaves similarly to `cordaProvided` in the sense that it declares a `compileOnly`
dependency that is excluded from both the CPK contents and the published POM. The difference is that the dependent JAR
is also added to a `META-INF/lib` folder inside the CorDapp's JAR and appended to the JAR's `Bundle-Classpath` manifest
attribute. It's important to note that an OSGi framework considers the `Bundle-Classpath` to contain ordinary JARs and
not bundles, even if those JARs contain their own OSGi metadata. Additionally, the transitive dependencies of the
embedded JARs will also be embedded unless they are explicitly added to another Gradle configuration. Please exercise
caution when using embedding. It is provided as a tool for cases where a dependency lacks OSGi metadata or its metadata
is unusable. You must refrain from embedding dependencies that already have valid OSGi metadata.

* `cordaRuntimeOnly`: This configuration declares a dependency added to the `runtimeClasspath`, but the CorDapp does not
need to compile against it, and it must not be packaged into the CPK file. This configuration serves as a replacement
for the legacy `cordaRuntime` configuration.

{{< note >}}
The legacy `cordaCompile` and `cordaRuntime` configurations are built upon Gradle's deprecated `compile` and `runtime`
configurations, which have finally been removed in Gradle 7.0.
{{</ note >}}


## Publishing

The `cordapp-cpk2` plugin creates a new Gradle `SoftwareComponent` named "cordapp", which you can use to create a `MavenPublication`:
```
plugins {
    id 'net.corda.plugins.cordapp-cpk2'
    id 'maven-publish'
}

publishing {
    publications {
        myCorDapp(MavenPublication) {
            from components.cordapp
        }
    }
}
```

## Tasks

### External Tasks

* `jar`: This task represents the standard JAR task created by Gradle's `java-library` plugin and further enhanced by
Bnd's `builder` plugin to generate an OSGi bundle. The contents of the `runtimeClasspath` configuration are added to the
JAR's `META-INF/privatelib` folder, excluding any JARs that have been declared as either a `cordapp`, `cordaProvided`,
`cordaEmbedded`, or `cordaRuntimeOnly`. The `jar` task is an automatic dependency of Gradle's `assemble` task.

### Internal Tasks

These tasks perform intermediate steps as part of creating a CPK:

* `cordappDependencyCalculator`: Calculates which JARs belong to which part of a CPK's packaging.

* `cordappCPKDependencies`: Generates the JAR's `META-INF/CPKDependencies.json` file.

* `verifyBundle`: Verifies if the JAR's OSGi metadata is consistent with the packages that have been included in the CPK.
This task uses Bnd's `Verifier` class with "strict" verification enabled to ensure that every `Import-Package` element
has an associated version too.

## OSGi Metadata

The `cordapp-cpk2` plugin automatically adds these dependencies to the CorDapp:

```
compileOnly "biz.aQute.bnd:biz.aQute.bnd.annotation:$bndVersion"
compileOnly "org.osgi:osgi.annotation:8.1.0"
```

These annotations control how [Bnd will generate OSGi metadata](https://bnd.bndtools.org/chapters/230-manifest-annotations.html)
for the JAR. In practice, the plugin already tries to handle the typical cases for creating CorDapps.

### Bundle Symbolic Name

An OSGi bundle should be uniquely identifiable by the combination of its `Bundle-SymbolicName` and `Bundle-Version`
manifest attributes. The `cordapp-cpk2` plugin always sets the `Bundle-Version` attribute to the JAR task's `archiveVersion`
property, and it generates a default `Bundle-SymbolicName` value according to the following pattern:

```
(${project.group}.)?${archiveBaseName}(-${archiveAppendix})?(-${archiveClassifier})?
```

However, if this default value is unacceptable for any reason, the `Bundle-SymbolicName` can also be set explicitly via:

```
tasks.named('jar', Jar) {
    osgi {
        symbolicName = '<value>'
    }
}
```

### Package Exports

The `cordapp-cpk2` plugin creates a Bnd `-exportcontents` command to generate the JAR's OSGi `Export-Package` header.
By default, it will automatically add every package inside the JAR to this `-exportcontents` command. The assumption
here is that a CorDapp does not have a complicated package structure, and that Corda's OSGi sandboxes provides
additional CorDapp isolation.

CorDapp developers who wish to configure their package exports more precisely can disable this default behaviour in the `jar` task:

```
tasks.named('jar', Jar) {
    osgi {
        autoExport = false
    }
}
```

You can then apply `@org.osgi.annotation.bundle.Export` annotations manually to selected `package-info.java` files.
You can also export package names explicitly, although applying `@Export` annotations is recommended:

```
tasks.named('jar', Jar) {
    osgi {
        exportPackage 'com.example.cordapp', 'com.example.cordapp.foo'
    }
}
```

### Package Imports

Ideally, Bnd would automatically generate the correct OSGi `Import-Package` manifest header. However, there are
instances where Bnd may detect unexpected package references from unused code paths within the bytecode. To address this,
the `cordapp-cpk2` plugin offers the following options to override the detected package settings:

```
tasks.named('jar', Jar) {
    osgi {
        // Declares that this CorDapp requires the OSGi framework to provide the 'com.example.cordapp' package.
        // This value is passed straight through to Bnd.
        importPackage 'com.example.cordapp'

        // Declares that this CorDapp uses the 'com.example.cordapp.foo` package.
        // However, Corda will not complain if no-one provides it at runtime. This
        // assumes that the missing package isn't really required at all.
        optionalImport 'com.example.cordapp.foo'

        // Like `optionalImport`, except that it also assigns this package an empty
        // version range. This is useful when the unused package doesn't have a version
        // range of its own because it does not belong to another OSGi bundle.
        suppressImportVersion 'com.example.cordapp.bar'
    }
}
```

### ServiceLoader

Bundles that use `java.util.ServiceLoader` require special handling to support their `META-INF/services/` files.
Bnd provides <a href="https://bnd.bndtools.org/chapters/240-spi-annotations.html">`@ServiceProvider` and `@ServiceConsumer` annotations</a>
to ensure that the bundle respects OSGi's [Service Loader Mediator Specification](https://docs.osgi.org/specification/osgi.cmpn/7.0.0/service.loader.html).


### Corda Metadata

The plugin generates `Corda-*-Classes` tags in the JAR's `MANIFEST.MF`. The generated tags are controlled by the
`net.corda.cordapp.cordapp-configuration` Gradle plugin in the [corda-api](https://github.com/corda/corda-api) repo.

Each tag contains a list of the classes within the JAR that have been identified as being a Corda contract, a Corda flow,
and so on. Each of these classes has also been confirmed as being public, static, and non-abstract, which allows Corda
to instantiate them. Empty tags are excluded from the final manifest, and so not every tag is guaranteed to be present.

The plugin generates these lists using Bnd's `${classes}` macro. However, it is important to note that you may need to
update these macros as Corda evolves. To avoid the need to update the `cordapp-cpk2` plugin simultaneously,
it is preferred to keep the macros separate from the plugin itself.
You can update the macros by modifying the following file inside the Gradle plugin:

```
net/corda/cordapp/cordapp-configuration.properties
```

{{< note >}}
The `cordapp-configuration` plugin is part of the Corda repository and its new versions will be released as part of Corda.
{{</ note >}}


Then apply this new plugin to the CorDapps's root project. Any property key inside this file that matches `Corda-*-Classes`
defines a filter to generate a new manifest tag or replace an existing tag. For example:

```
Corda-Contract-Classes=IMPLEMENTS;net.corda.v10.ledger.contracts.Contract
```

The `cordapp-cpk2` plugin appends additional clauses to each filter to ensure that it still only selects public, static,
non-abstract classes.

#### Dynamic Imports

The CPK needs to declare imports for the following packages so that OSGi can create lazy proxies for any JPA entities
that the bundle may contain:

* `org.hibernate.proxy`
* `javaassist.util.proxy`

You must also allow the bundle to import the package containing Hibernate-specific annotations:

* `org.hibernate.annotations`

You must declare all these packages as "dynamic" imports to avoid binding the CPK to a specific version of Hibernate.
It should make it easier for Corda itself to evolve without breaking everyone's CorDapps.

The plugin declares these packages using the OSGI `DynamicImport-Package` header.

If necessary, you can update these package names via the `cordapp-configuration.properties` file by adding a comma-separated
list to the `Required-Packages` key. It will completely override the plugin's hard-coded list of packages:

```
Required-Packages=org.foo,org.bar
```

#### Corda API Imports

Any CPK written for Corda 5.x must be compatible with every release of Corda 5.x. This requires the `cordapp-cpk2` plugin
to apply an explicit OSGi "consumer policy" for every Corda API package that the CPK may use:

```
version='${range;[=,+);${@}}'
```

You identify Corda's API packages using the `Import-Policy-Packages` property:

```
Import-Policy-Packages=net.corda.v5.*
```

You can prevent the `cordapp-cpk2` plugin from applying this policy by setting:

```
jar {
    osgi {
        applyImportPolicy = false
    }
}
```

However, this will likely prevent your CPK compiled for Corda 5.x from installing correctly into any Corda node where
`0 <= Corda version < x`.
