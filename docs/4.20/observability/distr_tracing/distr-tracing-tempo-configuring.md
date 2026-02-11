The Tempo Operator uses a custom resource definition (CRD) file that defines the architecture and configuration settings for creating and deploying the Distributed Tracing Platform resources. You can install the default configuration or modify the file.

# Configuring back-end storage

For information about configuring the back-end storage, see [Understanding persistent storage](../../storage/understanding-persistent-storage.xml#understanding-persistent-storage) and the relevant configuration section for your chosen storage option.

# Introduction to TempoStack configuration parameters

The `TempoStack` custom resource (CR) defines the architecture and settings for creating the Distributed Tracing Platform resources. You can modify these parameters to customize your implementation to your business needs.

<div class="formalpara">

<div class="title">

Example `TempoStack` CR

</div>

``` yaml
apiVersion: tempo.grafana.com/v1alpha1
kind: TempoStack
metadata:
  name: <name>
spec:
  storage: {}
  resources: {}
  replicationFactor: 1
  retention:
    global:
      traces: 48h
    perTenant: {}
  template:
      distributor: {}
      ingester: {}
      compactor: {}
      querier: {}
      queryFrontend: {}
      gateway: {}
  limits:
    global:
      ingestion: {}
      query: {}
  observability:
    grafana: {}
    metrics: {}
    tracing: {}
  search: {}
  managementState: managed
```

</div>

- API version to use when creating the object.

- Defines the kind of Kubernetes object to create.

- Data that uniquely identifies the object, including a `name` string, `UID`, and optional `namespace`. OpenShift Container Platform automatically generates the `UID` and completes the `namespace` with the name of the project where the object is created.

- Name of the TempoStack instance.

- Contains all of the configuration parameters of the TempoStack instance. When a common definition for all Tempo components is required, define it in the `spec` section. When the definition relates to an individual component, place it in the `spec.template.<component>` section.

- Storage is specified at instance deployment. See the installation page for information about storage options for the instance.

- Defines the compute resources for the Tempo container.

- Integer value for the number of ingesters that must acknowledge the data from the distributors before accepting a span.

- Configuration options for retention of traces. The default value is `48h`.

- Configuration options for the Tempo `distributor` component.

- Configuration options for the Tempo `ingester` component.

- Configuration options for the Tempo `compactor` component.

- Configuration options for the Tempo `querier` component.

- Configuration options for the Tempo `query-frontend` component.

- Configuration options for the Tempo `gateway` component.

- Limits ingestion and query rates.

- Defines ingestion rate limits.

- Defines query rate limits.

- Configures operands to handle telemetry data.

- Configures search capabilities.

- Defines whether or not this CR is managed by the Operator. The default value is `managed`.

| Parameter | Description | Values | Default value |
|----|----|----|----|
| `apiVersion:` | API version to use when creating the object. | `tempo.grafana.com/v1alpha1` | `tempo.grafana.com/v1alpha1` |
| `kind:` | Defines the kind of the Kubernetes object to create. | `tempo` |  |
| `metadata:` | Data that uniquely identifies the object, including a `name` string, `UID`, and optional `namespace`. |  | OpenShift Container Platform automatically generates the `UID` and completes the `namespace` with the name of the project where the object is created. |
| `name:` | Name for the object. | Name of your TempoStack instance. | `tempo-all-in-one-inmemory` |
| `spec:` | Specification for the object to be created. | Contains all of the configuration parameters for your TempoStack instance. When a common definition for all Tempo components is required, it is defined under the `spec` node. When the definition relates to an individual component, it is placed under the `spec.template.<component>` node. | N/A |
| `resources:` | Resources assigned to the TempoStack instance. |  |  |
| `storageSize:` | Storage size for ingester PVCs. |  |  |
| `replicationFactor:` | Configuration for the replication factor. |  |  |
| `retention:` | Configuration options for retention of traces. |  |  |
| `storage:` | Configuration options that define the storage. |  |  |
| `template.distributor:` | Configuration options for the Tempo distributor. |  |  |
| `template.ingester:` | Configuration options for the Tempo ingester. |  |  |
| `template.compactor:` | Configuration options for the Tempo compactor. |  |  |
| `template.querier:` | Configuration options for the Tempo querier. |  |  |
| `template.queryFrontend:` | Configuration options for the Tempo query frontend. |  |  |
| `template.gateway:` | Configuration options for the Tempo gateway. |  |  |

`TempoStack` CR parameters

<div>

<div class="title">

Additional resources

</div>

- [Installing a TempoStack instance](../../observability/distr_tracing/distr-tracing-tempo-installing.xml#distr-tracing-tempo-installing)

- [Installing a TempoMonolithic instance](../../observability/distr_tracing/distr-tracing-tempo-installing.xml#distr-tracing-tempo-installing)

</div>

# Query configuration options

Two components of the Distributed Tracing Platform, the querier and query frontend, manage queries. You can configure both of these components.

The querier component finds the requested trace ID in the ingesters or back-end storage. Depending on the set parameters, the querier component can query both the ingesters and pull bloom or indexes from the back end to search blocks in object storage. The querier component exposes an HTTP endpoint at `GET /querier/api/traces/<trace_id>`, but it is not expected to be used directly. Queries must be sent to the query frontend.

| Parameter | Description | Values |
|----|----|----|
| `nodeSelector` | The simple form of the node-selection constraint. | type: object |
| `replicas` | The number of replicas to be created for the component. | type: integer; format: int32 |
| `tolerations` | Component-specific pod tolerations. | type: array |

Configuration parameters for the querier component

The query frontend component is responsible for sharding the search space for an incoming query. The query frontend exposes traces via a simple HTTP endpoint: `GET /api/traces/<trace_id>`. Internally, the query frontend component splits the `blockID` space into a configurable number of shards and then queues these requests. The querier component connects to the query frontend component via a streaming gRPC connection to process these sharded queries.

| Parameter | Description | Values |
|----|----|----|
| `component` | Configuration of the query frontend component. | type: object |
| `component.nodeSelector` | The simple form of the node selection constraint. | type: object |
| `component.replicas` | The number of replicas to be created for the query frontend component. | type: integer; format: int32 |
| `component.tolerations` | Pod tolerations specific to the query frontend component. | type: array |
| `jaegerQuery` | The options specific to the Jaeger Query component. | type: object |
| `jaegerQuery.enabled` | When `enabled`, creates the Jaeger Query component,`jaegerQuery`. | type: boolean |
| `jaegerQuery.ingress` | The options for the Jaeger Query ingress. | type: object |
| `jaegerQuery.ingress.annotations` | The annotations of the ingress object. | type: object |
| `jaegerQuery.ingress.host` | The hostname of the ingress object. | type: string |
| `jaegerQuery.ingress.ingressClassName` | The name of an IngressClass cluster resource. Defines which ingress controller serves this ingress resource. | type: string |
| `jaegerQuery.ingress.route` | The options for the OpenShift route. | type: object |
| `jaegerQuery.ingress.route.termination` | The termination type. The default is `edge`. | type: string (enum: insecure, edge, passthrough, reencrypt) |
| `jaegerQuery.ingress.type` | The type of ingress for the Jaeger Query UI. The supported types are `ingress`, `route`, and `none`. | type: string (enum: ingress, route) |
| `jaegerQuery.monitorTab` | The monitor tab configuration. | type: object |
| `jaegerQuery.monitorTab.enabled` | Enables the monitor tab in the Jaeger console. The `PrometheusEndpoint` must be configured. | type: boolean |
| `jaegerQuery.monitorTab.prometheusEndpoint` | The endpoint to the Prometheus instance that contains the span rate, error, and duration (RED) metrics. For example, `https://thanos-querier.openshift-monitoring.svc.cluster.local:9092`. | type: string |

Configuration parameters for the query frontend component

<div class="formalpara">

<div class="title">

Example configuration of the query frontend component in a `TempoStack` CR

</div>

``` yaml
apiVersion: tempo.grafana.com/v1alpha1
kind: TempoStack
metadata:
  name: simplest
spec:
  storage:
    secret:
      name: minio
      type: s3
  storageSize: 200M
  resources:
    total:
      limits:
        memory: 2Gi
        cpu: 2000m
  template:
    queryFrontend:
      jaegerQuery:
        enabled: true
        ingress:
          route:
            termination: edge
          type: route
```

</div>

<div>

<div class="title">

Additional resources

</div>

- [Understanding taints and tolerations](../../nodes/scheduling/nodes-scheduler-taints-tolerations.xml#nodes-scheduler-taints-tolerations-about_nodes-scheduler-taints-tolerations)

</div>

# Configuring the UI

You can use the distributed tracing UI plugin of the Cluster Observability Operator (COO) as the user interface (UI) for the Red Hat OpenShift Distributed Tracing Platform. For more information about installing and using the distributed tracing UI plugin, see "Distributed tracing UI plugin" in *Cluster Observability Operator*.

<div>

<div class="title">

Additional resources

</div>

- [Distributed tracing UI plugin](https://docs.redhat.com/en/documentation/red_hat_openshift_cluster_observability_operator/1-latest/html/ui_plugins_for_red_hat_openshift_cluster_observability_operator/distributed-tracing-ui-plugin)

</div>

# Configuring the Monitor tab in Jaeger UI

You can have the request rate, error, and duration (RED) metrics extracted from traces and visualized through the Jaeger Console in the **Monitor** tab of the OpenShift Container Platform web console. The metrics are derived from spans in the OpenTelemetry Collector that are scraped from the Collector by Prometheus, which you can deploy in your user-workload monitoring stack. The Jaeger UI queries these metrics from the Prometheus endpoint and visualizes them.

<div>

<div class="title">

Prerequisites

</div>

- You have configured the permissions and tenants for the Distributed Tracing Platform. For more information, see "Configuring the permissions and tenants".

</div>

<div>

<div class="title">

Procedure

</div>

1.  In the `OpenTelemetryCollector` custom resource of the OpenTelemetry Collector, enable the Spanmetrics Connector (`spanmetrics`), which derives metrics from traces and exports the metrics in the Prometheus format.

    <div class="formalpara">

    <div class="title">

    Example `OpenTelemetryCollector` custom resource for span RED

    </div>

    ``` yaml
    apiVersion: opentelemetry.io/v1beta1
    kind: OpenTelemetryCollector
    metadata:
      name: otel
    spec:
      mode: deployment
      observability:
        metrics:
          enableMetrics: true
      config: |
        connectors:
          spanmetrics:
            metrics_flush_interval: 15s

        receivers:
          otlp:
            protocols:
              grpc:
              http:

        exporters:
          prometheus:
            endpoint: 0.0.0.0:8889
            add_metric_suffixes: false
            resource_to_telemetry_conversion:
              enabled: true

          otlp:
            auth:
              authenticator: bearertokenauth
            endpoint: tempo-redmetrics-gateway.mynamespace.svc.cluster.local:8090
            headers:
              X-Scope-OrgID: dev
            tls:
              ca_file: /var/run/secrets/kubernetes.io/serviceaccount/service-ca.crt
              insecure: false

        extensions:
          bearertokenauth:
            filename: /var/run/secrets/kubernetes.io/serviceaccount/token

        service:
          extensions:
          - bearertokenauth
          pipelines:
            traces:
              receivers: [otlp]
              exporters: [otlp, spanmetrics]
            metrics:
              receivers: [spanmetrics]
              exporters: [prometheus]

    # ...
    ```

    </div>

    - Creates the `ServiceMonitor` custom resource to enable scraping of the Prometheus exporter.

    - The Spanmetrics connector receives traces and exports metrics.

    - The OTLP receiver to receive spans in the OpenTelemetry protocol.

    - The Prometheus exporter is used to export metrics in the Prometheus format.

    - The resource attributes are dropped by default.

    - The Spanmetrics connector is configured as exporter in traces pipeline.

    - The Spanmetrics connector is configured as receiver in metrics pipeline.

2.  In the `TempoStack` custom resource, enable the **Monitor** tab and set the Prometheus endpoint to the Thanos querier service to query the data from your user-defined monitoring stack.

    <div class="formalpara">

    <div class="title">

    Example `TempoStack` custom resource with the enabled Monitor tab

    </div>

    ``` yaml
    apiVersion: tempo.grafana.com/v1alpha1
    kind: TempoStack
    metadata:
      name: redmetrics
    spec:
      storage:
        secret:
          name: minio-test
          type: s3
      storageSize: 1Gi
      tenants:
        mode: openshift
        authentication:
          - tenantName: dev
            tenantId: "1610b0c3-c509-4592-a256-a1871353dbfa"
      template:
        gateway:
          enabled: true
        queryFrontend:
          jaegerQuery:
            monitorTab:
              enabled: true
              prometheusEndpoint: https://thanos-querier.openshift-monitoring.svc.cluster.local:9092
              redMetricsNamespace: ""

    # ...
    ```

    </div>

    - Enables the monitoring tab in the Jaeger console.

    - The service name for Thanos Querier from user-workload monitoring.

    - Optional: The metrics namespace on which the Jaeger query retrieves the Prometheus metrics. Include this line only if you are using an OpenTelemetry Collector version earlier than 0.109.0. If you are using an OpenTelemetry Collector version 0.109.0 or later, omit this line.

3.  Optional: Use the span RED metrics generated by the `spanmetrics` connector with alerting rules. For example, for alerts about a slow service or to define service level objectives (SLOs), the connector creates a `duration_bucket` histogram and the `calls` counter metric. These metrics have labels that identify the service, API name, operation type, and other attributes.

    <table>
    <caption>Labels of the metrics created in the <code>spanmetrics</code> connector</caption>
    <colgroup>
    <col style="width: 33%" />
    <col style="width: 33%" />
    <col style="width: 33%" />
    </colgroup>
    <thead>
    <tr>
    <th style="text-align: left;">Label</th>
    <th style="text-align: left;">Description</th>
    <th style="text-align: left;">Values</th>
    </tr>
    </thead>
    <tbody>
    <tr>
    <td style="text-align: left;"><p><code>service_name</code></p></td>
    <td style="text-align: left;"><p>Service name set by the <code>otel_service_name</code> environment variable.</p></td>
    <td style="text-align: left;"><p><code>frontend</code></p></td>
    </tr>
    <tr>
    <td style="text-align: left;"><p><code>span_name</code></p></td>
    <td style="text-align: left;"><p>Name of the operation.</p></td>
    <td style="text-align: left;"><ul>
    <li><p><code>/</code></p></li>
    <li><p><code>/customer</code></p></li>
    </ul></td>
    </tr>
    <tr>
    <td style="text-align: left;"><p><code>span_kind</code></p></td>
    <td style="text-align: left;"><p>Identifies the server, client, messaging, or internal operation.</p></td>
    <td style="text-align: left;"><ul>
    <li><p><code>SPAN_KIND_SERVER</code></p></li>
    <li><p><code>SPAN_KIND_CLIENT</code></p></li>
    <li><p><code>SPAN_KIND_PRODUCER</code></p></li>
    <li><p><code>SPAN_KIND_CONSUMER</code></p></li>
    <li><p><code>SPAN_KIND_INTERNAL</code></p></li>
    </ul></td>
    </tr>
    </tbody>
    </table>

    <div class="formalpara">

    <div class="title">

    Example `PrometheusRule` custom resource that defines an alerting rule for SLO when not serving 95% of requests within 2000ms on the front-end service

    </div>

    ``` yaml
    apiVersion: monitoring.coreos.com/v1
    kind: PrometheusRule
    metadata:
      name: span-red
    spec:
      groups:
      - name: server-side-latency
        rules:
        - alert: SpanREDFrontendAPIRequestLatency
          expr: histogram_quantile(0.95, sum(rate(duration_bucket{service_name="frontend", span_kind="SPAN_KIND_SERVER"}[5m])) by (le, service_name, span_name)) > 2000
          labels:
            severity: Warning
          annotations:
            summary: "High request latency on {{$labels.service_name}} and {{$labels.span_name}}"
            description: "{{$labels.instance}} has 95th request latency above 2s (current value: {{$value}}s)"
    ```

    </div>

    - The expression for checking if 95% of the front-end server response time values are below 2000 ms. The time range (`[5m]`) must be at least four times the scrape interval and long enough to accommodate a change in the metric.

</div>

<div>

<div class="title">

Additional resources

</div>

- [Configuring the permissions and tenants](../../observability/distr_tracing/distr-tracing-tempo-installing.xml#distr-tracing-tempo-installing)

</div>

# Configuring the receiver TLS

The custom resource of your TempoStack or TempoMonolithic instance supports configuring the TLS for receivers by using user-provided certificates or OpenShift’s service serving certificates.

## Receiver TLS configuration for a TempoStack instance

You can provide a TLS certificate in a secret or use the service serving certificates that are generated by OpenShift Container Platform.

- To provide a TLS certificate in a secret, configure it in the `TempoStack` custom resource.

  > [!NOTE]
  > This feature is not supported with the enabled Tempo Gateway.

  <div class="formalpara">

  <div class="title">

  TLS for receivers and using a user-provided certificate in a secret

  </div>

  ``` yaml
  apiVersion: tempo.grafana.com/v1alpha1
  kind:  TempoStack
  # ...
  spec:
  # ...
    template:
      distributor:
        tls:
          enabled: true
          certName: <tls_secret>
          caName: <ca_name>
  # ...
  ```

  </div>

  - TLS enabled at the Tempo Distributor.

  - Secret containing a `tls.key` key and `tls.crt` certificate that you apply in advance.

  - Optional: CA in a config map to enable mutual TLS authentication (mTLS).

- Alternatively, you can use the service serving certificates that are generated by OpenShift Container Platform.

  > [!NOTE]
  > Mutual TLS authentication (mTLS) is not supported with this feature.

  <div class="formalpara">

  <div class="title">

  TLS for receivers and using the service serving certificates that are generated by OpenShift Container Platform

  </div>

  ``` yaml
  apiVersion: tempo.grafana.com/v1alpha1
  kind:  TempoStack
  # ...
  spec:
  # ...
    template:
      distributor:
        tls:
          enabled: true
  # ...
  ```

  </div>

  - Sufficient configuration for the TLS at the Tempo Distributor.

<div>

<div class="title">

Additional resources

</div>

- [Understanding service serving certificates](../../security/certificates/service-serving-certificate.xml#understanding-service-serving_service-serving-certificate)

- [Service CA certificates](../../security/certificate_types_descriptions/service-ca-certificates.xml#cert-types-service-ca-certificates)

</div>

## Receiver TLS configuration for a TempoMonolithic instance

You can provide a TLS certificate in a secret or use the service serving certificates that are generated by OpenShift Container Platform.

- To provide a TLS certificate in a secret, configure it in the `TempoMonolithic` custom resource.

  > [!NOTE]
  > This feature is not supported with the enabled Tempo Gateway.

  <div class="formalpara">

  <div class="title">

  TLS for receivers and using a user-provided certificate in a secret

  </div>

  ``` yaml
  apiVersion: tempo.grafana.com/v1alpha1
  kind:  TempoMonolithic
  # ...
    spec:
  # ...
    ingestion:
      otlp:
        grpc:
          tls:
            enabled: true
            certName: <tls_secret>
            caName: <ca_name>
  # ...
  ```

  </div>

  - TLS enabled at the Tempo Distributor.

  - Secret containing a `tls.key` key and `tls.crt` certificate that you apply in advance.

  - Optional: CA in a config map to enable mutual TLS authentication (mTLS).

- Alternatively, you can use the service serving certificates that are generated by OpenShift Container Platform.

  > [!NOTE]
  > Mutual TLS authentication (mTLS) is not supported with this feature.

  <div class="formalpara">

  <div class="title">

  TLS for receivers and using the service serving certificates that are generated by OpenShift Container Platform

  </div>

  ``` yaml
  apiVersion: tempo.grafana.com/v1alpha1
  kind:  TempoMonolithic
  # ...
    spec:
  # ...
    ingestion:
      otlp:
        grpc:
          tls:
            enabled: true
        http:
          tls:
            enabled: true
  # ...
  ```

  </div>

  - Minimal configuration for the TLS at the Tempo Distributor.

<div>

<div class="title">

Additional resources

</div>

- [Understanding service serving certificates](../../security/certificates/service-serving-certificate.xml#understanding-service-serving_service-serving-certificate)

- [Service CA certificates](../../security/certificate_types_descriptions/service-ca-certificates.xml#cert-types-service-ca-certificates)

</div>

# Configuring the query RBAC

As an administrator, you can set up the query role-based access control (RBAC) to filter the span attributes for your users by the namespaces for which you granted them permissions.

> [!NOTE]
> When you enable the query RBAC, users can still access traces from all namespaces, and the `service.name` and `k8s.namespace.name` attributes are also visible to all users.

<div>

<div class="title">

Prerequisites

</div>

- An active OpenShift CLI (`oc`) session by a cluster administrator with the `cluster-admin` role.

  <div class="tip">

  <div class="title">

  </div>

  - Ensure that your OpenShift CLI (`oc`) version is up to date and matches your OpenShift Container Platform version.

  - Run `oc login`:

    ``` terminal
    $ oc login --username=<your_username>
    ```

  </div>

</div>

<div>

<div class="title">

Procedure

</div>

1.  Enable multitenancy and query RBAC in the `TempoStack` custom resource (CR), for example:

    ``` yaml
    apiVersion: tempo.grafana.com/v1alpha1
    kind: TempoStack
    metadata:
      name: simplest
      namespace: chainsaw-multitenancy
    spec:
      storage:
        secret:
          name: minio
          type: s3
      storageSize: 1Gi
      resources:
        total:
          limits:
            memory: 2Gi
            cpu: 2000m
      tenants:
        mode: openshift
        authentication:
          - tenantName: dev
            tenantId: "1610b0c3-c509-4592-a256-a1871353dbfb"
      template:
        gateway:
          enabled: true
          rbac:
            enabled: true
        queryFrontend:
          jaegerQuery:
            enabled: false
    ```

    - Always set to `true`.

    - Always set to `true`.

    - Always set to `false`.

2.  Create a cluster role and cluster role binding to grant the target users the permissions to access the tenant that you specified in the `TempoStack` CR, for example:

    ``` yaml
    apiVersion: rbac.authorization.k8s.io/v1
    kind: ClusterRole
    metadata:
      name: tempo-dev-read
    rules:
    - apiGroups: [tempo.grafana.com]
      resources: [dev]
      resourceNames: [traces]
      verbs: [get]
    ---
    apiVersion: rbac.authorization.k8s.io/v1
    kind: ClusterRoleBinding
    metadata:
      name: tempo-dev-read
    roleRef:
      apiGroup: rbac.authorization.k8s.io
      kind: ClusterRole
      name: tempo-dev-read
    subjects:
      - kind: Group
        apiGroup: rbac.authorization.k8s.io
        name: system:authenticated
    ```

    - Tenant name in the `TempoStack` CR.

    - Means all authenticated OpenShift users.

3.  Grant the target users the permissions to read attributes for the project. You can do this by running the following command:

    ``` bash
    $ oc adm policy add-role-to-user view <username> -n <project>
    ```

</div>

# Using taints and tolerations

To schedule the TempoStack pods on dedicated nodes, see [How to deploy the different TempoStack components on infra nodes using nodeSelector and tolerations in OpenShift 4](https://access.redhat.com/solutions/7040685).

# Configuring monitoring and alerts

The Tempo Operator supports monitoring and alerts about each TempoStack component such as distributor, ingester, and so on, and exposes upgrade and operational metrics about the Operator itself.

## Configuring the TempoStack metrics and alerts

You can enable metrics and alerts of TempoStack instances.

<div>

<div class="title">

Prerequisites

</div>

- Monitoring for user-defined projects is enabled in the cluster.

</div>

<div>

<div class="title">

Procedure

</div>

1.  To enable metrics of a TempoStack instance, set the `spec.observability.metrics.createServiceMonitors` field to `true`:

    ``` yaml
    apiVersion: tempo.grafana.com/v1alpha1
    kind: TempoStack
    metadata:
      name: <name>
    spec:
      observability:
        metrics:
          createServiceMonitors: true
    ```

2.  To enable alerts for a TempoStack instance, set the `spec.observability.metrics.createPrometheusRules` field to `true`:

    ``` yaml
    apiVersion: tempo.grafana.com/v1alpha1
    kind: TempoStack
    metadata:
      name: <name>
    spec:
      observability:
        metrics:
          createPrometheusRules: true
    ```

</div>

<div class="formalpara">

<div class="title">

Verification

</div>

You can use the **Administrator** view of the web console to verify successful configuration:

</div>

1.  Go to **Observe** → **Targets**, filter for **Source: User**, and check that **ServiceMonitors** in the format `tempo-<instance_name>-<component>` have the **Up** status.

2.  To verify that alerts are set up correctly, go to **Observe** → **Alerting** → **Alerting rules**, filter for **Source: User**, and check that the **Alert rules** for the TempoStack instance components are available.

<div>

<div class="title">

Additional resources

</div>

- [Enabling monitoring for user-defined projects](https://docs.redhat.com/en/documentation/monitoring_stack_for_red_hat_openshift/4.20/html/configuring_user_workload_monitoring/preparing-to-configure-the-monitoring-stack-uwm#enabling-monitoring-for-user-defined-projects-uwm_preparing-to-configure-the-monitoring-stack-uwm)

</div>

## Configuring the Tempo Operator metrics and alerts

When installing the Tempo Operator from the web console, you can select the **Enable Operator recommended cluster monitoring on this Namespace** checkbox, which enables creating metrics and alerts of the Tempo Operator.

If the checkbox was not selected during installation, you can manually enable metrics and alerts even after installing the Tempo Operator.

<div>

<div class="title">

Procedure

</div>

- Add the `openshift.io/cluster-monitoring: "true"` label in the project where the Tempo Operator is installed, which is `openshift-tempo-operator` by default.

</div>

<div class="formalpara">

<div class="title">

Verification

</div>

You can use the **Administrator** view of the web console to verify successful configuration:

</div>

1.  Go to **Observe** → **Targets**, filter for **Source: Platform**, and search for `tempo-operator`, which must have the **Up** status.

2.  To verify that alerts are set up correctly, go to **Observe** → **Alerting** → **Alerting rules**, filter for **Source: Platform**, and locate the **Alert rules** for the **Tempo Operator**.
