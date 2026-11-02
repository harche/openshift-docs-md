Use OVN-Kubernetes metrics in OpenShift Container Platform to monitor user-defined networks. Track how long NAD sync, node annotation updates, and northbound database (NBDB) programming take during network setup.

# Enabling metrics for user-defined networks

User-defined network (UDN) scale metrics are not enabled by default. Enable OVN-Kubernetes scale metrics so you can collect those metrics from the OVN-Kubernetes metrics endpoints.

> [!IMPORTANT]
> UDN scale metrics are available only when you set `enable-scale-metrics` to `true`, because collecting those metrics can have a significant performance impact. Setting `enable-scale-metrics` to `true` also enables other non-UDN scale metrics that use the same flag.

To enable the metrics, set `enable-scale-metrics` to `true` in the `[metrics]` section of the OVN-Kubernetes configuration. On OpenShift Container Platform, that configuration is stored in the `ovnkube-config` config map in the `openshift-ovn-kubernetes` namespace.

| Parameter | Default | Description |
|----|----|----|
| `enable-scale-metrics` | `false` | When `true`, OVN-Kubernetes registers scale-related metrics, including the UDN NAD sync, node annotation update, and NBDB programming duration metrics, as well as other non-UDN scale metrics. When `false`, those metrics are unavailable. |

OVN-Kubernetes scale metrics configuration

<div class="formalpara">

<div class="title">

Example command to edit the `ovnkube-config` config map

</div>

``` terminal
$ oc edit configmap ovnkube-config -n openshift-ovn-kubernetes
```

</div>

<div class="formalpara">

<div class="title">

Example `[metrics]` section in `ovnkube.conf`

</div>

``` ini
[metrics]
enable-scale-metrics=true
```

</div>

# Metrics for user-defined networks

You can use OVN-Kubernetes metrics to monitor `NetworkAttachmentDefinition` (NAD) sync, node annotation updates, and northbound database (NBDB) programming for a user-defined network (UDN). These metrics help you identify bottlenecks when you create or scale user-defined networks.

The following metrics are available from the `ovnkube-cluster-manager` and `ovnkube-controller` metrics endpoints when scale metrics are enabled.

| Name | Description | Explanation |
|----|----|----|
| `ovnkube_clustermanager_udn_nad_sync_duration_seconds` | `name`: specifies the UDN or cluster user-defined network (CUDN) name | The time spent syncing `NetworkAttachmentDefinition` objects during UDN reconciliation. |
| `ovnkube_clustermanager_udn_update_node_annotation_duration_seconds` | `name`: specifies the UDN or CUDN name | The time spent updating node annotations during UDN network allocation. |
| `ovnkube_controller_udn_nbdb_programmed_duration_seconds` | `topology`: specifies the UDN topology, such as `layer2` or `layer3` | The time the OVN-Kubernetes controller takes to program logical objects for a UDN in the OVN northbound database (NBDB) when initializing the network on a node. Values are aggregated by topology. |
