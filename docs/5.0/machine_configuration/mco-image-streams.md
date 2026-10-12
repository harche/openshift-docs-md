If you have OpenShift Container Platform 5.0 with Red Hat Enterprise Linux CoreOS (RHCOS) version 9.x, you can update the nodes in your cluster to use RHCOS 10.x.

For new installations of OpenShift Container Platform 5.0, RHCOS 10.x is installed by default.

RHCOS is a purpose-designed operating system for use with containers that is deployed by default on all OpenShift Container Platform nodes. Each version of RHCOS is based on a specific version of Red Hat Enterprise Linux (RHEL). RHCOS 10.x is based on RHEL 10.x.

<div class="important">

You cannot update the RHCOS version in a cluster that is using the runC container runtime, because runC is deprecated in OpenShift Container Platform 5.0. You must configure your cluster to use the crun container runtime. Starting in OpenShift Container Platform 4.18, crun is the default container runtime for new installations. For more information, see "Configuring the container runtime".

</div>

# Updating the nodes in an existing cluster from RHCOS 9.x to RHCOS 10.x

For an existing OpenShift Container Platform 5.0 cluster that is using Red Hat Enterprise Linux CoreOS (RHCOS) 9.x, you can move the nodes to RHCOS 10.x.

<div class="important">

Running a cluster with a mixture of RHCOS 9.x and 10.x nodes is not supported. You must move all of your nodes to RHCOS 10.x.

</div>

The following procedure shows how to upgrade the nodes in your cluster to run RHCOS 10.x.

- The boot image in your cluster is at least RHCOS 9.x. Note that the boot image on each node remains at RHCOS 9.x after installing or upgrading to RHCOS 10.x. After you configure RHCOS 10.x in your cluster, new nodes boot using RHCOS 9.x initially and automatically upgrade to RHCOS 10.x. For more information, see "Manually updating the boot image".

- Your cluster is updated to OpenShift Container Platform 5.0.

- The nodes in your cluster are configured to use crun as the default container runtime. You cannot update the RHCOS version on nodes that use the runC container runtime, because runC is deprecated in OpenShift Container Platform 5.0. If you attempt to update a machine config pool (MCP) that has runC nodes, the nodes in the pool will degrade and will not update. The MCP status reports the following error:

  ``` terminal
  apiVersion: machineconfiguration.openshift.io/v1
  kind: MachineConfigPool
  metadata:
    name: worker
  # ...
  status
  # ...
    conditions
    - lastTransitionTime: "2026-09-24T22:42:24Z"
      message: 'Failed to render configuration for pool worker: MachineConfigPool worker
        targets a RHEL 10 OS image where runc is not available. To unblock, migrate
        to crun by removing any ContainerRuntimeConfig that sets defaultRuntime to runc,
        and removing any MachineConfig that sets default_runtime = "runc" in CRI-O configuration
        under /etc/crio/crio.conf.d/'
      reason: ""
      status: "True"
      type: RenderDegraded
    - lastTransitionTime: "2026-09-24T22:42:29Z"
      message: ""
      reason: ""
      status: "True"
      type: Degraded
  ```

  You must configure your cluster to use the crun container runtime. For more information, see "Configuring the container runtime".

1.  Confirm that your cluster has the RHCOS 10.x stream available by running the following command:

    ``` terminal
    $ oc get osImageStreams/cluster -o yaml | grep rhel-10
    ```

    <div class="formalpara-title">

    **Example output**

    </div>

    ``` terminal
      - name: rhel-10
    ```

2.  Update the nodes in your cluster to use RHCOS 10.x by running the following command to edit the `OSImageStream` custom resource:

    ``` terminal
    $ oc patch osimagestream cluster --type merge -p '{"spec":{"defaultStream":"rhel-10"}}'
    ```

    The `spec.defaultStream: rhel-10` parameter specifies that new nodes use the image referenced in `status.availableStreams.osImage.name: rhel-10` in the `OSImageStream` custom resource.

    <div class="important">

    Running a cluster with a mixture of RHCOS 9.x and 10.x nodes is not supported. You must move all of your nodes to RHCOS 10.x.

    </div>

    Wait for the pools to finish rolling out the update.

- After the nodes have returned to the `READY` state, check the machine config pool status for the nodes in a machine config pool to view the current RHCOS version by running the following command:

  ``` terminal
  $ oc get machineconfigpool -n openshift-machine-config-operator <machine_config_pool_name> -o yaml
  ```

  Replace `<machine_config_pool_name>` with the name of a machine config pool.

  <div class="formalpara-title">

  **Example output**

  </div>

  ``` terminal
  apiVersion: machineconfiguration.openshift.io/v1
  kind: MachineConfigPool
  metadata:
    name: worker
  # ...
  status
  # ...
    osImageStream:
      name: rhel-10
  ```

- Examine the `/etc/redhat-release` file on a node to see the current RHCOS version on that node by running the following command:

  ``` terminal
  $ oc debug node/<node_name> -- chroot /host cat /etc/redhat-release
  ```

  Replace `<node_name>` with the name of the node.

  <div class="formalpara-title">

  **Example output**

  </div>

  ``` terminal
  Red Hat Enterprise Linux release 10.2 (Coughlan)
  ```

- Examine the `/etc/os-release` file on a node to see the current RHCOS version on that node by running the following command:

  ``` terminal
  $ oc debug node/<node_name> -- chroot /host cat /etc/os-release
  ```

  Replace `<node_name>` with the name of the node.

  <div class="formalpara-title">

  **Example output**

  </div>

  ``` terminal
  NAME="Red Hat Enterprise Linux CoreOS"
  VERSION="10.2.20260824-0 (Coughlan)"
  RELEASE_TYPE=stable
  ID="rhel"
  ID_LIKE="centos fedora"
  VERSION_ID="10.2"
  PLATFORM_ID="platform:el10"
  PRETTY_NAME="Red Hat Enterprise Linux CoreOS 10.2.20260824-0 (Coughlan)"
  # ...
  ```

# Additional resources

- [Manually updating the boot image](../machine_configuration/mco-update-boot-images-manual.xml#mco-update-boot-images-manual)

- [Optional configuration parameters](../installing/install_config/installation-config-parameters-generic.xml#installation-configuration-parameters-optional_installation-config-parameters-generic)

- [Configuring the container runtime](../machine_configuration/machine-configs-custom.xml#config-container-runtime_machine-configs-custom)
