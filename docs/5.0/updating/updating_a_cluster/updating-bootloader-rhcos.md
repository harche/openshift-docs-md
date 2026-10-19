To update the boot loader on RHCOS nodes using `bootupd`, you must either run the `bootupctl update` command on RHCOS machines manually or provide a machine config with a `systemd` unit.

Unlike `grubby` or other boot loader tools, `bootupd` does not manage kernel space configuration such as passing kernel arguments. To configure kernel arguments, see [Add kernel arguments to nodes](../../nodes/nodes/nodes-nodes-managing.xml#nodes-nodes-kernel-arguments_nodes-nodes-managing).

For example, you can use `bootupd` to update the boot loader to protect against the BootHole vulnerability.

<div class="note">

On clusters that use the `x86_64` or ARM CPU architecture, RHCOS automatically updates the boot loader when a node gets upgraded to a new operating system image. For UEFI systems, the `bootloader-update.service` updates the boot loader inside the EFI System Partition. For Legacy BIOS systems, the `bootloader-update.service` writes the boot loader directly to the boot sectors. With these clusters, there is no need to manually update the boot loader.

On the `ppc64le` architecture, `bootupd` support exists, but RAID setups are not currently supported. On the `s390x` architecture, `bootupd` has no boot loader to update.

</div>

# Updating the boot loader manually

You can manually inspect the status of the system and update the boot loader by using the `bootupctl` command-line tool.

1.  Inspect the system status by running the following command:

    ``` terminal
    # bootupctl status
    ```

    <div class="formalpara-title">

    **Example output for `x86_64`**

    </div>

    ``` terminal
    Component EFI
      Installed: grub2-efi-x64-1:2.04-31.el8_4.1.x86_64,shim-x64-15-8.el8_1.x86_64
      Update: At latest version
    ```

    <div class="formalpara-title">

    **Example output for `aarch64`**

    </div>

    ``` terminal
    Component EFI
      Installed: grub2-efi-aa64-1:2.02-99.el8_4.1.aarch64,shim-aa64-15.4-2.el8_1.aarch64
      Update: At latest version
    ```

2.  OpenShift Container Platform clusters initially installed on version 4.4 and older require an explicit adoption phase.

    If the system status is `Adoptable`, perform the adoption by running the following command:

    ``` terminal
    # bootupctl adopt-and-update
    ```

    <div class="formalpara-title">

    **Example output**

    </div>

    ``` terminal
    Updated: grub2-efi-x64-1:2.04-31.el8_4.1.x86_64,shim-x64-15-8.el8_1.x86_64
    ```

3.  If an update is available, apply the update so that the changes take effect on the next reboot by running the following command:

    ``` terminal
    # bootupctl update
    ```

    <div class="formalpara-title">

    **Example output**

    </div>

    ``` terminal
    Updated: grub2-efi-x64-1:2.04-31.el8_4.1.x86_64,shim-x64-15-8.el8_1.x86_64
    ```

# Updating the boot loader automatically by using a machine config

You can automatically update the boot loader with `bootupd` by creating a systemd service unit that will update the boot loader as needed on every boot. This unit will run the `bootupctl update` command during the boot process and will be installed on the nodes via a machine config.

<div class="note">

This configuration is not enabled by default because unexpected interruptions of the update operation might lead to unbootable nodes. If you enable this configuration, make sure to avoid interrupting nodes during the boot process while the boot loader update is in progress. The boot loader update operation generally completes quickly thus the risk is low.

</div>

1.  Create a Butane config file, `99-worker-bootupctl-update.bu`, including the contents of the `bootupctl-update.service` systemd unit.

    <div class="note">

    The [Butane version](https://coreos.github.io/butane/specs/) you specify in the config file should match the OpenShift Container Platform version and always ends in `0`. For example, `4.17.0`. See "Creating machine configs with Butane" for information about Butane.

    </div>

    <div class="formalpara-title">

    **Example output**

    </div>

    ``` yaml
    variant: openshift
    version: 4.17.0
    metadata:
      name: 99-worker-chrony
      labels:
        machineconfiguration.openshift.io/role: worker
    systemd:
      units:
      - name: bootloader-update.service
        enabled: true
    ```

    On control plane nodes, substitute `master` for `worker` in `metadata.name` and `metadata.labels.machineconfiguration.openshift.io/role`.

2.  Generate a `MachineConfig` object file, `99-worker-bootupctl-update.yaml`, containing the configuration to be delivered to the nodes by running the following command:

    ``` terminal
    $ butane 99-worker-bootupctl-update.bu -o 99-worker-bootupctl-update.yaml
    ```

3.  Apply the configurations in one of two ways:

    - If the cluster is not running yet, after you generate manifest files, add the `MachineConfig` object file to the `<installation_directory>/openshift` directory, and then continue to create the cluster.

    - If the cluster is already running, apply the file by running the following command:

      ``` terminal
      $ oc apply -f ./99-worker-bootupctl-update.yaml
      ```

<!-- -->

1.  Check that the `99-worker-chrony` machine config object was created by running the following command:

    ``` terminal
    $ oc describe mc 99-worker-chrony
    ```

    <div class="formalpara-title">

    **Expected output**

    </div>

    ``` yaml
    Name:         99-worker-chrony
    Namespace:
    Labels:       machineconfiguration.openshift.io/role=worker
    Annotations:  <none>
    API Version:  machineconfiguration.openshift.io/v1
    Kind:         MachineConfig
    Metadata:
      Creation Timestamp:  2026-10-01T19:09:36Z
      Generation:          1
      Resource Version:    54580
      UID:                 cde98e8e-9b9c-4b9c-bad9-5608fbe8af74
    Spec:
      Config:
        Ignition:
          Version:  3.5.0
        Systemd:
          Units:
            Enabled:  true
            Name:     bootloader-update.service
    Events:           <none>
    ```

    - Check that the `bootloader-update.service` systemd unit is enabled on the nodes in the machine config pool specified in the machine config object:

      1.  Log in to a node:

          ``` terminal
          $ oc debug node/<node_name>
          ```

      2.  Set `/host` as the root directory within the debug shell:

          ``` terminal
          sh-5.1# chroot /host
          ```

      3.  Verify that the unit is enabled by running the following command:

              $ sh-5.2# systemctl is-enabled bootloader-update.service

          <div class="formalpara-title">

          **Expected output**

          </div>

          ``` terminal
          enabled
          ```
