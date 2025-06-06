---
description: "Learn about Corda security policies and the OSGi security model that they are based on."
title: "Security Policies"
date: '2023-05-16'
menu:
  corda51:
    identifier: corda51-cluster-security
    parent: corda51-cluster-config
    weight: 3050
---
# Security Policies

Corda security policies are based on [Conditional Permissions](https://docs.osgi.org/specification/osgi.core/8.0.0/service.condpermadmin.html#i1534586) of the OSGi security model. The following predefined security profiles are available:

* [high_security.policy](https://raw.githubusercontent.com/corda/corda-runtime-os/release/os/{{< version-num >}}/components/security-manager/src/main/resources/high_security.policy) — a high-security policy that prevents the most critical security risks and additionally prevents access to files, the network, and reflection. This is the default policy.
* [basic_security.policy](https://raw.githubusercontent.com/corda/corda-runtime-os/release/os/{{< version-num >}}/components/security-manager/src/main/resources/basic_security.policy) — a basic security policy that prevents only the most critical security risks.
* [medium_security.policy](https://raw.githubusercontent.com/corda/corda-runtime-os/release/os/{{< version-num >}}/components/security-manager/src/main/resources/medium_security.policy) —  a medium security policy that prevents the most critical security risks and additionally prevents access to files and the network.

Corda applies the strictest policy, `high_security.policy`, by default. You can override this by specifying a policy in the <a href = "./fields/security.md" >`corda.security` section</a> using [dynamic configuration]({{< relref "./dynamic.md" >}}). You can copy one of the predefined policies or customize one for your organization's specific needs.

Policies can have `ALLOW` and `DENY` access blocks that represent a string encoded [ConditionalPermissionInfo](https://docs.osgi.org/javadoc/r4v42/org/osgi/service/condpermadmin/ConditionalPermissionInfo.html#getEncoded()). A block at a higher position has a higher priority. Each block starts with conditions that must be satisfied in order to apply that block. Next, the block lists a set of permissions that are either allowed or denied based on the block type. The [basic syntax](https://docs.osgi.org/specification/osgi.core/8.0.0/service.condpermadmin.html#i1716478) is:

```java
policy      ::= access '{' conditions permissions '}' name?
access      ::= 'ALLOW' | 'DENY'       // case insensitive 
conditions  ::= ( '[' qname quoted-string* ']' )*
permissions ::= ( '(' qname (quoted-string quoted-string?)? ')' )+
name        ::= quoted-string
```

The following snippet shows an example of a deny-access block for the flow {{< tooltip >}}sandbox{{< /tooltip >}}:

```java
DENY {
[org.osgi.service.condpermadmin.BundleLocationCondition "FLOW/*"]

(java.io.FilePermission "<<ALL FILES>>" "read,write,delete,execute,readLink")
(java.lang.RuntimePermission "getFileSystemAttributes" "")
(java.lang.RuntimePermission "readFileDescriptor" "")
(java.lang.RuntimePermission "writeFileDescriptor" "")
(java.net.SocketPermission "*:1−" "accept,listen,connect,resolve")
(java.net.URLPermission "http://*:*" "*:*")
(java.net.URLPermission "https://*:*" "*:*")
(java.lang.RuntimePermission "accessDeclaredMembers" "")
(java.lang.reflect.ReflectPermission "suppressAccessChecks" "")
(java.lang.reflect.ReflectPermission "newProxyInPackage.*" "")

} "High security profile for FLOW Sandbox"
```

For more information about JDK permissions, see the [Oracle documentation](https://docs.oracle.com/en/java/javase/11/security/permissions-jdk1.html).
