You can configure how the control plane handles concurrency when you create or migrate virtual machines (VMs). For example, set the `QPS` or `burst` rates to batch create virtual machines (VMs) in a batch, or tune migration settings in the `HyperConverged` custom resource (CR).

# Tune the rate limit

You can tune the rate limit when creating and maintaining a large number of virtual machines (VMs) in one cluster.

The `hco.kubevirt.io/tuningPolicy` annotation is used to configure the rate limit. The annotation is only taken into account if the `annotation` tuning policy is applied to the HyperConverged CR.

- You have installed the OpenShift CLI (`oc`).

1.  Annotate the HyperConverged CR with the `hco.kubevirt.io/tuningPolicy` annotation, and a value of a json object with the following fields:

    - `qps`: indicates the maximum QPS to the apiserver from this client.

    - `burst`: Maximum burst for throttle.

      For example, to set the `qps` to 100 and the `burst` to 200, use the following command:

    ``` terminal
    $ oc annotate hco kubevirt-hyperconverged -n openshift-cnv 'hco.kubevirt.io/tuningPolicy={"qps": 100, "burst": 200}'
    ```

2.  Apply the following patch to enable the `annotation` tuning policy:

    ``` terminal
    $ oc patch hco kubevirt-hyperconverged -n openshift-cnv \
      --type=json -p='[{"op": "add", "path": "/spec/virtualization/tuningPolicy", \
      "value": "annotation"}]'
    ```

- Run the following command to verify the rate limit tuning:

  ``` terminal
  $ oc get kubevirt.kubevirt.io/kubevirt-kubevirt-hyperconverged \
    -n openshift-cnv -o go-template --template='{{range $config, \
    $value := .spec.configuration}} {{if eq $config "apiConfiguration" \
    "webhookConfiguration" "controllerConfiguration" "handlerConfiguration"}} \
    {{"\n"}} {{$config}} = {{$value}} {{end}} {{end}} {{"\n"}}
  ```
