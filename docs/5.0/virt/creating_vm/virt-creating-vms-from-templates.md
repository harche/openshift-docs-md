You can create, customize, and manage the virtual machine (VM) templates that you use to create VMs. To create a VM from a template, use the web console creation wizard.

# About VM templates

VM templates define a reusable VM configuration. You can create a VM from a template to deploy a standardized VM quickly.

Speed up creation with boot sources
You can speed up VM creation by using templates that have an available boot source. A template with a boot source displays the **Available boot source** label if it does not have a custom label.

A template without a boot source displays the **Boot source required** label.

Customize before starting the VM
You can customize the disk source and VM parameters before you start the VM.

<div class="note">

If you copy a VM template with all its labels and annotations, your version of the template is marked as deprecated when a new version of the Scheduling, Scale, and Performance (SSP) Operator is deployed. You can remove this designation. See "Removing a deprecated designation from a customized VM template by using the web console".

</div>

Single-node OpenShift
Due to differences in storage behavior, some templates are incompatible with single-node OpenShift. To ensure compatibility, do not set the `evictionStrategy` field for templates or VMs that use data volumes or storage profiles.

# Creating a custom VM template in the web console

You can create a virtual machine template by editing a YAML file example in the OpenShift Container Platform web console.

1.  In the web console, click **Virtualization** → **Templates** in the side menu.

2.  Optional: Use the **Project** drop-down menu to change the project associated with the new template. All templates are saved to the `openshift` project by default.

3.  Click **Create Template**.

4.  Specify the template parameters by editing the YAML file.

5.  Click **Create**.

    The template is displayed on the **Templates** page.

6.  Optional: Click **Download** to download and save the YAML file.

# Enabling dedicated resources for a virtual machine template

You can enable dedicated resources for a virtual machine (VM) template in the OpenShift Container Platform web console. VMs that are created from this template will be scheduled with dedicated resources.

1.  In the OpenShift Container Platform web console, click **Virtualization** → **Templates** in the side menu.

2.  Select the template that you want to edit to open the **Template details** page.

3.  On the **Scheduling** tab, click the edit icon beside **Dedicated Resources**.

4.  Select **Schedule this workload with dedicated resources (guaranteed policy)**.

5.  Click **Save**.

# Virtual machine template categories

You can assign a category to a virtual machine (VM) template to classify it by application type. Categories help you organize a growing template catalog and make it easier for VM consumers to find the right template.

Categories have the following characteristics:

- A template can have only one category.

- Category is optional. Templates without a category display a blank **Category** field.

- You can select a predefined category or create a custom category. The following predefined categories are available:

  - Databases

  - Operating-systems

  - Monitoring

  - Networking

  - Observability

  - Security

  - Storage

- The cluster stores categories as the `vm.kubevirt.io/category` label on the `VirtualMachineTemplate` object.

- The system normalizes custom category names to Kubernetes label-safe values. For example, it converts spaces to hyphens.

## Category support by template type

OpenShift Virtualization supports three template types. Category support varies by type:

`VirtualMachineTemplate` (`v1beta1`)
Full category support. You can set a category when saving a VM as a template and edit the category after creation. The **Category** column on the **Templates** list page displays the assigned application category.

`VirtualMachineTemplate` (`v1alpha1`)
Partial category support. You can edit the category after the template is created, but you cannot set a category during template creation. The `v1alpha1` `VirtualMachineTemplateRequest` custom resource definition (CRD) does not support propagating labels to the created template. The **Category** column displays the assigned application category.

OpenShift template
Does not support categories. OpenShift Container Platform templates use the workload profile instead. The **Category** column displays the workload profile, such as `desktop` or `server`.

## Edit a VM template category

You can edit the category of a `VirtualMachineTemplate` object by using the OpenShift Container Platform web console for either `v1alpha1` or `v1beta1` objects. Using the web console is the only way to assign a category to a `v1alpha1` `VirtualMachineTemplate` object.

- You have access to the OpenShift Container Platform web console.

- You have `edit` or `admin` permissions on the template.

1.  In the OpenShift Container Platform web console, navigate to **Virtualization** → **Templates**.

2.  Click the name of the **VirtualMachineTemplate** that you want to edit.

3.  On the template details page, click the **Actions** menu and select **Edit category**.

    <div class="note">

    You can also click the edit icon next to the **Category** field in the details grid.

    </div>

4.  Select a category from the list, or type a custom category name.

5.  Click **Save**.

- On the template details page, verify that the **Category** field displays the updated category.

- Navigate to **Virtualization** → **Templates** and verify that the **Category** column displays the updated category for the template.

## Remove a category from a VM template

You can remove the category from a `VirtualMachineTemplate` object by using the OpenShift Container Platform web console.

- You have access to the OpenShift Container Platform web console.

- You have `edit` or `admin` permissions on the template.

1.  In the OpenShift Container Platform web console, navigate to **Virtualization** → **Templates**.

2.  Click the name of the **VirtualMachineTemplate** that you want to edit.

3.  On the template details page, click the edit icon next to the **Category** field.

4.  In the **Edit category** dialog, click the clear icon (x) in the **Category** field to remove the current category.

    The **Category** field displays the **Select or create new** placeholder text.

5.  Click **Save**.

- On the template details page, verify that the **Category** field displays **None**.

## Filter VM templates by category

You can filter virtual machine (VM) templates by category to quickly find templates that match a specific application type. You can filter by category from the **Templates** list page or the Create VM wizard catalog.

- You have access to the OpenShift Container Platform web console.

- One or more templates have categories assigned.

1.  In the OpenShift Container Platform web console, navigate to one of the following locations:

    - **Virtualization** → **Templates** to filter from the **Templates** list page.

    - **Virtualization** → **VirtualMachines** → **Create** → **Create from Template** to filter from the Create VM wizard catalog.

2.  In the filter toolbar, select the **Category** filter.

3.  Select one or more categories to narrow the template list.

- Verify that only templates matching the selected categories are displayed.

## Set a category when saving a VM as a template

You can optionally set a category when saving a virtual machine (VM) as a `v1beta1` `VirtualMachineTemplate`. The category is stored as the `vm.kubevirt.io/category` label on the new template.

<div class="note">

Setting a category during template creation is supported only for `v1beta1` `VirtualMachineTemplate` objects. For `v1alpha1` `VirtualMachineTemplate` objects, you must edit the category after the template is created.

</div>

- You have access to the OpenShift Container Platform web console.

- You have `edit` or `admin` permissions in the project.

- You have a running or stopped VM.

1.  In the OpenShift Container Platform web console, navigate to **Virtualization** → **VirtualMachines**.

2.  Click the name of the VM that you want to save as a template.

3.  Click **Actions** → **Save as template**.

4.  In the template creation dialog, configure the template details.

5.  Optional: In the **Category** field, select a category from the list or type a custom category name.

6.  Click **Save**.

- Navigate to **Virtualization** → **Templates** and verify that the new template is displayed with the assigned category in the **Category** column.

## VM template category column

The **Category** column on the **Virtualization** → **Templates** list page displays different information depending on the template type.

| Template type                         | Category support               | Category column value                                                                                  |
|---------------------------------------|--------------------------------|--------------------------------------------------------------------------------------------------------|
| `VirtualMachineTemplate` (`v1beta1`)  | Full (set on creation or edit) | Shows the assigned category, such as **Database** or **Web Server**. Blank if no category is assigned. |
| `VirtualMachineTemplate` (`v1alpha1`) | Edit only (after creation)     | Shows the assigned category. Blank if no category is assigned.                                         |
| OpenShift template                    | Not supported                  | Shows the workload profile, such as **desktop** or **server**.                                         |

Category column behavior

The cluster stores categories as the `vm.kubevirt.io/category` label on `VirtualMachineTemplate` objects. The system normalizes category values to Kubernetes label-safe strings. For example, "Operating systems" becomes `operating-systems`.

# Removing a deprecated designation from a customized VM template by using the web console

You can customize an existing virtual machine (VM) template before you start the VM, by modifying the VM or template parameters, such as data sources, cloud-init, or SSH keys.

<div class="note">

If you customize a template by copying it and including all of its labels and annotations, the customized template is marked as deprecated when a new version of the Scheduling, Scale, and Performance (SSP) Operator is deployed. You can remove the deprecated designation from the customized template.

</div>

1.  Navigate to **Virtualization** → **Templates** in the web console.

2.  From the list of VM templates, click the template marked as deprecated.

3.  Click **Edit** next to the pencil icon beside **Labels**.

4.  Remove the following two labels:

    - `template.kubevirt.io/type: "base"`

    - `template.kubevirt.io/version: "version"`

5.  Click **Save**.

6.  Click the pencil icon beside the number of existing **Annotations**.

7.  Remove the following annotation:

    - `template.kubevirt.io/deprecated`

8.  Click **Save**.

# Additional resources

- [Create virtual machines by using the web console](../../virt/creating_vm/virt-creating-vms-web.xml#virt-creating-vm-from-template-web_virt-creating-vms-web)

- [Managing automatic boot source updates](../../virt/storage/virt-automatic-bootsource-updates.xml#virt-automatic-bootsource-updates)
