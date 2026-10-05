You can monitor the fencing health of your two-node OpenShift Container Platform cluster to prevent failures that could impact your workloads. The cluster provides metrics and alerts that tell you when critical issues occur, such as nodes going offline or fence devices becoming unreachable.

A two-node OpenShift Container Platform cluster with fencing (TNF) uses Pacemaker to manage cluster membership, fencing, and the `etcd` resource. The cluster exposes this Pacemaker state as Prometheus metrics and ships a set of alerts that fire on TNF-specific failure conditions.

# Overview of monitoring in a two-node OpenShift cluster with fencing

You can monitor the fencing layer of your two-node OpenShift Container Platform cluster by using the same observability tools you use for the rest of the cluster.

Integrated Prometheus metrics and alerts for Pacemaker help you detect node failures, fence device issues, and resource problems before they compromise high availability.

TNF monitoring reflects the state of the Pacemaker cluster:

- Pacemaker cluster membership and expected node count: This is not the `etcd` raft membership, which fluctuates by design during fencing and recovery.

- Node availability, maintenance, and standby state: This is distinct from the state of OpenShift Container Platform nodes.

- Fence device health for each node.

- The state of Pacemaker-managed resources, such as `etcd`, as reported by the resource agent.

Every TNF metric name is prefixed with `tnf_` and is grouped by level: `tnf_cluster_*`, `tnf_node_*`, and `tnf_resource_*`. Each metric is a gauge that mirrors a Pacemaker condition, where `1` means the condition is true (the healthy state) and `0` means the condition is not true.

TNF alerts are delivered as part of the cluster Etcd Operator alerting rules, in a `tnf-pacemaker.rules` group that is separate from the standard `etcd` alerts. The alerts fire only on TNF. Each alert targets a specific leaf condition, such as a node being offline or a fence device being unavailable, so that the firing alert names the actionable problem rather than a generic cluster unhealthy rollup.

You do not need to configure anything to enable TNF metrics and alerts. They are active automatically on a cluster that uses the TNF topology.

# Two-node OpenShift cluster with fencing metrics reference

You can build queries and dashboards to monitor health of your two-node OpenShift Container Platform cluster with fencing (TNF) by using Prometheus metrics. These gauge metrics track cluster health, node status, and Pacemaker resource state to help you identify and respond to availability issues.

The cluster-level metrics describe the cluster as a whole and have no labels.

| Metric                               | Description                                                                              |
|--------------------------------------|------------------------------------------------------------------------------------------|
| `tnf_cluster_healthy`                | Overall cluster health. `1` when the cluster is healthy.                                 |
| `tnf_cluster_in_service`             | Whether the cluster is in service. `0` indicates the cluster is in maintenance mode.     |
| `tnf_cluster_node_count_as_expected` | Whether the cluster has the expected node count. `1` when exactly two nodes are present. |

Cluster-level TNF metrics

The node-level metrics describe an individual node and carry a `node` label set to the node name:

| Metric                       | Description                                                                                         |
|------------------------------|-----------------------------------------------------------------------------------------------------|
| `tnf_node_healthy`           | Overall node health. `1` when the node is healthy.                                                  |
| `tnf_node_online`            | Whether the node is online. `0` indicates the node is offline.                                      |
| `tnf_node_in_service`        | Whether the node is in service. `0` indicates the node is in maintenance mode.                      |
| `tnf_node_active`            | Whether the node is active. `0` indicates the node is in standby mode.                              |
| `tnf_node_ready`             | Whether the node is ready. `0` indicates the node is pending.                                       |
| `tnf_node_clean`             | Whether the node is in a clean state. `0` indicates Pacemaker cannot confirm the node state.        |
| `tnf_node_member`            | Whether the node is a cluster member.                                                               |
| `tnf_node_fencing_available` | Whether at least one fence device for the node is healthy. `0` indicates the node cannot be fenced. |
| `tnf_node_fencing_healthy`   | Whether all fence devices for the node are healthy. `0` indicates reduced fencing redundancy.       |

Node-level TNF metrics

The resource-level metrics describe a Pacemaker-managed resource, such as `etcd`, on a specific node. They carry a `node` label and a `resource` label.

| Metric                     | Description                                                                                      |
|----------------------------|--------------------------------------------------------------------------------------------------|
| `tnf_resource_healthy`     | Overall resource health. `1` when the resource is healthy.                                       |
| `tnf_resource_in_service`  | Whether the resource is in service. `0` indicates maintenance mode.                              |
| `tnf_resource_managed`     | Whether the resource is managed by Pacemaker. `0` indicates the resource was manually unmanaged. |
| `tnf_resource_enabled`     | Whether the resource is enabled. `0` indicates the resource was manually disabled.               |
| `tnf_resource_operational` | Whether the resource is operational. `0` indicates the resource has failed and cannot start.     |
| `tnf_resource_active`      | Whether the resource is active.                                                                  |
| `tnf_resource_started`     | Whether the resource is started. `0` indicates the resource is stopped.                          |
| `tnf_resource_schedulable` | Whether the resource can be scheduled.                                                           |

Resource-level TNF metrics

# Two-node OpenShift cluster with fencing alerts reference

A two-node OpenShift Container Platform cluster with fencing (TNF) ships several alerts in the `tnf-pacemaker.rules` group.

`critical` alerts
Indicate a condition that breaks cluster functionality and requires immediate action.

`warning` alerts
Indicate a degraded state that needs attention while the cluster remains functional.

Each alert includes a `runbook_url` annotation that links to detailed investigation and remediation steps.

The cluster-level alerts describe the cluster as a whole and have no labels.

| Alert                     | Severity   | Fires when                                                                                                                                 | Runbook                                                                                                              |
|---------------------------|------------|--------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------|
| `TNFNodeCountMismatch`    | `critical` | The cluster does not have exactly two nodes, for example after a node is added or removed. Restore the cluster to two control plane nodes. | [Runbook](https://github.com/openshift/runbooks/blob/master/alerts/cluster-etcd-operator/TNFNodeCountMismatch.md)    |
| `TNFClusterInMaintenance` | `warning`  | The cluster is in maintenance mode. Expected during planned maintenance; investigate if unexpected.                                        | [Runbook](https://github.com/openshift/runbooks/blob/master/alerts/cluster-etcd-operator/TNFClusterInMaintenance.md) |

Cluster-level TNF alerts

The node-level alerts carry a `node` label that identifies the affected node.

| Alert                       | Severity   | Fires when                                                                                                                                                                                                    | Runbook                                                                                                                |
|-----------------------------|------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------|
| `TNFNodeOffline`            | `critical` | The node is offline because of a node failure, reboot, or network partition. The cluster has lost high-availability redundancy until the node recovers.                                                       | [Runbook](https://github.com/openshift/runbooks/blob/master/alerts/cluster-etcd-operator/TNFNodeOffline.md)            |
| `TNFNodeFencingUnavailable` | `critical` | All fence devices for the node are unhealthy, so the node cannot be fenced. Common causes are an unreachable BMC or invalid credentials. Restore fencing before relying on the cluster for high availability. | [Runbook](https://github.com/openshift/runbooks/blob/master/alerts/cluster-etcd-operator/TNFNodeFencingUnavailable.md) |
| `TNFNodeFencingDegraded`    | `warning`  | Fence device redundancy is lost, but at least one device remains healthy. The node can still be fenced. Repair the failed device.                                                                             | [Runbook](https://github.com/openshift/runbooks/blob/master/alerts/cluster-etcd-operator/TNFNodeFencingDegraded.md)    |
| `TNFNodeUnclean`            | `critical` | Pacemaker cannot confirm the node state, for example after a fencing, communication, or configuration problem.                                                                                                | [Runbook](https://github.com/openshift/runbooks/blob/master/alerts/cluster-etcd-operator/TNFNodeUnclean.md)            |
| `TNFNodeInMaintenance`      | `warning`  | The node is in maintenance mode. Expected during planned maintenance; investigate if unexpected.                                                                                                              | [Runbook](https://github.com/openshift/runbooks/blob/master/alerts/cluster-etcd-operator/TNFNodeInMaintenance.md)      |
| `TNFNodeStandby`            | `warning`  | The node is in standby mode and is not running resources. Expected during planned maintenance; investigate if unexpected.                                                                                     | [Runbook](https://github.com/openshift/runbooks/blob/master/alerts/cluster-etcd-operator/TNFNodeStandby.md)            |

Node-level TNF alerts

The resource-level alerts carry a `node` label and a `resource` label, for example `resource="etcd"`.

| Alert                  | Severity   | Fires when                                                                                                                             | Runbook                                                                                                           |
|------------------------|------------|----------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------|
| `TNFResourceStopped`   | `critical` | A Pacemaker-managed resource, such as `etcd`, is stopped. This can follow a quorum loss or a manual stop.                              | [Runbook](https://github.com/openshift/runbooks/blob/master/alerts/cluster-etcd-operator/TNFResourceStopped.md)   |
| `TNFResourceFailed`    | `critical` | A resource has failed and cannot start, for example because of a resource agent failure or a configuration error.                      | [Runbook](https://github.com/openshift/runbooks/blob/master/alerts/cluster-etcd-operator/TNFResourceFailed.md)    |
| `TNFResourceUnmanaged` | `warning`  | A resource is not managed by Pacemaker, typically after a manual unmanage operation. Pacemaker does not recover an unmanaged resource. | [Runbook](https://github.com/openshift/runbooks/blob/master/alerts/cluster-etcd-operator/TNFResourceUnmanaged.md) |
| `TNFResourceDisabled`  | `warning`  | A resource is disabled, typically after a manual disable operation.                                                                    | [Runbook](https://github.com/openshift/runbooks/blob/master/alerts/cluster-etcd-operator/TNFResourceDisabled.md)  |

Resource-level TNF alerts

# Additional resources

- [Operating a degraded two-node OpenShift cluster with fencing](../installing_tnf/operating-a-degraded-tnf.xml#operating-a-degraded-tnf)

- [Post-installation troubleshooting and recovery](../installing_tnf/install-post-tnf.xml#installing-post-tnf)

- [Accessing metrics as an administrator](https://docs.redhat.com/en/documentation/monitoring_stack_for_red_hat_openshift/latest/html/accessing_metrics/accessing-metrics-as-an-administrator)

- [Managing alerts as an administrator](https://docs.redhat.com/en/documentation/monitoring_stack_for_red_hat_openshift/latest/html/managing_alerts/managing-alerts-as-an-administrator)
