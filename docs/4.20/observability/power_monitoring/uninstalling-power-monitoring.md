> [!IMPORTANT]
> Power monitoring is a Technology Preview feature only. Technology Preview features are not supported with Red Hat production service level agreements (SLAs) and might not be functionally complete. Red Hat does not recommend using them in production. These features provide early access to upcoming product features, enabling customers to test functionality and provide feedback during the development process.
>
> For more information about the support scope of Red Hat Technology Preview features, see [Technology Preview Features Support Scope](https://access.redhat.com/support/offerings/techpreview/).

You can uninstall power monitoring by deleting the Kepler instance and then the Power Monitoring Operator in the OpenShift Container Platform web console.

# Deleting Kepler

You can delete Kepler by removing the Kepler instance of the `Kepler` custom resource definition (CRD) from the OpenShift Container Platform web console.

> [!IMPORTANT]
> Starting with power monitoring for Red Hat OpenShift 0.5 (Technology Preview), use the `PowerMonitor` CRD, and remove all instances of the `Kepler` CRD.

<div>

<div class="title">

Prerequisites

</div>

- You have access to the OpenShift Container Platform web console.

- You are logged in as a user with the `cluster-admin` role.

</div>

<div>

<div class="title">

Procedure

</div>

1.  In the web console, go to **Ecosystem** → **Installed Operators**.

2.  Click **Power monitoring for Red Hat OpenShift** from the **Installed Operators** list and go to the **Kepler** tab.

3.  Locate the Kepler instance entry in the list.

4.  Click ![kebab](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABsAAAAjCAIAAADqn+bCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAA+0lEQVRIie2WMQqEMBBFJ47gUXRBLyBYqbUXULCx9CR2XsAb6AlUEM9kpckW7obdZhwWYWHXX/3i8TPJZEKEUgpOlXFu3JX4V4kmB2qaZhgGKSUiZlkWxzEBC84N9zxv27bdO47Tti0Bs3at4wBgXVca/lJnfN/XPggCGmadIwAsywIAiGhZFk1ydy2EYJKgGCqK4vZUVVU0zKpxnmftp2mi4S/1GhG1N82DMWNNYVmW4zgqpRAxTVMa5t4evlg11nXd9/1eY57nSZIQMKtG13WllLu3bbvrOgJmdUbHwfur8Xniqw6Hh5UYRdGDNowwDA+WvP4UV+JPJ94B1gKUWcTOCT0AAAAASUVORK5CYII=) for this entry and select **Delete Kepler**.

5.  In the **Delete Kepler?** dialog, click **Delete** to delete the Kepler instance.

</div>

# Deleting the PowerMonitor custom resource

You can delete the `PowerMonitor` custom resource (CR) by removing the `power-monitor` instance of the `PowerMonitor` CR from the OpenShift Container Platform web console.

<div>

<div class="title">

Prerequisites

</div>

- You have access to the OpenShift Container Platform web console.

- You are logged in as a user with the `cluster-admin` role.

</div>

<div>

<div class="title">

Procedure

</div>

1.  In the web console, go to **Ecosystem** → **Installed Operators**.

2.  Click **Power monitoring for Red Hat OpenShift** from the **Installed Operators** list and go to the **PowerMonitor** tab.

3.  Locate the **PowerMonitor** instance entry in the list.

4.  Click the ![kebab](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABsAAAAjCAIAAADqn+bCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAA+0lEQVRIie2WMQqEMBBFJ47gUXRBLyBYqbUXULCx9CR2XsAb6AlUEM9kpckW7obdZhwWYWHXX/3i8TPJZEKEUgpOlXFu3JX4V4kmB2qaZhgGKSUiZlkWxzEBC84N9zxv27bdO47Tti0Bs3at4wBgXVca/lJnfN/XPggCGmadIwAsywIAiGhZFk1ydy2EYJKgGCqK4vZUVVU0zKpxnmftp2mi4S/1GhG1N82DMWNNYVmW4zgqpRAxTVMa5t4evlg11nXd9/1eY57nSZIQMKtG13WllLu3bbvrOgJmdUbHwfur8Xniqw6Hh5UYRdGDNowwDA+WvP4UV+JPJ94B1gKUWcTOCT0AAAAASUVORK5CYII=) for this entry and select **Delete PowerMonitor**.

5.  In the **Delete PowerMonitor?** dialog, click **Delete** to delete the `PowerMonitor` instance.

</div>

# Uninstalling the Power Monitoring Operator

If you installed the Power Monitoring Operator by using the software catalog, you can uninstall it from the OpenShift Container Platform web console.

<div>

<div class="title">

Prerequisites

</div>

- You have access to the OpenShift Container Platform web console.

- You are logged in as a user with the `cluster-admin` role.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Delete the Kepler instance.

    > [!WARNING]
    > Ensure that you have deleted the Kepler instance before uninstalling the Power Monitoring Operator.

2.  Go to **Ecosystem** → **Installed Operators**.

3.  Locate the **Power monitoring for Red Hat OpenShift** entry in the list.

4.  Click ![kebab](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABsAAAAjCAIAAADqn+bCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAA+0lEQVRIie2WMQqEMBBFJ47gUXRBLyBYqbUXULCx9CR2XsAb6AlUEM9kpckW7obdZhwWYWHXX/3i8TPJZEKEUgpOlXFu3JX4V4kmB2qaZhgGKSUiZlkWxzEBC84N9zxv27bdO47Tti0Bs3at4wBgXVca/lJnfN/XPggCGmadIwAsywIAiGhZFk1ydy2EYJKgGCqK4vZUVVU0zKpxnmftp2mi4S/1GhG1N82DMWNNYVmW4zgqpRAxTVMa5t4evlg11nXd9/1eY57nSZIQMKtG13WllLu3bbvrOgJmdUbHwfur8Xniqw6Hh5UYRdGDNowwDA+WvP4UV+JPJ94B1gKUWcTOCT0AAAAASUVORK5CYII=) for this entry and select **Uninstall Operator**.

5.  In the **Uninstall Operator?** dialog, click **Uninstall** to uninstall the Power Monitoring Operator.

</div>
