You can create Helm releases on an OpenShift Container Platform cluster by using the following methods:

- The CLI.

- The web console.

The Software Catalog displays Helm charts available in the cluster. By default, it lists charts from the Red Hat OpenShift Helm repository.

As a cluster administrator, you can add cluster-scoped and namespace-scoped Helm chart repositories in addition to the default. The Software Catalog displays charts from all of them.

As a project member with the required role-based access control (RBAC) permissions, you can also add namespace-scoped Helm chart repositories. The Software Catalog displays the Helm charts from these repositories.

On the **Ecosystem** → **Helm** page, you can:

- Create Helm Releases and Repositories using the **Create** button.

- Create, update, or delete a cluster-scoped or namespace-scoped Helm chart repository.

- View the list of the existing Helm chart repositories in the Repositories tab, which can also be easily distinguished as either cluster scoped or namespace scoped.

# Installing a Helm chart on an OpenShift Container Platform cluster

You can install a Helm chart on an OpenShift Container Platform cluster using the Helm CLI.

<div>

<div class="title">

Prerequisites

</div>

- You have a running OpenShift Container Platform cluster and you have logged into it.

- You have installed Helm.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Create a new project:

    ``` terminal
    $ oc new-project vault
    ```

2.  Add a repository of Helm charts to your local Helm client:

    ``` terminal
    $ helm repo add openshift-helm-charts https://charts.openshift.io/
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` terminal
    "openshift-helm-charts" has been added to your repositories
    ```

    </div>

3.  Update the repository:

    ``` terminal
    $ helm repo update
    ```

4.  Install an example HashiCorp Vault:

    ``` terminal
    $ helm install example-vault openshift-helm-charts/hashicorp-vault
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` terminal
    NAME: example-vault
    LAST DEPLOYED: Fri Mar 11 12:02:12 2022
    NAMESPACE: vault
    STATUS: deployed
    REVISION: 1
    NOTES:
    Thank you for installing HashiCorp Vault!
    ```

    </div>

5.  Verify that the chart has installed successfully:

    ``` terminal
    $ helm list
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` terminal
    NAME             NAMESPACE   REVISION    UPDATED                                 STATUS      CHART           APP VERSION
    example-vault   vault       1           2022-03-11 12:02:12.296226673 +0530 IST deployed    vault-0.19.0    1.9.2
    ```

    </div>

</div>

# Creating Helm releases by using the web console

You can use either the web console or the CLI to create a Helm release from a chart. The web console lists Helm releases on the **Ecosystem** → **Helm** page.

<div>

<div class="title">

Prerequisites

</div>

- You have logged in to the web console.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Navigate to **Ecosystem** → **Software Catalog**.

2.  Under **Type**, click **Helm Charts**.

3.  Select a chart and read the description, README, and other details about the chart.

4.  Click **Create**.

5.  In the **Create Helm Release** page:

    1.  Enter a unique name for the release in the **Release Name** field.

    2.  Select the required chart version from the **Chart Version** drop-down list.

    3.  Configure your Helm chart by using the **Form View** or the **YAML View**.

        > [!NOTE]
        > Where available, you can switch between the **YAML View** and **Form View**. The web console keeps your data when you switch between views.

    4.  Click **Create** to create a Helm release. The web console displays the new release on the **Ecosystem** → **Helm** page.

        If a Helm chart has release notes, the web console displays them.

        If a Helm chart creates workloads, the web console displays them on the **Helm release details** page. The workloads are `DaemonSet`, `CronJob`, `Pod`, `Deployment`, and `DeploymentConfig`.

        You can upgrade, roll back, or delete a Helm release from the overflow menu in its row on the **Ecosystem** → **Helm** page.

</div>

# Using Helm in the web terminal

You can run Helm CLI commands in the web terminal.

# Creating a custom Helm chart on OpenShift Container Platform

You can create a custom Helm chart on OpenShift Container Platform to package and deploy application resources using the Helm CLI.

<div>

<div class="title">

Procedure

</div>

1.  Create a new project:

    ``` terminal
    $ oc new-project nodejs-ex-k
    ```

2.  Download an example Node.js chart that contains OpenShift Container Platform objects:

    ``` terminal
    $ git clone https://github.com/redhat-developer/redhat-helm-charts
    ```

3.  Go to the directory with the sample chart:

    ``` terminal
    $ cd redhat-helm-charts/alpha/nodejs-ex-k/
    ```

4.  Edit the `Chart.yaml` file and add a description of your chart:

    ``` yaml
    apiVersion: v2
    name: nodejs-ex-k
    description: A Helm chart for OpenShift
    icon: https://static.redhat.com/libs/redhat/brand-assets/latest/corp/logo.svg
    version: 0.2.1
    ```

    where:

    `apiVersion`
    Specifies the chart API version. It should be `v2` for Helm charts that require at least Helm 3.

    `name`
    Specifies the name of your chart.

    `description`
    Specifies the description of your chart.

    `icon`
    Specifies the URL to an image to be used as an icon.

    `version`
    Specifies the version of your chart as per the Semantic Versioning (SemVer) 2.0.0 Specification.

5.  Verify that the chart is formatted properly:

    ``` terminal
    $ helm lint
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` terminal
    [INFO] Chart.yaml: icon is recommended

    1 chart(s) linted, 0 chart(s) failed
    ```

    </div>

6.  Navigate to the previous directory level:

    ``` terminal
    $ cd ..
    ```

7.  Install the chart:

    ``` terminal
    $ helm install nodejs-chart nodejs-ex-k
    ```

8.  Verify that the chart has installed successfully:

    ``` terminal
    $ helm list
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` terminal
    NAME NAMESPACE REVISION UPDATED STATUS CHART APP VERSION
    nodejs-chart nodejs-ex-k 1 2019-12-05 15:06:51.379134163 -0500 EST deployed nodejs-0.1.0  1.16.0
    ```

    </div>

</div>

# Adding custom Helm chart repositories

As a cluster administrator, you can add custom Helm chart repositories to your cluster. The Software Catalog then displays the Helm charts from these repositories.

<div>

<div class="title">

Procedure

</div>

1.  To add a new Helm Chart Repository, you must add the Helm Chart Repository custom resource (CR) to your cluster.

    <div class="formalpara">

    <div class="title">

    Sample Helm Chart Repository CR

    </div>

    ``` yaml
    apiVersion: helm.openshift.io/v1beta1
    kind: HelmChartRepository
    metadata:
      name: <name>
    spec:
     # optional name that might be used by console
     # name: <chart-display-name>
      connectionConfig:
        url: <helm-chart-repository-url>
    ```

    </div>

    For example, to add an Azure sample chart repository, run:

    ``` terminal
    $ cat <<EOF | oc apply -f -
    apiVersion: helm.openshift.io/v1beta1
    kind: HelmChartRepository
    metadata:
      name: azure-sample-repo
    spec:
      name: azure-sample-repo
      connectionConfig:
        url: https://raw.githubusercontent.com/Azure-Samples/helm-charts/master/docs
    EOF
    ```

2.  Navigate to **Ecosystem** → **Software Catalog** and verify that it displays the Helm charts from the chart repository.

    For example, use the **Chart repositories** filter to search for a Helm chart from the repository.

    You can also verify by running the following command:

    ``` terminal
    $ oc get helmchartrepositories
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

        NAME                     AGE
        azure-sample-repo        1m

    </div>

</div>

# Adding namespace-scoped custom Helm chart repositories

The cluster-scoped `HelmChartRepository` custom resource definition (CRD) for Helm repository provides the ability for administrators to add Helm repositories as custom resources. The namespace-scoped `ProjectHelmChartRepository` CRD allows project members with the appropriate role-based access control (RBAC) permissions to create Helm repository resources of their choice but scoped to their namespace. Such project members can see charts from both cluster-scoped and namespace-scoped Helm repository resources.

<div class="note">

<div class="title">

</div>

- Administrators can limit users from creating namespace-scoped Helm repository resources. By limiting users, administrators have the flexibility to control the RBAC through a namespace role instead of a cluster role. This avoids unnecessary permission elevation for the user and prevents access to unauthorized services or applications.

- The addition of the namespace-scoped Helm repository does not impact the behavior of the existing cluster-scoped Helm repository.

</div>

As a project member with the required RBAC permissions, you can add custom namespace-scoped Helm chart repositories to your cluster. The Software Catalog then displays the Helm charts from these repositories.

<div>

<div class="title">

Procedure

</div>

1.  To add a new namespace-scoped Helm Chart Repository, you must add the Helm Chart Repository custom resource (CR) to your namespace.

    <div class="formalpara">

    <div class="title">

    Sample Namespace-scoped Helm Chart Repository CR

    </div>

    ``` yaml
    apiVersion: helm.openshift.io/v1beta1
    kind: ProjectHelmChartRepository
    metadata:
      name: <name>
    spec:
      url: https://my.chart-repo.org/stable

      # optional name that might be used by console
      name: <chart-repo-display-name>

      # optional and only needed for UI purposes
      description: <My private chart repo>

      # required: chart repository URL
      connectionConfig:
        url: <helm-chart-repository-url>
    ```

    </div>

    For example, to add an Azure sample chart repository scoped to your `my-namespace` namespace, run:

    ``` terminal
    $ cat <<EOF | oc apply --namespace my-namespace -f -
    apiVersion: helm.openshift.io/v1beta1
    kind: ProjectHelmChartRepository
    metadata:
      name: azure-sample-repo
    spec:
      name: azure-sample-repo
      connectionConfig:
        url: https://raw.githubusercontent.com/Azure-Samples/helm-charts/master/docs
    EOF
    ```

    The output confirms that you created the namespace-scoped Helm Chart Repository CR:

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

        projecthelmchartrepository.helm.openshift.io/azure-sample-repo created

    </div>

2.  Navigate to **Ecosystem** → **Software Catalog** and verify that it displays the Helm charts from the chart repository in your `my-namespace` namespace.

    For example, use the **Chart repositories** filter to search for a Helm chart from the repository.

    You can also verify by running the following command:

    ``` terminal
    $ oc get projecthelmchartrepositories --namespace my-namespace
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

        NAME                     AGE
        azure-sample-repo        1m

    </div>

</div>

# Creating credentials and CA certificates to add Helm chart repositories

Some Helm chart repositories need credentials and custom certificate authority (CA) certificates to connect to it. You can use the web console as well as the CLI to add credentials and certificates.

<div>

<div class="title">

Procedure

</div>

1.  In the `openshift-config` namespace, create a `ConfigMap` object with a custom CA certificate in PEM encoded format, and store it under the `ca-bundle.crt` key within the config map:

    ``` terminal
    $ oc create configmap helm-ca-cert \
    --from-file=ca-bundle.crt=/path/to/certs/ca.crt \
    -n openshift-config
    ```

2.  In the `openshift-config` namespace, create a `Secret` object to add the client TLS configurations:

    ``` terminal
    $ oc create secret tls helm-tls-configs \
    --cert=/path/to/certs/client.crt \
    --key=/path/to/certs/client.key \
    -n openshift-config
    ```

    Note that the client certificate and key must be in PEM encoded format and stored under the keys `tls.crt` and `tls.key`, respectively.

3.  Add the Helm repository as follows:

    ``` terminal
    $ cat <<EOF | oc apply -f -
    apiVersion: helm.openshift.io/v1beta1
    kind: HelmChartRepository
    metadata:
      name: <helm-repository>
    spec:
      name: <helm-repository>
      connectionConfig:
        url: <URL for the Helm repository>
        tlsConfig:
            name: helm-tls-configs
        ca:
        name: helm-ca-cert
    EOF
    ```

    The `ConfigMap` and `Secret` are consumed in the HelmChartRepository CR using the `tlsConfig` and `ca` fields. These certificates are used to connect to the Helm repository URL.

4.  By default, all authenticated users have access to all configured charts. However, for chart repositories where certificates are needed, you must provide users with read access to the `helm-ca-cert` config map and `helm-tls-configs` secret in the `openshift-config` namespace, as follows:

    ``` terminal
    $ cat <<EOF | kubectl apply -f -
    apiVersion: rbac.authorization.k8s.io/v1
    kind: Role
    metadata:
      namespace: openshift-config
      name: helm-chartrepos-tls-conf-viewer
    rules:
    - apiGroups: [""]
      resources: ["configmaps"]
      resourceNames: ["helm-ca-cert"]
      verbs: ["get"]
    - apiGroups: [""]
      resources: ["secrets"]
      resourceNames: ["helm-tls-configs"]
      verbs: ["get"]
    ---
    kind: RoleBinding
    apiVersion: rbac.authorization.k8s.io/v1
    metadata:
      namespace: openshift-config
      name: helm-chartrepos-tls-conf-viewer
    subjects:
      - kind: Group
        apiGroup: rbac.authorization.k8s.io
        name: 'system:authenticated'
    roleRef:
      apiGroup: rbac.authorization.k8s.io
      kind: Role
      name: helm-chartrepos-tls-conf-viewer
    EOF
    ```

</div>

# Filtering Helm Charts by their certification level

You can filter Helm charts based on their certification level in the **Developer Catalog**.

<div>

<div class="title">

Procedure

</div>

1.  In the **Developer** perspective, navigate to the **+Add** view and select a project.

2.  From the **Developer Catalog** tile, select the **Helm Chart** option to see all the Helm charts in the **Developer Catalog**.

3.  Use the filters to the left of the list of Helm charts to filter the required charts:

    - Use the **Chart Repositories** filter to filter charts provided by **Red Hat Certification Charts** or **OpenShift Helm Charts**.

    - Use the **Source** filter to filter charts sourced from **Partners**, **Community**, or **Red Hat**. Certified charts are indicated with the (![odc verified icon](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAPCAYAAADtc08vAAAABHNCSVQICAgIfAhkiAAAABl0RVh0U29mdHdhcmUAZ25vbWUtc2NyZWVuc2hvdO8Dvz4AAAAtdEVYdENyZWF0aW9uIFRpbWUARnJpIDI1IEp1biAyMDIxIDA4OjM3OjIxIFBNIElTVHv+COAAAAIiSURBVCiRXZNLaxRBFIW/W10z3RkjTojkYUaIyBAMIRqICL4IqLhRceHKpSK6cCeu8if8BW7c+MCVG3URF4IPslEXSQwIJhpIyEzeTiYz3XVddNc4WFBNNX3PuafOPS3qVAEQAFAFyc7t76rgFEz2LQECwACof2jGoxnatZEJqCfKSpwn8EUKxKSFAK5NiQBWUgWi6TYC1nfz4I0YYlV+ruww0NVBV2gJA8gJCAqqGEnlCGB9h0RheVd58m6WasPyeqbKucEiR4sBE2MlRg8VCJGWWcakOOvbV+rKs+k1JqdWoW6BgJnfm5Brcms34sHlAYb3B7Q4MuXGu/t0epWHr75AA5AEjAVrweR4/OE7j55/pOGN/GcNRgzUYljacuBCcE2wCbDNWK/jxplByOVYbHSyVnM0AcVlM8imUF3f4fP0V6g7ho+UuH3yMJf6Eu5dHWFttQZ/hE/zi3yb+5FNO2ndwYDS293JxdPjEEb8qm5R7u/m5pVTvHw/z9TsEhBy9liZ0ZEygiJtZloFIguDB2KKUY2NTZh8M0epAAvVPdAAojrl/QWK+dR18SYIWHECBq6P91AXuPtilmQ3x8J2DJKHfJM7E0Pcv9BH5FGiWZgN1tPts8K1472sV5apNELezlSYGOqhv1M5f6LIQEeb/dKKD6LOZT+T4BSawJ5TFlZqlA5GFPIBRjPpPtNtS1RV+X8pqEtjK4FJQbEDf/bZB/4C9/DXN2Sq1nsAAAAASUVORK5CYII=)) icon.

      > [!NOTE]
      > The **Source** filter will not be visible when there is only one provider type.

      You can now select the required chart and install it.

</div>

# Disabling Helm Chart repositories

You can disable Helm Charts from a particular Helm Chart Repository in the catalog by setting the `disabled` property in the `HelmChartRepository` custom resource to `true`.

<div>

<div class="title">

Procedure

</div>

- To disable a Helm Chart repository by using CLI, add the `disabled: true` flag to the custom resource. For example, to remove an Azure sample chart repository, run:

      $ cat <<EOF | oc apply -f -
      apiVersion: helm.openshift.io/v1beta1
      kind: HelmChartRepository
      metadata:
        name: azure-sample-repo
      spec:
        connectionConfig:
         url:https://raw.githubusercontent.com/Azure-Samples/helm-charts/master/docs
        disabled: true
      EOF

- To disable a recently added Helm Chart repository by using Web Console:

  1.  Go to **Custom Resource Definitions** and search for the `HelmChartRepository` custom resource.

  2.  Go to **Instances**, find the repository you want to disable, and click its name.

  3.  Go to the **YAML** tab, add the `disabled: true` flag in the `spec` section, and click `Save`.

      <div class="formalpara">

      <div class="title">

      Example

      </div>

          spec:
            connectionConfig:
              url: <url-of-the-repositoru-to-be-disabled>
            disabled: true

      </div>

      The repository is now disabled and will not appear in the catalog.

</div>

# Additional resources

- [Red Hat Helm index file](https://charts.openshift.io/index.yaml)
