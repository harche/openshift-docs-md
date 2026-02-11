You can create a different compute machine set to serve a specific purpose in your OpenShift Container Platform cluster on VMware vSphere. For example, you might create infrastructure machine sets and related machines so that you can move supporting workloads to the new machines.

> [!IMPORTANT]
> You can use the advanced machine management and scaling capabilities only in clusters where the Machine API is operational. Clusters with user-provisioned infrastructure require additional validation and configuration to use the Machine API.
>
> Clusters with the infrastructure platform type `none` cannot use the Machine API. This limitation applies even if the compute machines that are attached to the cluster are installed on a platform that supports the feature. This parameter cannot be changed after installation.
>
> To view the platform type for your cluster, run the following command:
>
> ``` terminal
> $ oc get infrastructure cluster -o jsonpath='{.status.platform}'
> ```

# Sample YAML for a compute machine set custom resource on vSphere

This sample YAML defines a compute machine set that runs on VMware vSphere and creates nodes that are labeled with `node-role.kubernetes.io/<role>: ""`.

In this sample, `<infrastructure_id>` is the infrastructure ID label that is based on the cluster ID that you set when you provisioned the cluster, and `<role>` is the node label to add.

``` yaml
apiVersion: machine.openshift.io/v1beta1
kind: MachineSet
metadata:
  creationTimestamp: null
  labels:
    machine.openshift.io/cluster-api-cluster: <infrastructure_id>
  name: <infrastructure_id>-<role>
  namespace: openshift-machine-api
spec:
  replicas: 1
  selector:
    matchLabels:
      machine.openshift.io/cluster-api-cluster: <infrastructure_id>
      machine.openshift.io/cluster-api-machineset: <infrastructure_id>-<role>
  template:
    metadata:
      creationTimestamp: null
      labels:
        machine.openshift.io/cluster-api-cluster: <infrastructure_id>
        machine.openshift.io/cluster-api-machine-role: <role>
        machine.openshift.io/cluster-api-machine-type: <role>
        machine.openshift.io/cluster-api-machineset: <infrastructure_id>-<role>
    spec:
      metadata:
        creationTimestamp: null
        labels:
          node-role.kubernetes.io/<role>: ""
      providerSpec:
        value:
          apiVersion: machine.openshift.io/v1beta1
          credentialsSecret:
            name: vsphere-cloud-credentials
          dataDisks:
          - name: "<disk_name>"
            provisioningMode: "<mode>"
            sizeGiB: 20
          diskGiB: 120
          kind: VSphereMachineProviderSpec
          memoryMiB: 8192
          metadata:
            creationTimestamp: null
          network:
            devices:
            - networkName: "<vm_network_name>"
          numCPUs: 4
          numCoresPerSocket: 1
          snapshot: ""
          template: <vm_template_name>
          userDataSecret:
            name: worker-user-data
          workspace:
            datacenter: <vcenter_data_center_name>
            datastore: <vcenter_datastore_name>
            folder: <vcenter_vm_folder_path>
            resourcepool: <vsphere_resource_pool>
            server: <vcenter_server_ip>
```

- Specify the infrastructure ID that is based on the cluster ID that you set when you provisioned the cluster. If you have the OpenShift CLI (`oc`) installed, you can obtain the infrastructure ID by running the following command:

  ``` terminal
  $ oc get -o jsonpath='{.status.infrastructureName}{"\n"}' infrastructure cluster
  ```

- Specify the infrastructure ID and node label.

- Specify the node label to add.

- Specify one or more data disk definitions. For more information, see "Configuring data disks by using machine sets".

- Specify the vSphere VM network to deploy the compute machine set to. This VM network must be where other compute machines reside in the cluster.

- Specify the vSphere VM template to use, such as `user-5ddjd-rhcos`.

- Specify the vCenter datacenter to deploy the compute machine set on.

- Specify the vCenter datastore to deploy the compute machine set on.

- Specify the path to the vSphere VM folder in vCenter, such as `/dc1/vm/user-inst-5ddjd`.

- Specify the vSphere resource pool for your VMs.

- Specify the vCenter server IP or fully qualified domain name.

# Minimum required vCenter privileges for compute machine set management

To manage compute machine sets in an OpenShift Container Platform cluster on vCenter, you must use an account with privileges to read, create, and delete the required resources. Using an account that has global administrative privileges is the simplest way to access all of the necessary permissions.

If you cannot use an account with global administrative privileges, you must create roles to grant the minimum required privileges. The following table lists the minimum vCenter roles and privileges that are required to create, scale, and delete compute machine sets and to delete machines in your OpenShift Container Platform cluster.

<div class="example">

<div class="title">

Minimum vCenter roles and privileges required for compute machine set management

</div>

<table>
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;">vSphere object for role</th>
<th style="text-align: left;">When required</th>
<th style="text-align: left;">Required privileges</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;"><p>vSphere vCenter</p></td>
<td style="text-align: left;"><p>Always</p></td>
<td style="text-align: left;"><p><code>InventoryService.Tagging.AttachTag</code><br />
<code>InventoryService.Tagging.CreateCategory</code><br />
<code>InventoryService.Tagging.CreateTag</code><br />
<code>InventoryService.Tagging.DeleteCategory</code><br />
<code>InventoryService.Tagging.DeleteTag</code><br />
<code>InventoryService.Tagging.EditCategory</code><br />
<code>InventoryService.Tagging.EditTag</code><br />
<code>Sessions.ValidateSession</code><br />
<code>StorageProfile.Update</code><sup>1</sup><br />
<code>StorageProfile.View</code><sup>1</sup></p></td>
</tr>
<tr>
<td style="text-align: left;"><p>vSphere vCenter Cluster</p></td>
<td style="text-align: left;"><p>Always</p></td>
<td style="text-align: left;"><p><code>Resource.AssignVMToPool</code></p></td>
</tr>
<tr>
<td style="text-align: left;"><p>vSphere datastore</p></td>
<td style="text-align: left;"><p>Always</p></td>
<td style="text-align: left;"><p><code>Datastore.AllocateSpace</code><br />
<code>Datastore.Browse</code></p></td>
</tr>
<tr>
<td style="text-align: left;"><p>vSphere Port Group</p></td>
<td style="text-align: left;"><p>Always</p></td>
<td style="text-align: left;"><p><code>Network.Assign</code></p></td>
</tr>
<tr>
<td style="text-align: left;"><p>Virtual Machine Folder</p></td>
<td style="text-align: left;"><p>Always</p></td>
<td style="text-align: left;"><p><code>VirtualMachine.Config.AddRemoveDevice</code><br />
<code>VirtualMachine.Config.AdvancedConfig</code><br />
<code>VirtualMachine.Config.Annotation</code><br />
<code>VirtualMachine.Config.CPUCount</code><br />
<code>VirtualMachine.Config.DiskExtend</code><br />
<code>VirtualMachine.Config.Memory</code><br />
<code>VirtualMachine.Config.Settings</code><br />
<code>VirtualMachine.Interact.PowerOff</code><br />
<code>VirtualMachine.Interact.PowerOn</code><br />
<code>VirtualMachine.Inventory.CreateFromExisting</code><br />
<code>VirtualMachine.Inventory.Delete</code><br />
<code>VirtualMachine.Provisioning.Clone</code></p></td>
</tr>
<tr>
<td style="text-align: left;"><p>vSphere vCenter data center</p></td>
<td style="text-align: left;"><p>If the installation program creates the virtual machine folder.</p></td>
<td style="text-align: left;"><p><code>Resource.AssignVMToPool</code><br />
<code>VirtualMachine.Provisioning.DeployTemplate</code></p></td>
</tr>
<tr>
<td colspan="3" style="text-align: left;"><p><sup>1</sup> The <code>StorageProfile.Update</code> and <code>StorageProfile.View</code> permissions are required only for storage backends that use the Container Storage Interface (CSI).</p></td>
</tr>
</tbody>
</table>

</div>

The following table details the permissions and propagation settings that are required for compute machine set management.

<div class="example">

<div class="title">

Required permissions and propagation settings

</div>

<table>
<colgroup>
<col style="width: 25%" />
<col style="width: 25%" />
<col style="width: 25%" />
<col style="width: 25%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;">vSphere object</th>
<th style="text-align: left;">Folder type</th>
<th style="text-align: left;">Propagate to children</th>
<th style="text-align: left;">Permissions required</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;"><p>vSphere vCenter</p></td>
<td style="text-align: left;"><p>Always</p></td>
<td style="text-align: left;"><p>Not required</p></td>
<td style="text-align: left;"><p>Listed required privileges</p></td>
</tr>
<tr>
<td rowspan="2" style="text-align: left;"><p>vSphere vCenter data center</p></td>
<td style="text-align: left;"><p>Existing folder</p></td>
<td style="text-align: left;"><p>Not required</p></td>
<td style="text-align: left;"><p><code>ReadOnly</code> permission</p></td>
</tr>
<tr>
<td style="text-align: left;"><p>Installation program creates the folder</p></td>
<td style="text-align: left;"><p>Required</p></td>
<td style="text-align: left;"><p>Listed required privileges</p></td>
</tr>
<tr>
<td style="text-align: left;"><p>vSphere vCenter Cluster</p></td>
<td style="text-align: left;"><p>Always</p></td>
<td style="text-align: left;"><p>Required</p></td>
<td style="text-align: left;"><p>Listed required privileges</p></td>
</tr>
<tr>
<td style="text-align: left;"><p>vSphere vCenter datastore</p></td>
<td style="text-align: left;"><p>Always</p></td>
<td style="text-align: left;"><p>Not required</p></td>
<td style="text-align: left;"><p>Listed required privileges</p></td>
</tr>
<tr>
<td style="text-align: left;"><p>vSphere Switch</p></td>
<td style="text-align: left;"><p>Always</p></td>
<td style="text-align: left;"><p>Not required</p></td>
<td style="text-align: left;"><p><code>ReadOnly</code> permission</p></td>
</tr>
<tr>
<td style="text-align: left;"><p>vSphere Port Group</p></td>
<td style="text-align: left;"><p>Always</p></td>
<td style="text-align: left;"><p>Not required</p></td>
<td style="text-align: left;"><p>Listed required privileges</p></td>
</tr>
<tr>
<td style="text-align: left;"><p>vSphere vCenter Virtual Machine Folder</p></td>
<td style="text-align: left;"><p>Existing folder</p></td>
<td style="text-align: left;"><p>Required</p></td>
<td style="text-align: left;"><p>Listed required privileges</p></td>
</tr>
</tbody>
</table>

</div>

For more information about creating an account with only the required privileges, see [vSphere Permissions and User Management Tasks](https://docs.vmware.com/en/VMware-vSphere/7.0/com.vmware.vsphere.security.doc/GUID-5372F580-5C23-4E9C-8A4E-EF1B4DD9033E.html) in the vSphere documentation.

# Requirements for clusters with user-provisioned infrastructure to use compute machine sets

To use compute machine sets on clusters that have user-provisioned infrastructure, you must ensure that you cluster configuration supports using the Machine API.

## Obtaining the infrastructure ID

To create compute machine sets, you must be able to supply the infrastructure ID for your cluster.

<div>

<div class="title">

Procedure

</div>

- To obtain the infrastructure ID for your cluster, run the following command:

  ``` terminal
  $ oc get infrastructure cluster -o jsonpath='{.status.infrastructureName}'
  ```

</div>

## Satisfying vSphere credentials requirements

To use compute machine sets, the Machine API must be able to interact with vCenter. Credentials that authorize the Machine API components to interact with vCenter must exist in a secret in the `openshift-machine-api` namespace.

<div>

<div class="title">

Procedure

</div>

1.  To determine whether the required credentials exist, run the following command:

    ``` terminal
    $ oc get secret \
      -n openshift-machine-api vsphere-cloud-credentials \
      -o go-template='{{range $k,$v := .data}}{{printf "%s: " $k}}{{if not $v}}{{$v}}{{else}}{{$v | base64decode}}{{end}}{{"\n"}}{{end}}'
    ```

    <div class="formalpara">

    <div class="title">

    Sample output

    </div>

    ``` terminal
    <vcenter-server>.password=<openshift-user-password>
    <vcenter-server>.username=<openshift-user>
    ```

    </div>

    where `<vcenter-server>` is the IP address or fully qualified domain name (FQDN) of the vCenter server and `<openshift-user>` and `<openshift-user-password>` are the OpenShift Container Platform administrator credentials to use.

2.  If the secret does not exist, create it by running the following command:

    ``` terminal
    $ oc create secret generic vsphere-cloud-credentials \
      -n openshift-machine-api \
      --from-literal=<vcenter-server>.username=<openshift-user> --from-literal=<vcenter-server>.password=<openshift-user-password>
    ```

</div>

## Satisfying Ignition configuration requirements

Provisioning virtual machines (VMs) requires a valid Ignition configuration. The Ignition configuration contains the `machine-config-server` address and a system trust bundle for obtaining further Ignition configurations from the Machine Config Operator.

By default, this configuration is stored in the `worker-user-data` secret in the `machine-api-operator` namespace. Compute machine sets reference the secret during the machine creation process.

<div>

<div class="title">

Procedure

</div>

1.  To determine whether the required secret exists, run the following command:

    ``` terminal
    $ oc get secret \
      -n openshift-machine-api worker-user-data \
      -o go-template='{{range $k,$v := .data}}{{printf "%s: " $k}}{{if not $v}}{{$v}}{{else}}{{$v | base64decode}}{{end}}{{"\n"}}{{end}}'
    ```

    <div class="formalpara">

    <div class="title">

    Sample output

    </div>

    ``` terminal
    disableTemplating: false
    userData:
      {
        "ignition": {
          ...
          },
        ...
      }
    ```

    </div>

    - The full output is omitted here, but should have this format.

2.  If the secret does not exist, create it by running the following command:

    ``` terminal
    $ oc create secret generic worker-user-data \
      -n openshift-machine-api \
      --from-file=<installation_directory>/worker.ign
    ```

    where `<installation_directory>` is the directory that was used to store your installation assets during cluster installation.

</div>

<div>

<div class="title">

Additional resources

</div>

- [Understanding the Machine Config Operator](../../machine_configuration/index.xml#machine-config-operator_machine-config-overview)

- [Installing RHCOS and starting the OpenShift Container Platform bootstrap process](../../installing/installing_vsphere/upi/installing-vsphere.xml#installation-vsphere-machines_installing-vsphere)

</div>

# Creating a compute machine set

In addition to the compute machine sets created by the installation program, you can create your own to dynamically manage the machine compute resources for specific workloads of your choice.

> [!NOTE]
> Clusters that are installed with user-provisioned infrastructure have a different networking stack than clusters with infrastructure that is provisioned by the installation program. As a result of this difference, automatic load balancer management is unsupported on clusters that have user-provisioned infrastructure. For these clusters, a compute machine set can only create `worker` and `infra` type machines.

<div>

<div class="title">

Prerequisites

</div>

- Deploy an OpenShift Container Platform cluster.

- Install the OpenShift CLI (`oc`).

- Log in to `oc` as a user with `cluster-admin` permission.

- Have the necessary permissions to deploy VMs in your vCenter instance and have the required access to the datastore specified.

- If your cluster uses user-provisioned infrastructure, you have satisfied the specific Machine API requirements for that configuration.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Create a new YAML file that contains the compute machine set custom resource (CR) sample and is named `<file_name>.yaml`.

    Ensure that you set the `<clusterID>` and `<role>` parameter values.

2.  Optional: If you are not sure which value to set for a specific field, you can check an existing compute machine set from your cluster.

    1.  To list the compute machine sets in your cluster, run the following command:

        ``` terminal
        $ oc get machinesets -n openshift-machine-api
        ```

        <div class="formalpara">

        <div class="title">

        Example output

        </div>

        ``` terminal
        NAME                                DESIRED   CURRENT   READY   AVAILABLE   AGE
        agl030519-vplxk-worker-us-east-1a   1         1         1       1           55m
        agl030519-vplxk-worker-us-east-1b   1         1         1       1           55m
        agl030519-vplxk-worker-us-east-1c   1         1         1       1           55m
        agl030519-vplxk-worker-us-east-1d   0         0                             55m
        agl030519-vplxk-worker-us-east-1e   0         0                             55m
        agl030519-vplxk-worker-us-east-1f   0         0                             55m
        ```

        </div>

    2.  To view values of a specific compute machine set custom resource (CR), run the following command:

        ``` terminal
        $ oc get machineset <machineset_name> \
          -n openshift-machine-api -o yaml
        ```

        <div class="formalpara">

        <div class="title">

        Example output

        </div>

        ``` yaml
        apiVersion: machine.openshift.io/v1beta1
        kind: MachineSet
        metadata:
          labels:
            machine.openshift.io/cluster-api-cluster: <infrastructure_id>
          name: <infrastructure_id>-<role>
          namespace: openshift-machine-api
        spec:
          replicas: 1
          selector:
            matchLabels:
              machine.openshift.io/cluster-api-cluster: <infrastructure_id>
              machine.openshift.io/cluster-api-machineset: <infrastructure_id>-<role>
          template:
            metadata:
              labels:
                machine.openshift.io/cluster-api-cluster: <infrastructure_id>
                machine.openshift.io/cluster-api-machine-role: <role>
                machine.openshift.io/cluster-api-machine-type: <role>
                machine.openshift.io/cluster-api-machineset: <infrastructure_id>-<role>
            spec:
              providerSpec:
                ...
        ```

        </div>

        - The cluster infrastructure ID.

        - A default node label.

          > [!NOTE]
          > For clusters that have user-provisioned infrastructure, a compute machine set can only create `worker` and `infra` type machines.

        - The values in the `<providerSpec>` section of the compute machine set CR are platform-specific. For more information about `<providerSpec>` parameters in the CR, see the sample compute machine set CR configuration for your provider.

    3.  If you are creating a compute machine set for a cluster that has user-provisioned infrastructure, note the following important values:

        <div class="formalpara">

        <div class="title">

        Example vSphere `providerSpec` values

        </div>

        ``` yaml
        apiVersion: machine.openshift.io/v1beta1
        kind: MachineSet
        ...
        template:
          ...
          spec:
            providerSpec:
              value:
                apiVersion: machine.openshift.io/v1beta1
                credentialsSecret:
                  name: vsphere-cloud-credentials
                dataDisks:
                - name: <disk_name>
                  provisioningMode: <mode>
                  sizeGiB: 10
                diskGiB: 120
                kind: VSphereMachineProviderSpec
                memoryMiB: 16384
                network:
                  devices:
                    - networkName: "<vm_network_name>"
                numCPUs: 4
                numCoresPerSocket: 4
                snapshot: ""
                template: <vm_template_name>
                userDataSecret:
                  name: worker-user-data
                workspace:
                  datacenter: <vcenter_data_center_name>
                  datastore: <vcenter_datastore_name>
                  folder: <vcenter_vm_folder_path>
                  resourcepool: <vsphere_resource_pool>
                  server: <vcenter_server_address>
        ```

        </div>

        - The name of the secret in the `openshift-machine-api` namespace that contains the required vCenter credentials.

        - The collection of data disk definitions. For more information, see "Configuring data disks by using machine sets".

        - The name of the RHCOS VM template for your cluster that was created during installation.

        - The name of the secret in the `openshift-machine-api` namespace that contains the required Ignition configuration credentials.

        - The IP address or fully qualified domain name (FQDN) of the vCenter server.

3.  Create a `MachineSet` CR by running the following command:

    ``` terminal
    $ oc create -f <file_name>.yaml
    ```

</div>

<div>

<div class="title">

Verification

</div>

- View the list of compute machine sets by running the following command:

  ``` terminal
  $ oc get machineset -n openshift-machine-api
  ```

  <div class="formalpara">

  <div class="title">

  Example output

  </div>

  ``` terminal
  NAME                                DESIRED   CURRENT   READY   AVAILABLE   AGE
  agl030519-vplxk-infra-us-east-1a    1         1         1       1           11m
  agl030519-vplxk-worker-us-east-1a   1         1         1       1           55m
  agl030519-vplxk-worker-us-east-1b   1         1         1       1           55m
  agl030519-vplxk-worker-us-east-1c   1         1         1       1           55m
  agl030519-vplxk-worker-us-east-1d   0         0                             55m
  agl030519-vplxk-worker-us-east-1e   0         0                             55m
  agl030519-vplxk-worker-us-east-1f   0         0                             55m
  ```

  </div>

  When the new compute machine set is available, the `DESIRED` and `CURRENT` values match. If the compute machine set is not available, wait a few minutes and run the command again.

</div>

# Labeling GPU machine sets for the cluster autoscaler

You can use a machine set label to indicate which machines the cluster autoscaler can use to deploy GPU-enabled nodes.

<div>

<div class="title">

Prerequisites

</div>

- Your cluster uses a cluster autoscaler.

</div>

<div>

<div class="title">

Procedure

</div>

- On the machine set that you want to create machines for the cluster autoscaler to use to deploy GPU-enabled nodes, add a `cluster-api/accelerator` label:

  ``` yaml
  apiVersion: machine.openshift.io/v1beta1
  kind: MachineSet
  metadata:
    name: machine-set-name
  spec:
    template:
      spec:
        metadata:
          labels:
            cluster-api/accelerator: <accelerator_name>
  ```

  where:

  \<accelerator_name\>
  Specifies a label of your choice that consists of alphanumeric characters, `-`, `_`, or `.` and starts and ends with an alphanumeric character. For example, you might use `nvidia-t4` to represent Nvidia T4 GPUs, or `nvidia-a10g` for A10G GPUs.

  > [!NOTE]
  > You must specify the value of this label for the `spec.resourceLimits.gpus.type` parameter in your `ClusterAutoscaler` CR. For more information, see "Cluster autoscaler resource definition".

</div>

<div>

<div class="title">

Additional resources

</div>

- [Cluster autoscaler resource definition](../../machine_management/applying-autoscaling.xml#cluster-autoscaler-cr_applying-autoscaling)

</div>

# Adding tags to machines by using machine sets

OpenShift Container Platform adds a cluster-specific tag to each virtual machine (VM) that it creates. The installation program uses these tags to select the VMs to delete when uninstalling a cluster.

In addition to the cluster-specific tags assigned to VMs, you can configure a machine set to add up to 10 additional vSphere tags to the VMs it provisions.

<div>

<div class="title">

Prerequisites

</div>

- You have access to an OpenShift Container Platform cluster installed on vSphere using an account with `cluster-admin` permissions.

- You have access to the VMware vCenter console associated with your cluster.

- You have created a tag in the vCenter console.

- You have installed the OpenShift CLI (`oc`).

</div>

<div>

<div class="title">

Procedure

</div>

1.  Use the vCenter console to find the tag ID for any tag that you want to add to your machines:

    1.  Log in to the vCenter console.

    2.  From the **Home** menu, click **Tags & Custom Attributes**.

    3.  Select a tag that you want to add to your machines.

    4.  Use the browser URL for the tag that you select to identify the tag ID.

        <div class="formalpara">

        <div class="title">

        Example tag URL

        </div>

        ``` text
        https://vcenter.example.com/ui/app/tags/tag/urn:vmomi:InventoryServiceTag:208e713c-cae3-4b7f-918e-4051ca7d1f97:GLOBAL/permissions
        ```

        </div>

        <div class="formalpara">

        <div class="title">

        Example tag ID

        </div>

        ``` text
        urn:vmomi:InventoryServiceTag:208e713c-cae3-4b7f-918e-4051ca7d1f97:GLOBAL
        ```

        </div>

2.  In a text editor, open the YAML file for an existing machine set or create a new one.

3.  Edit the following lines under the `providerSpec` field:

    ``` yaml
    apiVersion: machine.openshift.io/v1beta1
    kind: MachineSet
    # ...
    spec:
      template:
        spec:
          providerSpec:
            value:
              tagIDs:
              - <tag_id_value>
    # ...
    ```

    - Specify a list of up to 10 tags to add to the machines that this machine set provisions.

    - Specify the value of the tag that you want to add to your machines. For example, `urn:vmomi:InventoryServiceTag:208e713c-cae3-4b7f-918e-4051ca7d1f97:GLOBAL`.

</div>

# Configuring multiple network interface controllers by using machine sets

OpenShift Container Platform clusters on VMware vSphere support connecting up to 10 network interface controllers (NICs) to a node. By configuring multiple NICs, you can provide dedicated network links in the node virtual machines (VMs) for uses such as storage or databases.

You can use machine sets to manage this configuration.

- If you want to use multiple NICs in a vSphere cluster that was not configured to do so during installation, you can use machine sets to implement this configuration.

- If your cluster was set up during installation to use multiple NICs, machine sets that you create can use your existing failure domain configuration.

- If your failure domain configuration changes, you can use machine sets to make updates that reflect those changes.

<div>

<div class="title">

Prerequisites

</div>

- You have administrator access to OpenShift CLI (`oc`) for an OpenShift Container Platform cluster on vSphere.

</div>

<div>

<div class="title">

Procedure

</div>

1.  For a cluster that already uses multiple NICs, obtain the following values from the `Infrastructure` resource by running the following command:

    ``` terminal
    $ oc get infrastructure cluster -o=jsonpath={.spec.platformSpec.vsphere.failureDomains}
    ```

    | `Infrastructure` resource value | Placeholder value for sample machine set | Description |
    |----|----|----|
    | `failureDomain.topology.networks[0]` | `<vm_network_name_1>` | The name of the first NIC to use. |
    | `failureDomain.topology.networks[1]` | `<vm_network_name_2>` | The name of the second NIC to use. |
    | `failureDomain.topology.networks[<n-1>]` | `<vm_network_name_n>` | The name of the *n*th NIC to use. Collect the name of each NIC in the `Infrastructure` resource. |
    | `failureDomain.topology.template` | `<vm_template_name>` | The vSphere VM template to use. |
    | `failureDomain.topology.datacenter` | `<vcenter_data_center_name>` | The vCenter data center to deploy the machine set on. |
    | `failureDomain.topology.datastore` | `<vcenter_datastore_name>` | The vCenter datastore to deploy the machine set on. |
    | `failureDomain.topology.folder` | `<vcenter_vm_folder_path>` | The path to the vSphere VM folder in vCenter, such as `/dc1/vm/user-inst-5ddjd`. |
    | `failureDomain.topology.computeCluster` + `/Resources` | `<vsphere_resource_pool>` | The vSphere resource pool for your VMs. |
    | `failureDomain.server` | `<vcenter_server_ip>` | The vCenter server IP or fully qualified domain name (FQDN). |

    Required network interface controller values

2.  In a text editor, open the YAML file for an existing machine set or create a new one.

3.  Use a machine set configuration formatted like the following example.

    - For a cluster that currently uses multiple NICs, use the values from the `Infrastructure` resource to populate the values in the machine set custom resource.

    - For a cluster that is not using multiple NICs, populate the values you want to use in the machine set custom resource.

    <div class="formalpara">

    <div class="title">

    Sample machine set

    </div>

    ``` yaml
    apiVersion: machine.openshift.io/v1beta1
    kind: MachineSet
    # ...
    spec:
      template:
        spec:
          providerSpec:
            value:
              network:
                devices:
                - networkName: "<vm_network_name_1>"
                - networkName: "<vm_network_name_2>"
              template: <vm_template_name>
              workspace:
                datacenter: <vcenter_data_center_name>
                datastore: <vcenter_datastore_name>
                folder: <vcenter_vm_folder_path>
                resourcepool: <vsphere_resource_pool>
                server: <vcenter_server_ip>
    # ...
    ```

    </div>

    - Specify a list of up to 10 NICs to use.

    - Specify the vSphere VM template to use, such as `user-5ddjd-rhcos`.

    - Specify the vCenter data center to deploy the machine set on.

    - Specify the vCenter datastore to deploy the machine set on.

    - Specify the path to the vSphere VM folder in vCenter, such as `/dc1/vm/user-inst-5ddjd`.

    - Specify the vSphere resource pool for your VMs.

    - Specify the vCenter server IP or fully qualified domain name (FQDN).

</div>

# Configuring data disks by using machine sets

OpenShift Container Platform clusters on VMware vSphere support adding up to 29 disks to the virtual machine (VM) controller.

> [!IMPORTANT]
> Configuring vSphere data disks is a Technology Preview feature only. Technology Preview features are not supported with Red Hat production service level agreements (SLAs) and might not be functionally complete. Red Hat does not recommend using them in production. These features provide early access to upcoming product features, enabling customers to test functionality and provide feedback during the development process.
>
> For more information about the support scope of Red Hat Technology Preview features, see [Technology Preview Features Support Scope](https://access.redhat.com/support/offerings/techpreview/).

By configuring data disks, you can attach disks to VMs and use them to store data for etcd, container images, and other uses. Separating data can help avoid filling the primary disk so that important activities such as upgrades have the resources that they require.

> [!NOTE]
> Adding data disks attaches them to the VM and mounts them to the location that RHCOS designates.

<div>

<div class="title">

Prerequisites

</div>

- You have administrator access to OpenShift CLI (`oc`) for an OpenShift Container Platform cluster on vSphere.

</div>

<div>

<div class="title">

Procedure

</div>

1.  In a text editor, open the YAML file for an existing machine set or create a new one.

2.  Edit the following lines under the `providerSpec` field:

    ``` yaml
    apiVersion: machine.openshift.io/v1beta1
    kind: MachineSet
    # ...
    spec:
      template:
        spec:
          providerSpec:
            value:
              dataDisks:
              - name: "<disk_name>"
                provisioningMode: "<mode>"
                sizeGiB: 20
              - name: "<disk_name>"
                provisioningMode: "<mode>"
                sizeGiB: 20
    # ...
    ```

    - Specify a collection of 1-29 data disk definitions. This sample configuration shows the formatting to include two data disk definitions.

    - Specify the name of the data disk. The name must meet the following requirements:

      - Start and end with an alphanumeric character

      - Consist only of alphanumeric characters, hyphens (`-`), and underscores (`_`)

      - Have a maximum length of 80 characters

    - Specify the data disk provisioning method. This value defaults to the vSphere default storage policy if not set. Valid values are `Thin`, `Thick`, and `EagerlyZeroed`.

    - Specify the size of the data disk in GiB. The maximum size is 16384 GiB.

</div>
