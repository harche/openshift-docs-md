You can increase the number of virtual machines (VMs) on nodes by overcommitting memory (RAM). This is useful when you have many similar or underused workloads.

<div class="note">

Memory overcommitment can lower workload performance on a highly utilized system.

</div>

# Enabling higher VM workload density

You can increase the number of virtual machines (VMs) on nodes by overcommitting memory and using swap resources. When you enable memory overcommitment, the `virt-platform-autopilot` controller automatically deploys the necessary node-level configurations.

If swap storage is not provisioned, the configurations deployed by `virt-platform-autopilot` have no effect.

<div class="important">

Swap resources can only be assigned to virtual machine workloads (VM pods) of the `Burstable` Quality of Service (QoS) class. VM pods of the `Guaranteed` QoS class and pods of any QoS class that do not belong to VMs cannot use swap resources.

For descriptions of QoS classes, see [Configure Quality of Service for Pods](https://kubernetes.io/docs/tasks/configure-pod-container/quality-service-pod/) (Kubernetes documentation).

Using `spec.domain.resources.requests.memory` in the VM manifest disables the memory overcommit configuration. Use `spec.domain.memory.guest` instead.

</div>

- You have installed the OpenShift CLI (`oc`).

- You are logged in to the cluster with the `cluster-admin` role.

- A memory overcommit ratio is defined.

- The node belongs to a worker pool.

1.  Provision swap by creating a `MachineConfig` object:

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
                    ConditionPathExists=!/var/tmp/ocpswap.file

                    [Service]
                    Type=oneshot
                    Environment=SWAP_SIZE_MB=5000
                    ExecStart=/bin/sh -c "sudo fallocate -l ${SWAP_SIZE_MB}M /var/tmp/ocpswap.file && \
                    sudo chmod 600 /var/tmp/ocpswap.file && \
                    sudo mkswap /var/tmp/ocpswap.file && \
                    sudo swapon /var/tmp/ocpswap.file && \
                    free -h"

                    [Install]
                    RequiredBy=kubelet-dependencies.target
                  enabled: true
                  name: swap-provision.service
        ```

        Set the `SWAP_SIZE_MB` value to the amount of swap space to provision on the node, in MB. Adjust this value by using the formula that follows.

        Ensure that the provisioned swap space is at least equal to the overcommitted RAM. Calculate the amount of swap space to provision on a node by using the following formula:

            NODE_SWAP_SPACE = NODE_RAM * (MEMORY_OVER_COMMIT_PERCENT / 100% - 1)

        Example:

            NODE_SWAP_SPACE = 16 GB * (150% / 100% - 1)
                           = 16 GB * (1.5 - 1)
                           = 16 GB * (0.5)
                           =  8 GB

    2.  Wait for the worker nodes to sync with the new configuration by running the following command:

        ``` terminal
        $ oc wait mcp worker --for condition=Updated=True --timeout=-1s
        ```

2.  Enable memory overcommitment in OpenShift Virtualization by using the web console or the CLI.

    - Web console

      1.  In the OpenShift Container Platform web console, go to **Virtualization** → **Settings**.

      2.  Click **Cluster**.

      3.  Expand **Memory Density**.

      4.  Turn on **Configure memory density**.

      5.  Expand the **Current memory density** line.

      6.  Set the density value by moving the **Requested memory density** slider. You can increase the density from 100% up to 400% in increments of 25%.

          The **Memory density** field shows the actual and requested values.

      7.  Click **Save**.

    - CLI

      - Configure OpenShift Virtualization to enable higher memory density and set the overcommit rate:

        ``` terminal
        $ oc patch -n openshift-cnv hco kubevirt-hyperconverged --type='json' -p='[ \
          { \
          "op": "replace", \
          "path": "/spec/virtualization/higherWorkloadDensity/memoryOvercommitPercentage", \
          "value": 150 \
          } \
        ]'
        ```

        <div class="formalpara-title">

        **Example output**

        </div>

        ``` terminal
        hyperconverged.hco.kubevirt.io/kubevirt-hyperconverged patched
        ```

3.  The `virt-platform-autopilot` controller deploys the `90-worker-swap-online` machine config, which triggers a worker machine config pool upgrade. Wait for the upgrade to complete by running the following command:

    ``` terminal
    $ oc wait mcp worker --for condition=Updated=True --timeout=-1s
    ```

<!-- -->

1.  To verify the deployment of `90-worker-swap-online`, run the following command:

    ``` terminal
    $ oc get mc 90-worker-swap-online
    ```

    <div class="formalpara-title">

    **Example output**

    </div>

    ``` terminal
    NAME             GENERATEDBYCONTROLLER   IGNITIONVERSION   AGE
    90-worker-swap-online                           3.5.0             1m
    ```

2.  To verify that swap is correctly provisioned, complete the following steps:

    1.  View a list of worker nodes by running the following command:

        ``` terminal
        $ oc get nodes -l node-role.kubernetes.io/worker
        ```

    2.  Select a node from the list and display its memory usage by running the following command:

        ``` terminal
        $ oc debug node/<selected_node> -- free -m
        ```

        Replace `<selected_node>` with the node name.

        If swap is provisioned, an amount greater than zero is displayed in the `Swap:` row.

        <div class="formalpara-title">

        **Example output**

        </div>

        ``` terminal
                       total        used        free      shared  buff/cache   available
        Mem:           31846       23155        1044        6014       14483        8690
        Swap:           8191        2337        5854
        ```

3.  Verify the OpenShift Virtualization memory overcommitment configuration by running the following command:

    ``` terminal
    $ oc get -n openshift-cnv hco kubevirt-hyperconverged -o jsonpath='{.spec.virtualization.higherWorkloadDensity}{"\n"}'
    ```

    <div class="formalpara-title">

    **Example output**

    </div>

    ``` terminal
    {"memoryOvercommitPercentage":150}
    ```

    The returned value must match the value you configured earlier.

# Disabling higher VM workload density

If you no longer need memory overcommitment, you can disable higher VM workload density and remove the associated swap resources from your cluster.

- You have installed the OpenShift CLI (`oc`).

- You are logged in to the cluster with the `cluster-admin` role.

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

- Confirm that swap is no longer enabled on a node by running the following command:

  ``` terminal
  $ oc debug node/<selected_node> -- free -m
  ```

  Ensure that the `Swap:` row shows `0` or that no swap space is provisioned.
