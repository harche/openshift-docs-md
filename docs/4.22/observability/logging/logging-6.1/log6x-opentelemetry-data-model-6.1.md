This document outlines the protocol and semantic conventions for Red Hat OpenShift Logging’s OpenTelemetry support with Logging 6.1.

> [!IMPORTANT]
> The OpenTelemetry Protocol (OTLP) output log forwarder is a Technology Preview feature only. Technology Preview features are not supported with Red Hat production service level agreements (SLAs) and might not be functionally complete. Red Hat does not recommend using them in production. These features provide early access to upcoming product features, enabling customers to test functionality and provide feedback during the development process.
>
> For more information about the support scope of Red Hat Technology Preview features, see [Technology Preview Features Support Scope](https://access.redhat.com/support/offerings/techpreview/).

# Forwarding and ingestion protocol

Red Hat OpenShift Logging collects and forwards logs to OpenTelemetry endpoints using [OTLP Specification](https://opentelemetry.io/docs/specs/otlp/). OTLP encodes, transports, and delivers telemetry data. You can also deploy Loki storage, which provides an OTLP endpont to ingest log streams. This document defines the semantic conventions for the logs collected from various OpenShift cluster sources.

# Semantic conventions

The log collector in this solution gathers the following log streams:

- Container logs

- Cluster node journal logs

- Cluster node auditd logs

- Kubernetes and OpenShift API server logs

- OpenShift Virtual Network (OVN) logs

You can forward these streams according to the semantic conventions defined by OpenTelemetry semantic attributes. The semantic conventions in OpenTelemetry define a resource as an immutable representation of the entity producing telemetry, identified by attributes. For example, a process running in a container includes attributes such as `container_name`, `cluster_id`, `pod_name`, `namespace`, and possibly `deployment` or `app_name`. These attributes are grouped under the resource object, which helps reduce repetition and optimizes log transmission as telemetry data.

In addition to resource attributes, logs might also contain scope attributes specific to instrumentation libraries and log attributes specific to each log entry. These attributes provide greater detail about each log entry and enhance filtering capabilities when querying logs in storage.

The following sections define the attributes that are generally forwarded.

## Log entry structure

All log streams include the following [log data](https://opentelemetry.io/docs/specs/otel/logs/data-model/#log-and-event-record-definition) fields:

The **Applicable Sources** column indicates which log sources each field applies to:

- `all`: This field is present in all logs.

- `container`: This field is present in Kubernetes container logs, both application and infrastructure.

- `audit`: This field is present in Kubernetes, OpenShift API, and OVN logs.

- `auditd`: This field is present in node auditd logs.

- `journal`: This field is present in node journal logs.

| Name | Applicable Sources | Comment |
|----|----|----|
| `body` | all |  |
| `observedTimeUnixNano` | all |  |
| `timeUnixNano` | all |  |
| `severityText` | container, journal |  |
| `attributes` | all | (Optional) Present when forwarding stream specific attributes |

## Attributes

Log entries include a set of resource, scope, and log attributes based on their source, as described in the following table.

The **Location** column specifies the type of attribute:

- `resource`: Indicates a resource attribute

- `scope`: Indicates a scope attribute

- `log`: Indicates a log attribute

The **Storage** column indicates whether the attribute is stored in a LokiStack using the default `openshift-logging` mode and specifies where the attribute is stored:

- `stream label`:

  - Enables efficient filtering and querying based on specific labels.

  - Can be labeled as `required` if the Loki Operator enforces this attribute in the configuration.

- `structured metadata`:

  - Allows for detailed filtering and storage of key-value pairs.

  - Enables users to use direct labels for streamlined queries without requiring JSON parsing.

With OTLP, users can filter queries directly by labels rather than using JSON parsing, improving the speed and efficiency of queries.

| Name | Location | Applicable Sources | Storage (LokiStack) | Comment |
|----|----|----|----|----|
| `log_source` | resource | all | required stream label | **(DEPRECATED)** Compatibility attribute, contains same information as `openshift.log.source` |
| `log_type` | resource | all | required stream label | **(DEPRECATED)** Compatibility attribute, contains same information as `openshift.log.type` |
| `kubernetes.container_name` | resource | container | stream label | **(DEPRECATED)** Compatibility attribute, contains same information as `k8s.container.name` |
| `kubernetes.host` | resource | all | stream label | **(DEPRECATED)** Compatibility attribute, contains same information as `k8s.node.name` |
| `kubernetes.namespace_name` | resource | container | required stream label | **(DEPRECATED)** Compatibility attribute, contains same information as `k8s.namespace.name` |
| `kubernetes.pod_name` | resource | container | stream label | **(DEPRECATED)** Compatibility attribute, contains same information as `k8s.pod.name` |
| `openshift.cluster_id` | resource | all |  | **(DEPRECATED)** Compatibility attribute, contains same information as `openshift.cluster.uid` |
| `level` | log | container, journal |  | **(DEPRECATED)** Compatibility attribute, contains same information as `severityText` |
| `openshift.cluster.uid` | resource | all | required stream label |  |
| `openshift.log.source` | resource | all | required stream label |  |
| `openshift.log.type` | resource | all | required stream label |  |
| `openshift.labels.*` | resource | all | structured metadata |  |
| `k8s.node.name` | resource | all | stream label |  |
| `k8s.namespace.name` | resource | container | required stream label |  |
| `k8s.container.name` | resource | container | stream label |  |
| `k8s.pod.labels.*` | resource | container | structured metadata |  |
| `k8s.pod.name` | resource | container | stream label |  |
| `k8s.pod.uid` | resource | container | structured metadata |  |
| `k8s.cronjob.name` | resource | container | stream label | Conditionally forwarded based on creator of pod |
| `k8s.daemonset.name` | resource | container | stream label | Conditionally forwarded based on creator of pod |
| `k8s.deployment.name` | resource | container | stream label | Conditionally forwarded based on creator of pod |
| `k8s.job.name` | resource | container | stream label | Conditionally forwarded based on creator of pod |
| `k8s.replicaset.name` | resource | container | structured metadata | Conditionally forwarded based on creator of pod |
| `k8s.statefulset.name` | resource | container | stream label | Conditionally forwarded based on creator of pod |
| `log.iostream` | log | container | structured metadata |  |
| `k8s.audit.event.level` | log | audit | structured metadata |  |
| `k8s.audit.event.stage` | log | audit | structured metadata |  |
| `k8s.audit.event.user_agent` | log | audit | structured metadata |  |
| `k8s.audit.event.request.uri` | log | audit | structured metadata |  |
| `k8s.audit.event.response.code` | log | audit | structured metadata |  |
| `k8s.audit.event.annotation.*` | log | audit | structured metadata |  |
| `k8s.audit.event.object_ref.resource` | log | audit | structured metadata |  |
| `k8s.audit.event.object_ref.name` | log | audit | structured metadata |  |
| `k8s.audit.event.object_ref.namespace` | log | audit | structured metadata |  |
| `k8s.audit.event.object_ref.api_group` | log | audit | structured metadata |  |
| `k8s.audit.event.object_ref.api_version` | log | audit | structured metadata |  |
| `k8s.user.username` | log | audit | structured metadata |  |
| `k8s.user.groups` | log | audit | structured metadata |  |
| `process.executable.name` | resource | journal | structured metadata |  |
| `process.executable.path` | resource | journal | structured metadata |  |
| `process.command_line` | resource | journal | structured metadata |  |
| `process.pid` | resource | journal | structured metadata |  |
| `service.name` | resource | journal | stream label |  |
| `systemd.t.*` | log | journal | structured metadata |  |
| `systemd.u.*` | log | journal | structured metadata |  |

> [!NOTE]
> Attributes marked as **Compatibility attribute** support minimal backward compatibility with the ViaQ data model. These attributes are deprecated and function as a compatibility layer to ensure continued UI functionality. These attributes will remain supported until the Logging UI fully supports the OpenTelemetry counterparts in future releases.

Loki changes the attribute names when persisting them to storage. The names will be lowercased, and all characters in the set: (`.`,`/`,`-`) will be replaced by underscores (`_`). For example, `k8s.namespace.name` will become `k8s_namespace_name`.

# Additional resources

- [Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/)

- [Logs Data Model](https://opentelemetry.io/docs/specs/otel/logs/data-model/)

- [General Logs Attributes](https://opentelemetry.io/docs/specs/semconv/general/logs/)
