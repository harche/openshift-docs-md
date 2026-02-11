To update the boot loader on RHCOS nodes using `bootupd`, you must either run the `bootupctl update` command on RHCOS machines manually or provide a machine config with a `systemd` unit.

Unlike `grubby` or other boot loader tools, `bootupd` does not manage kernel space configuration such as passing kernel arguments. To configure kernel arguments, see [Adding kernel arguments to nodes](../../nodes/nodes/nodes-nodes-managing.xml#nodes-nodes-kernel-arguments_nodes-nodes-managing).

<div class="note">

You can use `bootupd` to update the boot loader to protect against the BootHole vulnerability.

</div>

# Updating the boot loader manually

You can manually inspect the status of the system and update the boot loader by using the `bootupctl` command-line tool.

1.  Inspect the system status:

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

<!-- -->

1.  OpenShift Container Platform clusters initially installed on version 4.4 and older require an explicit adoption phase.

    If the system status is `Adoptable`, perform the adoption:

    ``` terminal
    # bootupctl adopt-and-update
    ```

    <div class="formalpara-title">

    **Example output**

    </div>

    ``` terminal
    Updated: grub2-efi-x64-1:2.04-31.el8_4.1.x86_64,shim-x64-15-8.el8_1.x86_64
    ```

2.  If an update is available, apply the update so that the changes take effect on the next reboot:

    ``` terminal
    # bootupctl update
    ```

    <div class="formalpara-title">

    **Example output**

    </div>

    ``` terminal
    Updated: grub2-efi-x64-1:2.04-31.el8_4.1.x86_64,shim-x64-15-8.el8_1.x86_64
    ```

# Updating the bootloader automatically via a machine config

Another way to automatically update the boot loader with `bootupd` is to create a systemd service unit that will update the boot loader as needed on every boot. This unit will run the `bootupctl update` command during the boot process and will be installed on the nodes via a machine config.

<div class="note">

This configuration is not enabled by default as unexpected interruptions of the update operation may lead to unbootable nodes. If you enable this configuration, make sure to avoid interrupting nodes during the boot process while the bootloader update is in progress. The boot loader update operation generally completes quickly thus the risk is low.

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
      - name: bootupctl-update.service
        enabled: true
        contents: |
          [Unit]
          Description=Bootupd automatic update

          [Service]
          ExecStart=/usr/bin/bootupctl update
          RemainAfterExit=yes

          [Install]
          WantedBy=multi-user.target
    ```

    - On control plane nodes, substitute `master` for `worker` in both of these locations.

2.  Use Butane to generate a `MachineConfig` object file, `99-worker-bootupctl-update.yaml`, containing the configuration to be delivered to the nodes:

    ``` terminal
    $ butane 99-worker-bootupctl-update.bu -o 99-worker-bootupctl-update.yaml
    ```

3.  Apply the configurations in one of two ways:

    - If the cluster is not running yet, after you generate manifest files, add the `MachineConfig` object file to the `<installation_directory>/openshift` directory, and then continue to create the cluster.

    - If the cluster is already running, apply the file:

      ``` terminal
      $ oc apply -f ./99-worker-bootupctl-update.yaml
      ```
