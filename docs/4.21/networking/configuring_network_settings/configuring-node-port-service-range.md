To meet your cluster node port requirements in OpenShift Container Platform, you can configure the node port service range during installation or expand it after installation. You can expand the default range of `30000-32768` on either side while preserving this default range within your new configuration.

> [!IMPORTANT]
> Red Hat has not performed testing outside the default port range of `30000-32768`. For ranges outside the default port range, ensure that you test to verify the expanding node port range does not impact your cluster. In particular, ensure that there is:
>
> - No overlap with any ports already in use by host processes
>
> - No overlap with any ports already in use by pods that are configured with host networking
>
> If you expanded the range and a port allocation issue occurs, create a new cluster and set the required range for it.
>
> If you expand the node port range and OpenShift CLI (`oc`) stops working because of a port conflict with the OpenShift Container Platform API server, you must create a new cluster.

# Expanding the node port range

To expand the node port range for your OpenShift Container Platform cluster after installation, you can use the `oc patch` command to update the `serviceNodePortRange` parameter. You can expand the range on either side, but you cannot shrink it after installation.

> [!IMPORTANT]
> Red Hat has not performed testing outside the default port range of `30000-32768`. For ranges outside the default port range, ensure that you test to verify that expanding your node port range does not impact your cluster. If you expanded the range and a port allocation issue occurs, create a new cluster and set the required range for it.

<div>

<div class="title">

Prerequisites

</div>

- Installed the OpenShift CLI (`oc`).

- Logged in to the cluster as a user with `cluster-admin` privileges.

- You ensured that your cluster infrastructure allows access to the ports that exist in the extended range. For example, if you expand the node port range to `30000-32900`, your firewall or packet filtering configuration must allow the inclusive port range of `30000-32900`.

</div>

<div>

<div class="title">

Procedure

</div>

- To expand the range for the `serviceNodePortRange` parameter in the `network.config.openshift.io` object that your cluster uses to manage traffic for pods, enter the following command:

  ``` terminal
  $ oc patch network.config.openshift.io cluster --type=merge -p \
    '{
      "spec":
        { "serviceNodePortRange": "<port_range>" }
    }'
  ```

  where:

  `<port_range>`
  Specifies the expanded range, such as `30000-32900`.

  > [!TIP]
  > You can also apply the following YAML to update the node port range:
  >
  > ``` yaml
  > apiVersion: config.openshift.io/v1
  > kind: Network
  > metadata:
  >   name: cluster
  > spec:
  >   serviceNodePortRange: "<port_range>"
  > # ...
  > ```

  <div class="formalpara">

  <div class="title">

  Example output

  </div>

  ``` terminal
  network.config.openshift.io/cluster patched
  ```

  </div>

</div>

<div>

<div class="title">

Verification

</div>

- To confirm that the updated configuration is active, enter the following command. The update can take several minutes to apply.

  ``` terminal
  $ oc get configmaps -n openshift-kube-apiserver config \
    -o jsonpath="{.data['config\.yaml']}" | \
    grep -Eo '"service-node-port-range":["[[:digit:]]+-[[:digit:]]+"]'
  ```

  <div class="formalpara">

  <div class="title">

  Example output

  </div>

  ``` terminal
  "service-node-port-range":["30000-32900"]
  ```

  </div>

</div>

# Additional resources

- [Configuring ingress cluster traffic using a NodePort](../../networking/ingress_load_balancing/configuring_ingress_cluster_traffic/configuring-ingress-cluster-traffic-nodeport.xml#configuring-ingress-cluster-traffic-nodeport)

- [Network \[config.openshift.io/v1](../../rest_api/config_apis/network-config-openshift-io-v1.xml#network-config-openshift-io-v1)\]

- [Service \[core/v1](../../rest_api/network_apis/service-v1.xml#service-v1)\]
