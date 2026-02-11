The steps for removing the Red Hat OpenShift Distributed Tracing Platform from an OpenShift Container Platform cluster are as follows:

1.  Shut down all Distributed Tracing Platform pods.

2.  Remove any TempoStack instances.

3.  Remove the Tempo Operator.

# Removing by using the web console

You can remove a TempoStack instance in the **Administrator** view of the web console.

- You are logged in to the OpenShift Container Platform web console as a cluster administrator with the `cluster-admin` role.

- For Red Hat OpenShift Dedicated, you must be logged in using an account with the `dedicated-admin` role.

1.  Go to **Ecosystem** → **Installed Operators** → **Tempo Operator** → **TempoStack**.

2.  To remove the TempoStack instance, select ![kebab](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABsAAAAjCAIAAADqn+bCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAA+0lEQVRIie2WMQqEMBBFJ47gUXRBLyBYqbUXULCx9CR2XsAb6AlUEM9kpckW7obdZhwWYWHXX/3i8TPJZEKEUgpOlXFu3JX4V4kmB2qaZhgGKSUiZlkWxzEBC84N9zxv27bdO47Tti0Bs3at4wBgXVca/lJnfN/XPggCGmadIwAsywIAiGhZFk1ydy2EYJKgGCqK4vZUVVU0zKpxnmftp2mi4S/1GhG1N82DMWNNYVmW4zgqpRAxTVMa5t4evlg11nXd9/1eY57nSZIQMKtG13WllLu3bbvrOgJmdUbHwfur8Xniqw6Hh5UYRdGDNowwDA+WvP4UV+JPJ94B1gKUWcTOCT0AAAAASUVORK5CYII=) → **Delete TempoStack** → **Delete**.

3.  Optional: Remove the Tempo Operator.

# Removing by using the CLI

You can remove a TempoStack instance on the command line.

- An active OpenShift CLI (`oc`) session by a cluster administrator with the `cluster-admin` role.

  <div class="tip">

  - Ensure that your OpenShift CLI (`oc`) version is up to date and matches your OpenShift Container Platform version.

  - Run `oc login`:

    ``` terminal
    $ oc login --username=<your_username>
    ```

  </div>

1.  Get the name of the TempoStack instance by running the following command:

    ``` terminal
    $ oc get deployments -n <project_of_tempostack_instance>
    ```

2.  Remove the TempoStack instance by running the following command:

    ``` terminal
    $ oc delete tempo <tempostack_instance_name> -n <project_of_tempostack_instance>
    ```

3.  Optional: Remove the Tempo Operator.

<!-- -->

1.  Run the following command to verify that the TempoStack instance is not found in the output, which indicates its successful removal:

    ``` terminal
    $ oc get deployments -n <project_of_tempostack_instance>
    ```

# Additional resources

- [Deleting Operators from a cluster](../../operators/admin/olm-deleting-operators-from-cluster.xml#olm-deleting-operators-from-a-cluster)

- [Getting started with the OpenShift CLI](../../cli_reference/openshift_cli/getting-started-cli.xml#getting-started-cli)
