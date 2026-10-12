After deploying virtualized control plane clusters, you must manage the hosting cluster to maintain the availability and performance of the target clusters it supports.

# Overview of hosting cluster management

A hosting cluster that runs virtualized control plane VMs requires ongoing management to maintain the availability and performance of all target clusters it supports.

Hosting cluster management includes the following tasks:

- Updating the hosting cluster and OpenShift Virtualization without disrupting the target clusters.

- Performing node maintenance on hosting cluster nodes while preserving `etcd` quorum in target clusters.

Because multiple target clusters can share the same hosting cluster, a misconfigured update or unplanned maintenance event on the hosting cluster can affect multiple target clusters simultaneously. Plan and execute all hosting cluster operations with awareness of which target cluster VMs run on which physical nodes.

# Update a hosting cluster for virtualized control planes

Update the hosting cluster and OpenShift Virtualization while maintaining the availability of the target clusters.

During a hosting cluster update, the Machine Config Operator drains and reboots nodes one at a time. If pod disruption budgets and anti-affinity rules are configured correctly, the update proceeds without losing `etcd` quorum in any target cluster.

- Control plane VMs are distributed across hosting cluster nodes by using anti-affinity rules.

- A `PodDisruptionBudget` with `minAvailable: 2` is configured for each target cluster’s control plane VMs.

- The VM eviction strategy is set to `None` for all control plane VMs.

1.  Verify that all target cluster control plane VMs are healthy before starting the update by running the following command:

    ``` terminal
    $ oc get vm -A -l <vm_selector_label>=<value>
    ```

    Replace `<vm_selector_label>=<value>` with the label you configured in your KubeVirt Redfish `vm_selector`, for example `redfish-enabled=true`.

    All control plane VMs must show a `Running` status.

2.  Verify `etcd` health on each target cluster by running the following command:

    ``` terminal
    $ oc --kubeconfig=<target_cluster_kubeconfig> get etcd -o=jsonpath='{range .items[0].status.conditions[?(@.type=="EtcdMembersAvailable")]}{end}'
    ```

    - `target_cluster_kubeconfig` is the path to the target cluster’s kubeconfig file.

3.  Start the hosting cluster update by following the standard OpenShift Container Platform update process.

    The Machine Config Operator drains and reboots each node in sequence. The `PodDisruptionBudget` CR prevents more than one control plane VM for each target cluster from being evicted at a time.

4.  Monitor the update progress by running the following commands:

    ``` terminal
    $ oc get clusterversion
    $ oc get nodes
    ```

5.  After the hosting cluster update completes, update OpenShift Virtualization if a new version is available.

6.  Verify that all control plane VMs are running after the update by running the following command:

    ``` terminal
    $ oc get vm -A -l <vm_selector_label>=<value>
    ```

    Replace `<vm_selector_label>=<value>` with the label you configured in your KubeVirt Redfish `vm_selector`, for example `redfish-enabled=true`.

    All control plane VMs must show a `Running` status.

<!-- -->

1.  Verify `etcd` health on each target cluster after the update by running the following command:

    ``` terminal
    $ oc --kubeconfig=<target_cluster_kubeconfig> get etcd -o=jsonpath='{range .items[0].status.conditions[?(@.type=="EtcdMembersAvailable")]}{end}'
    ```

    - `target_cluster_kubeconfig` is the path to the target cluster’s kubeconfig file.

2.  Verify that the target cluster API is responsive by running the following command:

    ``` terminal
    $ oc --kubeconfig=<target_cluster_kubeconfig> get nodes
    ```

    - `target_cluster_kubeconfig` is the path to the target cluster’s kubeconfig file.

# Performing node maintenance on a hosting cluster

Perform maintenance on a hosting cluster node, such as applying operating system updates or hardware repairs, without disrupting the target clusters.

When you drain a hosting cluster node, the control plane VM on that node shuts down. If pod disruption budgets and anti-affinity rules are configured correctly, only one control plane VM for each target cluster is affected, and `etcd` quorum is preserved.

- Control plane VMs are distributed across hosting cluster nodes by using anti-affinity rules.

- A `PodDisruptionBudget` with `minAvailable: 2` is configured for each target cluster’s control plane VMs.

- The VM eviction strategy is set to `None` for all control plane VMs.

1.  Identify which control plane VMs are running on the node you plan to maintain by running the following command:

    ``` terminal
    $ oc get pods --field-selector spec.nodeName=<node_name> -n <vm_namespace> -l vcp-cluster=<cluster_name>
    ```

    - `<node_name>` is the name of the node you plan to maintain.

    - `<vm_namespace>` is the namespace of the control plane VMs.

    - `<cluster_name>` is the name of the target cluster.

      <div class="note">

      Use `oc get pods` with the `spec.nodeName` field selector to filter by node. The `oc get vmi` command does not support the `status.nodeName` field selector.

      </div>

2.  Verify that all target clusters affected by this node have healthy `etcd` quorum before proceeding by running the following command:

    ``` terminal
    $ oc --kubeconfig=<target_cluster_kubeconfig> get etcd -o=jsonpath='{range .items[0].status.conditions[?(@.type=="EtcdMembersAvailable")]}{end}'
    ```

    - `target_cluster_kubeconfig` is the path to the target cluster’s kubeconfig file.

3.  Cordon the node to prevent new workloads from being scheduled by running the following command:

    ``` terminal
    $ oc adm cordon <node_name>
    ```

    - `<node_name>` is the name of the node you plan to maintain.

4.  Drain the node to evict all pods, including control plane VM pods, by running the following command:

    ``` terminal
    $ oc adm drain <node_name> --ignore-daemonsets --delete-emptydir-data
    ```

    - `<node_name>` is the name of the node you plan to maintain.

      The `PodDisruptionBudget` ensures that only one control plane VM per target cluster is evicted. The drain operation blocks until the PDB allows eviction.

5.  Verify that the remaining control plane VMs maintain `etcd` quorum on each affected target cluster by running the following command:

    ``` terminal
    $ oc --kubeconfig=<target_cluster_kubeconfig> get etcd -o=jsonpath='{range .items[0].status.conditions[?(@.type=="EtcdMembersAvailable")]}{end}'
    ```

    - `target_cluster_kubeconfig` is the path to the target cluster’s kubeconfig file.

6.  Perform the required maintenance on the physical node.

7.  Uncordon the node to allow workloads to be scheduled again by running the following command:

    ``` terminal
    $ oc adm uncordon <node_name>
    ```

    - `<node_name>` is the name of the node you plan to maintain.

8.  Verify that the control plane VM restarts on the node and rejoins the target cluster by running the following command:

    ``` terminal
    $ oc get vmi -A -l <vm_selector_label>=<value>
    ```

    Replace `<vm_selector_label>=<value>` with the label you configured in your KubeVirt Redfish `vm_selector`, for example `redfish-enabled=true`.

    All control plane VMs must show a `Running` phase.

    <div class="note">

    Use `oc get vmi` (VirtualMachineInstance) instead of `oc get vm` (VirtualMachine) to verify the actual runtime state. The `VirtualMachine` resource reflects the desired state, while the `VirtualMachineInstance` resource reflects whether the VM is currently running.

    </div>

- Verify `etcd` health on each affected target cluster by running the following command:

  ``` terminal
  $ oc --kubeconfig=<target_cluster_kubeconfig> get etcd -o=jsonpath='{range .items[0].status.conditions[?(@.type=="EtcdMembersAvailable")]}{end}'
  ```

  - `target_cluster_kubeconfig` is the path to the target cluster’s kubeconfig file.

# Additional resources

- [High availability for virtualized control planes](vcp-overview.xml#con_virt-vcp-high-availability_vcp-overview)

- [Understanding how to evacuate pods on nodes](../nodes/nodes/nodes-nodes-working.xml#nodes-nodes-working-evacuating_nodes-nodes-working)

- [Effects of disk latency on etcd](../etcd/etcd-performance.xml#etcd-disk-latency_etcd-performance)
