---
date: '2023-05-10'
title: "Logs"
menu:
  corda5:
    parent: corda5-cluster-observability
    identifier: corda5-cluster-logs
    weight: 3000
section_menu: corda5
---

Corda workers write their logs to standard out/standard error from where they are collected by Kubernetes.
You can retrieve the logs for a single pod using `kubectl`:

```kubectl
kubectl logs <POD_NAME>
```

If the pod has restarted due to an error, you can retrieve the logs from the previous instance:

```kubectl
kubectl logs --previous <POD_NAME>
```

You can use a selector to retrieve logs from all of the Corda pods, each line prefixed with the name of the pod:

```kubectl
kubectl logs --selector=app.kubernetes.io/name=corda --prefix
```

Most observability platforms are capable of receiving logs from containers running on Kubernetes.

## Log Format

By default, the logs are JSON formatted using the [JsonLayout](https://logging.apache.org/log4j/2.x/manual/json-template-layout.html#event-templates)
template for Log4J’s `JsonTemplateLayout`.
When working without the benefit of an observability platform to parse the JSON logs, it may be desirable
to install Corda with a text log format instead. Use the following overrides when installing the Corda Helm chart:

```yaml
logging:
format: "text"
```

## Log Level

The default log level is `info`. To get additional diagnostic information, you may modify this via the Helm chart overrides. For example:

```yaml
logging:
level: "debug"
```

You can also modify the log level for just a single type of worker. For example:

```yaml
workers:
db:
logging:
level: "trace"
```

The supported values for the log level are `all`, `trace`, `debug`, `info`, `warn`, `error`, `fatal`, and `off`.
Pods will be restarted for the new log level to take effect.
