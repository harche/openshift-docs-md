You can migrate one or more virtual disks to a different storage class to optimize storage performance or reduce costs without stopping your virtual machine (VM) or virtual machine instance (VMI).

# About storage class migration

A persistent volume claim (PVC) requests storage with specific attributes, such as size and performance, defined by its storage class. You cannot change a PVC’s storage class after you create it.

The storage backend that provisioned the original PVC holds the VM’s data. The target storage class might use a different backend, which does not have that data until you migrate it there.

To move a VM disk to a new storage class, you create a migration plan. The migration plan creates a new PVC in the target storage class and copies the data from the original PVC to the new PVC.

# Assign storage migration permissions

Cluster administrators must grant users permission to perform storage migrations. Permissions to perform storage migrations are not part of the administrative or editing roles in the cluster by default.

- You have cluster administrator privileges.

1.  (Optional) To assign the user single namespace storage migration permissions, run the following command:

    ``` terminal
    $ kubectl create rolebinding <role_binding_name> \
        --clusterrole=migrations.kubevirt.io:storagemigrate \
        --user=<user_name> -n <namespace>
    ```

    where:

    \<role_binding_name\>
    The name to assign to this role binding instance.

    \<user_name\>
    The user to assign the storage migration permission.

    \<namespace\>
    The applicable namespace for this role binding instance.

2.  (Optional) To assign the user multiple namespace storage migration permissions, run the following command:

    ``` terminal
    $ kubectl create clusterrolebinding <role_binding_name> \
        --clusterrole=migrations.kubevirt.io:storagemigrate-multins \
        --user=<user_name>
    ```

    where:

    \<role_binding_name\>
    The name to assign to this role binding instance.

    \<user_name\>
    The user to assign the storage migration permission.

# Migrating VM disks to a different storage class by using the web console

You can migrate one or more disks attached to a virtual machine (VM) to a different storage class by using the OpenShift Container Platform web console. This procedure works for both running and offline VMs. When migrating a running VM, the VM operation is not interrupted and the data on the migrated disks remains accessible.

1.  Navigate to **Virtualization** → **VirtualMachines** in the web console.

2.  Click the **Virtual machines** tab.

3.  Click the **Options** menu ![kebab](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABsAAAAjCAIAAADqn+bCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAA+0lEQVRIie2WMQqEMBBFJ47gUXRBLyBYqbUXULCx9CR2XsAb6AlUEM9kpckW7obdZhwWYWHXX/3i8TPJZEKEUgpOlXFu3JX4V4kmB2qaZhgGKSUiZlkWxzEBC84N9zxv27bdO47Tti0Bs3at4wBgXVca/lJnfN/XPggCGmadIwAsywIAiGhZFk1ydy2EYJKgGCqK4vZUVVU0zKpxnmftp2mi4S/1GhG1N82DMWNNYVmW4zgqpRAxTVMa5t4evlg11nXd9/1eY57nSZIQMKtG13WllLu3bbvrOgJmdUbHwfur8Xniqw6Hh5UYRdGDNowwDA+WvP4UV+JPJ94B1gKUWcTOCT0AAAAASUVORK5CYII=) beside the virtual machine and select **Migration** → **Storage**.

    You can also access this option from the **VirtualMachine details** page by selecting **Actions** → **Migration** → **Storage**.

    Alternatively, right-click the VM in the tree view and select **Migration** → **Storage** from the menu.

4.  On the **Migration details** page, perform the following actions:

    1.  Enter a migration plan name in the **VirtualMachine storage migration plan name** field or use the provided default.

    2.  Use the provided option buttons to select whether to migrate **The entire VirtualMachine** or **Selected volumes**.

    3.  (Optional) If you selected **Selected volumes** in the previous step, use the provided checkboxes to select the volumes to migrate. Volumes that cannot be migrated have a greyed out checkbox.

    4.  Click **Next**.

5.  On the **Source and target StorageClass** page, perform the following actions:

    1.  Select the storage migration target with the **Select the target storage for the VirtualMachine storage migration** dropdown list.

    2.  The system automatically decommissions the migration source volumes once the migration completes. Select the **Keep original volumes at source after successful migration** checkbox if you want to manually verify and remove the source volumes later.

    3.  Click **Next**.

6.  On the **Review** page, confirm the storage migration options.

7.  (Optional) Click **Back** to move back to previous pages to change storage migration options.

8.  Click **Migrate VirtualMachine storage** to start the migration.

9.  Stay on the **Migrate VirtualMachine storage** page to watch the progress and wait for the confirmation that the migration completed successfully.

10. (Optional) Click **View storage migrations** to view all storage migration plans.

<!-- -->

1.  From the **VirtualMachine details** page, navigate to **Configuration** → **Storage**.

2.  Verify that all disks have the expected storage class listed in the **Storage class** column.
