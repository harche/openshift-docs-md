Install OpenShift Virtualization to add virtualization functionality to your OpenShift Container Platform cluster.

<div class="important">

If you install OpenShift Virtualization in a restricted environment with no internet connectivity, you must [configure Operator Lifecycle Manager for disconnected environments](../../disconnected/using-olm.xml#olm-restricted-networks).

If you have limited internet connectivity, you can [configure proxy support in OLM](../../operators/admin/olm-configuring-proxy-support.xml#olm-configuring-proxy-support) to access the software catalog.

</div>

# Installing the OpenShift Virtualization Operator

Install the OpenShift Virtualization Operator by using the OpenShift Container Platform web console or the command line.

## Installing the OpenShift Virtualization Operator by using the web console

You can deploy the OpenShift Virtualization Operator by using the OpenShift Container Platform web console.

- Install OpenShift Container Platform 4.17 on your cluster.

- Log in to the OpenShift Container Platform web console as a user with `cluster-admin` permissions.

1.  From the **Administrator** perspective, click **Ecosystem** → **Software Catalog**.

2.  In the **Filter by keyword** field, type **Virtualization**.

3.  Select the **OpenShift Virtualization Operator** tile with the **Red Hat** source label.

4.  Read the information about the Operator and click **Install**.

5.  On the **Install Operator** page:

    1.  Select **stable** from the list of available **Update Channel** options. This ensures that you install the version of OpenShift Virtualization that is compatible with your OpenShift Container Platform version.

    2.  For **Installed Namespace**, ensure that the **Operator recommended namespace** option is selected. This installs the Operator in the mandatory `openshift-cnv` namespace, which is automatically created if it does not exist.

        <div class="warning">

        Attempting to install the OpenShift Virtualization Operator in a namespace other than `openshift-cnv` causes the installation to fail.

        </div>

    3.  For **Approval Strategy**, it is highly recommended that you select **Automatic**, which is the default value, so that OpenShift Virtualization automatically updates when a new version is available in the **stable** update channel.

        Selecting the **Manual** approval strategy is not recommended, as it poses a high risk to cluster support and functionality. Only select **Manual** if you fully understand these risks and cannot use **Automatic**.

        <div class="warning">

        Because OpenShift Virtualization is only supported when used with the corresponding OpenShift Container Platform version, missing OpenShift Virtualization updates can cause your cluster to become unsupported.

        </div>

6.  Click **Install** to make the Operator available to the `openshift-cnv` namespace.

7.  When the Operator installs successfully, click **Create HyperConverged**.

8.  Optional: Configure **Infra** and **Workloads** node placement options for OpenShift Virtualization components.

9.  Click **Create** to launch OpenShift Virtualization.

- Navigate to the **Workloads** → **Pods** page and monitor the OpenShift Virtualization pods until they are all **Running**. After all the pods display the **Running** state, you can use OpenShift Virtualization.

## Installing the OpenShift Virtualization Operator by using the command line

Subscribe to the OpenShift Virtualization catalog and install the OpenShift Virtualization Operator by applying manifests to your cluster.

### Subscribing to the OpenShift Virtualization catalog by using the CLI

Before you install OpenShift Virtualization, you must subscribe to the OpenShift Virtualization catalog. Subscribing gives the `openshift-cnv` namespace access to the OpenShift Virtualization Operators.

To subscribe, configure `Namespace`, `OperatorGroup`, and `Subscription` objects by applying a single manifest to your cluster.

- Install OpenShift Container Platform 4.17 on your cluster.

- Install the OpenShift CLI (`oc`).

- Log in as a user with `cluster-admin` privileges.

1.  Create a YAML file that contains the following manifest:

    ``` yaml
    apiVersion: v1
    kind: Namespace
    metadata:
      name: openshift-cnv
      labels:
        openshift.io/cluster-monitoring: "true"
    ---
    apiVersion: operators.coreos.com/v1
    kind: OperatorGroup
    metadata:
      name: kubevirt-hyperconverged-group
      namespace: openshift-cnv
    spec:
      targetNamespaces:
        - openshift-cnv
    ---
    apiVersion: operators.coreos.com/v1alpha1
    kind: Subscription
    metadata:
      name: hco-operatorhub
      namespace: openshift-cnv
    spec:
      source: redhat-operators
      sourceNamespace: openshift-marketplace
      name: kubevirt-hyperconverged
      startingCSV: kubevirt-hyperconverged-operator.v4.20.3
      channel: "stable"
    ```

    Using the `stable` channel ensures that you install the version of OpenShift Virtualization that is compatible with your OpenShift Container Platform version.

2.  Create the required `Namespace`, `OperatorGroup`, and `Subscription` objects for OpenShift Virtualization by running the following command:

    ``` terminal
    $ oc apply -f <filename>.yaml
    ```

<div class="formalpara-title">

**Verification**

</div>

You must verify that the subscription creation was successful before you can proceed with installing OpenShift Virtualization.

1.  Check that the `ClusterServiceVersion` (CSV) object was created successfully. Run the following command and verify the output:

    ``` terminal
    $ oc get csv -n openshift-cnv
    ```

    If the CSV was created successfully, the output shows an entry that contains a `NAME` value of `kubevirt-hyperconverged-operator-*`, a `DISPLAY` value of `OpenShift Virtualization`, and a `PHASE` value of `Succeeded`, as shown in the following example output:

    Example output:

    ``` terminal
    NAME                                       DISPLAY                    VERSION   REPLACES                                   PHASE
    kubevirt-hyperconverged-operator.v4.20.3   OpenShift Virtualization   4.20.3    kubevirt-hyperconverged-operator.v4.19.0   Succeeded
    ```

2.  Check that the `HyperConverged` custom resource (CR) has the correct version. Run the following command and verify the output:

    ``` terminal
    $ oc get hco -n openshift-cnv kubevirt-hyperconverged -o json | jq .status.versions
    ```

    Example output:

    ``` terminal
    {
    "name": "operator",
    "version": "4.20.3"
    }
    ```

3.  Verify the `HyperConverged` CR conditions. Run the following command and check the output:

    ``` terminal
    $ oc get hco kubevirt-hyperconverged -n openshift-cnv -o json | jq -r '.status.conditions[] | {type,status}'
    ```

    Example output:

    ``` terminal
    {
      "type": "ReconcileComplete",
      "status": "True"
    }
    {
      "type": "Available",
      "status": "True"
    }
    {
      "type": "Progressing",
      "status": "False"
    }
    {
      "type": "Degraded",
      "status": "False"
    }
    {
      "type": "Upgradeable",
      "status": "True"
    }
    ```

<div class="note">

You can [configure certificate rotation](../../virt/post_installation_configuration/virt-configuring-certificate-rotation.xml#virt-configuring-certificate-rotation) parameters in the YAML file.

</div>

### Deploying the OpenShift Virtualization Operator by using the CLI

You can deploy the OpenShift Virtualization Operator by using the `oc` CLI.

- Install the OpenShift CLI (`oc`).

- Subscribe to the OpenShift Virtualization catalog in the `openshift-cnv` namespace.

- Log in as a user with `cluster-admin` privileges.

1.  Create a YAML file that contains the following manifest:

    ``` yaml
    apiVersion: hco.kubevirt.io/v1beta1
    kind: HyperConverged
    metadata:
      name: kubevirt-hyperconverged
      namespace: openshift-cnv
    spec:
    ```

2.  Deploy the OpenShift Virtualization Operator by running the following command:

    ``` terminal
    $ oc apply -f <file_name>.yaml
    ```

- Ensure that OpenShift Virtualization deployed successfully by watching the `PHASE` of the cluster service version (CSV) in the `openshift-cnv` namespace. Run the following command:

  ``` terminal
  $ watch oc get csv -n openshift-cnv
  ```

  The following output displays if deployment was successful:

  ``` terminal
  NAME                                      DISPLAY                    VERSION   REPLACES   PHASE
  kubevirt-hyperconverged-operator.v4.20.3   OpenShift Virtualization   4.20.3                Succeeded
  ```

# Next steps

- The [hostpath provisioner](../../virt/storage/virt-configuring-local-storage-with-hpp.xml#virt-creating-hpp-basic-storage-pool_virt-configuring-local-storage-with-hpp) is a local storage provisioner designed for OpenShift Virtualization. If you want to configure local storage for virtual machines, you must enable the hostpath provisioner first.
