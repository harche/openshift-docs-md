Reserve CPUs for Open vSwitch Data Plane Development Kit (OVS-DPDK) poll mode driver (PMD) threads by using a `PerformanceProfile` custom resource (CR). The Node Tuning Operator applies multi-layer CPU isolation so that those host-side threads can run with reduced interference from the operating system and Kubernetes scheduling.

<div class="important">

OVS-DPDK CPU reservation is a Technology Preview feature only. Technology Preview features are not supported with Red Hat production service level agreements (SLAs) and might not be functionally complete. Red Hat does not recommend using them in production. These features provide early access to upcoming product features, enabling customers to test functionality and provide feedback during the development process.

For more information about the support scope of Red Hat Technology Preview features, see [Technology Preview Features Support Scope](https://access.redhat.com/support/offerings/techpreview/).

</div>

# OVS-DPDK CPU isolation

OVS-DPDK poll mode driver (PMD) threads busy-poll the NIC on the host. As a result, they need exclusive CPUs. Use `spec.cpu.ovsDpdk` in a `PerformanceProfile` custom resource (CR) when `reserved` and `isolated` alone cannot protect those threads from jitter.

OVS-DPDK PMD threads run as host processes outside the pod scheduling path. Interruption from the kernel, system daemons, or other workloads can introduce jitter and reduce throughput. A performance profile already defines the following CPU sets, which do not fully cover that case:

`reserved`
CPUs for operating system daemons and Kubernetes infrastructure. Without additional controls, `Burstable` and `BestEffort` pods can still run on reserved CPUs.

`isolated`
CPUs for `Guaranteed` application pods that the `kubelet` schedules. Isolated CPUs are not intended for host processes such as OVS-DPDK.

Because OVS-DPDK runs as a daemon on the host, the profile needs a third CPU set that is excluded from `kubelet` scheduling and from host interference sources.

When you set `spec.cpu.ovsDpdk`, the Node Tuning Operator ensures that pods of any QoS class are not placed on these CPUs. The Node Tuning Operator also bans them from `irqbalance`, removes them from `systemd` CPU affinity, adds them to kernel isolation parameters, and places them under the OVS cgroup hierarchy.

<div class="important">

The `ovsDpdk` CPU set is specific to OVS-DPDK. Do not use it as a generic pool for other DPDK applications. The Node Tuning Operator places these CPUs under the existing `ovs.slice` hierarchy for `ovs-vswitchd`.

</div>

For the CPU set listed in `spec.cpu.ovsDpdk`, the Node Tuning Operator applies configuration across several layers, including the following:

- Adds the CPUs to the `kubelet` `reservedSystemCPUs` set together with `spec.cpu.reserved`. When `spec.cpu.shared` is also set, `reservedSystemCPUs` is the union of `reserved`, `shared`, and `ovsDpdk`. The `ovsDpdk` CPUs are not added to the CRI-O shared cpuset. For more information about shared CPUs, see "How ExecCPUAffinity prevents latency spikes from exec operations" in *Additional resources*.

- Adds the CPUs to TuneD `isolated_cores` together with `spec.cpu.isolated`.

- Includes the CPUs in kernel boot parameters such as `isolcpus`, `nohz_full`, and `rcu_nocbs`.

- Excludes the CPUs from `systemd.cpu_affinity`.

- Updates `IRQBALANCE_BANNED_CPUS` so that hardware IRQs are not balanced onto those CPUs.

- Creates and configures `ovsdpdk.slice` under `ovs.slice/ovs-vswitchd.service`, including exclusive CPU assignment for OVS-DPDK.

You can add the `performance.openshift.io/cpu-load-balancing-ovs-dpdk` annotation to the performance profile to control kernel scheduler load balancing on the `ovsDpdk` CPUs.

- Set the annotation to `disable` to exclude `ovsDpdk` CPUs from the kernel scheduler load-balancing pool. The Node Tuning Operator configures the OVS-DPDK cgroup partition as `isolated`.

- Omit the annotation or set it to `enable` to keep the default behavior.

The Node Tuning Operator requires either workload partitioning or the `kubelet` CPU Manager `strict-cpu-reservation` policy option to prevent `Burstable` and `BestEffort` pods from running on OVS-DPDK CPUs. If neither prerequisite is satisfied, the performance profile enters a `Degraded` state with reason `OvsDpdkCPUsPrerequisiteNotMet`.

Choose one of the following options:

- **Recommended:** Use workload partitioning. Enable workload partitioning at cluster install time by setting `cpuPartitioningMode: AllNodes`. The performance profile populates the workload partitioning CPU sets when applied. Workload partitioning provides comprehensive CPU isolation for platform and infrastructure workloads.

- **Alternative:** Configure `strict-cpu-reservation` using the `kubeletconfig.experimental` annotation in your OVS-DPDK performance profile. Use this option only if workload partitioning was not enabled during cluster installation.

<div class="note">

You must choose NUMA-aligned CPUs for your OVS-DPDK NICs. The Operator does not automatically assign CPUs based on NIC locality.

</div>

# Reserve OVS-DPDK CPUs with a performance profile

Create or update a `PerformanceProfile` custom resource (CR) that reserves CPUs for OVS-DPDK by setting `spec.cpu.ovsDpdk`. You can optionally add the `performance.openshift.io/cpu-load-balancing-ovs-dpdk` annotation in the same CR to disable kernel scheduler load balancing on the OVS-DPDK CPUs.

- You have access to the cluster as a user with the `cluster-admin` role.

- You have installed the OpenShift CLI (`oc`).

- You have identified whether workload partitioning was enabled at cluster installation (`cpuPartitioningMode: AllNodes`).

1.  Generate a base performance profile by using the Performance Profile Creator (PPC) tool with `must-gather` data from your cluster:

    1.  Collect `must-gather` data from the cluster by running the following command:

        ``` terminal
        $ oc adm must-gather
        ```

    2.  Generate the base profile by running the PPC tool:

        ``` terminal
        $ podman run --entrypoint performance-profile-creator \
          -v <path_to_must_gather>:/must-gather:z \
          registry.redhat.io/openshift4/ose-cluster-node-tuning-rhel9-operator:v4.17 \
          --must-gather-dir-path /must-gather \
          --mcp-name=<mcp_name> \
          --profile-name=ovs-dpdk-isolation \
          --reserved-cpu-count=<reserved_count> \
          --ovs-dpdk-cpu-count=<ovs_dpdk_count> \
          --rt-kernel=true \
          --split-reserved-cpus-across-numa=false \
          --power-consumption-mode=ultra-low-latency \
          > my-performance-profile.yaml
        ```

        `<path_to_must_gather>`
        Replace with the path to the `must-gather` output directory created by the `oc adm must-gather` command. The directory name follows the pattern `must-gather.local.<id>`.

        `<mcp_name>`
        Replace with the name of the machine config pool for the target nodes. For single-node OpenShift, use `--mcp-name=master`.

        `<reserved_count>`
        Replace with the number of CPUs to reserve for platform and cluster management.

        `<ovs_dpdk_count>`
        Replace with the number of CPUs to reserve for OVS-DPDK. When you specify this parameter, the PPC tool populates `spec.cpu.ovsDpdk` with the specified number of CPUs.

        <div class="note">

        For more information about other PPC arguments, see "Running the Performance Profile Creator using Podman".

        </div>

2.  Review and edit the generated profile to ensure that the CPUs in `spec.cpu.ovsDpdk` are on the same NUMA node as the OVS-DPDK NICs by running the following command:

    ``` terminal
    $ cat my-performance-profile.yaml
    ```

    The PPC tool allocates CPUs by count and ensures they are siblings on the same physical core, but does not consider NUMA locality relative to the OVS-DPDK NICs. Verify that the `ovsDpdk` CPUs match the NUMA node identified in the prerequisites. If the allocated CPUs are on the wrong NUMA node, edit the `ovsDpdk` field to specify CPUs from the correct NUMA node. Ensure that the CPUs you specify are not already in the `reserved` set.

3.  If workload partitioning is not enabled on your cluster, edit the generated PerformanceProfile to add the `strict-cpu-reservation` annotation. This prevents `Burstable` and `BestEffort` pods from running on reserved CPUs:

    ``` yaml
    apiVersion: performance.openshift.io/v2
    kind: PerformanceProfile
    metadata:
      name: ovs-dpdk-isolation
      annotations:
        kubeletconfig.experimental: |
          {
           "cpuManagerPolicyOptions":{"strict-cpu-reservation":"true"}
          }
    spec:
      cpu:
        isolated: "4-7"
        ovsDpdk: "2-3"
        reserved: "0-1"
      machineConfigPoolSelector:
        pools.operator.machineconfiguration.openshift.io/worker: ""
      nodeSelector:
        node-role.kubernetes.io/worker: ""
    ```

    <div class="note">

    If workload partitioning is enabled, skip this step.

    </div>

4.  Optional: To disable kernel scheduler load balancing on the OVS-DPDK CPUs, add the `performance.openshift.io/cpu-load-balancing-ovs-dpdk` annotation set to `disable`:

    ``` yaml
    apiVersion: performance.openshift.io/v2
    kind: PerformanceProfile
    metadata:
      name: ovs-dpdk-isolation
      annotations:
        performance.openshift.io/cpu-load-balancing-ovs-dpdk: "disable"
        kubeletconfig.experimental: |
          {
           "cpuManagerPolicyOptions":{"strict-cpu-reservation":"true"}
          }
    spec:
      cpu:
        isolated: "4-7"
        ovsDpdk: "2-3"
        reserved: "0-1"
      machineConfigPoolSelector:
        pools.operator.machineconfiguration.openshift.io/worker: ""
      nodeSelector:
        node-role.kubernetes.io/worker: ""
    ```

    Omit the `kubeletconfig.experimental` annotation if workload partitioning is enabled on your cluster.

5.  Apply the performance profile by running the following command:

    ``` terminal
    $ oc apply -f my-performance-profile.yaml
    ```

6.  Wait for the Machine Config Operator to apply the configuration and for the target nodes to reboot. Confirm that the relevant machine config pool has finished updating by running the following command:

    ``` terminal
    $ oc get mcp -w
    ```

    The pool that matches your profile selector must show `UPDATED=True` and `UPDATING=False`. Press Ctrl+C to stop watching.

<!-- -->

1.  Verify that the performance profile is available by running the following command:

    ``` terminal
    $ oc get performanceprofile ovs-dpdk-isolation -o yaml
    ```

    Check the status conditions in the output. The `Available` condition must have `status: "True"` and the `Degraded` condition must have `status: "False"`.

    A properly configured system generates an output similar to this healthy profile example:

    ``` yaml
    status:
      conditions:
      - status: "True"
        type: Available
      - status: "False"
        type: Degraded
      runtimeClass: performance-ovs-dpdk-isolation
    ```

    <div class="note">

    If the `Degraded` condition shows `status: "True"` with `reason: OvsDpdkCPUsPrerequisiteNotMet`, the OVS-DPDK CPU feature requires strict CPU reservation. Verify that workload partitioning is enabled or that you have added the `kubeletconfig.experimental` annotation to configure `strict-cpu-reservation` in the performance profile, then reapply the profile.

    </div>

2.  Verify that `kubelet` reserved system CPUs are the union of `reserved` and `ovsDpdk` by running the following command:

    ``` terminal
    $ oc get --raw "/api/v1/nodes/<node_name>/proxy/configz" | \
      python3 -c 'import sys,json; print(json.load(sys.stdin)["kubeletconfig"]["reservedSystemCPUs"])'
    ```

    The reported set must equal the union of `reserved` and `ovsDpdk`. For example, with `reserved: "0-1"` and `ovsDpdk: "2-3"`, the output is `0-3`.

3.  Start a debug session on a node that matches the performance profile by running the following command:

    ``` terminal
    $ oc debug node/<node_name>
    ```

4.  Set `/host` as the root directory for the debug shell by running the following command:

    ``` terminal
    # chroot /host
    ```

5.  Verify that kernel boot parameters include the OVS-DPDK CPUs by running the following command:

    ``` terminal
    # cat /proc/cmdline
    ```

    Confirm the following:

    - `isolcpus` includes the union of `isolated` and `ovsDpdk` CPUs.

    - `nohz_full` and `rcu_nocbs` include the `ovsDpdk` CPUs.

    - `systemd.cpu_affinity` does not include the `ovsDpdk` CPUs.

6.  Verify that IRQ balancing excludes the OVS-DPDK CPUs by running the following command:

    ``` terminal
    # grep -E "^IRQBALANCE_BANNED_CPUS=" /etc/sysconfig/irqbalance
    ```

    Confirm that `IRQBALANCE_BANNED_CPUS` includes a hex mask that covers the `ovsDpdk` CPUs. For example, `ovsDpdk: "2-3"` (CPUs 2 and 3) produces `IRQBALANCE_BANNED_CPUS=c`. The mask value is not zero-padded.

7.  Verify that the default SMP affinity mask excludes the OVS-DPDK CPUs by running the following command:

    ``` terminal
    # cat /proc/irq/default_smp_affinity
    ```

    The mask must clear the bits for `ovsDpdk` CPUs. For example, with `ovsDpdk: "2-3"` on an 8-CPU node, the output is `f3`.

8.  Verify that the OVS-DPDK cgroup slice has the correct exclusive CPUs assigned by running the following command:

    ``` terminal
    # cat /sys/fs/cgroup/ovs.slice/ovs-vswitchd.service/ovsdpdk.slice/cpuset.cpus.exclusive
    ```

    The output must match the `ovsDpdk` value from the performance profile. For example, with `ovsDpdk: "2-3"`, the output is `2-3`.

<div class="note">

These checks confirm that the platform configuration for OVS-DPDK CPU isolation is in place. Measuring OVS-DPDK dataplane throughput and packet loss requires your OVS-DPDK application test environment.

</div>

# Update or remove OVS-DPDK CPU reservation

Change the `spec.cpu.ovsDpdk` CPU set on a Day 2 retune, or remove the field when you no longer need OVS-DPDK CPU isolation. Keep CPU sets disjoint, wait for the Machine Config Operator (MCO) to apply changes, and re-verify isolation or cleanup on the node.

- You have access to the cluster as a user with the `cluster-admin` role.

- You have installed the OpenShift CLI (`oc`).

- You have a `PerformanceProfile` custom resource (CR) with `spec.cpu.ovsDpdk` already applied.

- You have workload partitioning enabled, or the `kubelet` CPU Manager `strict-cpu-reservation` policy option configured on the target nodes.

1.  Choose one of the following options:

    - To change the OVS-DPDK CPU set, edit the performance profile and replace `spec.cpu.ovsDpdk` with the new CPU list. Adjust `spec.cpu.isolated` and `spec.cpu.reserved` so that the sets do not overlap.

      <div class="formalpara-title">

      **Example expansion of the OVS-DPDK set (before)**

      </div>

      ``` yaml
      spec:
        cpu:
          isolated: "4-7"
          ovsDpdk: "2-3"
          reserved: "0-1"
      ```

      <div class="formalpara-title">

      **Example expansion of the OVS-DPDK set (after)**

      </div>

      ``` yaml
      spec:
        cpu:
          isolated: "6-7"
          ovsDpdk: "2-5"
          reserved: "0-1"
      ```

    - To remove OVS-DPDK CPU reservation, edit the performance profile, delete `spec.cpu.ovsDpdk`, remove the `performance.openshift.io/cpu-load-balancing-ovs-dpdk` annotation if present, and move the former OVS-DPDK CPUs into `isolated` or another appropriate set so that your CPU layout remains valid.

2.  Apply the updated performance profile by running the following command:

    ``` terminal
    $ oc apply -f my-performance-profile.yaml
    ```

3.  Wait for the Machine Config Operator to apply the configuration and for the target nodes to reboot. Confirm that the relevant machine config pool has finished updating by running the following command:

    ``` terminal
    $ oc get mcp -w
    ```

    The pool that matches your profile selector must show `UPDATED=True` and `UPDATING=False`.

- For an updated `ovsDpdk` set, repeat the verification checks from *Reserve OVS-DPDK CPUs with a performance profile* against the new CPU list. Additionally, confirm that CPUs that left the `ovsDpdk` set are no longer banned or exclusively assigned for OVS-DPDK, and they match their new role in `isolated` or `reserved`.

- For a removed `ovsDpdk` field, confirm that no OVS-DPDK isolation artifacts remain:

  - `reservedSystemCPUs` no longer includes the former `ovsDpdk` CPUs (unless those CPUs were moved into `reserved`).

  - `IRQBALANCE_BANNED_CPUS` and `default_smp_affinity` no longer isolate those CPUs for OVS-DPDK.

  - The `ovsdpdk.slice` directory under `ovs.slice/ovs-vswitchd.service/` is gone.

  - Former `ovsDpdk` CPUs behave according to their new role in the performance profile.

# OVS-DPDK performance profile fields

Use the following reference when you reserve OVS-DPDK CPUs in a `PerformanceProfile` custom resource (CR).

<table>
<caption>OVS-DPDK performance profile fields</caption>
<colgroup>
<col style="width: 33%" />
<col style="width: 16%" />
<col style="width: 50%" />
</colgroup>
<thead>
<tr class="header">
<th style="text-align: left;">Field or annotation</th>
<th style="text-align: left;">Type</th>
<th style="text-align: left;">Description</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p><code>spec.cpu.ovsDpdk</code></p></td>
<td style="text-align: left;"><p>string (CPU set)</p></td>
<td style="text-align: left;"><p>Optional. CPUs reserved for OVS-DPDK PMD threads. Example value: <code>"2-3,8-9"</code>. Must not overlap <code>reserved</code>, <code>isolated</code>, <code>shared</code>, or <code>offlined</code>.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><code>metadata.annotations["performance.openshift.io/cpu-load-balancing-ovs-dpdk"]</code></p></td>
<td style="text-align: left;"><p>string</p></td>
<td style="text-align: left;"><p>Optional. Set to <code>disable</code> to exclude <code>ovsDpdk</code> CPUs from kernel scheduler load balancing and scheduling domains, and to set the OVS-DPDK cgroup partition to <code>isolated</code>. Omit the annotation or set it to <code>enable</code> to keep the default <code>member</code> partition.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><code>metadata.annotations["kubeletconfig.experimental"]</code></p></td>
<td style="text-align: left;"><p>string (JSON)</p></td>
<td style="text-align: left;"><p>Required if workload partitioning is not enabled. Configure kubelet settings as a JSON string. To satisfy the OVS-DPDK prerequisite when workload partitioning is disabled, set <code>cpuManagerPolicyOptions</code> with <code>strict-cpu-reservation</code> to <code>true</code>. Example:</p>
<div class="sourceCode" id="cb1"><pre class="sourceCode json"><code class="sourceCode json"><span id="cb1-1"><a href="#cb1-1" aria-hidden="true" tabindex="-1"></a><span class="fu">{</span><span class="dt">&quot;cpuManagerPolicyOptions&quot;</span><span class="fu">:{</span><span class="dt">&quot;strict-cpu-reservation&quot;</span><span class="fu">:</span><span class="st">&quot;true&quot;</span><span class="fu">}}</span></span></code></pre></div></td>
</tr>
</tbody>
</table>

OVS-DPDK performance profile fields

# Additional resources

- [Running the Performance Profile Creator using Podman](../scalability_and_performance/cnf-tuning-low-latency-nodes-with-perf-profile.xml#running-the-performance-profile-profile-cluster-using-podman_cnf-tuning-low-latency-nodes-with-perf-profile)

- [Creating a performance profile](../scalability_and_performance/cnf-tuning-low-latency-nodes-with-perf-profile.xml#cnf-create-performance-profiles_cnf-tuning-low-latency-nodes-with-perf-profile)

- [How ExecCPUAffinity prevents latency spikes from exec operations](../scalability_and_performance/cnf-tuning-low-latency-nodes-with-perf-profile.xml#cnf-protecting-low-latency-workloads_cnf-tuning-low-latency-nodes-with-perf-profile)

- [Workload partitioning](../scalability_and_performance/enabling-workload-partitioning.xml#enabling-workload-partitioning)

- [Using the Node Tuning Operator](../scalability_and_performance/using-node-tuning-operator.xml#using-node-tuning-operator)
