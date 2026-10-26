Monitor network traffic immediately after cluster creation by automatically installing network observability during the installation process. This Technology Preview feature requires enabling the `NetworkObservabilityInstall` feature gate.

> [!IMPORTANT]
> {FeatureName} is a Technology Preview feature only. Technology Preview features are not supported with Red Hat production service level agreements (SLAs) and might not be functionally complete. Red Hat does not recommend using them in production. These features provide early access to upcoming product features, enabling customers to test functionality and provide feedback during the development process.
>
> For more information about the support scope of Red Hat Technology Preview features, see [Technology Preview Features Support Scope](https://access.redhat.com/support/offerings/techpreview/).

# Automatic network observability installation

Technology Preview clusters with the `NetworkObservabilityInstall` feature gate enabled automatically install the Network Observability Operator during cluster creation.

> [!IMPORTANT]
> Automatic network observability installation is a Technology Preview feature only. Technology Preview features are not supported with Red Hat production service level agreements (SLAs) and might not be functionally complete. Red Hat does not recommend using them in production. These features provide early access to upcoming product features, enabling customers to test functionality and provide feedback during the development process.
>
> For more information about the support scope of Red Hat Technology Preview features, see [Technology Preview Features Support Scope](https://access.redhat.com/support/offerings/techpreview/).

> [!IMPORTANT]
> The `NetworkObservabilityInstall` feature gate is required to use this Technology Preview feature in OpenShift Container Platform 5.0. Clusters created with this feature gate cannot be upgraded when the feature becomes generally available. You must create a new cluster to use the GA version.

On OpenShift Container Platform 5.0 clusters with the `NetworkObservabilityInstall` feature gate enabled, the Network Observability Operator and its dependencies are automatically installed and configured during cluster creation. This provides immediate access to network traffic monitoring capabilities through the OpenShift Container Platform web console.

You can use network observability to complete the following tasks:

- Monitor network traffic between pods, services, and external endpoints.

- Identify network performance issues such as packet loss and latency.

- Troubleshoot connectivity problems between applications.

- Analyze network usage patterns for capacity planning.

- Detect security anomalies in network behavior.

## Prerequisites for automatic network observability installation (Technology Preview)

Network Observability automatic installation is a Technology Preview feature that requires the `NetworkObservabilityInstall` feature gate. To use this feature during cluster installation, you must complete the following tasks:

- Enable the `NetworkObservabilityInstall` feature gate by creating a manifest file during cluster installation.

- Accept that enabling the `CustomNoUpgrade` feature set prevents minor version updates.

- Understand that clusters installed with this Technology Preview feature cannot be upgraded when the feature reaches general availability (GA). You must create a new cluster using the GA version.

## When network observability is enabled

When the `NetworkObservabilityInstall` feature gate is enabled, the following cluster types enable network observability by default during cluster installation:

- Standard multi-node clusters

- Hosted Control Plane clusters

The following cluster types do not enable network observability by default:

- Single-node OpenShift clusters, due to resource constraints. You can override this by setting `installationPolicy` to `InstallAndEnable` in the installation configuration.

- Clusters where you set `installationPolicy` to `NoAction` in the installation configuration.

## Accessing network observability features

After cluster installation completes, you can access network observability features immediately without additional configuration:

Network traffic overview
View cluster-wide network traffic metrics and identify top talkers from **Observe** → **Network Traffic** in the web console.

Network topology visualization
Explore visual representations of network traffic flows between namespaces, workloads, and nodes.

Metrics and dashboards
Access Prometheus metrics and Grafana dashboards that track network performance indicators including throughput, packet drops, and connection counts.

## Resource impact

The default network observability configuration balances monitoring capabilities with cluster resource usage. On typical clusters, network observability consumes approximately 3-5% of CPU and memory resources per node.

The automatic installation creates a `FlowCollector` resource with the following default configuration:

- **Agent type**: eBPF with DNS tracking enabled

- **Sampling interval**: 400 (collects 1 in every 400 flows)

- **Deployment model**: Service

- **Loki storage**: None (metrics are stored, but flows are not persisted)

- **Namespace**: `netobserv`

> [!NOTE]
> To enable flow persistence and features that require flow records, you must configure a `LokiStack`. Without a `LokiStack`, flow data is not stored for historical analysis.

If you need to reduce resource consumption, you can customize the `FlowCollector` resource configuration to adjust sampling rates, filter traffic, or disable specific features.

## Deployment lifecycle

The automatic network observability installation occurs during cluster creation in OpenShift Container Platform 5.0 or later, or when upgrading from OpenShift Container Platform 4.22 to 5.0. The Cluster Network Operator (CNO) installs the Network Observability Operator and creates a default `FlowCollector` custom resource (CR).

The installation process typically completes within a few minutes after the cluster becomes available. If installation fails, the CNO automatically rolls back the changes.

The CNO does not monitor or manage the Network Observability Operator after installation attempts complete. If you delete the Network Observability Operator or the `FlowCollector` resource, they are not automatically reinstalled.

The CNO does not manage the `FlowCollector` resource because it is managed by the Network Observability Operator.

> [!NOTE]
> To reset the installation state and allow the CNO to retry automatic installation, remove the `NetworkObservabilityInstalledByCNO` status condition from the Network CR:
>
> ``` terminal
> $ oc edit network.operator cluster --subresource=status
> ```
>
> Delete the condition entry where `type: NetworkObservabilityInstalledByCNO`. After saving, the CNO can attempt installation again based on the configured `installationPolicy`.

To remove network observability, see "Uninstalling Network Observability Operator".

> [!NOTE]
> To prevent automatic installation during an upgrade from OpenShift Container Platform 4.22 to 5.0, set `installationPolicy` to `NoAction` in the Network CR before upgrading.

# Network observability automatic installation process

The cluster installation process automatically deploys network observability capabilities when you run the `openshift-install` program with the `NetworkObservabilityInstall` feature gate enabled. You do not need to add network observability configuration to your `install-config.yaml` file unless you want to override the default behavior.

## Installation flow

If the `NetworkObservabilityInstall` feature gate is not enabled, automatic network observability installation does not occur during cluster creation.

When the feature gate is enabled, you can choose one of the following outcomes:

Default (enabled on supported cluster types)
Standard multi-node and hosted control planes clusters enable network observability by default. You do not need to add or change the `networkObservability` section in your `install-config.yaml` file.

With this default configuration:

- The Cluster Network Operator (CNO) automatically installs network observability on standard multi-node clusters and hosted control planes clusters.

- Single-node OpenShift clusters do not install network observability by default due to resource constraints.

Do not install
Add the following configuration to your `install-config.yaml` file to prevent installation on all cluster types:

``` yaml
networking:
  networkObservability:
    installationPolicy: NoAction
```

Always install and enable
Add the following configuration to your `install-config.yaml` file to install network observability on all cluster types, including single-node OpenShift clusters:

``` yaml
networking:
  networkObservability:
    installationPolicy: InstallAndEnable
```

During cluster installation, the following sequence occurs:

1.  You optionally configure the `networking.networkObservability.installationPolicy` field in the `install-config.yaml` file to override the default behavior.

2.  The `openshift-install` program generates the Network CR using the network observability configuration in the `install-config.yaml` file.

3.  The Cluster Network Operator (CNO) reads the `installationPolicy` field in the Network custom resource (CR) if it exists. Based on the `installationPolicy` value and your cluster type, the CNO applies the default, `NoAction`, or `InstallAndEnable` outcome.

4.  If the policy enables installation on your cluster type, the CNO:

    - Installs the Network Observability Operator

    - Creates a default `FlowCollector` configuration that starts collecting network flow data

5.  If the effective policy is `NoAction`, the CNO skips network observability installation.

> [!NOTE]
> The automatic installation process deploys the Network Observability Operator in the `netobserv-operator` namespace and creates the FlowCollector in the `netobserv` namespace, the same namespaces used by standard Operator installation.

## Configuration copying

When you override the default behavior, the `install-config.yaml` file contains the network observability configuration. The following example sets `installationPolicy` to `InstallAndEnable`:

``` yaml
apiVersion: v1
baseDomain: example.com
networking:
  networkObservability:
    installationPolicy: InstallAndEnable
```

The Network custom resource (CR) copies this configuration during cluster creation:

``` yaml
apiVersion: config.openshift.io/v1
kind: Network
metadata:
  name: cluster
spec:
  networkObservability:
    installationPolicy: InstallAndEnable
```

The CNO installs the Network Observability Operator only once during cluster creation or upgrade. After installation, the CNO does not monitor or reinstall the Operator if you remove it.

The CNO supports only two installation policies: `InstallAndEnable` and `NoAction`. The CNO never removes network observability components.

> [!NOTE]
> To prevent automatic installation during an upgrade from OpenShift Container Platform 4.22 to 5.0, set `installationPolicy` to `NoAction` in the Network CR before upgrading.

# Prevent automatic network observability installation

When the `NetworkObservabilityInstall` feature gate is enabled, disable automatic installation of the Network Observability Operator during cluster creation by setting `installationPolicy` to `NoAction` in your `install-config.yaml` file.

> [!NOTE]
> Since automatic network observability installation is a Technology Preview feature in OpenShift Container Platform 5.0, network observability is not installed automatically unless you enable the `NetworkObservabilityInstall` feature gate. If you have not enabled this feature gate, you do not need this procedure.

When the `NetworkObservabilityInstall` feature gate is enabled, OpenShift Container Platform installs the Network Observability Operator automatically on new clusters. You can prevent this behavior by configuring the `install-config.yaml` file before creating the cluster. Disabling network observability prevents the installation of the Network Observability Operator and reduces the cluster’s base resource footprint.

<div>

<div class="title">

Prerequisites

</div>

- You are enabling the `NetworkObservabilityInstall` feature gate for Technology Preview.

- You have access to the `install-config.yaml` file before creating installation manifests.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Edit the `install-config.yaml` file before creating installation manifests.

2.  Add the `networkObservability` field to the `networking` section:

    ``` yaml
    apiVersion: v1
    baseDomain: example.com
    metadata:
      name: my-cluster
    networking:
      networkObservability:
        installationPolicy: NoAction
    # ...
    ```

    where:

    `networking.networkObservability.installationPolicy`
    Controls whether the Network Observability Operator is installed during cluster creation. Set to `NoAction` to prevent installation on all cluster types. Set to `InstallAndEnable` to force installation. Omit this field to use the default behavior: automatic installation on multi-node and Hosted Control Plane clusters, but not on single-node OpenShift clusters. Valid values are `InstallAndEnable`, `NoAction`, or omitted (empty string default).

3.  Configure the `FeatureGate` manifest in your installation directory to include the `NetworkObservabilityInstall` feature gate under the designated feature set.

4.  Complete the cluster installation using your platform’s standard deployment method.

</div>

<div>

<div class="title">

Verification

</div>

1.  Verify that the Network Observability Operator is not installed by running the following command:

    ``` terminal
    $ oc get pods -n netobserv-operator
    ```

    The output should indicate that the namespace does not exist:

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` terminal
    Error from server (NotFound): namespaces "netobserv-operator" not found
    ```

    </div>

</div>

# Verify automatic network observability installation

Verify that the Network Observability Operator and `FlowCollector` are running after automatic installation during cluster creation.

<div>

<div class="title">

Prerequisites

</div>

- You created the cluster with the `NetworkObservabilityInstall` feature gate enabled.

- You have access to the cluster as a user with the `cluster-admin` role.

- The OpenShift CLI (`oc`) is installed.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Verify that the Network Observability Operator is installed and running by running the following command:

    ``` terminal
    $ oc get pods -n netobserv-operator
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` terminal
    NAME                                                READY   STATUS    RESTARTS   AGE
    netobserv-controller-manager-6d4b8d9f8c-xk7lm      2/2     Running   0          5m
    ```

    </div>

2.  Verify that the cluster has a `FlowCollector` resource by running the following command:

    ``` terminal
    $ oc get flowcollector cluster
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` terminal
    NAME      AGENT   SAMPLING   DEPLOYMENT MODEL   STATUS
    cluster   eBPF    400        Service            Ready
    ```

    </div>

3.  Verify that network traffic data is available in the web console by navigating to **Observe** → **Network Traffic**.

</div>

# Network observability and cluster upgrades

Understand how upgrading from OpenShift Container Platform 4.22 to 5.0 affects automatic network observability installation when the `NetworkObservabilityInstall` feature gate is enabled.

When you upgrade an existing cluster from OpenShift Container Platform 4.22 to 5.0 with the `NetworkObservabilityInstall` feature gate enabled, the CNO evaluates the `installationPolicy` field in the Network custom resource (CR) to determine whether to install network observability.

If the `NetworkObservabilityInstall` feature gate is not enabled, automatic network observability installation does not occur during the upgrade.

## Default upgrade behavior

When the feature gate is enabled and you upgrade from OpenShift Container Platform 4.22 to 5.0, the following behaviors apply by default:

- If the Network CR does not have the `networkObservability.installationPolicy` field configured, the CNO automatically installs network observability on multi-node and Hosted Control Plane clusters.

- Single-node OpenShift clusters do not automatically install network observability due to resource constraints.

- If network observability is already installed by using the standard Operator installation method, no changes occur. The automatic installation process detects the existing installation and takes no action.

To prevent automatic installation during the upgrade, see "Prevent automatic network observability installation during upgrades".

## Prevent automatic network observability installation during upgrades

You can configure the Network custom resource (CR) to prevent the Cluster Network Operator (CNO) from automatically installing network observability during a cluster upgrade.

> [!NOTE]
> Since automatic network observability installation is a Technology Preview feature in OpenShift Container Platform 5.0, network observability is not installed automatically during upgrades unless you enable the `NetworkObservabilityInstall` feature gate. If the feature gate is disabled, network observability is not installed, and this procedure is not needed.

<div>

<div class="title">

Prerequisites

</div>

- You have access to the cluster as a user with the `cluster-admin` role.

- The OpenShift CLI (`oc`) is installed.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Before upgrading your cluster, configure the Network CR to prevent automatic network observability installation. Choose one of the following methods:

    - Use `oc patch` by running the following command:

      ``` terminal
      $ oc patch network.config.openshift.io cluster --type=merge -p '
      spec:
        networkObservability:
          installationPolicy: NoAction
      '
      ```

    - Alternatively, edit the Network CR manually by running the following command:

      ``` terminal
      $ oc edit network.config.openshift.io cluster
      ```

      Add the `NoAction` installation policy to the `spec` section:

      ``` yaml
      apiVersion: config.openshift.io/v1
      kind: Network
      metadata:
        name: cluster
      spec:
        networkObservability:
          installationPolicy: NoAction
      # ...
      ```

      Save and close the file to apply the changes.

2.  Proceed with the cluster upgrade. The CNO skips the network observability installation during and after the upgrade process.

</div>

# Additional resources

- [Installing the Network Observability Operator](../network_observability/installing-operators.xml#installing-network-observability-operators)

- [Configuring the FlowCollector custom resource](../network_observability/configuring-operator.xml#network-observability-flowcollector-view_network_observability)

- [Cluster Network Operator](../../networking/networking_operators/cluster-network-operator.xml#cluster-network-operator)

- [Uninstalling Network Observability Operator](../network_observability/installing-operators.xml#network-observability-operator-uninstall_network_observability)
