In OpenShift Container Platform version 4.17, you can install a three-node cluster on Red Hat OpenStack Platform (RHOSP). A three-node cluster consists of three control plane machines, which also act as compute machines.

This type of cluster provides a smaller, more resource efficient cluster, for cluster administrators and developers to use for testing, development, and production.

You can install a three-node cluster on installer-provisioned infrastructure only. After you install a three-node cluster on RHOSP, you can apply customizations to the cluster. For more information, see "Installing a cluster on RHOSP with customizations".

# Configuring a three-node cluster

To configure a three-node cluster, set the number of worker nodes to `0` in the `install-config.yaml` file before you deploy the cluster.

Setting the number of worker nodes to `0` ensures that the control plane machines are schedulable. This allows application workloads to be scheduled to run from the control plane nodes.

<div class="note">

Because application workloads run from control plane nodes, additional subscriptions are required, as the control plane nodes are considered to be compute nodes.

</div>

- You have an existing `install-config.yaml` file.

<!-- -->

- Set the number of compute replicas to `0` in your `install-config.yaml` file, as shown in the following `compute` stanza:

  <div class="formalpara-title">

  **Example `install-config.yaml` file for a three-node cluster**

  </div>

  ``` yaml
  apiVersion: v1
  baseDomain: example.com
  compute:
  - name: worker
    platform: {}
    replicas: 0
  # ...
  ```

# Additional resources

- [Installing a cluster on RHOSP with customizations](../../installing/installing_openstack/installing-openstack-installer-custom.xml#installing-openstack-installer-custom)
