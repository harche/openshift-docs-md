As a cluster administrator, you can update the Compliance Operator on your OpenShift Container Platform cluster.

<div class="important">

Updating your OpenShift Container Platform cluster to version 4.14 might cause the Compliance Operator to not work as expected. This is due to an ongoing known issue. For more information, see [OCPBUGS-18025](https://issues.redhat.com/browse/OCPBUGS-18025).

</div>

# About preparing for an Operator update

You can change the update channel to start tracking and receiving updates from a newer channel to access new features and bug fixes. The subscription of an installed Operator specifies an update channel that tracks and receives updates for the Operator.

The names of update channels in a subscription can differ between Operators, but the naming scheme typically follows a common convention within a given Operator. For example, channel names might follow a minor release update stream for the application provided by the Operator (`1.2`, `1.3`) or a release frequency (`stable`, `fast`).

<div class="note">

You cannot change installed Operators to a channel that is older than the current channel.

</div>

Red Hat Customer Portal Labs include an application that helps administrators prepare to update their Operators. See Additional resources.

# Changing the update channel for an Operator

You can change the update channel for an Operator by using the OpenShift Container Platform web console.

<div class="tip">

If the approval strategy in the subscription is set to **Automatic**, the update process initiates as soon as a new Operator version is available in the selected channel. If the approval strategy is set to **Manual**, you must manually approve pending updates.

</div>

- An Operator previously installed using Operator Lifecycle Manager (OLM).

1.  In the web console, navigate to **Ecosystem** → **Installed Operators**.

2.  Click the name of the Operator you want to change the update channel for.

3.  Click the **Subscription** tab.

4.  Click the name of the update channel under **Update channel**.

5.  Click the newer update channel that you want to change to, then click **Save**.

6.  For subscriptions with an **Automatic** approval strategy, the update begins automatically. Navigate back to the **Ecosystem** → **Installed Operators** page to monitor the progress of the update. When complete, the status changes to **Succeeded** and **Up to date**.

    For subscriptions with a **Manual** approval strategy, you can manually approve the update from the **Subscription** tab.

# Approving a pending Operator update manually

If an installed Operator has the approval strategy in its subscription set to **Manual**, you must manually approve the update before installation can begin. Manual approval reviews the changes and control when updates are applied to prevent unexpected downtime.

- An Operator previously installed using Operator Lifecycle Manager (OLM).

1.  In the OpenShift Container Platform web console, navigate to **Ecosystem** → **Installed Operators**.

2.  Operators that have a pending update display a status with **Upgrade available**. Click the name of the Operator you want to update.

3.  Click the **Subscription** tab. Any updates requiring approval are displayed next to **Upgrade status**. For example, it might display **1 requires approval**.

4.  Click **1 requires approval**, then click **Preview Install Plan**.

5.  Review the resources that are listed as available for update. When satisfied, click **Approve**.

6.  Navigate back to the **Ecosystem** → **Installed Operators** page to monitor the progress of the update. When complete, the status changes to **Succeeded** and **Up to date**.
