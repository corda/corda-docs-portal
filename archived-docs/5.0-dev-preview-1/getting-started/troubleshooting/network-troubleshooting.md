---
date: '2021-09-07'
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-gettingstarted
    weight: 750
section_menu: corda-5-dev-preview
title: Troubleshooting a local Corda 5 network
expiryDate: '2022-09-28'
---

## ERROR: The Compose file is invalid

If you see this error while trying to use `docker-compose` with your generated `.yaml` config file, you may have an old version of Docker.
Try to upgrade.

```console
ERROR: The Compose file is invalid because:
networks.smoke-tests-network value Additional properties are not allowed ('name' was unexpected)
```

## Mac Docker memory allocation

Docker Desktop for Mac, by default, only assigns two GB of RAM to the Docker daemon. This isn't sufficient for running a three-node Corda network.
You can increase this in the Docker Desktop: go to **Preferences** and configure Docker Desktop to have at least six GB of RAM and use six cores.

## Windows Docker daemon

If you are using Docker on Windows, you may get this error when executing the end-to-end tests:

```console
org.apache.hc.client5.http.HttpHostConnectException: Connect to http://localhost:2375 [localhost/127.0.0.1, localhost/0:0:0:0:0:0:0:1] failed: Connection refused: connect
java.lang.RuntimeException: org.apache.hc.client5.http.HttpHostConnectException: Connect to http://localhost:2375 [localhost/127.0.0.1, localhost/0:0:0:0:0:0:0:1] failed: Connection refused: connect
  at com.github.dockerjava.httpclient5.ApacheDockerHttpClientImpl.execute(ApacheDockerHttpClientImpl.java:153)
  at com.github.dockerjava.httpclient5.ApacheDockerHttpClient.execute(ApacheDockerHttpClient.java:8)
  at
```

This is because we use the Docker Java API to interact with the Docker daemon (Unix sockets are used on Linux and macOS). On Windows you need to expose the daemon on port 2375 explicitly. Go to **Settings > General** and select the following options:

* **Expose daemon on tcp://localhost:2375 without TLS**
* **Use the WSL 2 based engine**

## Windows file sharing

If you use Windows, you may see an error like this:

```console  
ERROR: for smoke-tests-network-bootstrapper  Cannot create container for service bootstrapper: status code not OK but 500:  ☺   ˙˙˙˙☺       ♀☻   FDocker.Core, Version=3.0.2.51106, Culture=neutral, PublicKeyToken=null♣☺   ←Docker.Core.DockerException♀      ClassNameMessage♦Data♫InnerExceptionHelpURL►StackTraceString▬RemoteStackTraceString►RemoteStackIndex☼ExcWatsonBuckets☺☺♥♥☺☺☺ ☺ ☺▲System.Collections.IDictionary►System.Excepti☻☻   ♠♥   ←Docker.Core.DockerException♠♦   ▲Filesharing has been cancelled
♠♣   Ś‼   at Docker.ApiServices.Mounting.FileSharing.<DoShareAsync>d__8.MoveNext() in C:\workspaces\PR-15138\src\github.com\docker\pinata\win\src\Docker.ApiServices\Mounting\FileSharing.cs:line 0
--- End of stack trace from previous location where exception was thrown ---
   at System.Runtime.ExceptionServices.ExceptionDispatchInfo.Throw()
```

To resolve this, add the path to the **File sharing** options:

{{<
  figure
	 src="docker-windows-file-sharing.png"
	 zoom="docker-windows-file-sharing.png"
   width=80%
	 figcaption="Docker Windows File Sharing"
	 alt="docker windows file sharing"
>}}
