As a cluster administrator, you can configure additional route advertisements for your cluster. You must use the OVN-Kubernetes network plugin.

# Enabling route advertisements

As a cluster administrator, you can enable additional routing support for your cluster.

<div>

<div class="title">

Prerequisites

</div>

- You have installed the OpenShift CLI (`oc`).

- You are logged in to the cluster as a user with the `cluster-admin` role.

- The cluster is installed on compatible infrastructure.

</div>

<div>

<div class="title">

Procedure

</div>

- To enable a routing provider and additional route advertisements, enter the following command:

  ``` terminal
  $ oc patch Network.operator.openshift.io cluster --type=merge \
    -p='{
      "spec": {
        "additionalRoutingCapabilities": {
          "providers": ["FRR"]
          },
          "defaultNetwork": {
            "ovnKubernetesConfig": {
              "routeAdvertisements": "Enabled"
      }}}}'
  ```

</div>
