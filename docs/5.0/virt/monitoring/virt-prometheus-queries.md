Monitor the consumption of cluster infrastructure resources by using the metrics provided by OpenShift Virtualization. These metrics are also used to query live migration status.

<div class="note">

- To use the vCPU metric, apply the `schedstats=enable` kernel argument to the `MachineConfig` object. This kernel argument enables scheduler statistics used for debugging and performance tuning and adds a minor additional load to the scheduler.

- For guest memory swapping queries to return data, enable memory swapping on the virtual guests.

</div>

# Querying metrics for all projects with the OpenShift Container Platform web console

Monitor the state of a cluster and any user-defined workloads by using the OpenShift Container Platform metrics query browser. The query browser uses Prometheus Query Language (PromQL) queries to examine metrics visualized on a plot.

As a cluster administrator or as a user with view permissions for all projects, you can access metrics for all default OpenShift Container Platform and user-defined projects in the Metrics UI.

- You have access to the cluster as a user with the `cluster-admin` cluster role or with view permissions for all projects.

- You have installed the OpenShift CLI (`oc`).

1.  In the OpenShift Container Platform web console, click **Observe** → **Metrics**.

2.  To add one or more queries, perform any of the following actions:

    <table>
    <colgroup>
    <col style="width: 50%" />
    <col style="width: 50%" />
    </colgroup>
    <thead>
    <tr class="header">
    <th style="text-align: left;">Option</th>
    <th style="text-align: left;">Description</th>
    </tr>
    </thead>
    <tbody>
    <tr class="odd">
    <td style="text-align: left;"><p>Select an existing query.</p></td>
    <td style="text-align: left;"><p>From the <strong>Select query</strong> drop-down list, select an existing query.</p></td>
    </tr>
    <tr class="even">
    <td style="text-align: left;"><p>Create a custom query.</p></td>
    <td style="text-align: left;"><p>Add your Prometheus Query Language (PromQL) query to the <strong>Expression</strong> field.</p>
    <p>As you type a PromQL expression, autocomplete suggestions appear in a drop-down list. These suggestions include functions, metrics, labels, and time tokens. Use the keyboard arrows to select one of these suggested items and then press Enter to add the item to your expression. Move your mouse pointer over a suggested item to view a brief description of that item.</p></td>
    </tr>
    <tr class="odd">
    <td style="text-align: left;"><p>Add multiple queries.</p></td>
    <td style="text-align: left;"><p>Click <strong>Add query</strong>.</p></td>
    </tr>
    <tr class="even">
    <td style="text-align: left;"><p>Duplicate an existing query.</p></td>
    <td style="text-align: left;"><p>Click the options menu <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABsAAAAjCAIAAADqn+bCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAA+0lEQVRIie2WMQqEMBBFJ47gUXRBLyBYqbUXULCx9CR2XsAb6AlUEM9kpckW7obdZhwWYWHXX/3i8TPJZEKEUgpOlXFu3JX4V4kmB2qaZhgGKSUiZlkWxzEBC84N9zxv27bdO47Tti0Bs3at4wBgXVca/lJnfN/XPggCGmadIwAsywIAiGhZFk1ydy2EYJKgGCqK4vZUVVU0zKpxnmftp2mi4S/1GhG1N82DMWNNYVmW4zgqpRAxTVMa5t4evlg11nXd9/1eY57nSZIQMKtG13WllLu3bbvrOgJmdUbHwfur8Xniqw6Hh5UYRdGDNowwDA+WvP4UV+JPJ94B1gKUWcTOCT0AAAAASUVORK5CYII=" alt="kebab" /> next to the query, then choose <strong>Duplicate query</strong>.</p></td>
    </tr>
    <tr class="odd">
    <td style="text-align: left;"><p>Disable a query from being run.</p></td>
    <td style="text-align: left;"><p>Click the options menu <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABsAAAAjCAIAAADqn+bCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAA+0lEQVRIie2WMQqEMBBFJ47gUXRBLyBYqbUXULCx9CR2XsAb6AlUEM9kpckW7obdZhwWYWHXX/3i8TPJZEKEUgpOlXFu3JX4V4kmB2qaZhgGKSUiZlkWxzEBC84N9zxv27bdO47Tti0Bs3at4wBgXVca/lJnfN/XPggCGmadIwAsywIAiGhZFk1ydy2EYJKgGCqK4vZUVVU0zKpxnmftp2mi4S/1GhG1N82DMWNNYVmW4zgqpRAxTVMa5t4evlg11nXd9/1eY57nSZIQMKtG13WllLu3bbvrOgJmdUbHwfur8Xniqw6Hh5UYRdGDNowwDA+WvP4UV+JPJ94B1gKUWcTOCT0AAAAASUVORK5CYII=" alt="kebab" /> next to the query and choose <strong>Disable query</strong>.</p></td>
    </tr>
    </tbody>
    </table>

3.  To run queries that you created, click **Run queries**. The metrics from the queries are visualized on the plot. If a query is invalid, the UI shows an error message.

    <div class="note">

    - When drawing time series graphs, queries that operate on large amounts of data might time out or overload the browser. To avoid this, click **Hide graph** and calibrate your query by using only the metrics table. Then, after finding a feasible query, enable the plot to draw the graphs.

    - By default, the query table shows an expanded view that lists every metric and its current value. Click the **˅** down arrowhead to minimize the expanded view for a query.

    </div>

4.  Optional: Save the page URL to use this set of queries again in the future.

5.  Explore the visualized metrics. Initially, all metrics from all enabled queries are shown on the plot. Select which metrics are shown by performing any of the following actions:

    <table>
    <colgroup>
    <col style="width: 50%" />
    <col style="width: 50%" />
    </colgroup>
    <thead>
    <tr class="header">
    <th style="text-align: left;">Option</th>
    <th style="text-align: left;">Description</th>
    </tr>
    </thead>
    <tbody>
    <tr class="odd">
    <td style="text-align: left;"><p>Hide all metrics from a query.</p></td>
    <td style="text-align: left;"><p>Click the options menu <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABsAAAAjCAIAAADqn+bCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAA+0lEQVRIie2WMQqEMBBFJ47gUXRBLyBYqbUXULCx9CR2XsAb6AlUEM9kpckW7obdZhwWYWHXX/3i8TPJZEKEUgpOlXFu3JX4V4kmB2qaZhgGKSUiZlkWxzEBC84N9zxv27bdO47Tti0Bs3at4wBgXVca/lJnfN/XPggCGmadIwAsywIAiGhZFk1ydy2EYJKgGCqK4vZUVVU0zKpxnmftp2mi4S/1GhG1N82DMWNNYVmW4zgqpRAxTVMa5t4evlg11nXd9/1eY57nSZIQMKtG13WllLu3bbvrOgJmdUbHwfur8Xniqw6Hh5UYRdGDNowwDA+WvP4UV+JPJ94B1gKUWcTOCT0AAAAASUVORK5CYII=" alt="kebab" /> for the query and click <strong>Hide all series</strong>.</p></td>
    </tr>
    <tr class="even">
    <td style="text-align: left;"><p>Hide a specific metric.</p></td>
    <td style="text-align: left;"><p>Go to the query table and click the colored square near the metric name.</p></td>
    </tr>
    <tr class="odd">
    <td style="text-align: left;"><p>Zoom into the plot and change the time range.</p></td>
    <td style="text-align: left;"><p>Perform one of the following actions:</p>
    <ul>
    <li><p>Visually select the time range by clicking and dragging on the plot horizontally.</p></li>
    <li><p>Use the menu to select the time range.</p></li>
    </ul></td>
    </tr>
    <tr class="even">
    <td style="text-align: left;"><p>Reset the time range.</p></td>
    <td style="text-align: left;"><p>Click <strong>Reset zoom</strong>.</p></td>
    </tr>
    <tr class="odd">
    <td style="text-align: left;"><p>Display outputs for all queries at a specific point in time.</p></td>
    <td style="text-align: left;"><p>Hover over the plot at the point you are interested in. The query outputs appear in a pop-up box.</p></td>
    </tr>
    <tr class="even">
    <td style="text-align: left;"><p>Hide the plot.</p></td>
    <td style="text-align: left;"><p>Click <strong>Hide graph</strong>.</p></td>
    </tr>
    </tbody>
    </table>

# Querying metrics for user-defined projects with the OpenShift Container Platform web console

Monitor user-defined workloads by using the OpenShift Container Platform metrics query browser. The query browser uses Prometheus Query Language (PromQL) queries to examine metrics visualized on a plot.

To query metrics in the **Developer** perspective, you must specify a project name that represents the namespace. You must have the required privileges to view metrics for the selected project.

- You have access to the cluster as a developer or as a user with view permissions for the project that you are viewing metrics for.

- You have enabled monitoring for user-defined projects.

- You have deployed a service in a user-defined project.

- You have created a `ServiceMonitor` custom resource definition (CRD) for the service to define how the service is monitored.

1.  In the OpenShift Container Platform web console, click **Observe** → **Metrics**.

2.  To add one or more queries, perform any of the following actions:

    <table>
    <colgroup>
    <col style="width: 50%" />
    <col style="width: 50%" />
    </colgroup>
    <thead>
    <tr class="header">
    <th style="text-align: left;">Option</th>
    <th style="text-align: left;">Description</th>
    </tr>
    </thead>
    <tbody>
    <tr class="odd">
    <td style="text-align: left;"><p>Select an existing query.</p></td>
    <td style="text-align: left;"><p>From the <strong>Select query</strong> drop-down list, select an existing query.</p></td>
    </tr>
    <tr class="even">
    <td style="text-align: left;"><p>Create a custom query.</p></td>
    <td style="text-align: left;"><p>Add your Prometheus Query Language (PromQL) query to the <strong>Expression</strong> field.</p>
    <p>As you type a PromQL expression, autocomplete suggestions appear in a drop-down list. These suggestions include functions, metrics, labels, and time tokens. Use the keyboard arrows to select one of these suggested items and then press Enter to add the item to your expression. Move your mouse pointer over a suggested item to view a brief description of that item.</p></td>
    </tr>
    <tr class="odd">
    <td style="text-align: left;"><p>Add multiple queries.</p></td>
    <td style="text-align: left;"><p>Click <strong>Add query</strong>.</p></td>
    </tr>
    <tr class="even">
    <td style="text-align: left;"><p>Duplicate an existing query.</p></td>
    <td style="text-align: left;"><p>Click the options menu <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABsAAAAjCAIAAADqn+bCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAA+0lEQVRIie2WMQqEMBBFJ47gUXRBLyBYqbUXULCx9CR2XsAb6AlUEM9kpckW7obdZhwWYWHXX/3i8TPJZEKEUgpOlXFu3JX4V4kmB2qaZhgGKSUiZlkWxzEBC84N9zxv27bdO47Tti0Bs3at4wBgXVca/lJnfN/XPggCGmadIwAsywIAiGhZFk1ydy2EYJKgGCqK4vZUVVU0zKpxnmftp2mi4S/1GhG1N82DMWNNYVmW4zgqpRAxTVMa5t4evlg11nXd9/1eY57nSZIQMKtG13WllLu3bbvrOgJmdUbHwfur8Xniqw6Hh5UYRdGDNowwDA+WvP4UV+JPJ94B1gKUWcTOCT0AAAAASUVORK5CYII=" alt="kebab" /> next to the query, then choose <strong>Duplicate query</strong>.</p></td>
    </tr>
    <tr class="odd">
    <td style="text-align: left;"><p>Disable a query from being run.</p></td>
    <td style="text-align: left;"><p>Click the options menu <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABsAAAAjCAIAAADqn+bCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAA+0lEQVRIie2WMQqEMBBFJ47gUXRBLyBYqbUXULCx9CR2XsAb6AlUEM9kpckW7obdZhwWYWHXX/3i8TPJZEKEUgpOlXFu3JX4V4kmB2qaZhgGKSUiZlkWxzEBC84N9zxv27bdO47Tti0Bs3at4wBgXVca/lJnfN/XPggCGmadIwAsywIAiGhZFk1ydy2EYJKgGCqK4vZUVVU0zKpxnmftp2mi4S/1GhG1N82DMWNNYVmW4zgqpRAxTVMa5t4evlg11nXd9/1eY57nSZIQMKtG13WllLu3bbvrOgJmdUbHwfur8Xniqw6Hh5UYRdGDNowwDA+WvP4UV+JPJ94B1gKUWcTOCT0AAAAASUVORK5CYII=" alt="kebab" /> next to the query and choose <strong>Disable query</strong>.</p></td>
    </tr>
    </tbody>
    </table>

3.  To run queries that you created, click **Run queries**. The metrics from the queries are visualized on the plot. If a query is invalid, the UI shows an error message.

    <div class="note">

    - When drawing time series graphs, queries that operate on large amounts of data might time out or overload the browser. To avoid this, click **Hide graph** and calibrate your query by using only the metrics table. Then, after finding a feasible query, enable the plot to draw the graphs.

    - By default, the query table shows an expanded view that lists every metric and its current value. Click the **˅** down arrowhead to minimize the expanded view for a query.

    </div>

4.  Optional: Save the page URL to use this set of queries again in the future.

5.  Explore the visualized metrics. Initially, all metrics from all enabled queries are shown on the plot. Select which metrics are shown by performing any of the following actions:

    <table>
    <colgroup>
    <col style="width: 50%" />
    <col style="width: 50%" />
    </colgroup>
    <thead>
    <tr class="header">
    <th style="text-align: left;">Option</th>
    <th style="text-align: left;">Description</th>
    </tr>
    </thead>
    <tbody>
    <tr class="odd">
    <td style="text-align: left;"><p>Hide all metrics from a query.</p></td>
    <td style="text-align: left;"><p>Click the options menu <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABsAAAAjCAIAAADqn+bCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAA+0lEQVRIie2WMQqEMBBFJ47gUXRBLyBYqbUXULCx9CR2XsAb6AlUEM9kpckW7obdZhwWYWHXX/3i8TPJZEKEUgpOlXFu3JX4V4kmB2qaZhgGKSUiZlkWxzEBC84N9zxv27bdO47Tti0Bs3at4wBgXVca/lJnfN/XPggCGmadIwAsywIAiGhZFk1ydy2EYJKgGCqK4vZUVVU0zKpxnmftp2mi4S/1GhG1N82DMWNNYVmW4zgqpRAxTVMa5t4evlg11nXd9/1eY57nSZIQMKtG13WllLu3bbvrOgJmdUbHwfur8Xniqw6Hh5UYRdGDNowwDA+WvP4UV+JPJ94B1gKUWcTOCT0AAAAASUVORK5CYII=" alt="kebab" /> for the query and click <strong>Hide all series</strong>.</p></td>
    </tr>
    <tr class="even">
    <td style="text-align: left;"><p>Hide a specific metric.</p></td>
    <td style="text-align: left;"><p>Go to the query table and click the colored square near the metric name.</p></td>
    </tr>
    <tr class="odd">
    <td style="text-align: left;"><p>Zoom into the plot and change the time range.</p></td>
    <td style="text-align: left;"><p>Perform one of the following actions:</p>
    <ul>
    <li><p>Visually select the time range by clicking and dragging on the plot horizontally.</p></li>
    <li><p>Use the menu to select the time range.</p></li>
    </ul></td>
    </tr>
    <tr class="even">
    <td style="text-align: left;"><p>Reset the time range.</p></td>
    <td style="text-align: left;"><p>Click <strong>Reset zoom</strong>.</p></td>
    </tr>
    <tr class="odd">
    <td style="text-align: left;"><p>Display outputs for all queries at a specific point in time.</p></td>
    <td style="text-align: left;"><p>Hover over the plot at the point you are interested in. The query outputs appear in a pop-up box.</p></td>
    </tr>
    <tr class="even">
    <td style="text-align: left;"><p>Hide the plot.</p></td>
    <td style="text-align: left;"><p>Click <strong>Hide graph</strong>.</p></td>
    </tr>
    </tbody>
    </table>

# Virtualization metrics

Metric descriptions including example Prometheus Query Language (PromQL) queries. These metrics are not an API and might change between versions.

<div class="note">

The following examples use `topk` queries that specify a time period. If virtual machines (VMs) are deleted during that time period, they can still appear in the query output.

</div>

## vCPU metrics

The following query can identify virtual machines that are waiting for Input/Output (I/O):

`kubevirt_vmi_vcpu_wait_seconds_total`
Returns the wait time (in seconds) on I/O for vCPUs of a virtual machine. Type: Counter.

A value above '0' means that the vCPU wants to run, but the host scheduler cannot run it yet. This inability to run indicates that there is an issue with I/O.

<div class="note">

To query the vCPU metric, the `schedstats=enable` kernel argument must first be applied to the `MachineConfig` object. This kernel argument enables scheduler statistics used for debugging and performance tuning and adds a minor additional load to the scheduler.

</div>

`kubevirt_vmi_vcpu_delay_seconds_total`
Returns the cumulative time, in seconds, that a vCPU was enqueued by the host scheduler but could not run immediately. This delay appears to the virtual machine as *steal time*, which is CPU time lost when the host runs other workloads. Steal time can impact performance and often indicates CPU overcommitment or contention on the host. Type: Counter.

Example vCPU delay query:

The following query returns the average per-second delay over a 5-minute period. A high value may indicate CPU overcommitment or contention on the node:

``` promql
irate(kubevirt_vmi_vcpu_delay_seconds_total[5m]) > 0.05
```

Example vCPU wait time query:

The following query returns the top 3 VMs waiting for I/O at every given moment over a six-minute time period:

``` promql
topk(3, sum by (name, namespace) (rate(kubevirt_vmi_vcpu_wait_seconds_total[6m]))) > 0
```

## vGPU metrics

You can monitor virtual machines using NVIDIA GPUs with this metric.

`kubevirt_vmi_gpu_info`
Returns information about the GPU resources attached to the virtual machine. This metric is implemented as a Gauge with the following metadata attached:

- **Node** - The associated virtual machine using the GPU resource.

- **Namespace** - The associated namespace using the GPU resource.

- **Pod** - The associated pod using the GPU resource.

- **Resource** - The `Extended Resource` type defined in the virtual machine specification.

- **UUID** - The unique hardware identifier of the GPU resource.

  Implement the Data Center GPU Manager Exporter (`dcgm-exporter`) in the virtual machine with the attached GPU resources.

  <div class="note">

  For information on implementing the `dcgm-exporter`, see [Install DCGM Exporter](https://docs.nvidia.com/datacenter/dcgm/latest/installation/install-dcgm-exporter.html).

  </div>

  Expose the `dcgm-exporter` with a `Service` object. For information on configuring a `Service` object for this purpose, see [Configuring the node exporter service](https://docs.redhat.com/en/documentation/openshift_container_platform/4.22/html/virtualization/monitoring#virt-configuring-node-exporter-service_virt-exposing-custom-metrics-for-vms). This section describes how to configure a node exporter service. It is the same process to configure the `dcgm-exporter`. Substitute your `dcgm-exporter` configuration where appropriate.

## Network metrics

The following queries can identify virtual machines that are saturating the network:

`kubevirt_vmi_network_receive_bytes_total`
Returns the total amount of traffic received (in bytes) on the virtual machine’s network. Type: Counter.

`kubevirt_vmi_network_transmit_bytes_total`
Returns the total amount of traffic transmitted (in bytes) on the virtual machine’s network. Type: Counter.

Example network traffic query:

The following query returns the top 3 VMs transmitting the most network traffic at every given moment over a six-minute time period:

``` promql
topk(3, sum by (name, namespace) (rate(kubevirt_vmi_network_receive_bytes_total[6m])) + sum by (name, namespace) (rate(kubevirt_vmi_network_transmit_bytes_total[6m]))) > 0
```

## Storage metrics

You can monitor virtual machine storage traffic and identify high-traffic VMs by using Prometheus queries.

The following queries can identify VMs that are writing large amounts of data:

`kubevirt_vmi_storage_read_traffic_bytes_total`
Returns the total amount (in bytes) of the virtual machine’s storage-related traffic. Type: Counter.

`kubevirt_vmi_storage_write_traffic_bytes_total`
Returns the total amount of storage writes (in bytes) of the virtual machine’s storage-related traffic. Type: Counter.

Example storage-related traffic queries:

- The following query returns the top 3 VMs performing the most storage traffic at every given moment over a six-minute time period:

  ``` promql
  topk(3, sum by (name, namespace) (rate(kubevirt_vmi_storage_read_traffic_bytes_total[6m])) + sum by (name, namespace) (rate(kubevirt_vmi_storage_write_traffic_bytes_total[6m]))) > 0
  ```

- The following query returns the top 3 VMs with the highest average read latency at every given moment over a six-minute time period:

  ``` promql
  topk(3, sum by (name, namespace) (rate(kubevirt_vmi_storage_read_times_seconds_total{name='${name}',namespace='${namespace}'${clusterFilter}}[6m]) / rate(kubevirt_vmi_storage_iops_read_total{name='${name}',namespace='${namespace}'${clusterFilter}}[6m]) > 0)) > 0
  ```

The following queries can track data restored from storage snapshots:

`vm:kubevirt_vmsnapshot_disks_restored:sum`
Returns the total number of virtual machine disks restored from the source virtual machine. Type: Gauge.

`vm:kubevirt_vmsnapshot_restored_bytes:sum`
Returns the amount of space in bytes restored from the source virtual machine. Type: Gauge.

Examples of storage snapshot data queries:

- The following query returns the total number of virtual machine disks restored from the source virtual machine:

  ``` promql
  vm:kubevirt_vmsnapshot_disks_restored:sum{vm_name="simple-vm", vm_namespace="default"}
  ```

- The following query returns the amount of space in bytes restored from the source virtual machine:

  ``` promql
  vm:kubevirt_vmsnapshot_restored_bytes:sum{vm_name="simple-vm", vm_namespace="default"}
  ```

The following queries can determine the I/O performance of storage devices:

`kubevirt_vmi_storage_iops_read_total`
Returns the amount of read I/O operations the virtual machine is performing per second. Type: Counter.

`kubevirt_vmi_storage_iops_write_total`
Returns the amount of write I/O operations the virtual machine is performing per second. Type: Counter.

Example I/O performance query:

The following query returns the top 3 VMs performing the most I/O operations per second at every given moment over a six-minute time period:

``` promql
topk(3, sum by (name, namespace) (rate(kubevirt_vmi_storage_iops_read_total[6m])) + sum by (name, namespace) (rate(kubevirt_vmi_storage_iops_write_total[6m]))) > 0
```

## Guest memory swapping metrics

The following queries can identify which swap-enabled guests are performing the most memory swapping:

`kubevirt_vmi_memory_swap_in_traffic_bytes`
Returns the total amount (in bytes) of memory the virtual guest is swapping in. Type: Gauge.

`kubevirt_vmi_memory_swap_out_traffic_bytes`
Returns the total amount (in bytes) of memory the virtual guest is swapping out. Type: Gauge.

Example memory swapping query:

The following query returns the top 3 VMs where the guest is performing the most memory swapping at every given moment over a six-minute time period:

``` promql
topk(3, sum by (name, namespace) (rate(kubevirt_vmi_memory_swap_in_traffic_bytes[6m])) + sum by (name, namespace) (rate(kubevirt_vmi_memory_swap_out_traffic_bytes[6m]))) > 0
```

<div class="note">

Memory swapping indicates that the virtual machine is under memory pressure. Increasing the memory allocation of the virtual machine can mitigate this issue.

</div>

## Crash detection metrics

You can track guest operating system panic events to identify unstable virtual machines (VMs) and problematic VM images. OpenShift Virtualization detects a guest operating system panic through the `pvpanic` device on Linux and Windows guests, or through the Hyper-V enlightenment mechanism on Windows guests, and records each event in the following metric.

`kubevirt_vmi_guest_os_panic_total`
Returns the total number of guest operating system panic events detected for a VM. Type: Counter.

This metric includes the following labels:

- `namespace` and `name` identify the affected VM.

- `type` identifies the panic source, for example `pvpanic` or `hyper-v`.

- `bugcheck_code` provides the bug check code for a Windows guest. Use this code to identify the cause of a Windows stop error.

Example crash frequency query:

The following query returns the top 3 VMs with the most guest operating system panic events over a one-hour period. A consistently high value can indicate an unstable workload or a problematic VM image:

``` promql
topk(3, sum by (namespace, name) (increase(kubevirt_vmi_guest_os_panic_total[1h]))) > 0
```

Example 24-hour crash count query:

The following query returns the number of guest operating system panic events for each VM over a rolling 24-hour window. Use this query for immediate awareness of crash activity across your environment:

``` promql
sum by (namespace, name) (increase(kubevirt_vmi_guest_os_panic_total[24h])) > 0
```

Example query to identify a problematic VM image:

To determine whether a VM image is the source of instability, compare the guest operating system panic events of VMs that were created from the same image. If multiple VMs share the same `type` or `bugcheck_code` value, the image or its drivers are the likely cause. The following query groups panic events by panic type over a 24-hour window:

``` promql
sum by (namespace, name, type, bugcheck_code) (increase(kubevirt_vmi_guest_os_panic_total[24h])) > 0
```

<div class="note">

The `ClusterVMPanicDetected` and `VMNonRecoverableOSPanic` alerts are based on the `kubevirt_vmi_guest_os_panic_total` metric. When a VM has a run strategy of `Always`, the VM restarts automatically after a non-recoverable panic. Repeated panic events for the same VM can indicate a crash loop that requires investigation.

</div>

## Monitoring AAQ operator metrics

The following metrics are exposed by the Application Aware Quota (AAQ) controller for monitoring resource quotas:

`kube_application_aware_resourcequota`
Returns the current quota usage and the CPU and memory limits enforced by the AAQ Operator resources. Type: Gauge.

`kube_application_aware_resourcequota_creation_timestamp`
Returns the time, in UNIX timestamp format, when the AAQ Operator resource is created. Type: Gauge.

## VM label metrics

`kubevirt_vm_labels`
Returns virtual machine labels as Prometheus labels. Type: Gauge.

You can expose and ignore specific labels by editing the `kubevirt-vm-labels-config` config map. After you apply the config map to your cluster, the configuration is loaded dynamically.

Example config map:

``` yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: kubevirt-vm-labels-config
  namespace: openshift-cnv
data:
  allowlist: "*"
  ignorelist: ""
```

- `data.allowlist` specifies labels to expose.

  - If `data.allowlist` has a value of `"*"`, all labels are included.

  - If `data.allowlist` has a value of `""`, the metric does not return any labels.

  - If `data.allowlist` contains a list of label keys, only the explicitly named labels are exposed. For example: `allowlist: "example.io/name,example.io/version"`.

- `data.ignorelist` specifies labels to ignore. The ignore list overrides the allow list.

  - The `data.ignorelist` field does not support wildcard patterns. It can be empty or include a list of specific labels to ignore.

  - If `data.ignorelist` has a value of `""`, no labels are ignored.

## Live migration metrics

You can query metrics to show live migration status.

`kubevirt_vmi_migration_data_processed_bytes`
The amount of guest operating system data that has migrated to the new virtual machine (VM). Type: Gauge.

`kubevirt_vmi_migration_data_remaining_bytes`
The amount of guest operating system data that remains to be migrated. Type: Gauge.

`kubevirt_vmi_migration_memory_transfer_rate_bytes`
The rate at which memory is becoming dirty in the guest operating system. Dirty memory is data that has been changed but not yet written to disk. Type: Gauge.

`kubevirt_vmi_migrations_in_pending_phase`
The number of pending migrations. Type: Gauge.

`kubevirt_vmi_migrations_in_scheduling_phase`
The number of scheduling migrations. Type: Gauge.

`kubevirt_vmi_migrations_in_running_phase`
The number of running migrations. Type: Gauge.

`kubevirt_vmi_migration_succeeded`
The number of successfully completed migrations. Type: Gauge.

`kubevirt_vmi_migration_failed`
The number of failed migrations. Type: Gauge.

# Virtualization dashboards overview

OpenShift Virtualization includes Perses-based dashboards that give you visibility into virtual machine (VM) inventory, health, resource usage, service levels, and capacity across your cluster.

The dashboards are deployed automatically as `PersesDashboard` custom resources by the HyperConverged Cluster Operator (HCO) in the `openshift-cnv` namespace.

To access these dashboards, click **Observe** → **Dashboards(Perses)** in the web console.

The dashboards require Cluster Observability Operator (COO) with the monitoring stack enabled.

The following table describes the available OpenShift Virtualization dashboards:

<table>
<colgroup>
<col style="width: 33%" />
<col style="width: 66%" />
</colgroup>
<thead>
<tr class="header">
<th style="text-align: left;">Dashboard</th>
<th style="text-align: left;">Description</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p><strong>Virtual Machines Inventory</strong></p></td>
<td style="text-align: left;"><p>Lists all VMs in the cluster with status, instance type, guest operating system, resource allocation, and operational flags such as live-migratable and evictable.</p>
<p>Use this dashboard to manage your VM fleet and find VMs that match specific criteria.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>Virtual Machines Utilization</strong></p></td>
<td style="text-align: left;"><p>Shows resource usage for each VM, including CPU, memory, swap, storage, network, and filesystem metrics.</p>
<p>Use this dashboard to monitor resources, right-size VMs, and optimize costs.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>Virtual Machines Service Level</strong></p></td>
<td style="text-align: left;"><p>Tracks VM uptime and downtime over a defined range of time, showing planned and unplanned breakdowns.</p>
<p>Use this dashboard to report on service-level agreements (SLAs) and find VMs with unexpected downtime.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>Virtual Machines Time in Status</strong></p></td>
<td style="text-align: left;"><p>Shows how long each VM has been in its current state, with filters for time thresholds.</p>
<p>Use this dashboard to find stuck VMs or long-stopped VMs that can be cleaned up.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>Top Consumers</strong></p></td>
<td style="text-align: left;"><p>Ranks VMs by resource consumption across memory, CPU, storage, network, vCPU wait time, and swap.</p>
<p>Use this dashboard to plan capacity and identify resource contention.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>Nodes Memory</strong></p></td>
<td style="text-align: left;"><p>Shows memory usage per node, including overcommit ratios, memory pressure, and system reservations.</p>
<p>Use this dashboard to plan memory capacity, analyze overcommit, and prevent out-of-memory events.</p></td>
</tr>
</tbody>
</table>

## Dashboard panel types

The OpenShift Virtualization dashboards combine the following panel types to display data. Understanding each panel type helps you interpret any dashboard.

Gauge panels
Display a single percentage value against thresholds that classify the value as healthy, warning, or critical. Each state also has a color: healthy is green, warning is amber, and critical is red.

Time series panels
Display multi-line plots over a time range. Use these panels to identify trends and compare entities over time.

Stat panels
Display a single numeric value with unit formatting, such as bytes, percentage, or hours.

Table panels
Display multi-column, sortable data with filtering and conditional formatting. Most dashboards use table panels as their primary display.

## Nodes Memory dashboard concepts

The Nodes Memory dashboard helps you plan memory capacity, analyze overcommit, and prevent out-of-memory events. To use the dashboard effectively, you must understand the following concepts.

<div class="note">

The dashboard filters all data by node and by Kubernetes node role. The role filter defaults to `worker`, so the dashboard excludes control plane nodes until you change the filter.

</div>

Memory overcommit
Overcommit is the practice of assigning more virtual memory to VMs than the physical memory available on a node. The overcommit ratio compares assigned virtual memory to physical memory or to pod memory requests. A higher ratio increases VM density but also increases the risk of memory contention if VMs use their assigned memory at the same time.

Virtual committed memory
Virtual committed memory is the total memory committed to VMs, including launcher overhead, measured against allocatable physical memory. Comparing committed virtual memory to node capacity shows the worst-case memory demand if all VMs use their full memory allocation at once.

Pressure stall information (PSI)
PSI measures the time that processes are delayed or blocked while waiting for memory. A `Waiting` value indicates processes that are delayed, and a `Stalled` value indicates processes that are completely blocked. Rising PSI values indicate memory contention that can affect workload performance.

Swap usage
Rising swap usage indicates memory pressure that has not yet caused PSI stalls. Monitor swap usage as an early warning of memory constraints.

System reserved memory
System reserved memory is the memory set aside for system processes on each node. When active system process memory approaches the reserved budget, the node can trigger the `SystemMemoryExceedsReservation` alert.

Use these metrics together to detect memory pressure before it affects workloads, evaluate overcommit ratios, and plan node scaling decisions. The following thresholds indicate the overall memory health of the cluster:

Healthy
Memory utilization is below 70%, virtual committed memory is below 120%, PSI values are near zero, and no node exceeds its system reserved memory.

Warning
Memory utilization is between 80% and 90%, virtual committed memory approaches 150%, or individual nodes diverge significantly from the cluster average, which indicates imbalanced scheduling.

Critical
Memory utilization is above 90%, PSI values exceed 0.5, a node exceeds its system reserved memory, or the virtual commit ratio on a node exceeds 200%. These conditions indicate that the cluster is at risk of out-of-memory events and VM eviction.

# Additional resources

- [KubeVirt components metrics](https://github.com/kubevirt/monitoring/blob/main/docs/metrics.md)

- [Add kernel arguments to nodes](../../machine_configuration/machine-configs-configure.xml#nodes-nodes-kernel-arguments_machine-configs-configure)

- [About OpenShift Container Platform monitoring](https://docs.redhat.com/en/documentation/monitoring_stack_for_red_hat_openshift/latest/html/about_monitoring/about-ocp-monitoring)

- [Querying Prometheus](https://prometheus.io/docs/prometheus/latest/querying/basics/)

- [Prometheus query examples](https://prometheus.io/docs/prometheus/latest/querying/examples/)
