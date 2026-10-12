Labels and annotations are metadata administrators attach to virtual machines. Labels identify and group virtual machines for use by system processes. Annotations are descriptive information intended for administrators and software integrations.

# Creating cluster auto-applied labels

Create labels that are automatically applied to every virtual machine created in a cluster. Labels allow administrators to group and filter virtual machines.

<div class="important">

New labels are only applied to virtual machines created after the label is created.

</div>

- You have access to the OpenShift Container Platform web console.

- You have `edit` or `admin` permissions in the target project.

1.  Click **Virtualization** → **Settings** on the side menu to access the cluster settings.

2.  Click the **Cluster** tab.

3.  Click **Auto-applied VM labels**.

4.  Click **Add new key**.

5.  Enter the label name in the **Key** field.

6.  Click the checkmark icon to save the new label.

    <div class="note">

    Click the trash can icon to discard the change if needed.

    </div>

7.  Optional: Enter a default value in the **Value** field.

    1.  Click the pencil icon.

    2.  Enter a value in the **Value** field.

    3.  Click the checkmark icon to save the new value.

8.  Optional: Select the **Required** slider to make a value for this label mandatory for all cluster VMs.

# Editing user auto-applied labels

Edit labels that are automatically applied to every virtual machine created by a specific user in a cluster. Labels allow administrators to group and filter virtual machines.

- You have access to the OpenShift Container Platform web console.

- You have `edit` or `admin` permissions in the target project.

1.  Click **Virtualization** → **Settings** on the side menu to access the cluster settings.

2.  Click the **User** tab.

3.  Click **Default VM labels**.

4.  Optional: Enter a default value in the **Value** field.

    1.  Click the pencil icon.

    2.  Enter a value in the **Value** field.

    3.  Click the checkmark icon to save the new value.

# Applying VM labels

Apply labels to a virtual machine in a cluster. Some labels are automatically applied and others are applied on a per-virtual machine basis. Labels allow administrators to group and filter virtual machines.

<div class="important">

New labels are only applied to virtual machines created after the label is created.

</div>

- You have access to the OpenShift Container Platform web console.

- You have `edit` or `admin` permissions in the target project.

1.  Click **Virtualization** → **VirtualMachines** on the side menu to access the cluster settings.

2.  Select a virtual machine using the **Local cluster** tree view or **Virtual machines** tab.

3.  Click the **Configuration** tab.

4.  Click **Labels and annotations**.

5.  Click **Add Labels**.

6.  Optional: Edit existing labels using the **Key** and **Value** fields.

7.  Optional: Add a new label.

    1.  Click **Add label**.

    2.  Use the **Key** and **Value** fields to add the new label values.

    3.  Click **Save**.

8.  Optional: Delete a label using the minus icon to the right of the **Value** field.

# Applying VM annotations

Apply annotations to a virtual machine in a cluster to attach descriptive information.

- You have access to the OpenShift Container Platform web console.

- You have `edit` or `admin` permissions in the target project.

1.  Click **Virtualization** → **VirtualMachines** on the side menu to access the cluster settings.

2.  Select a virtual machine using the **Local cluster** tree view or **Virtual machines** tab.

3.  Click the **Configuration** tab.

4.  Click **Labels and annotations**.

5.  Click **Add annotations**.

6.  Optional: Edit existing annotations using the **Key** and **Value** fields.

7.  Optional: Add a new annotation.

    1.  Click **Add more**.

    2.  Use the **Key** and **Value** fields to add the new label values.

    3.  Click **Save**.

8.  Optional: Delete an annotation using the minus icon to the right of the **Value** field.
