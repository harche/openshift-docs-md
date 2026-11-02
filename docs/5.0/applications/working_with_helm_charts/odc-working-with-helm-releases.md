You can use the web console to create, update, roll back, or delete a Helm release.

# Installing a Helm release from a URL

A Helm release is a deployed instance of a Helm chart in your OpenShift Container Platform cluster. You can install a Helm release directly from a chart URL instead of from the software catalog.

Usually, you install charts from the software catalog in the web console. By default, the catalog lists charts that Red Hat provides, and administrators can add more charts for the whole cluster or for a single namespace. If you need only one or two charts, you can skip adding them to the catalog and install a chart directly from its URL instead. However, a chart that you install from a URL does not get the review that Red Hat and your administrators give catalog charts, so use this method only when you trust the source of the chart.

> [!WARNING]
> Charts that Red Hat or your administrators have not reviewed can introduce security risks to your cluster.

<div>

<div class="title">

Prerequisites

</div>

- You have logged in to the OpenShift Container Platform web console.

- You have the necessary project permissions to install a Helm chart.

- You have a URL for a Helm chart.

</div>

<div>

<div class="title">

Procedure

</div>

1.  In the OpenShift Container Platform web console, navigate to **Ecosystem \> Helm**. The **Helm** view opens.

2.  In the **Project** drop-down menu, select the project where you want to install the Helm release; for example, **default**.

3.  From the **Helm releases** tab, click **Create**.

4.  Select **Helm chart URL**. The **Install Helm chart from URL** view opens.

5.  In the **Chart URL** field, enter the URL for the Helm chart you want to install.

    > [!NOTE]
    > For Helm charts stored in an OCI-compliant registry, the URL must use the `oci://` protocol; for example, `oci://quay.io/organization/repository/chart-name`.

6.  In the **Release name** field, enter a name for the Helm release you want to install.

7.  In the **Chart version** field, enter the chart version number if the web console does not detect it automatically.

8.  Optional: If the chart URL requires authentication, select a secret from the **Secret for Basic authentication** list. If the secret you need does not exist, create it:

    1.  From the **Secret for Basic authentication** list, select **Create Secret**. The **Create authentication Secret** dialog opens.

    2.  In the **Secret name** field, enter a unique name for the secret.

    3.  Optional: In the **Secret username** field, enter the username for the chart URL.

    4.  In the **Secret password or token** field, enter the password or token for the chart URL.

    5.  Click **Create**. The web console selects the new secret in the **Secret for Basic authentication** list.

9.  Click **Next**. The **Configure Helm release** view opens.

10. Review the configuration. Make sure that the **Chart URL**, **Release name**, and **Version** fields are correct.

11. For the **Configure via** option, select either **Form view** or **YAML view**.

    - Choose **Form view** (the default) for a guided configuration of standard parameters.

    - Choose **YAML view** if you need to change advanced settings that are not available in **Form view**.

      > [!NOTE]
      > The **Form view** might not display every field from your Helm chart. If the chart does not include a values schema, **Form view** is unavailable and you must use **YAML view**. For full control over all configuration parameters, select **YAML view**.

12. Click **Install**. The **Helm releases** tab opens and displays a status of **Deployed** if the installation succeeds.

</div>

<div>

<div class="title">

Verification

</div>

- The **Helm releases** tab displays the new Helm release in the table.

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

2.  Click the overflow menu in the release’s row and select **Upgrade Helm release**.

3.  On the **Upgrade Helm release** page, select the chart version you want, if available.

4.  Optional: If the release uses a chart URL that requires authentication, select a secret from the **Secret for Basic authentication** list. If you selected a secret when you installed the release, that secret is already selected. If that secret no longer exists, the page displays a notification, and you must select or create a different secret.

5.  Edit the values as needed, then click **Upgrade** to create a revision of the Helm release. The **Ecosystem** → **Helm** page shows the updated revision count.

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
