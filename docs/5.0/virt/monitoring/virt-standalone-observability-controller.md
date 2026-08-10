You can decouple OpenShift Virtualization monitoring from the main deployment by using the standalone observability controller. The controller externalizes monitoring into a standalone Operator.

<div class="important">

The standalone observability controller is a Technology Preview feature only. Technology Preview features are not supported with Red Hat production service level agreements (SLAs) and might not be functionally complete. Red Hat does not recommend using them in production. These features provide early access to upcoming product features, enabling customers to test functionality and provide feedback during the development process.

For more information about the support scope of Red Hat Technology Preview features, see [Technology Preview Features Support Scope](https://access.redhat.com/support/offerings/techpreview/).

</div>

The standalone observability controller provides the following capabilities:

- Prometheus metrics for OpenShift Virtualization resources, including virtual machines, virtual machine instances, migrations, and instance types.

- Alerting rules and recording rules, reconciled through `PrometheusRule` custom resources.

- Metric collection endpoints, reconciled through `ServiceMonitor` custom resources.

# Enable the standalone observability controller

You can enable the standalone observability controller by setting the `deployObservabilityController` feature gate in the `HyperConverged` custom resource (CR). By enabling the standalone observability controller, you can update monitoring and alerts independently of the OpenShift Virtualization control plane.

<div class="important">

The standalone observability controller is a Technology Preview feature only. Technology Preview features are not supported with Red Hat production service level agreements (SLAs) and might not be functionally complete. Red Hat does not recommend using them in production. These features provide early access to upcoming product features, enabling customers to test functionality and provide feedback during the development process.

For more information about the support scope of Red Hat Technology Preview features, see [Technology Preview Features Support Scope](https://access.redhat.com/support/offerings/techpreview/).

</div>

- You have access to the cluster as a user with `cluster-admin` permissions.

- You have installed the OpenShift CLI (`oc`).

<!-- -->

- Enable the `deployObservabilityController` feature gate by running the following command:

  ``` terminal
  $ oc patch hco kubevirt-hyperconverged -n openshift-cnv \
    --type json -p '[{"op": "add", "path": "/spec/featureGates/-", \
    "value": {"name": "deployObservabilityController"}}]'
  ```

<!-- -->

- Verify that the feature gate is enabled by running the following command:

  ``` terminal
  $ oc get hco kubevirt-hyperconverged -n openshift-cnv \
    -o jsonpath='{.spec.featureGates}'
  ```

  <div class="formalpara-title">

  **Expected output**

  </div>

  ``` json
  [{"name":"deployObservabilityController"}]
  ```
