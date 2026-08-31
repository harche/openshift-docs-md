To manage SR-IOV network devices and network attachments on your cluster, install the Single Root I/O Virtualization (SR-IOV) Network Operator. By using this Operator, you can centralize the configuration and lifecycle management of your SR-IOV resources.

As a cluster administrator, you can install the Single Root I/O Virtualization (SR-IOV) Network Operator by using the OpenShift Container Platform CLI or the web console.

# Using the CLI to install the SR-IOV Network Operator

You can use the CLI to install the SR-IOV Network Operator. By using the CLI, you can deploy the Operator directly from your terminal to manage SR-IOV network devices and attachments without navigating the web console.

- You installed the OpenShift CLI (`oc`).

- You have an account with `cluster-admin` privileges.

- You installed a cluster on bare-metal hardware, and you ensured that cluster nodes have hardware that supports SR-IOV.

1.  Create the `openshift-sriov-network-operator` namespace by entering the following command:

    ``` terminal
    $ cat << EOF| oc create -f -
    apiVersion: v1
    kind: Namespace
    metadata:
      name: openshift-sriov-network-operator
      annotations:
        workload.openshift.io/allowed: management
    EOF
    ```

2.  Create an `OperatorGroup` custom resource (CR) by entering the following command:

    ``` terminal
    $ cat << EOF| oc create -f -
    apiVersion: operators.coreos.com/v1
    kind: OperatorGroup
    metadata:
      name: sriov-network-operators
      namespace: openshift-sriov-network-operator
    spec:
      targetNamespaces:
      - openshift-sriov-network-operator
    EOF
    ```

3.  Create a `Subscription` CR for the SR-IOV Network Operator by entering the following command:

    ``` terminal
    $ cat << EOF| oc create -f -
    apiVersion: operators.coreos.com/v1alpha1
    kind: Subscription
    metadata:
      name: sriov-network-operator-subscription
      namespace: openshift-sriov-network-operator
    spec:
      channel: stable
      name: sriov-network-operator
      source: redhat-operators
      sourceNamespace: openshift-marketplace
    EOF
    ```

4.  Create an `SriovoperatorConfig` resource by entering the following command:

    ``` terminal
    $ cat <<EOF | oc create -f -
    apiVersion: sriovnetwork.openshift.io/v1
    kind: SriovOperatorConfig
    metadata:
      name: default
      namespace: openshift-sriov-network-operator
    spec:
      enableInjector: true
      enableOperatorWebhook: true
      logLevel: 2
      disableDrain: false
    EOF
    ```

    <div class="important">

    The following configuration applies only to IBM Z `s390x` systems and is required: The Mellanox firmware plugin is not supported on `s390x` because `mstflint` is not available on this architecture. On `s390x`, disable the Mellanox plugin so that the SR-IOV Network Operator uses the generic plugin for VF configuration. The network adapter must be supplied with SR-IOV already enabled in firmware.

    **Option 1** — Add the following to the `spec` block of the `SriovOperatorConfig` create command above before running it:

    ``` yaml
    disablePlugins:
      - mellanox
    ```

    **Option 2** — If the `SriovOperatorConfig` resource is already created, patch it by entering the following command:

    ``` terminal
    $ oc patch sriovoperatorconfig default \
      -n openshift-sriov-network-operator \
      --type=merge \
      -p '{"spec":{"disablePlugins":["mellanox"]}}'
    ```

    </div>

- To verify that the Operator is installed, enter the following command and then check that the output shows `Succeeded` for the Operator:

  ``` terminal
  $ oc get csv -n openshift-sriov-network-operator \
    -o custom-columns=Name:.metadata.name,Phase:.status.phase
  ```

# Using the web console to install the SR-IOV Network Operator

You can use the web console to install the SR-IOV Network Operator. By using the web console, you can deploy the Operator and manage SR-IOV network devices and attachments directly from a graphical interface without having to use the CLI.

- You have an account with `cluster-admin` privileges.

- You installed a cluster on bare-metal hardware, and you ensured that cluster nodes have hardware that supports SR-IOV.

1.  Install the SR-IOV Network Operator:

    1.  In the OpenShift Container Platform web console, click **Ecosystem** → **Software Catalog**.

    2.  Select **SR-IOV Network Operator** from the list of available Operators, and then click **Install**.

    3.  On the **Install Operator** page, under **Installed Namespace**, select **Operator recommended Namespace**.

    4.  Click **Install**.

        <div class="important">

        The following configuration applies only to IBM Z `s390x` systems and is required:

        The Mellanox firmware plugin is not supported on `s390x` because `mstflint` is not available on this architecture. On `s390x`, disable the Mellanox plugin so that the SR-IOV Network Operator uses the generic plugin for VF configuration. The network adapter must be supplied with SR-IOV already enabled in firmware.

        To disable the Mellanox plugin, patch the `SriovOperatorConfig` resource by entering the following command:

        ``` terminal
        $ oc patch sriovoperatorconfig default \
          -n openshift-sriov-network-operator \
          --type=merge \
          -p '{"spec":{"disablePlugins":["mellanox"]}}'
        ```

        </div>

<!-- -->

1.  Navigate to the **Ecosystem** → **Installed Operators** page.

2.  Ensure that **SR-IOV Network Operator** is listed in the **openshift-sriov-network-operator** project with a **Status** of **InstallSucceeded**.

    <div class="note">

    During installation an Operator might display a **Failed** status. If the installation later succeeds with an **InstallSucceeded** message, you can ignore the **Failed** message.

    </div>

3.  If the Operator does not show as installed, complete any of the following steps to troubleshoot the issue:

    - Inspect the **Operator Subscriptions** and **Install Plans** tabs for any failure or errors under **Status**.

    - Navigate to the **Workloads** → **Pods** page and check the logs for pods in the `openshift-sriov-network-operator` project.

    - Check the namespace of the YAML file. If the annotation is missing, you can add the annotation `workload.openshift.io/allowed=management` to the Operator namespace with the following command:

      ``` terminal
      $ oc annotate ns/openshift-sriov-network-operator workload.openshift.io/allowed=management
      ```

      <div class="note">

      For single-node OpenShift clusters, the annotation `workload.openshift.io/allowed=management` is required for the namespace.

      </div>

# Additional resources

- [Configuring the SR-IOV Network Operator](../../../networking/networking_operators/sr-iov-operator/configuring-sriov-operator.xml#configuring-sriov-operator)
