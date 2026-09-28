To optimize performance or reduce costs, you can migrate virtual machines (VMs) between storage classes within a single cluster. You can use the OpenShift Container Platform web console to migrate a single VM’s disks or perform these migrations in bulk. Storage migration can be performed on both online and offline VMs.

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

# Migrating VMs in a single cluster to a different storage class by using the web console

You can migrate the disks attached to single cluster virtual machines (VMs) from one storage class to a different storage class by using the OpenShift Container Platform web console. This procedure works for both running and offline VMs. When performing this action on a running VM, the operation of the VM is not interrupted and the data on the migrated disks remains accessible.

1.  Navigate to **Virtualization** → **VirtualMachines** in the web console.

2.  Click the **Virtual machines** tab.

3.  Select multiple VMs using the checkboxes to the left of the **Name** field. Alternatively, use the multi-select checkbox under the **Project** dropdown list to deselect the currently selected VMs (**Select none**), select all VMs on the currently displayed page (**Select page**), or select all VMs in the cluster (**Select all**).

4.  Click the **Actions** menu and select **Migration** → **Storage**.

5.  On the **Migration details** page, perform the following actions:

    1.  Enter a migration plan name in the **VirtualMachine storage migration plan name** field or use the provided default.

    2.  Use the provided option buttons to select whether to migrate **The entire VirtualMachine** or **Selected volumes**.

        <div class="note">

        If you select **The entire VirtualMachine**, all disks on all selected VMs are migrated to the same target storage.

        </div>

    3.  (Optional) If you selected **Selected volumes** in the previous step, use the provided checkboxes to select the volumes to migrate. Volumes that cannot be migrated have a greyed out checkbox.

    4.  Click **Next**.

6.  On the **Source and target StorageClass** page, perform the following actions:

    1.  Select the storage migration target with the **Select the target storage for the VirtualMachine storage migration** dropdown list.

    2.  The system automatically decommissions the migration source volumes once the migration completes. Select the **Keep original volumes at source after successful migration** checkbox if you want to manually verify and remove the source volumes later.

    3.  Click **Next**.

7.  On the **Review** page, confirm the storage migration options.

8.  (Optional) Click **Back** to move back to previous pages to change storage migration options.

9.  Click **Migrate VirtualMachine storage** to start the migration.

10. Stay on the **Migrate VirtualMachine storage** page to watch the progress and wait for the confirmation that the migration completed successfully.

11. (Optional) Click **View storage migrations** to view all storage migration plans.

<!-- -->

1.  From the **VirtualMachine details** page for each VM, navigate to **Configuration** → **Storage**.

2.  Verify that all disks have the expected storage class listed in the **Storage class** column.

# Canceling a storage migration by using the web console

You can cancel a storage migration by deleting the associated storage migration plan by using the OpenShift Container Platform web console.

1.  Navigate to **Virtualization** → **Migration** → **Storage migrations** in the web console.

2.  (Optional) Use the **Filter** dropdown to filter the migration plan list by **Running** or **Pending** plans.

3.  (Optional) Perform the following tasks to search the migration plan list:

    1.  Select either **Name** or **Label** from the search type dropdown list.

    2.  Enter the search text in the search textbox. The migration plan list filters as the search criteria entered.

4.  Click the **Options** menu ![kebab](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABsAAAAjCAIAAADqn+bCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAA+0lEQVRIie2WMQqEMBBFJ47gUXRBLyBYqbUXULCx9CR2XsAb6AlUEM9kpckW7obdZhwWYWHXX/3i8TPJZEKEUgpOlXFu3JX4V4kmB2qaZhgGKSUiZlkWxzEBC84N9zxv27bdO47Tti0Bs3at4wBgXVca/lJnfN/XPggCGmadIwAsywIAiGhZFk1ydy2EYJKgGCqK4vZUVVU0zKpxnmftp2mi4S/1GhG1N82DMWNNYVmW4zgqpRAxTVMa5t4evlg11nXd9/1eY57nSZIQMKtG13WllLu3bbvrOgJmdUbHwfur8Xniqw6Hh5UYRdGDNowwDA+WvP4UV+JPJ94B1gKUWcTOCT0AAAAASUVORK5CYII=) beside the migration plan.

5.  Click **Delete MultiNamespaceVirtualMachineStorageMigrationPlan**.

6.  Click **Delete**.

# Deleting storage migration plans by using the web console

You can delete old or unwanted storage migration plans by using the OpenShift Container Platform web console.

1.  Navigate to **Virtualization** → **Migration** → **Storage migrations** in the web console.

2.  (Optional) Use the **Filter** dropdown to filter the migration plan list by **Running**, **Pending**, **Failed**, and **Completed** plans.

3.  (Optional) Perform the following tasks to search the migration plan list:

    1.  Select either **Name** or **Label** from the search type dropdown list.

    2.  Enter the search text in the search textbox. The migration plan list filters as the search criteria entered.

4.  Click the **Options** menu ![kebab](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABsAAAAjCAIAAADqn+bCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAA+0lEQVRIie2WMQqEMBBFJ47gUXRBLyBYqbUXULCx9CR2XsAb6AlUEM9kpckW7obdZhwWYWHXX/3i8TPJZEKEUgpOlXFu3JX4V4kmB2qaZhgGKSUiZlkWxzEBC84N9zxv27bdO47Tti0Bs3at4wBgXVca/lJnfN/XPggCGmadIwAsywIAiGhZFk1ydy2EYJKgGCqK4vZUVVU0zKpxnmftp2mi4S/1GhG1N82DMWNNYVmW4zgqpRAxTVMa5t4evlg11nXd9/1eY57nSZIQMKtG13WllLu3bbvrOgJmdUbHwfur8Xniqw6Hh5UYRdGDNowwDA+WvP4UV+JPJ94B1gKUWcTOCT0AAAAASUVORK5CYII=) beside the migration plan.

5.  Click **Delete MultiNamespaceVirtualMachineStorageMigrationPlan**.

6.  Click **Delete**.

# Deleting persistent volume claims by using the web console

You can delete old or unwanted persistent volume claims (PVC) by using the OpenShift Container Platform web console.

If you chose to keep the original source volumes during a storage migration, follow this procedure to delete them when you no longer want to retain them.

1.  Navigate to **Virtualization** → **Storage** → **PersistentVolumeClaims** in the web console.

2.  (Optional) Perform the following tasks to filter the persistent volume claim list:

    1.  Use the **Filter** dropdown to filter the persistent volume claim list by **Status**, **Name**, or **Label**.

    2.  (Optional) If **Status** is selected, select **Pending**, **Bound**, or **Lost** from the **Filter by status** dropdown.

    3.  (Optional) If **Name** or **Label** is selected, enter the search criteria in the **Filter by name** or **Filter by label** textbox. The list filters as the search criteria is entered.

3.  Click the **Options** menu ![kebab](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABsAAAAjCAIAAADqn+bCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAA+0lEQVRIie2WMQqEMBBFJ47gUXRBLyBYqbUXULCx9CR2XsAb6AlUEM9kpckW7obdZhwWYWHXX/3i8TPJZEKEUgpOlXFu3JX4V4kmB2qaZhgGKSUiZlkWxzEBC84N9zxv27bdO47Tti0Bs3at4wBgXVca/lJnfN/XPggCGmadIwAsywIAiGhZFk1ydy2EYJKgGCqK4vZUVVU0zKpxnmftp2mi4S/1GhG1N82DMWNNYVmW4zgqpRAxTVMa5t4evlg11nXd9/1eY57nSZIQMKtG13WllLu3bbvrOgJmdUbHwfur8Xniqw6Hh5UYRdGDNowwDA+WvP4UV+JPJ94B1gKUWcTOCT0AAAAASUVORK5CYII=) beside the persistent volume claim.

4.  Click **Delete PersistentVolumeClaim**.

5.  Click **Delete**.
