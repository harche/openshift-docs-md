Use the web console or OpenShift CLI (`oc`) to list your virtual machines (VMs). From the list, you can filter and search for specific VMs.

# List virtual machines by using the CLI

You can either list all of the virtual machines (VMs) in your cluster or limit the list to VMs in a specified namespace by using the OpenShift CLI (`oc`).

- You have installed the OpenShift CLI (`oc`).

<!-- -->

- List all of the VMs in your cluster by running the following command:

  ``` terminal
  $ oc get vms -A
  ```

- List all of the VMs in a specific namespace by running the following command:

  ``` terminal
  $ oc get vms -n <namespace>
  ```

# List virtual machines by using the web console

You can list all the virtual machines (VMs) in your cluster by using the web console.

1.  Click **Virtualization** → **VirtualMachines** from the side menu to access the tree view of all projects and VMs in your cluster.

2.  Optional: Enable the **Show only projects with VirtualMachines** option above the tree view to limit the displayed projects.

3.  Select a project or cluster in the tree view to automatically filter the VM list to that selection.

4.  Click the **Virtual machines** tab.

# Searching for virtual machines by using the web console

You can search for virtual machines (VMs) by using the search bar on the **VirtualMachines** page and applying various filters.

1.  In the OpenShift Container Platform console, click **Virtualization** → **VirtualMachines** from the side menu. Open the **Virtual machines** tab.

2.  Select search filters in one of the following ways:

    - Put the cursor in the search bar at the top of the page and select the required key from the **Search by** dropdown menu. The name of the filter appears in the search bar, and a drop-down menu displays all possible values for the selected filter.

    - Start typing the name of the required filter in the search bar, for example, Name, Project, Status. The autocomplete function displays suggestions for the whole filter name.

    - Select one of the filters that appear under the search bar and the filter’s value from a dropdown menu that opens. The name of the filter with its value appears in the search bar. To display additional filter options, click **Show more filters**.

    - Click the **Advanced search** icon on the right side of the search bar and select the required filter from the **Advanced search** dialog box.

      The following filters are available for advanced search:

      <table>
      <colgroup>
      <col style="width: 50%" />
      <col style="width: 50%" />
      </colgroup>
      <thead>
      <tr class="header">
      <th style="text-align: left;">Filter</th>
      <th style="text-align: left;">Description</th>
      </tr>
      </thead>
      <tbody>
      <tr class="odd">
      <td style="text-align: left;"><p>Name</p></td>
      <td style="text-align: left;"><p>The virtual machine name.</p></td>
      </tr>
      <tr class="even">
      <td style="text-align: left;"><p>Project</p></td>
      <td style="text-align: left;"><p>A project that is part of your deployment.</p></td>
      </tr>
      <tr class="odd">
      <td style="text-align: left;"><p>Group</p></td>
      <td style="text-align: left;"><p>The group to which the VM belongs.</p>
      <p>Groups are a preview feature. To use this filter, you need to enable this feature in <strong>Virtualization</strong> → <strong>Settings</strong> → <strong>Preview features</strong>.</p></td>
      </tr>
      <tr class="even">
      <td style="text-align: left;"><p>Description</p></td>
      <td style="text-align: left;"><p>Text in the description of the virtual machine.</p></td>
      </tr>
      <tr class="odd">
      <td style="text-align: left;"><p>Status</p></td>
      <td style="text-align: left;"><p>The status of the virtual machine.</p></td>
      </tr>
      <tr class="even">
      <td style="text-align: left;"><p>Operating system</p></td>
      <td style="text-align: left;"><p>The operating system of the virtual machine.</p></td>
      </tr>
      <tr class="odd">
      <td style="text-align: left;"><p>vCPU</p></td>
      <td style="text-align: left;"><p>The number of vCPUs allotted to the virtual machine. Select a modifying expression and enter a value to search on.</p></td>
      </tr>
      <tr class="even">
      <td style="text-align: left;"><p>Memory</p></td>
      <td style="text-align: left;"><p>The amount of memory allotted to the virtual machine. Select a modifying expression, enter a value to search on, and select the unit of measurement.</p></td>
      </tr>
      <tr class="odd">
      <td style="text-align: left;"><p>Storage class</p></td>
      <td style="text-align: left;"><p>The storage class the virtual machine uses.</p></td>
      </tr>
      <tr class="even">
      <td style="text-align: left;"><p>Hardware devices</p></td>
      <td style="text-align: left;"><p>The type of hardware device associated with the virtual machine.</p></td>
      </tr>
      <tr class="odd">
      <td style="text-align: left;"><p>Date created</p></td>
      <td style="text-align: left;"><p>The date range the virtual machine was created in.</p></td>
      </tr>
      <tr class="even">
      <td style="text-align: left;"><p>Labels</p></td>
      <td style="text-align: left;"><p>The labels associated with the virtual machine.</p></td>
      </tr>
      <tr class="odd">
      <td style="text-align: left;"><p>Scheduling</p></td>
      <td style="text-align: left;"><p>The scheduling logic associated with the virtual machine.</p></td>
      </tr>
      <tr class="even">
      <td style="text-align: left;"><p>Guest agent</p></td>
      <td style="text-align: left;"><p>The status of the Quick Emulator (QEMU) Guest Agent daemon. The possible values are <strong>Reporting</strong> (communicating) and <strong>Not reporting</strong> (not installed, not running, or has lost its connection). This filter applies only to running VMs.</p></td>
      </tr>
      <tr class="odd">
      <td style="text-align: left;"><p>Nodes</p></td>
      <td style="text-align: left;"><p>The nodes associated with the virtual machine.</p></td>
      </tr>
      <tr class="even">
      <td style="text-align: left;"><p>IP address</p></td>
      <td style="text-align: left;"><p>The IP address of the virtual machine.</p></td>
      </tr>
      <tr class="odd">
      <td style="text-align: left;"><p>Network Attachment Definitions</p></td>
      <td style="text-align: left;"><p>Select the appropriate definition.</p></td>
      </tr>
      </tbody>
      </table>

3.  Select the required value for the selected filter from a drop-down menu or start typing it.

    The page displays a list of all VMs that satisfy the search parameters.

4.  You can apply multiple filters and multiple values for each filter:

    - To apply multiple values for a filter, select the values from a menu or type them separated with commas. A search with a filter with multiple values brings VMs that satisfy any of the values.

    - To apply multiple filters, type their names with values and separate the filters with spaces. A search with multiple filters brings VMs that satisfy all the filters.

5.  You can use any filter as an exclusion filter by typing a minus sign before the filter’s name in the search bar. For example, to exclude any running VMs from the search, type `-status:Running` in the search bar.

6.  To save a search, click the **Save search** icon on the right side of the search bar. In the **Save search** dialog box, enter the name for the search and click **Save**. You can also add the search to favorites by selecting the **Add to favorites** checkbox.

    To see the saved searches, click the **Saved searches** button.

7.  You might find it useful to see and run some search examples. To see the examples, click the **Help** icon next to the search bar. You can run any example search by selecting it from the **Search tips** dropdown menu.

# Organize virtual machines by using the web console

In addition to creating virtual machines (VMs) in different projects, you can use the tree view to further organize them in groups.

<div class="important">

Enabling groups in the virtual machine tree is a Technology Preview feature only. Technology Preview features are not supported with Red Hat production service level agreements (SLAs) and might not be functionally complete. Red Hat does not recommend using them in production. These features provide early access to upcoming product features, enabling customers to test functionality and provide feedback during the development process.

For more information about the support scope of Red Hat Technology Preview features, see [Technology Preview Features Support Scope](https://access.redhat.com/support/offerings/techpreview/).

</div>

<div class="note">

OpenShift Virtualization does not enable groups in the virtual machine tree by default. To enable groups, go to **Virtualization** → **Settings**. In the **Preview features** tab, select **Enable groups in VirtualMachines tree view**.

</div>

1.  Click **Virtualization** → **VirtualMachines** from the side menu to access the tree view with all projects and VMs in your cluster.

2.  Perform one of the following actions depending on your use case:

    - To move the VM to a new group in the same project:

      1.  Right-click the name of the VM in the tree view.

      2.  Select **Move to group** from the menu.

      3.  Type the name of the group to create in the "Search group" bar.

      4.  Click **Create group** in the drop-down list.

      5.  Click **Save**.

    - To move the VM to an existing group in the same project:

      - Click the name of the VM in the tree view and drag it to a group in the same project. A highlight is displayed on the group for permitted operations.

    - To move the VM from a group to the project:

      - Click the name of the VM in the tree view and drag it on the project name. A highlight is displayed on the group for permitted operations.
