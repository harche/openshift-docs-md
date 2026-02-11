You can delete a virtual machine by using the web console or the `oc` command line interface.

# Deleting a virtual machine using the web console

Deleting a virtual machine (VM) permanently removes it from the cluster.

If the VM is delete protected, the **Delete** action is disabled in the VM’s **Actions** menu.

- You have disabled the VM’s delete protection setting.

- You have stopped the VM.

1.  From the OpenShift Container Platform web console, choose your view:

    - For a virtualization-focused view, select **Administrator** → **Virtualization** → **VirtualMachines**.

    - For a general view, navigate to **Virtualization** → **VirtualMachines**.

2.  Click the **Options** menu ![kebab](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABsAAAAjCAIAAADqn+bCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAA+0lEQVRIie2WMQqEMBBFJ47gUXRBLyBYqbUXULCx9CR2XsAb6AlUEM9kpckW7obdZhwWYWHXX/3i8TPJZEKEUgpOlXFu3JX4V4kmB2qaZhgGKSUiZlkWxzEBC84N9zxv27bdO47Tti0Bs3at4wBgXVca/lJnfN/XPggCGmadIwAsywIAiGhZFk1ydy2EYJKgGCqK4vZUVVU0zKpxnmftp2mi4S/1GhG1N82DMWNNYVmW4zgqpRAxTVMa5t4evlg11nXd9/1eY57nSZIQMKtG13WllLu3bbvrOgJmdUbHwfur8Xniqw6Hh5UYRdGDNowwDA+WvP4UV+JPJ94B1gKUWcTOCT0AAAAASUVORK5CYII=) beside a VM and select **Delete**.

    Alternatively, click the VM’s name to open the **VirtualMachine details** page and click **Actions** → **Delete**.

    You can also right-click the VM in the tree view and select **Delete** from the pop-up menu.

3.  Optional: Select **With grace period** or clear **Delete disks**.

4.  Click **Delete** to permanently delete the VM.

# Deleting a virtual machine by using the CLI

You can delete a virtual machine (VM) by using the `oc` command-line interface (CLI). The `oc` client enables you to perform actions on multiple VMs.

- You have disabled the VM’s delete protection setting.

- You have stopped the VM.

- You have installed the OpenShift CLI (`oc`).

<!-- -->

- Delete the VM by running the following command:

  ``` terminal
  $ oc delete vm <vm_name>
  ```

  <div class="note">

  This command only deletes a VM in the current project. Specify the `-n <project_name>` option if the VM you want to delete is in a different project or namespace.

  </div>
