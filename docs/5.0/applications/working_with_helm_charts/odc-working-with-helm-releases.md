You can use the web console to create, update, roll back, or delete a Helm release.

# Installing a Helm release from a URL

A Helm release is a deployed instance of a Helm chart within your OpenShift Container Platform cluster. You can install charts from the Software Catalog or by using a direct chart URL. Using a direct URL avoids the need for a configured Helm repository. However, this method circumvents the validation that the Software Catalog provides. Use the direct URL method only when a chart is not available from the Software Catalog or configured repositories.

> [!WARNING]
> Install charts only from URLs you trust, because unverified charts can introduce security risks to your cluster. When possible, use charts from the Software Catalog or a configured Helm repository instead.

<div>

<div class="title">

Prerequisites

</div>

- You’ve logged in to the OpenShift Container Platform web console.

- You have the necessary project permissions to install a Helm chart.

- You have a URL for a Helm chart.

</div>

<div>

<div class="title">

Procedure

</div>

1.  In the OpenShift Container Platform web console, select **Ecosystem \> Helm** from the navigation menu. The **Helm** view opens.

2.  In the **Project** drop-down menu, select the project where you want to install the Helm release; for example, **default**.

3.  From the **Helm Releases** tab, click **Create**.

4.  Select **Helm chart URL**. The **Install Helm chart from URL** view opens.

5.  In the **Chart URL** field, enter the URL for the Helm chart you want to install.

    > [!NOTE]
    > For Helm charts stored in an OCI-compliant registry, the URL must use the `oci://` protocol; for example, `oci://quay.io/organization/repository/chart-name`.

6.  In the **Release name** field, enter a name for the Helm release you want to install.

7.  In the **Chart version** field, enter the chart version number if it is not detected automatically.

8.  Click **Next**. The **Configure Helm release** view opens.

    - Review the configuration. Make sure that **Chart URL**, **Release name**, and **Chart version** are correct.

9.  For the **Configure via** option, select either **Form view** or **YAML view**.

    - Choose **Form view** (the default) for a guided configuration of standard parameters.

    - Choose **YAML view** if you need to change advanced settings that are not available in Form view.

      > [!NOTE]
      > The **Form view** might not display every field from your Helm chart. For full control over all configuration parameters, select **YAML view**.

10. Click **Install**. The **Helm Releases** tab opens and displays a status of **Deployed** if the installation succeeds.

</div>

<div>

<div class="title">

Verification

</div>

- The **Helm Releases** tab displays the new Helm release in the table.

- The **Status** column for the Helm release displays **Deployed**.

</div>

<div>

<div class="title">

Additional resources

</div>

- [Official Helm documentation](https://helm.sh)

- [Quay OCI artifact support for Helm charts](https://www.redhat.com/en/blog/quay-oci-artifact-support-for-helm-charts)

</div>

# Upgrading a Helm release

You can upgrade a Helm release to use a new chart version or update your release configuration.

<div>

<div class="title">

Procedure

</div>

1.  Navigate to **Ecosystem** → **Helm**.

2.  Click the overflow menu in the release’s row and select **Upgrade Helm Release**.

3.  On the **Upgrade Helm Release** page, select the chart version you want if available, edit the values as needed, then click **Upgrade** to create a revision of the Helm release. The **Ecosystem** → **Helm** page shows the updated revision count.

</div>

# Roll back a Helm release

If upgrading a release fails, you can roll back the Helm release to an earlier version.

<div>

<div class="title">

Procedure

</div>

1.  Navigate to **Ecosystem** → **Helm**.

2.  Click the overflow menu in the release’s row and select **Rollback**.

3.  On the Rollback Helm Release page, select the Revision you want to roll back to and click **Rollback**.

4.  On the **Ecosystem** → **Helm** page, click the chart to see the details and resources for that release.

5.  Go to the **Revision History** tab to see all the revisions for the chart.

6.  Optional: Click the overflow menu next to a revision and select the revision to roll back to.

</div>

# Deleting a Helm release

You can delete a Helm release that you no longer need.

<div>

<div class="title">

Procedure

</div>

1.  Navigate to **Ecosystem** → **Helm**.

2.  Click the overflow menu in the release’s row and select **Delete Helm Release**.

3.  In the confirmation prompt, enter the name of the release and click **Delete**.

</div>

# Additional resources

- [OpenShift web console](https://console.redhat.com/openshift/overview)
