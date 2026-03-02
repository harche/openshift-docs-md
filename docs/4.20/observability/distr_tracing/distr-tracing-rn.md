# About this release

Distributed Tracing Platform 3.9 is provided through the [Tempo Operator 0.20.0](https://catalog.redhat.com/software/containers/rhosdt/tempo-operator-bundle/642c3e0eacf1b5bdbba7654a/history) and based on the open source [Grafana Tempo](https://grafana.com/oss/tempo/) 2.10.0.

<div class="note">

Only supported features are documented. Undocumented features are currently unsupported. If you need assistance with a feature, contact Red Hat’s support.

</div>

# New features and enhancements

The Distributed Tracing Platform 3.9 release adds the following features and enhancements.

Upgrade to UBI 9
This release upgrades the Red Hat Universal Base Image (UBI) to version 9.

Network policies in `TempoStack` CRD
This update extends the `TempoStack` Custom Resource Definition (CRD) with a network policy option that enables the Operator to reconcile network policies among all components. This option is enabled by default.

[TRACING-5807](https://issues.redhat.com/browse/TRACING-5807)

Environment variables for Operator configuration
This update adds support for overriding the Operator configuration by using environment variables. You can configure Operator settings through the `Subscription` custom resource of the Operator Lifecycle Manager (OLM) without modifying ConfigMaps. The `--config` flag remains available for custom configuration files if needed.

[TRACING-5745](https://issues.redhat.com/browse/TRACING-5745)

T-shirt sizes for `TempoStack` deployments
This update introduces the `size` field for `TempoStack` deployments, which provides predefined t-shirt size configurations. Instead of manually calculating CPU, memory, and storage for each component, you can select a size that matches your workload scale. The following sizes are available: `1x.demo`, `1x.pico`, `1x.extra-small`, `1x.small`, and `1x.medium`. This field is optional and existing configurations using `resources.total` or per-component overrides continue to work unchanged.

[TRACING-5376](https://issues.redhat.com/browse/TRACING-5376)

Improved memory management for `TempoMonolithic` deployments
The Operator now automatically sets the `GOMEMLIMIT` soft memory limit for the Go garbage collector to 80% of the container memory limit for all Tempo components in a Tempo monolithic deployment. This reduces the likelihood of out-of-memory terminations.

[TRACING-4554](https://issues.redhat.com/browse/TRACING-4554)

A `TempoStack` or `TempoMonolithic` instance without the gateway is not supported
This update requires tenant configuration and an enabled gateway for `TempoStack` and `TempoMonolithic` instances. If you do not enable the gateway, the Operator displays a warning. For a `TempoStack` instance, enable the gateway by setting `.spec.template.gateway.enabled` to `true`. For a `TempoMonolithic` instance, the gateway is enabled automatically when any tenant is configured. `TempoStack` and `TempoMonolithic` instances without an enabled gateway are not supported.

[TRACING-5750](https://issues.redhat.com/browse/TRACING-5750)

<div class="note">

Some linked Jira tickets are accessible only with Red Hat credentials.

</div>

# Known issues

The Distributed Tracing Platform 3.9 release has the following known issue.

Gateway fails to forward OTLP HTTP traffic when receiver TLS is enabled
When Tempo Monolithic is configured with `multitenancy.enabled: true` and `ingestion.otlp.http.tls.enabled: true`, the gateway forwards OTLP HTTP traffic to the Tempo receiver using plain HTTP instead of HTTPS. As a consequence, the connection fails with a `connection reset by peer` error because the receiver expects TLS connections. OTLP gRPC ingestion through the gateway is not affected.

To work around this problem, disable TLS on the OTLP HTTP receiver by setting `ingestion.otlp.http.tls.enabled: false`.

[TRACING-5973](https://issues.redhat.com/browse/TRACING-5973)

# Fixed issues

The Distributed Tracing Platform 3.9 release fixes the following issues.

Fixed network policies for managed OpenShift services
Before this update, the Operator network policies used a hard-coded port 6443 for the API server. As a consequence, the Operator failed to connect to managed OpenShift services that expose the API on port 443. With this update, the Operator dynamically retrieves the control plane address from service endpoints. As a result, network policies work correctly on all OpenShift environments.

[TRACING-5974](https://issues.redhat.com/browse/TRACING-5974)

CVE-2025-61726
Before this update, a flaw existed in the `net/url` package in the Go standard library. As a consequence, a denial-of-service HTTP request with a massive number of query parameters could cause the application to consume an excessive amount of memory and eventually become unresponsive. This release eliminates this flaw.

[CVE-2025-61726](https://access.redhat.com/security/cve/cve-2025-61726)

CVE-2025-61729
Before this update, the `HostnameError.Error()` function in the Go `crypto/x509` package used string concatenation in a loop without limiting the number of printed hostnames. As a consequence, processing a malicious certificate with many hostnames could cause excessive CPU and memory consumption, leading to a denial-of-service condition. This release includes the fix for this flaw.

[CVE-2025-61729](https://access.redhat.com/security/cve/CVE-2025-61729)

CVE-2025-68121
Before this update, a flaw existed in the `crypto/tls` package in the Go standard library. As a consequence, during TLS session resumption, unauthorized clients or servers could bypass certificate validation if CA pools were mutated between handshakes. This release includes the fix for this flaw.

[CVE-2025-68121](https://access.redhat.com/security/cve/CVE-2025-68121)

<div class="note">

Some linked Jira tickets are accessible only with Red Hat credentials.

</div>

# Getting support

If you experience difficulty with a procedure described in this documentation, or with OpenShift Container Platform in general, visit the [Red Hat Customer Portal](http://access.redhat.com).

From the Customer Portal, you can:

- Search or browse through the Red Hat Knowledgebase of articles and solutions relating to Red Hat products.

- Submit a support case to Red Hat Support.

- Access other product documentation.

To identify issues with your cluster, you can use Red Hat Lightspeed in [OpenShift Cluster Manager](https://console.redhat.com/openshift). Red Hat Lightspeed provides details about issues and, if available, information on how to solve a problem.

If you have a suggestion for improving this documentation or have found an error, submit a [Jira issue](https://issues.redhat.com/secure/CreateIssueDetails!init.jspa?pid=12332330&summary=Documentation_issue&issuetype=1&components=12367614&priority=10200&versions=12385624) for the most relevant documentation component. Please provide specific details, such as the section name and OpenShift Container Platform version.

<div class="warning">

The deprecated Red Hat OpenShift Distributed Tracing Platform (Jaeger) 3.5 was the last release of the Red Hat OpenShift Distributed Tracing Platform (Jaeger) that Red Hat supported.

All support and maintenance for the deprecated Red Hat OpenShift Distributed Tracing Platform (Jaeger) 3.5 ended on November 3, 2025.

If you still use Red Hat OpenShift Distributed Tracing Platform (Jaeger), you must migrate to Red Hat build of OpenTelemetry Operator and Tempo Operator for distributed tracing collection and storage. For more information, see "Migrating" in the Red Hat build of OpenTelemetry documentation, "Installing" in the Red Hat build of OpenTelemetry documentation, and "Installing" in the Red Hat OpenShift Distributed Tracing Platform documentation.

For more information, see the Red Hat Knowledgebase solution [Jaeger Deprecation and Removal in OpenShift](https://access.redhat.com/solutions/7083722).

</div>
