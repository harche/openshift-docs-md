You can change the secondary network of a virtual machine (VM) without rebooting your VM. The change is transparent to the guest operating system, preserving properties such as the MAC address.

By hot swapping the secondary network, you can move a running VM to a different network segment or VLAN and apply new network policies or reconfigure network topology without interrupting the workload. OpenShift Virtualization supports hot swapping for VMs that are connected to an OVN-Kubernetes localnet and a Linux bridge secondary network.

To hot swap a VM secondary network, you must edit the network configuration of the running VM to refer to a new `NetworkAttachmentDefinition` or `ClusterUserDefinedNetwork` manifest. This action triggers a live migration, connecting the VM to the new network without a reboot.

# Hot swap limitations

OpenShift Virtualization supports hot swapping for VMs that are connected to an OVN-Kubernetes localnet and a Linux bridge secondary network.

Consider the following limitations before hot swapping a VM secondary network:

- Hot swapping only works for VMs that are live migratable.

- Network connectivity might be interrupted during the live migration process.

- If you update network references for multiple VMs, the updates might be queued because only a limited number of live migrations can run in parallel across the cluster.

- You cannot hot swap to a new network binding type or a Container Network Interface (CNI) plugin. For example, you cannot change from bridge binding to SR-IOV binding.

- The target `NetworkAttachmentDefinition` and `ClusterUserDefinedNetwork` objects must be valid and all referenced resources such as bridges, VLANs, and network resources must exist. Migration completes even if the network configuration is invalid, but the VM will lose network connectivity.

- This feature applies only to secondary networks attached by using `NetworkAttachmentDefinition` or `ClusterUserDefinedNetwork` manifests. You cannot hot swap the primary pod network, regardless of whether it uses the default cluster network or a custom primary user-defined network.

- If the new network requires a different IP configuration, such as a different subnet or gateway, you must reconfigure the guest operating system network settings. The hot swap does not automatically update the guest network configuration.

# Hot swapping a virtual machine secondary network by using the command line

You can hot swap a virtual machine (VM) secondary network by using the command line.

- The VM to which you want to hot swap the network is running and is live migratable.

- You have installed the OpenShift CLI (`oc`).

- The target `NetworkAttachmentDefinition` object exists in the same namespace as the VM. If you created a `ClusterUserDefinedNetwork` object, verify that the cluster user-defined network controller has created the corresponding `NetworkAttachmentDefinition` object.

  Example `NetworkAttachmentDefinition` manifest:

  ``` yaml
  apiVersion: k8s.cni.cncf.io/v1
  kind: NetworkAttachmentDefinition
  metadata:
    name: nad-with-vlan20
  spec:
    config: '{
      "cniVersion": "0.3.1",
      "name": "nad-with-vlan20",
      "type": "bridge",
      "bridge": "br2",
      "vlan": 20
    }'
  ```

1.  Use your preferred text editor to edit the `VirtualMachine` manifest, as shown in the following example:

    ``` yaml
    apiVersion: kubevirt.io/v1
    kind: VirtualMachine
    ...
      template:
        spec:
          domain:
            devices:
              interfaces:
              - bridge: {}
                name: bridge-net
          networks:
          - name: bridge-net
            multus:
              networkName: nad-with-vlan20
    #...
    ```

    - `spec.networks.name` specifies the name of the network. This must be the same as the `name` of the new network interface that you defined in the `template.spec.domain.devices.interfaces` list.

    - `spec.networks.multus.networkName` specifies the name of the target `NetworkAttachmentDefinition` object.

2.  Save your changes and exit the editor.

3.  For the new configuration to take effect, apply the changes by running the following command. If your OpenShift Container Platform cluster has live migration enabled, applying the changes triggers automatic VM live migration and connects the new network to the running VM.

    ``` terminal
    $ oc apply -f <filename>.yaml
    ```

    where:

    `<filename>`
    Specifies the name of your `VirtualMachine` manifest YAML file.

<!-- -->

1.  Verify that the VM live migration is progressing successfully by using the following command.

    ``` terminal
    $ oc get vmi vm-fedora -w -o jsonpath='{.status.conditions[?(@.type=="MigrationRequired")]}{"\n"}'
    ```

    Example output:

    ``` terminal
    {"type":"MigrationRequired","status":"True","lastProbeTime":null,"lastTransitionTime":"2024-05-27T10:15:30Z","reason":"AutoMigrationDueToLiveUpdate","message":""}
    ```

2.  Use the following command to connect to the VM console and to devices on the new network:

    ``` terminal
    $ virtctl console vm-fedora
    ```

# Hot swapping a virtual machine secondary network by using the web console

You can hot swap the secondary network of a running virtual machine (VM) by using the OpenShift Container Platform web console. Hot swapping the secondary network preserves the workload and avoids the need for a VM reboot.

- The VM is running and is live migratable.

- The target `NetworkAttachmentDefinition` object exists in the same namespace as the VM. If you created a `ClusterUserDefinedNetwork` object, verify that the cluster user-defined network controller has created the corresponding `NetworkAttachmentDefinition` object.

1.  Navigate to **Virtualization** → **VirtualMachines** in the web console.

2.  Click a running VM to view the **VirtualMachine details** page.

3.  Click the **Configuration** tab and then click the **Network interfaces** tab.

4.  Click the Options menu ![kebab](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABsAAAAjCAIAAADqn+bCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAA+0lEQVRIie2WMQqEMBBFJ47gUXRBLyBYqbUXULCx9CR2XsAb6AlUEM9kpckW7obdZhwWYWHXX/3i8TPJZEKEUgpOlXFu3JX4V4kmB2qaZhgGKSUiZlkWxzEBC84N9zxv27bdO47Tti0Bs3at4wBgXVca/lJnfN/XPggCGmadIwAsywIAiGhZFk1ydy2EYJKgGCqK4vZUVVU0zKpxnmftp2mi4S/1GhG1N82DMWNNYVmW4zgqpRAxTVMa5t4evlg11nXd9/1eY57nSZIQMKtG13WllLu3bbvrOgJmdUbHwfur8Xniqw6Hh5UYRdGDNowwDA+WvP4UV+JPJ94B1gKUWcTOCT0AAAAASUVORK5CYII=) beside the network interface that you want to modify and select **Edit**.

5.  Select the target network from the **Network** list.

6.  Click **Save**.

    The network interface row displays a **Pending** label. A warning banner indicates that the VM has pending network changes. The pending changes are applied during the next live migration or reboot.

<!-- -->

1.  On the **VirtualMachine details** page, click the **Diagnostics** tab.

2.  Check the **Status conditions** table and verify that the `MigrationRequired` condition is listed with the reason `AutoMigrationDueToLiveUpdate`.

    After the live migration completes, the `MigrationRequired` condition disappears and the **Pending** label is removed from the network interface.

# Additional resources

- [About live migration](../../virt/live_migration/virt-about-live-migration.xml#virt-about-live-migration-permissions_virt-about-live-migration)

- [Connecting a virtual machine to a secondary localnet user-defined network](../../virt/vm_networking/virt-connecting-vm-to-secondary-udn.xml#virt-connecting-vm-to-secondary-udn)

- [Creating a Linux bridge network attachment definition](../../virt/vm_networking/virt-connecting-vm-to-linux-bridge.xml#virt-connecting-vm-to-linux-bridge)

- [Creating an SR-IOV network attachment definition](../../virt/vm_networking/virt-connecting-vm-to-sriov.xml#nw-sriov-additional-network_virt-connecting-vm-to-sriov)
