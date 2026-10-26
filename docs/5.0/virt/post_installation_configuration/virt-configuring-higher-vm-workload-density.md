You can increase the number of virtual machines (VMs) on nodes by overcommitting memory (RAM). You overcommit memory by provisioning swap storage on worker nodes. This is useful when you have many similar or underused workloads.

> [!NOTE]
> Memory overcommitment can lower workload performance on a highly utilized system.

# Swap provisioning methods

You can provision swap storage on worker nodes by using either an NVMe partition or a file-based approach. The method you choose depends on your hardware configuration and performance requirements.

**NVMe partition-based swap** requires a dedicated NVMe device on each worker node and provides better performance for production workloads with heavy memory overcommitment. This method is permanent and requires repartitioning to remove.

**File-based swap** uses existing filesystem space and works on any worker node without dedicated hardware. This method has slower I/O performance than partition-based swap but is easier to provision and remove. Use this method for testing, development, or production clusters where dedicated NVMe devices are not available.

# Swap space requirements

The swap space that you provision on a node must be at least equal to the overcommitted RAM. This requirement applies to both NVMe partition-based swap and file-based swap.

Calculate the amount of swap space to provision on a node by using the following formula:

    NODE_SWAP_SPACE = NODE_RAM * (MEMORY_OVER_COMMIT_PERCENT / 100% - 1)

Example:

    NODE_SWAP_SPACE = 16 GB * (150% / 100% - 1)
                   = 16 GB * (1.5 - 1)
                   = 16 GB * (0.5)
                   =  8 GB

# Provision swap on an NVMe device

You can provision a dedicated NVMe device for swap. The `virt-platform-autopilot` controller automatically enables a swap partition labeled `OCPSWAP` for virtualization workloads. Use this method for production clusters requiring better performance.

<div>

<div class="title">

Prerequisites

</div>

- You have installed the OpenShift CLI (`oc`).

- You are logged in to the cluster with the `cluster-admin` role.

- You have installed OpenShift Virtualization. The `virt-platform-autopilot` controller is enabled by default.

- The worker node has a dedicated NVMe device.

- The NVMe device has enough capacity for the node’s worst-case memory overcommitment.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Select a worker node where you want to enable memory overcommitment and start a debug session by running the following command:

    ``` terminal
    $ oc debug node/<node_name>
    ```

    Replace `<node_name>` with the name of the worker node.

2.  Enter the host context by running the following command:

    ``` terminal
    $ chroot /host
    ```

3.  List the available NVMe disks and their World Wide Names (WWNs) by running the following command:

    ``` terminal
    $ lsblk -p -o +WWN
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` terminal
    NAME         TYPE MODEL                  SERIAL            REV TRAN   RQ-SIZE  MQ WWN
    /dev/nvme0n1 disk KXG8AZNV512G LA KIOXIA 63QFXXXXXXEU 5108APLA nvme      1023  12 eui.8ce38e0500e775a4
    ```

    </div>

4.  Find the device path by using its WWN. The path follows the `/dev/disk/by-id/nvme-<WWN>` format. Run the following command, replacing `<WWN>` with the value from the previous command:

    ``` terminal
    $ ls /dev/disk/by-id/nvme-<WWN>
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` terminal
    /dev/disk/by-id/nvme-eui.8ce38e0500e775a4
    ```

    </div>

5.  Create a GUID Partition Table (GPT) partition table and an `OCPSWAP` partition by running the following command, replacing `<WWN>` with the WWN of the selected device:

    > [!WARNING]
    > The following command erases all data on the selected NVMe device. Back up any data that you need to retain before you continue.

    ``` terminal
    $ echo -e 'label: gpt\nname="OCPSWAP", type=swap' | sfdisk --wipe always /dev/disk/by-id/nvme-<WWN>
    ```

    The partition name must be `OCPSWAP` so that the `virt-platform-autopilot` controller can discover and enable the partition.

    > [!WARNING]
    > Only one partition on the node can use the `OCPSWAP` label. If more than one partition uses this label, the `/dev/disk/by-partlabel/OCPSWAP` path does not resolve deterministically, and later commands can format or enable the wrong partition.

6.  Format the partition as Linux swap and set its filesystem label to `OCPSWAP` by running the following command:

    ``` terminal
    $ mkswap -L OCPSWAP /dev/disk/by-partlabel/OCPSWAP
    ```

    The `/dev/disk/by-partlabel/OCPSWAP` path resolves to the partition that you created in the previous step. The `-L OCPSWAP` option sets the swap filesystem label, which the `virt-platform-autopilot` controller uses to identify the swap partition. You must format the partition, not the whole NVMe device.

7.  Verify the swap partition before rebooting the node by running the following commands:

    ``` terminal
    $ swapon /dev/disk/by-partlabel/OCPSWAP
    $ free -m
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` terminal
                   total        used        free      shared  buff/cache   available
    Mem:           31728       20964         906        4586       12269       10764
    Swap:           8191          95        8096
    ```

    </div>

8.  Reboot the node by running the following command:

    ``` terminal
    $ systemctl reboot
    ```

</div>

<div>

<div class="title">

Verification

</div>

1.  After the node reboots, start a debug session by running the following command:

    ``` terminal
    $ oc debug node/<node_name>
    ```

2.  Enter the host context by running the following command:

    ``` terminal
    $ chroot /host
    ```

3.  Verify that the `virt-platform-autopilot` controller discovered the swap partition by running the following command:

    ``` terminal
    $ ls /dev/disk/by-partlabel/OCPSWAP
    ```

4.  Verify that swap space is available by running the following command:

    ``` terminal
    $ free -m
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` terminal
                   total        used        free      shared  buff/cache   available
    Mem:           31728       20964         906        4586       12269       10764
    Swap:           8191          95        8096
    ```

    </div>

</div>

# Provision swap by using a file

You can provision swap by creating a file on the worker node. The `MachineConfig` object that you create provisions the swap file and enables it for virtualization workloads. Use this method when dedicated NVMe devices are not available.

<div>

<div class="title">

Prerequisites

</div>

- You have installed the OpenShift CLI (`oc`).

- You are logged in to the cluster with the `cluster-admin` role.

- The node belongs to a worker pool.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Create a `MachineConfig` file with the parameters shown in the following example:

    ``` yaml
    apiVersion: machineconfiguration.openshift.io/v1
    kind: MachineConfig
    metadata:
      labels:
        machineconfiguration.openshift.io/role: worker
      name: 90-worker-swap
    spec:
      config:
        ignition:
          version: 3.5.0
        systemd:
          units:
            - contents: |
                [Unit]
                Description=Provision and enable swap
                ConditionFirstBoot=no
                ConditionPathExists=!/var/tmp/swapfile

                [Service]
                Type=oneshot
                Environment=SWAP_SIZE_MB=5000
                ExecStart=/bin/sh -c "sudo fallocate -l ${SWAP_SIZE_MB}M /var/tmp/swapfile && \
                sudo chmod 600 /var/tmp/swapfile && \
                sudo mkswap /var/tmp/swapfile && \
                sudo swapon /var/tmp/swapfile && \
                free -h"

                [Install]
                RequiredBy=kubelet-dependencies.target
              enabled: true
              name: swap-provision.service
            - contents: |
                [Unit]
                Description=Enable swap
                ConditionFirstBoot=no
                ConditionPathExists=/var/tmp/swapfile

                [Service]
                Type=oneshot
                ExecStart=/bin/sh -c "sudo swapon /var/tmp/swapfile"

                [Install]
                RequiredBy=kubelet-dependencies.target
              enabled: true
              name: swap-enable.service
    ```

    Set the `SWAP_SIZE_MB` value to the amount of swap space to provision on the node, in MB.

2.  Wait for the worker nodes to sync with the new configuration by running the following command:

    ``` terminal
    $ oc wait mcp worker --for condition=Updated=True --timeout=-1s
    ```

</div>

<div>

<div class="title">

Verification

</div>

1.  View a list of worker nodes by running the following command:

    ``` terminal
    $ oc get nodes -l node-role.kubernetes.io/worker
    ```

2.  Select a node from the list and display its memory usage by running the following command:

    ``` terminal
    $ oc debug node/<selected_node> -- free -m
    ```

    Replace `<selected_node>` with the node name.

    The `Swap:` row displays an amount greater than zero if the node has swap enabled.

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` terminal
                   total        used        free      shared  buff/cache   available
    Mem:           31846       23155        1044        6014       14483        8690
    Swap:           8191        2337        5854
    ```

    </div>

</div>

# Remove swap from an NVMe device

You can remove a swap partition from an NVMe device, freeing the device for other use. The node must be placed in maintenance mode before you remove the swap partition.

<div>

<div class="title">

Prerequisites

</div>

- You have installed the OpenShift CLI (`oc`).

- You are logged in to the cluster with the `cluster-admin` role.

- The worker node has an NVMe swap partition labeled `OCPSWAP`.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Place the node in maintenance mode by using the `oc adm cordon` and `oc adm drain` commands.

2.  Verify that all pod and VM workloads are evicted from the node by running the following commands:

    ``` terminal
    $ oc get pods --all-namespaces --field-selector spec.nodeName=<node_name>
    ```

    ``` terminal
    $ oc get vmi -A --field-selector spec.nodeName=<node_name>
    ```

    Only DaemonSet pods should remain on the node.

3.  Start a debug session by running the following command:

    ``` terminal
    $ oc debug node/<node_name>
    ```

    Replace `<node_name>` with the name of the worker node.

4.  Enter the host context by running the following command:

    ``` terminal
    $ chroot /host
    ```

5.  Disable the swap partition by running the following command:

    ``` terminal
    $ swapoff /dev/disk/by-partlabel/OCPSWAP
    ```

6.  Verify that swap is disabled by running the following command:

    ``` terminal
    $ free -m
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` terminal
                   total        used        free      shared  buff/cache   available
    Mem:           31728       20964         906        4586       12269       10764
    Swap:              0           0           0
    ```

    </div>

    The `Swap:` row displays zero values when swap is disabled.

    > [!NOTE]
    > If the `Swap:` row shows non-zero values, the swap partition is still active. Verify that all workloads are evacuated and retry the `swapoff` command. If the issue persists, reboot the node to force swap deactivation.

7.  Remove the swap partition:

    1.  Set the `$DISK` variable to the disk device path by running the following command:

        ``` terminal
        $ DISK="/dev/$(lsblk -no PKNAME /dev/disk/by-partlabel/OCPSWAP)"
        ```

    2.  Delete the partition by running the following command:

        > [!WARNING]
        > This command removes all partitions on the device, not just the `OCPSWAP` partition. If you manually created additional partitions on this device, they will be deleted.

        ``` terminal
        $ sfdisk --delete $DISK
        ```

8.  Verify that the `OCPSWAP` partition label is removed by running the following command:

    ``` terminal
    $ ls /dev/disk/by-partlabel/OCPSWAP
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` terminal
    ls: cannot access '/dev/disk/by-partlabel/OCPSWAP': No such file or directory
    ```

    </div>

    > [!NOTE]
    > If the partition label still exists after running `sfdisk --delete`, verify the correct disk device was used and retry the deletion command. Reboot the node if the partition table was not updated.

9.  Exit the debug session by running the following commands:

    ``` terminal
    $ exit
    ```

    ``` terminal
    $ exit
    ```

    The first `exit` command leaves the chroot environment. The second `exit` command terminates the debug pod.

10. Remove the node from maintenance mode by using the `oc adm uncordon` command.

</div>

# Enable memory overcommitment and provision swap

You can increase the number of virtual machines (VMs) on a node by overcommitting memory and provisioning swap resources. When you enable memory overcommitment, the `virt-platform-autopilot` controller automatically deploys the necessary node-level configurations.

<div>

<div class="title">

Prerequisites

</div>

- You have installed the OpenShift CLI (`oc`).

- You are logged in to the cluster with the `cluster-admin` role.

- You have defined a memory overcommit ratio.

- You have provisioned swap storage on worker nodes.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Choose one of the following methods to enable memory overcommitment in OpenShift Virtualization:

    After you enable memory overcommitment, only virtual machine workloads (VM pods) of the `Burstable` Quality of Service (`QoS`) class can use swap resources. VM pods of the `Guaranteed` `QoS` class and pods of any `QoS` class that do not belong to VMs cannot use swap resources. For descriptions of `QoS` classes, see [Configure Quality of Service for Pods](https://kubernetes.io/docs/tasks/configure-pod-container/quality-service-pod/) (Kubernetes documentation).

    When you configure virtual machines for memory overcommitment, use `spec.domain.memory.guest` in the VM manifest. Using `spec.domain.resources.requests.memory` disables the memory overcommit configuration.

    - To use the web console:

      1.  In the OpenShift Container Platform web console, go to **Virtualization** → **Settings**.

      2.  Click the **Cluster** tab.

      3.  Expand **General settings**.

      4.  Expand **Memory request ratio**.

      5.  In the **Request ratio** field, enter a value from 25 to 100.

          The request ratio is the percentage of each virtual machine’s configured memory that the cluster requests. A lower ratio increases overcommitment. At a ratio of 25%, a VM configured with 4 GiB of memory requests 1 GiB on the cluster. At a ratio of 100%, it requests the full 4 GiB.

          The web console indicates the level of risk for the value you enter. It shows **Recommended** at 75% or greater, **Use with caution** from 50% to 74.9%, and **High overcommit risk** from 25% to 49.9%.

          The **Active ratio** line shows the ratio currently calculated across all virtual machines on the cluster, which can differ from the ratio you request. It shows `No running VMs` if no virtual machines are running.

      6.  Click **Save**.

    - To use the CLI, run the following command to enable higher memory density and set the overcommit rate:

      ``` terminal
      $ oc patch -n openshift-cnv hco kubevirt-hyperconverged --type='json' -p='[ \
        { \
        "op": "replace", \
        "path": "/spec/virtualization/higherWorkloadDensity/memoryOvercommitPercentage", \
        "value": 150 \
        } \
      ]'
      ```

      <div class="formalpara">

      <div class="title">

      Example output

      </div>

      ``` terminal
      hyperconverged.hco.kubevirt.io/kubevirt-hyperconverged patched
      ```

      </div>

</div>

<div>

<div class="title">

Verification

</div>

- Verify the OpenShift Virtualization memory overcommitment configuration by running the following command:

  ``` terminal
  $ oc get -n openshift-cnv hco kubevirt-hyperconverged -o jsonpath='{.spec.virtualization.higherWorkloadDensity}{"\n"}'
  ```

  <div class="formalpara">

  <div class="title">

  Example output

  </div>

  ``` terminal
  {"memoryOvercommitPercentage":150}
  ```

  </div>

  The returned value must match the value you configured earlier.

</div>

# Disable memory overcommitment and remove swap

You can disable higher virtual machine (VM) workload density if you no longer need memory overcommitment, and remove the associated swap resources from your cluster.

<div>

<div class="title">

Prerequisites

</div>

- You have installed the OpenShift CLI (`oc`).

- You are logged in to the cluster with the `cluster-admin` role.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Revert the memory overcommitment configuration by running the following command:

    ``` terminal
    $ oc patch -n openshift-cnv hco kubevirt-hyperconverged \
      --type='json' \
      -p='[{"op": "remove", "path": "/spec/virtualization/higherWorkloadDensity"}]'
    ```

2.  Delete the `MachineConfig` objects that provision and configure swap by running the following commands:

    ``` terminal
    $ oc delete machineconfig 90-worker-swap
    ```

    ``` terminal
    $ oc delete machineconfig 90-worker-swap-online
    ```

3.  Wait for the worker nodes to sync with the new configuration by running the following command:

    ``` terminal
    $ oc wait mcp worker --for condition=Updated=True --timeout=-1s
    ```

</div>

<div>

<div class="title">

Verification

</div>

- Confirm that swap is no longer enabled on a node by running the following command:

  ``` terminal
  $ oc debug node/<selected_node> -- free -m
  ```

  Ensure that the `Swap:` row shows `0` or that no swap space is provisioned.

</div>

# Additional resources

- [Understanding how to evacuate pods on nodes](../../nodes/nodes/nodes-nodes-working.xml#nodes-nodes-working-evacuating_nodes-nodes-working)

- [Run automated postinstallation configuration](../../virt/post_installation_configuration/virt-platform-autopilot.xml#virt-platform-autopilot)

- [Configure Quality of Service for Pods](https://kubernetes.io/docs/tasks/configure-pod-container/quality-service-pod/)
