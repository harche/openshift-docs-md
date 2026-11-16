OpenShift Container Platform administrators can control the level of overcommit and manage container density on developer containers by using the ClusterResourceOverride Operator.

> [!NOTE]
> In OpenShift Container Platform, you must enable cluster-level overcommit. Node overcommitment is enabled by default.

In an *overcommitted* state, the sum of the container compute resource requests and limits exceeds the resources available on the system. For example, you might want to use overcommitment in development environments where a trade-off of guaranteed performance for capacity is acceptable.

Containers can specify compute resource requests and limits. Requests are used for scheduling your container and provide a minimum service guarantee. Limits constrain the amount of compute resource that can be consumed on your node.

The scheduler attempts to optimize the compute resource use across all nodes in your cluster. It places pods onto specific nodes, taking the pods' compute resource requests and nodes' available capacity into consideration.

# Resource requests and overcommitment

You can use resource requests in an overcommitted environment help you ensure that your cluster is properly configured.

For each compute resource, a container can specify a resource request and limit. Scheduling decisions are made based on the request to ensure that a node has enough capacity available to meet the requested value. If a container specifies limits, but omits requests, the requests are defaulted to the limits. A container is not able to exceed the specified limit on the node.

The enforcement of limits is dependent upon the compute resource type. If a container makes no request or limit, the container is scheduled to a node with no resource guarantees. In practice, the container is able to consume as much of the specified resource as is available with the lowest local priority. In low resource situations, containers that specify no resource requests are given the lowest quality of service.

Scheduling is based on resources requested, where quota and hard limits refer to resource limits, which can be set higher than requested resources. The difference between the request and the limit determines the level of overcommit. For example, if a container is given a memory request of 1Gi and a memory limit of 2Gi, the container is scheduled based on the 1Gi request being available on the node, but could use up to 2Gi; so it is 100% overcommitted.

# Cluster-level overcommit using the Cluster Resource Override Operator

You can use the Cluster Resource Override Operator to control the level of overcommit and manage container density across all the nodes in your cluster. The Operator, which is an admission webhook, controls how nodes in specific projects can exceed defined memory and CPU limits.

The Operator modifies the ratio between the requests and limits that are set on developer containers. In conjunction with a per-project limit range that specifies limits and defaults, you can achieve the desired level of overcommit.

You must install the Cluster Resource Override Operator by using the OpenShift Container Platform console or CLI as shown in the following sections. After you deploy the Cluster Resource Override Operator, the Operator modifies all new pods in specific namespaces. The Operator does not edit pods that existed before you deployed the Operator.

During the installation, you create a `ClusterResourceOverride` custom resource (CR), where you set the level of overcommit, as shown in the following example:

``` yaml
apiVersion: operator.autoscaling.openshift.io/v1
kind: ClusterResourceOverride
metadata:
    name: cluster
spec:
  podResourceOverride:
    spec:
      memoryRequestToLimitPercent: 50
      cpuRequestToLimitPercent: 25
      limitCPUToMemoryPercent: 200
      cpuRequestToRequestPercent: 50
# ...
```

where:

`metadata.name`
Specifies a name for the object. The name must be `cluster`.

`spec.podResourceOverride.spec.memoryRequestToLimitPercent`
If a container memory limit has been specified or defaulted, the memory request is overridden to this percentage of the limit, between 1-100. The default is 50.

`spec.podResourceOverride.spec.cpuRequestToLimitPercent`
If a container CPU limit has been specified or defaulted, the CPU request is overridden to this percentage of the limit, between 1-100. The default is 25.

`spec.podResourceOverride.spec.limitCPUToMemoryPercent`
If a container memory limit has been specified or defaulted, the CPU limit is overridden to a percentage of the memory limit, if specified. Scaling 1Gi of RAM at 100 percent is equal to 1 CPU core. This is processed before overriding the CPU request (if configured). The default is 200.

`spec.podResourceOverride.spec.cpuRequestToRequestPercent`
If a container CPU request has been specified or defaulted, the CPU request is overridden to this percentage of that submitted request, from 1 to 100. The webhook applies this parameter after the other override parameters. The percentage comes from the CPU request in the submitted pod, before those parameters change it. You can use this parameter when the container has no CPU limit. This parameter is optional.

> [!NOTE]
> The `memoryRequestToLimitPercent`, `cpuRequestToLimitPercent`, and `limitCPUToMemoryPercent` parameters have no effect unless the container has a limit, or a `LimitRange` object defaults one. The `cpuRequestToRequestPercent` parameter applies when the container has a CPU request, or a `LimitRange` object defaults one. That parameter does not require a CPU limit.

Set limits and requests in the pod spec or in a `LimitRange` object for each namespace for these overrides to apply.

When configured, you can enable overrides on a per-project basis by applying the following label to the `Namespace` object for each project where you want the overrides to apply. For example, you can configure override so that infrastructure components are not subject to the overrides.

``` yaml
apiVersion: v1
kind: Namespace
metadata:

# ...

  labels:
    clusterresourceoverrides.admission.autoscaling.openshift.io/enabled: "true"

# ...
```

A pod in a namespace with this label uses the ratios from the `ClusterResourceOverride` object unless a `ResourceOverride` object in that namespace matches the pod. If a pod in a project with this label matches a `ResourceOverride` object in that namespace, the webhook applies the ratios in the `ResourceOverride` object. For more information, see "Namespace-level resource overrides" in this section.

The Operator watches for the `ClusterResourceOverride` CR and ensures that the `ClusterResourceOverride` admission webhook is installed into the same namespace as the operator.

For example, a pod has the following resource limits and CPU request:

``` yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
  namespace: my-namespace
# ...
spec:
  containers:
    - name: hello-openshift
      image: openshift/hello-openshift
      resources:
        limits:
          memory: "512Mi"
          cpu: "2000m"
        requests:
          cpu: "2000m"
# ...
```

The Cluster Resource Override Operator intercepts the original pod request, then overrides the resources according to the configuration set in the `ClusterResourceOverride` object.

``` yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
  namespace: my-namespace
# ...
spec:
  containers:
  - image: openshift/hello-openshift
    name: hello-openshift
    resources:
      limits:
        cpu: "1"
        memory: 512Mi
      requests:
        cpu: 1000m
        memory: 256Mi
# ...
```

where:

`spec.containers.resources.limits.cpu`
Specifies that the CPU limit has been overridden to `1` because the `limitCPUToMemoryPercent` parameter is set to `200` in the `ClusterResourceOverride` object. As such, 200% of the memory limit, 512Mi in CPU terms, is 1 CPU core.

`spec.containers.resources.requests.cpu`
Specifies that the CPU request is `1000m` because the `cpuRequestToRequestPercent` parameter is `50` and the submitted CPU request is `2000m`. The webhook applies the `cpuRequestToRequestPercent` parameter after the `cpuRequestToLimitPercent` parameter. With the `cpuRequestToLimitPercent` parameter set to `25`, that parameter would set the request to `250m`, which is 25% of the overridden 1 CPU limit. The `cpuRequestToRequestPercent` parameter then sets the final request from the submitted `2000m`.

`spec.containers.resources.requests.memory`
Specifies that the memory request is `256Mi` because the `memoryRequestToLimitPercent` parameter is `50`. As such, 50% of the 512Mi memory limit is 256Mi.

## Install the Cluster Resource Override Operator using the web console

You can use the OpenShift Container Platform web console to install the Cluster Resource Override Operator to help you control overcommit in your cluster.

By default, the installation process creates a Cluster Resource Override Operator pod on a worker node in the `clusterresourceoverride-operator` namespace. You can move this pod to another node, such as an infrastructure node, as needed. Infrastructure nodes are not counted toward the total number of subscriptions that are required to run the environment. For more information, see "Moving the Cluster Resource Override Operator pods".

<div>

<div class="title">

Prerequisites

</div>

- The Cluster Resource Override Operator has no effect if limits have not been set on containers. You must specify default limits for a project using a `LimitRange` object or configure limits in `Pod` specs for the overrides to apply.

</div>

<div>

<div class="title">

Procedure

</div>

1.  In the OpenShift Container Platform web console, navigate to **Home** → **Projects**

    1.  Click **Create Project**.

    2.  Specify `clusterresourceoverride-operator` as the name of the project.

    3.  Click **Create**.

2.  Navigate to **Ecosystem** → **Software Catalog**.

    1.  Choose **ClusterResourceOverride Operator** from the list of available Operators and click **Install**.

    2.  On the **Install Operator** page, make sure **A specific Namespace on the cluster** is selected for **Installation Mode**.

    3.  Make sure **clusterresourceoverride-operator** is selected for **Installed Namespace**.

    4.  Select an **Update Channel** and **Approval Strategy**.

    5.  Click **Install**.

3.  On the **Installed Operators** page, click **ClusterResourceOverride**.

    1.  On the **ClusterResourceOverride Operator** details page, click **Create ClusterResourceOverride**.

    2.  On the **Create ClusterResourceOverride** page, click **YAML view** and edit the YAML template to set the overcommit values as needed:

        ``` yaml
        apiVersion: operator.autoscaling.openshift.io/v1
        kind: ClusterResourceOverride
        metadata:
          name: cluster
        spec:
          podResourceOverride:
            spec:
              memoryRequestToLimitPercent: 50
              cpuRequestToLimitPercent: 25
              limitCPUToMemoryPercent: 200
        ```

        where:

        `metadata.name`
        Specifies a name for the CR. The name must be `cluster`.

        `spec.podResourceOverride.spec.memoryRequestToLimitPercent`
        Specifies the percentage to override the container memory limit, if used, between 1-100. The default is `50`. This parameter is optional.

        `spec.podResourceOverride.spec.cpuRequestToLimitPercent`
        Specifies the percentage of the container CPU limit to use as the CPU request, if a CPU limit is set, between 1-100. The default is `25`. This parameter is optional.

        `spec.podResourceOverride.spec.limitCPUToMemoryPercent`
        Specifies the percentage of the container memory limit to use as the CPU limit, if a memory limit is set. Scaling 1 Gi of RAM at 100 percent is equal to 1 CPU core. This is processed before overriding the CPU request, if configured. The default is `200`. This parameter is optional.

    3.  Click **Create**.

4.  Check the current state of the admission webhook by checking the status of the cluster custom resource:

    1.  On the **ClusterResourceOverride Operator** page, click **cluster**.

    2.  On the **ClusterResourceOverride Details** page, click **YAML**. The `mutatingWebhookConfigurationRef` section displays when the webhook is called.

        ``` yaml
        apiVersion: operator.autoscaling.openshift.io/v1
        kind: ClusterResourceOverride
        metadata:
          annotations:
            kubectl.kubernetes.io/last-applied-configuration: |
              {"apiVersion":"operator.autoscaling.openshift.io/v1","kind":"ClusterResourceOverride","metadata":{"annotations":{},"name":"cluster"},"spec":{"podResourceOverride":{"spec":{"cpuRequestToLimitPercent":25,"limitCPUToMemoryPercent":200,"memoryRequestToLimitPercent":50}}}}
          creationTimestamp: "2019-12-18T22:35:02Z"
          generation: 1
          name: cluster
          resourceVersion: "127622"
          selfLink: /apis/operator.autoscaling.openshift.io/v1/clusterresourceoverrides/cluster
          uid: 978fc959-1717-4bd1-97d0-ae00ee111e8d
        spec:
          podResourceOverride:
            spec:
              cpuRequestToLimitPercent: 25
              limitCPUToMemoryPercent: 200
              memoryRequestToLimitPercent: 50
        status:

        # ...

            mutatingWebhookConfigurationRef:
              apiVersion: admissionregistration.k8s.io/v1
              kind: MutatingWebhookConfiguration
              name: clusterresourceoverrides.admission.autoscaling.openshift.io
              resourceVersion: "127621"
              uid: 98b3b8ae-d5ce-462b-8ab5-a729ea8f38f3

        # ...
        ```

        where:

        `status.mutatingWebhookConfigurationRef`
        Specifies the `ClusterResourceOverride` admission webhook.

</div>

## Install the Cluster Resource Override Operator using the CLI

You can use the OpenShift CLI to install the Cluster Resource Override Operator to help you control overcommit in your cluster.

By default, the installation process creates a Cluster Resource Override Operator pod on a worker node in the `clusterresourceoverride-operator` namespace. You can move this pod to another node, such as an infrastructure node, as needed. Infrastructure nodes are not counted toward the total number of subscriptions that are required to run the environment. For more information, see "Moving the Cluster Resource Override Operator pods".

<div>

<div class="title">

Prerequisites

</div>

- The Cluster Resource Override Operator has no effect if limits have not been set on containers. You must specify default limits for a project using a `LimitRange` object or configure limits in `Pod` specs for the overrides to apply.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Create a namespace for the Cluster Resource Override Operator:

    1.  Create a `Namespace` object YAML file (for example, `cro-namespace.yaml`) for the Cluster Resource Override Operator:

        ``` yaml
        apiVersion: v1
        kind: Namespace
        metadata:
          name: clusterresourceoverride-operator
        ```

    2.  Create the namespace:

        ``` terminal
        $ oc create -f <file-name>.yaml
        ```

        For example:

        ``` terminal
        $ oc create -f cro-namespace.yaml
        ```

2.  Create an Operator group:

    1.  Create an `OperatorGroup` object YAML file (for example, cro-og.yaml) for the Cluster Resource Override Operator:

        ``` yaml
        apiVersion: operators.coreos.com/v1
        kind: OperatorGroup
        metadata:
          name: clusterresourceoverride-operator
          namespace: clusterresourceoverride-operator
        spec:
          targetNamespaces:
            - clusterresourceoverride-operator
        ```

    2.  Create the Operator Group:

        ``` terminal
        $ oc create -f <file-name>.yaml
        ```

        For example:

        ``` terminal
        $ oc create -f cro-og.yaml
        ```

3.  Create a subscription:

    1.  Create a `Subscription` object YAML file (for example, cro-sub.yaml) for the Cluster Resource Override Operator:

        ``` yaml
        apiVersion: operators.coreos.com/v1alpha1
        kind: Subscription
        metadata:
          name: clusterresourceoverride
          namespace: clusterresourceoverride-operator
        spec:
          channel: "stable"
          name: clusterresourceoverride
          source: redhat-operators
          sourceNamespace: openshift-marketplace
        ```

    2.  Create the subscription:

        ``` terminal
        $ oc create -f <file-name>.yaml
        ```

        For example:

        ``` terminal
        $ oc create -f cro-sub.yaml
        ```

4.  Create a `ClusterResourceOverride` custom resource (CR) object in the `clusterresourceoverride-operator` namespace:

    1.  Change to the `clusterresourceoverride-operator` namespace.

        ``` terminal
        $ oc project clusterresourceoverride-operator
        ```

    2.  Create a `ClusterResourceOverride` object YAML file (for example, cro-cr.yaml) for the Cluster Resource Override Operator:

        ``` yaml
        apiVersion: operator.autoscaling.openshift.io/v1
        kind: ClusterResourceOverride
        metadata:
            name: cluster
        spec:
          podResourceOverride:
            spec:
              memoryRequestToLimitPercent: 50
              cpuRequestToLimitPercent: 25
              limitCPUToMemoryPercent: 200
        ```

        where

        `metadata.name`
        Specifies a name for the CR. The name must be `cluster`.

        `spec.podResourceOverride.spec.memoryRequestToLimitPercent`
        Specifies the percentage to override the container memory limit, if used, between 1-100. The default is `50`. This parameter is optional.

        `spec.podResourceOverride.spec.cpuRequestToLimitPercent`
        Specifies the percentage of the container CPU limit to use as the CPU request, if a CPU limit is set, between 1-100. The default is `25`. This parameter is optional.

        `spec.podResourceOverride.spec.limitCPUToMemoryPercent`
        Specifies the percentage of the container memory limit to use as the CPU limit, if a memory limit is set. Scaling 1 Gi of RAM at 100 percent is equal to 1 CPU core. This is processed before overriding the CPU request, if configured. The default is `200`. This parameter is optional.

    3.  Create the `ClusterResourceOverride` object:

        ``` terminal
        $ oc create -f <file-name>.yaml
        ```

        For example:

        ``` terminal
        $ oc create -f cro-cr.yaml
        ```

5.  Verify the current state of the admission webhook by checking the status of the cluster custom resource.

    ``` terminal
    $ oc get clusterresourceoverride cluster -n clusterresourceoverride-operator -o yaml
    ```

    The `mutatingWebhookConfigurationRef` section displays when the webhook is called.

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` yaml
    apiVersion: operator.autoscaling.openshift.io/v1
    kind: ClusterResourceOverride
    metadata:
      annotations:
        kubectl.kubernetes.io/last-applied-configuration: |
          {"apiVersion":"operator.autoscaling.openshift.io/v1","kind":"ClusterResourceOverride","metadata":{"annotations":{},"name":"cluster"},"spec":{"podResourceOverride":{"spec":{"cpuRequestToLimitPercent":25,"limitCPUToMemoryPercent":200,"memoryRequestToLimitPercent":50}}}}
      creationTimestamp: "2019-12-18T22:35:02Z"
      generation: 1
      name: cluster
      resourceVersion: "127622"
      selfLink: /apis/operator.autoscaling.openshift.io/v1/clusterresourceoverrides/cluster
      uid: 978fc959-1717-4bd1-97d0-ae00ee111e8d
    spec:
      podResourceOverride:
        spec:
          cpuRequestToLimitPercent: 25
          limitCPUToMemoryPercent: 200
          memoryRequestToLimitPercent: 50
    status:

    # ...

        mutatingWebhookConfigurationRef:
          apiVersion: admissionregistration.k8s.io/v1
          kind: MutatingWebhookConfiguration
          name: clusterresourceoverrides.admission.autoscaling.openshift.io
          resourceVersion: "127621"
          uid: 98b3b8ae-d5ce-462b-8ab5-a729ea8f38f3

    # ...
    ```

    </div>

    where:

    `status.mutatingWebhookConfigurationRef`
    Specifies the `ClusterResourceOverride` admission webhook.

</div>

## Move the Cluster Resource Override Operator pods

By default, the Cluster Resource Override Operator installation process creates an Operator pod and two Cluster Resource Override pods on nodes in the `clusterresourceoverride-operator` namespace. You can move these pods to other nodes, such as infrastructure nodes, as needed.

You can create and use infrastructure nodes to host only infrastructure components, such as the default router, the integrated container image registry, and the components for cluster metrics and monitoring. These infrastructure nodes are not counted toward the total number of subscriptions that are required to run the environment. For more information about infrastructure nodes, see "Creating infrastructure machine sets".

The following example shows that the Cluster Resource Override pods are deployed to control plane nodes.

``` terminal
NAME                                                READY   STATUS    RESTARTS   AGE   IP            NODE                                        NOMINATED NODE   READINESS GATES
clusterresourceoverride-786b8c898c-9wrdq            1/1     Running   0          23s   10.128.2.32   ip-10-0-14-183.us-west-2.compute.internal   <none>           <none>
clusterresourceoverride-786b8c898c-vn2lf            1/1     Running   0          26s   10.130.2.10   ip-10-0-20-140.us-west-2.compute.internal   <none>           <none>
clusterresourceoverride-operator-6b8b8b656b-lvr62   1/1     Running   0          56m   10.131.0.33   ip-10-0-2-39.us-west-2.compute.internal     <none>           <none>
```

The following example shows that the Cluster Resource Override Operator pod is deployed to a worker node.

``` terminal
NAME                                        STATUS   ROLES                  AGE   VERSION
ip-10-0-14-183.us-west-2.compute.internal   Ready    control-plane,master   65m   v1.36.3
ip-10-0-2-39.us-west-2.compute.internal     Ready    worker                 58m   v1.36.3
ip-10-0-20-140.us-west-2.compute.internal   Ready    control-plane,master   65m   v1.36.3
ip-10-0-23-244.us-west-2.compute.internal   Ready    infra                  55m   v1.36.3
ip-10-0-77-153.us-west-2.compute.internal   Ready    control-plane,master   65m   v1.36.3
ip-10-0-99-108.us-west-2.compute.internal   Ready    worker                 24m   v1.36.3
ip-10-0-24-233.us-west-2.compute.internal   Ready    infra                  55m   v1.36.3
ip-10-0-88-109.us-west-2.compute.internal   Ready    worker                 24m   v1.36.3
ip-10-0-67-453.us-west-2.compute.internal   Ready    infra                  55m   v1.36.3
```

<div>

<div class="title">

Procedure

</div>

1.  Move the Cluster Resource Override Operator pod by adding a node selector to the `Subscription` custom resource (CR) for the Cluster Resource Override Operator.

    1.  Edit the CR:

        ``` terminal
        $ oc edit -n clusterresourceoverride-operator subscriptions.operators.coreos.com clusterresourceoverride
        ```

    2.  Add a node selector to match the node role label on the node where you want to install the Cluster Resource Override Operator pod:

        ``` terminal
        apiVersion: operators.coreos.com/v1alpha1
        kind: Subscription
        metadata:
          name: clusterresourceoverride
          namespace: clusterresourceoverride-operator
        # ...
        spec:
          config:
            nodeSelector:
              node-role.kubernetes.io/infra: ""
        ```

        where:

        `spec.config.nodeSelector`
        Specifies the role of the node where you want to deploy the Cluster Resource Override Operator pod.

    > [!NOTE]
    > If the infra node uses taints, you need to add a toleration to the `Subscription` CR. For example:
    >
    > ``` terminal
    > apiVersion: operators.coreos.com/v1alpha1
    > kind: Subscription
    > metadata:
    >   name: clusterresourceoverride
    >   namespace: clusterresourceoverride-operator
    > # ...
    > spec:
    >   config:
    >     nodeSelector:
    >       node-role.kubernetes.io/infra: ""
    >     tolerations:
    >     - key: "node-role.kubernetes.io/infra"
    >       operator: "Exists"
    >       effect: "NoSchedule"
    > ```
    >
    > where:
    >
    > `spec.config.tolerations`
    > Specifies a toleration for a taint on the infra node.

2.  Move the Cluster Resource Override pods by adding a node selector to the `ClusterResourceOverride` custom resource (CR):

    1.  Edit the CR:

        ``` terminal
        $ oc edit ClusterResourceOverride cluster -n clusterresourceoverride-operator
        ```

    2.  Add a node selector to match the node role label on the infra node:

        ``` terminal
        apiVersion: operator.autoscaling.openshift.io/v1
        kind: ClusterResourceOverride
        metadata:
          name: cluster
          resourceVersion: "37952"
        spec:
          podResourceOverride:
            spec:
              cpuRequestToLimitPercent: 25
              limitCPUToMemoryPercent: 200
              memoryRequestToLimitPercent: 50
          deploymentOverrides:
            replicas: 1
            nodeSelector:
              node-role.kubernetes.io/infra: ""
        # ...
        ```

        where:

        `spec.deploymentOverrides.replicas`
        Specifies the number of Cluster Resource Override pods to deploy. The default is `2`. Only one pod is allowed per node. This parameter is optional.

        `spec.deploymentOverrides.nodeSelector`
        Specifies the role of the node where you want to deploy the Cluster Resource Override pods. This parameter is optional.

    > [!NOTE]
    > If the infra node uses taints, you need to add a toleration to the `ClusterResourceOverride` CR. For example:
    >
    > ``` terminal
    > apiVersion: operator.autoscaling.openshift.io/v1
    > kind: ClusterResourceOverride
    > metadata:
    >   name: cluster
    > # ...
    > spec:
    >   podResourceOverride:
    >     spec:
    >       memoryRequestToLimitPercent: 50
    >       cpuRequestToLimitPercent: 25
    >       limitCPUToMemoryPercent: 200
    >   deploymentOverrides:
    >     replicas: 3
    >     nodeSelector:
    >       node-role.kubernetes.io/worker: ""
    >     tolerations:
    >     - key: "key"
    >       operator: "Equal"
    >       value: "value"
    >       effect: "NoSchedule"
    > ```
    >
    > where:
    >
    > `spec.deploymentOverrides.tolerations`
    > Specifies a toleration for a taint on the infra node.

</div>

<div>

<div class="title">

Verification

</div>

- You can verify that the pods have moved by using the following command:

  ``` terminal
  $ oc get pods -n clusterresourceoverride-operator -o wide
  ```

  The Cluster Resource Override pods are now deployed to the infra nodes.

  <div class="formalpara">

  <div class="title">

  Example output

  </div>

  ``` terminal
  NAME                                                READY   STATUS    RESTARTS   AGE   IP            NODE                                        NOMINATED NODE   READINESS GATES
  clusterresourceoverride-786b8c898c-9wrdq            1/1     Running   0          23s   10.127.2.25   ip-10-0-23-244.us-west-2.compute.internal   <none>           <none>
  clusterresourceoverride-786b8c898c-vn2lf            1/1     Running   0          26s   10.128.0.80   ip-10-0-24-233.us-west-2.compute.internal   <none>           <none>
  clusterresourceoverride-operator-6b8b8b656b-lvr62   1/1     Running   0          56m   10.129.0.71   ip-10-0-67-453.us-west-2.compute.internal   <none>           <none>
  ```

  </div>

</div>

## Configure cluster-level overcommit

You can use the OpenShift CLI to configure the Cluster Resource Override Operator to help control overcommit in your cluster.

The Cluster Resource Override Operator requires a `ClusterResourceOverride` custom resource (CR) and a label for each namespace where you want the Operator to control overcommit.

If pods in that namespace need ratios that differ from the cluster-wide `ClusterResourceOverride` object, create a `ResourceOverride` object, which applies its own ratios to pods in the same namespace that have a matching pod selector. For more information, see "Namespace-level resource overrides".

By default, the installation process creates two Cluster Resource Override pods on the control plane nodes in the `clusterresourceoverride-operator` namespace. You can move these pods to other nodes, such as infrastructure nodes, as needed. Infrastructure nodes are not counted toward the total number of subscriptions that are required to run the environment. For more information, see "Moving the Cluster Resource Override Operator pods".

<div>

<div class="title">

Prerequisites

</div>

- To use the `memoryRequestToLimitPercent`, `cpuRequestToLimitPercent`, or `limitCPUToMemoryPercent` parameters, the containers must have a memory or CPU limit in the pod specification or from a `LimitRange` object.

- To use the `cpuRequestToRequestPercent` parameter, the containers must have a CPU request in the pod specification or from a `LimitRange` object.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Edit the `ClusterResourceOverride` CR:

    ``` yaml
    apiVersion: operator.autoscaling.openshift.io/v1
    kind: ClusterResourceOverride
    metadata:
        name: cluster
    spec:
      podResourceOverride:
        spec:
          memoryRequestToLimitPercent: 50
          cpuRequestToLimitPercent: 25
          limitCPUToMemoryPercent: 200
          cpuRequestToRequestPercent: 50
    # ...
    ```

    where:

    `spec.podResourceOverride.spec.memoryRequestToLimitPercent`
    Specifies the percentage of the container memory limit to use as the memory request, if used, between 1-100. The default is `50`. This parameter is optional.

    `spec.podResourceOverride.spec.cpuRequestToLimitPercent`
    Specifies the percentage of the container CPU limit to use as the CPU request, if a CPU limit is set, between 1-100. The default is `25`. This parameter is optional.

    `spec.podResourceOverride.spec.limitCPUToMemoryPercent`
    Specifies the percentage of the container memory limit to use as the CPU limit, if a memory limit is set. Scaling 1Gi of RAM at 100 percent is equal to 1 CPU core. This is processed before overriding the CPU request, if configured. The default is `200`. This parameter is optional.

    `spec.podResourceOverride.spec.cpuRequestToRequestPercent`
    Specifies the percentage of the submitted container CPU request to use as the CPU request, between 1-100. For example, `50` changes a request of `2000m` to `1000m`. The webhook applies this parameter after the `cpuRequestToLimitPercent` parameter and replaces the CPU request that parameter set. This parameter is optional.

2.  Ensure the following label has been added to the namespace object for each project where you want the Cluster Resource Override Operator to control overcommit:

    ``` yaml
    apiVersion: v1
    kind: Namespace
    metadata:

    # ...

      labels:
        clusterresourceoverrides.admission.autoscaling.openshift.io/enabled: "true"

    # ...
    ```

    where:

    `metadata.labels.clusterresourceoverrides.admission.autoscaling.openshift.io/enabled: "true"`
    Specifies that you want to use the Cluster Resource Override Operator with this project.

</div>

## Namespace-level resource overrides

You can use a `ResourceOverride` custom resource (CR) to set CPU and memory override ratios for pods in a specific OpenShift Container Platform namespace. Use a resource override when pods in that namespace need ratios that differ from the cluster-wide `ClusterResourceOverride` object.

> [!NOTE]
> To use a resource override in a specific namespace, the namespace must be configured to use the cluster-wide the `ClusterResourceOverride` object. For more information about the label, see "Cluster-level overcommit using the Cluster Resource Override Operator". The

You can create one or more resource override objects in a namespace. Each resource override object has a specific pod selector. For new pods in the namespace with a matching label, the webhook applies the ratios in the `ResourceOverride` object. New pods that do not match the `ResourceOverride` pod selector receive the ratios in the `ClusterResourceOverride` object. If you omit the pod selector or leave the parameter value empty, the webhook applies the `ResourceOverride` ratios to every new pod in the namespace. Pods that existed before the override objects were applied do not change in response to the overrides.

If more than one `ResourceOverride` object in the namespace matches a pod, the webhook applies the object whose `metadata.name` parameter comes first in alphabetical order. Any other matching objects are not used. The webhook records an `OverrideConflict` warning event on each matching object that it does not apply.

Users with the `admin` or `edit` role on the namespace can create, update, and delete `ResourceOverride` objects. Users with the `view` role can read them.

For steps to create an resource override object, see "Create a project-level resource override".

### Create a namespace-level resource override

You can create a namespace-scoped `ResourceOverride` custom resource (CR) if selected pods in a namespace need ratios that differ from the cluster-wide `ClusterResourceOverride` object.

Any new pods created in that namespace that have a matching pod selector receive the ratios specified in the resource override object, rather than the cluster-wide ratios. The namespace must have the `ClusterResourceOverride` label assigned to it.

New pods in the namespace that do not match the pod selector receive the cluster-wide ratios. Pods that existed before adding the cluster-wide ratios do not change.

<div>

<div class="title">

Prerequisites

</div>

- The Cluster Resource Override Operator is installed.

- A `ClusterResourceOverride` CR named `cluster` exists.

- You have the `admin` or `edit` role on the project.

- To use the `memoryRequestToLimitPercent`, `cpuRequestToLimitPercent`, or `limitCPUToMemoryPercent` parameters, the containers must have a memory or CPU limit in the pod specification or from a `LimitRange` object.

- To use the `cpuRequestToRequestPercent` parameter, the containers must have a CPU request in the pod specification or from a `LimitRange` object.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Add the Cluster Resource Override opt-in label to the project by running the following command:

    ``` terminal
    $ oc label namespace <namespace_name> clusterresourceoverrides.admission.autoscaling.openshift.io/enabled=true
    ```

    Replace `<namespace_name>` with the name of the project to apply the label.

    <div class="formalpara">

    <div class="title">

    Example command

    </div>

    ``` terminal
    $ oc label namespace my-namespace clusterresourceoverrides.admission.autoscaling.openshift.io/enabled=true
    ```

    </div>

    If the project already has the label, the command reports that the namespace was not labeled. You can continue to the next step.

2.  In that same project, create a `ResourceOverride` object by using the following steps:

    1.  Create a YAML file similar to the following example:

        ``` yaml
        apiVersion: autoscaling.openshift.io/v1
        kind: ResourceOverride
        metadata:
          name: stateless
          namespace: my-namespace
        spec:
          podResourceOverride:
            memoryRequestToLimitPercent: 25
            cpuRequestToLimitPercent: 10
            limitCPUToMemoryPercent: 150
            cpuRequestToRequestPercent: 50
          podSelector:
            matchLabels:
              tier: stateless
        ```

        where:

        `apiVersion`
        Specifies `autoscaling.openshift.io/v1`.

        `metadata.name`
        Specifies the name of the object. The name must be unique in the namespace.

        `metadata.namespace`
        Specifies the namespace for this object. A `ResourceOverride` object belongs to one namespace. A namespace can have more than one `ResourceOverride` object.

        `spec.podResourceOverride.memoryRequestToLimitPercent`
        If a container memory limit has been specified or defaulted, the memory request is overridden to this percentage of the limit, from 1 to 100. This parameter is optional.

        `spec.podResourceOverride.cpuRequestToLimitPercent`
        If a container CPU limit has been specified or defaulted, the CPU request is overridden to this percentage of the limit, from 1 to 100. This parameter is optional.

        `spec.podResourceOverride.limitCPUToMemoryPercent`
        If a container memory limit has been specified or defaulted, the CPU limit is overridden to a percentage of the memory limit. Scaling 1Gi of RAM at 100 percent is equal to 1 CPU core. The webhook processes this parameter before it overrides the CPU request. This parameter is optional.

        `spec.podResourceOverride.cpuRequestToRequestPercent`
        Specifies the percentage of the submitted container CPU request to use as the CPU request, from 1 to 100. For example, `50` changes a request of `2000m` to `1000m`. The webhook applies this parameter after the `cpuRequestToLimitPercent` parameter and replaces the CPU request that parameter set. This parameter is optional.

        `spec.podSelector`
        Optional label selector for pods in the same namespace. If you omit the `podSelector` parameter, or leave the `matchLabels` or `matchExpressions` values empty, the object matches every pod in the namespace. If the selector is not a valid label selector, the webhook ignores the object.

        `spec.podSelector.matchLabels`
        A map of labels. A pod must include every label in the map to match. You can use a `matchLabels` or `matchExpressions` parameter.

    2.  Create the `ResourceOverride` object by running the following command:

        ``` terminal
        $ oc create -f <file_name>.yaml
        ```

        <div class="formalpara">

        <div class="title">

        Example

        </div>

        ``` terminal
        $ oc create -f ro-cr.yaml
        ```

        </div>

3.  In that same namespace, set a matching label on your workload object, such as a deployment, so every new pod gets the label by running a command similar to the following:

    ``` terminal
    $ oc patch deployment <name> -n <namespace_name> --type=merge -p '{"spec":{"template":{"metadata":{"labels":{"<key>":"<value>"}}}}}'
    ```

    Replace `<name>` with the workload name, `<namespace_name>` with the namespace where the workload is deployed, and `<key>/<value>` with the pod selector.

    <div class="formalpara">

    <div class="title">

    Example command

    </div>

    ``` terminal
    $ oc patch deployment my-deployment -n my-namespace --type=merge -p '{"spec":{"template":{"metadata":{"labels":{"tier":"stateless"}}}}}'
    ```

    </div>

    Any new workload pods with a label that matches the resource override label receive the ratios in the resource override object.

</div>

<div>

<div class="title">

Verification

</div>

- Confirm that the `ResourceOverride` object exists by running a command similar to the following:

  ``` terminal
  $ oc get resourceoverride <name> -n <namespace_name>
  ```

  Replace `<name>` with the name of the resource override object and `<namespace_name>` with the name of namespace where the object should be applied.

  <div class="formalpara">

  <div class="title">

  Example command

  </div>

  ``` terminal
  $ oc get resourceoverride stateless -n my-namespace
  ```

  </div>

- Check that the resource override ratios are applied to a new pod in the namespace:

  1.  In the workload, check the original container CPU request and memory limit by running a command similar to the following:

      <div class="formalpara">

      <div class="title">

      Example command

      </div>

      ``` terminal
      $ oc get deployment <workload_name> -n <namespace_name> -o jsonpath='{.spec.template.spec.containers[*].resources}{"\n"}'
      ```

      </div>

      Replace `<workload_name>` with the name of your workload and `<namespace_name>` with the name of namespace where the deployment is deployed.

      <div class="formalpara">

      <div class="title">

      Example output

      </div>

      ``` terminal
      {"limits":{"cpu":"500m","memory":"128Mi"},"requests":{"cpu":"100m"}}
      ```

      </div>

  2.  Check the CPU request and memory limit values from new pods in that workload that have the appropriate pod selector, created after the resource override object was created, by running a command similar to the following:

      <div class="formalpara">

      <div class="title">

      Example command

      </div>

      ``` terminal
      $ oc get pods -n <namespace_name> -l <key>=<value> -o custom-columns=NAME:.metadata.name,REQUESTS:.spec.containers[*].resources.requests,LIMITS:.spec.containers[*].resources.limits
      ```

      </div>

      <div class="formalpara">

      <div class="title">

      Example pod output

      </div>

      ``` terminal
      NAME                               REQUESTS                   LIMITS
      my-deployment-2-6857c84855-25xxk   map[cpu:50m memory:32Mi]   map[cpu:187m memory:128Mi]
      my-deployment-2-6857c84855-97qqp   map[cpu:50m memory:32Mi]   map[cpu:187m memory:128Mi]
      my-deployment-749f9646fc-xjgnq     map[cpu:50m memory:64Mi]   map[cpu:250m memory:128Mi]
      ```

      </div>

      For the `my-deployment-2-*` pods, the deployment submits a CPU request of `100m`, a CPU limit of `500m`, and a memory limit of `128Mi`. The `cpuRequestToRequestPercent: 50` parameter sets the CPU request to `50m`. The `memoryRequestToLimitPercent: 25` parameter sets the memory request to `32Mi`. The `limitCPUToMemoryPercent: 150` parameter sets the CPU limit to `187m` from that memory limit.

      The `cpuRequestToLimitPercent: 10` parameter is applied first and would set the CPU request to `18m`. The `cpuRequestToRequestPercent` parameter is applied after the other override parameters and replaces that request with `50m`.

      The `my-deployment-749f9646fc-xjgnq` pod has the same submitted CPU request of `100m` and memory limit of `128Mi`, but it does not match the `ResourceOverride` selector. The webhook applies the `ClusterResourceOverride` object named `cluster`. With the ratios in the cluster object example in this section, the `memoryRequestToLimitPercent: 50` and `limitCPUToMemoryPercent: 200` parameters set the memory request to `64Mi` and the CPU limit to `250m`. The `cpuRequestToLimitPercent: 25` parameter would set the CPU request to `62m`, and the `cpuRequestToRequestPercent: 50` parameter then sets it to `50m`.

      If the `cpuRequestToRequestPercent` parameter is set in the resource override, the `clusterresourceoverrides.admission.autoscaling.openshift.io/original-cpu-request-<container_name>` annotation is added to the pod. The annotation records the submitted CPU request, which is `100m` in this example:

      <div class="formalpara">

      <div class="title">

      Example pod spec

      </div>

      ``` yaml
      apiVersion: v1
      kind: Pod
      metadata:
        annotations:
          clusterresourceoverrides.admission.autoscaling.openshift.io/original-cpu-request-hello-openshift: 100m
        generateName: my-deployment-2-6857c84855-
      # ...
      ```

      </div>

</div>

# Node-level overcommit

You can use various ways to control overcommit on specific nodes, such as quality of service (QOS) guarantees, CPU limits, or reserve resources. You can also disable overcommit for specific nodes and specific projects.

## Understanding container CPU and memory requests

Review the following information to learn about container CPU and memory requests to help you ensure that your cluster is properly configured.

A container is guaranteed the amount of CPU it requests and is additionally able to consume excess CPU available on the node, up to any limit specified by the container. If multiple containers are attempting to use excess CPU, CPU time is distributed based on the amount of CPU requested by each container.

For example, if one container requested 500m of CPU time and another container requested 250m of CPU time, any extra CPU time available on the node is distributed among the containers in a 2:1 ratio. If a container specified a limit, it will be throttled not to use more CPU than the specified limit. CPU requests are enforced using the CFS shares support in the Linux kernel. By default, CPU limits are enforced using the CFS quota support in the Linux kernel over a 100ms measuring interval, though this can be disabled.

A container is guaranteed the amount of memory it requests. A container can use more memory than requested, but once it exceeds its requested amount, it could be terminated in a low memory situation on the node. If a container uses less memory than requested, it will not be terminated unless system tasks or daemons need more memory than was accounted for in the node’s resource reservation. If a container specifies a limit on memory, it is immediately terminated if it exceeds the limit amount.

## Understanding overcommitment and quality of service classes

You can use Quality of Service (QoS) classes in an overcommitted environment to help you ensure that your cluster is properly configured.

A node is *overcommitted* when it has a pod scheduled that makes no request, or when the sum of limits across all pods on that node exceeds available machine capacity.

In an overcommitted environment, the pods on the node might attempt to use more compute resource than is available at any given point in time. When this occurs, the node must give priority to one pod over another. The facility used to make this decision is referred to as a Quality of Service (QoS) class.

A pod is designated as one of three QoS classes with decreasing order of priority:

| Priority | Class Name | Description |
|----|----|----|
| 1 (highest) | **Guaranteed** | If limits and optionally requests are set (not equal to 0) for all resources and they are equal, then the pod is classified as **Guaranteed**. |
| 2 | **Burstable** | If requests and optionally limits are set (not equal to 0) for all resources, and they are not equal, then the pod is classified as **Burstable**. |
| 3 (lowest) | **BestEffort** | If requests and limits are not set for any of the resources, then the pod is classified as **BestEffort**. |

Quality of Service classes

Memory is an incompressible resource, so in low memory situations, containers that have the lowest priority are terminated first:

- **Guaranteed** containers are considered top priority, and are guaranteed to only be terminated if they exceed their limits, or if the system is under memory pressure and there are no lower priority containers that can be evicted.

- **Burstable** containers under system memory pressure are more likely to be terminated when they exceed their requests and no other **BestEffort** containers exist.

- **BestEffort** containers are treated with the lowest priority. Processes in these containers are first to be terminated if the system runs out of memory.

### Understanding how to reserve memory across quality of service tiers

You can use the `qos-reserved` parameter to specify a percentage of memory to be reserved by a pod in a particular QoS level. This feature attempts to reserve requested resources to exclude pods from lower QoS classes from using resources requested by pods in higher QoS classes.

OpenShift Container Platform uses the `qos-reserved` parameter as follows:

- A value of `qos-reserved=memory=100%` prevents the `Burstable` and `BestEffort` QoS classes from consuming memory that was requested by a higher QoS class. This increases the risk of inducing OOM on `BestEffort` and `Burstable` workloads in favor of increasing memory resource guarantees for `Guaranteed` and `Burstable` workloads.

- A value of `qos-reserved=memory=50%` allows the `Burstable` and `BestEffort` QoS classes to consume half of the memory requested by a higher QoS class.

- A value of `qos-reserved=memory=0%` allows a `Burstable` and `BestEffort` QoS classes to consume up to the full node allocatable amount if available, but increases the risk that a `Guaranteed` workload does not have access to requested memory. This condition effectively disables this feature.

## Understanding swap memory and QoS

Review the following information to learn how swap memory and QoS interact in an overcommitted environment to help you ensure that your cluster is properly configured.

You can disable swap by default on your nodes to preserve quality of service (QoS) guarantees. Otherwise, physical resources on a node can oversubscribe, affecting the resource guarantees the Kubernetes scheduler makes during pod placement.

For example, if two guaranteed pods have reached their memory limit, each container could start using swap memory. Eventually, if there is not enough swap space, processes in the pods can be terminated due to the system being oversubscribed.

Failing to disable swap causes nodes to not recognize that they are experiencing **MemoryPressure**, resulting in pods not receiving the memory they made in their scheduling request. As a result, additional pods are placed on the node to further increase memory pressure, ultimately increasing your risk of experiencing a system out of memory (OOM) event.

> [!IMPORTANT]
> If swap is enabled, any out-of-resource handling eviction thresholds for available memory will not work as expected. Out-of-resource handling allows pods to be evicted from a node when it is under memory pressure, and rescheduled on an alternative node that has no such pressure.

## Understanding nodes overcommitment

To maintain optimal system performance and stability in an overcommitted environment in OpenShift Container Platform, configure your nodes to manage resource contention effectively.

When the node starts, it ensures that the kernel tunable flags for memory management are set properly. The kernel should never fail memory allocations unless it runs out of physical memory.

To ensure this behavior, OpenShift Container Platform configures the kernel to always overcommit memory by setting the `vm.overcommit_memory` parameter to `1`, overriding the default operating system setting.

OpenShift Container Platform also configures the kernel to not panic when it runs out of memory by setting the `vm.panic_on_oom` parameter to `0`. A setting of 0 instructs the kernel to call the OOM killer in an Out of Memory (OOM) condition, which kills processes based on priority.

You can view the current setting by running the following commands on your nodes:

``` terminal
$ sysctl -a |grep commit
```

<div class="formalpara">

<div class="title">

Example output

</div>

``` terminal
#...
vm.overcommit_memory = 0
#...
```

</div>

``` terminal
$ sysctl -a |grep panic
```

<div class="formalpara">

<div class="title">

Example output

</div>

``` terminal
#...
vm.panic_on_oom = 0
#...
```

</div>

> [!NOTE]
> The previous commands should already be set on nodes, so no further action is required.

You can also perform the following configurations for each node:

- Disable or enforce CPU limits using CPU CFS quotas

- Reserve resources for system processes

- Reserve memory across quality of service tiers

## Disable or enforce CPU limits using CPU CFS quotas

You can disable the default enforcement of CPU limits for nodes in a machine config pool.

By default, nodes enforce specified CPU limits using the Completely Fair Scheduler (CFS) quota support in the Linux kernel.

If you disable CPU limit enforcement, it is important to understand the impact on your node:

- If a container has a CPU request, the request continues to be enforced by CFS shares in the Linux kernel.

- If a container does not have a CPU request, but does have a CPU limit, the CPU request defaults to the specified CPU limit, and is enforced by CFS shares in the Linux kernel.

- If a container has both a CPU request and limit, the CPU request is enforced by CFS shares in the Linux kernel, and the CPU limit has no impact on the node.

<div>

<div class="title">

Prerequisites

</div>

- You have the label associated with the static `MachineConfigPool` CRD for the type of node you want to configure.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Create a custom resource (CR) for your configuration change.

    <div class="formalpara">

    <div class="title">

    Sample configuration for a disabling CPU limits

    </div>

    ``` yaml
    apiVersion: machineconfiguration.openshift.io/v1
    kind: KubeletConfig
    metadata:
      name: disable-cpu-units
    spec:
      machineConfigPoolSelector:
        matchLabels:
          pools.operator.machineconfiguration.openshift.io/worker: ""
      kubeletConfig:
        cpuCfsQuota: false
    ```

    </div>

    where:

    `metadata.name`
    Specifies a name for the CR.

    `spec.machineConfigPoolSelector.matchLabels`
    Specifies the label from the machine config pool.

    `spec.kubeletConfig.cpuCfsQuota`
    Specifies the `cpuCfsQuota` parameter to `false`.

2.  Run the following command to create the CR:

    ``` terminal
    $ oc create -f <file_name>.yaml
    ```

</div>

## Reserving resources for system processes

You can explicitly reserve resources for non-pod processes by allocating node resources through specifying resources available for scheduling.

To provide more reliable scheduling and minimize node resource overcommitment, each node can reserve a portion of its resources for use by the system daemons that are required to run on your node for your cluster to function.

> [!NOTE]
> It is recommended that you reserve resources for incompressible resources such as memory.

For more details, see "Allocating Resources for Nodes".

## Disable overcommitment for a node

When overcommitment is enabled on a node, you can disable overcommitment on that node. Disabling overcommit can help ensure predictability, stability, and high performance in your cluster.

<div>

<div class="title">

Procedure

</div>

- Run the following command on a node to disable overcommitment on that node:

  ``` terminal
  $ sysctl -w vm.overcommit_memory=0
  ```

</div>

# Project-level limits

To help control overcommit, you can set per-project resource limit ranges, specifying memory and CPU limits and defaults for a project that overcommit cannot exceed.

For information on project-level resource limits, see the *Additional resources* section.

Alternatively, you can disable overcommitment for specific projects.

## Disable overcommitment for a project

If overcommitment is enabled on a project, you can disable overcommitment for that project. This allows infrastructure components to be configured independently of overcommitment.

<div>

<div class="title">

Procedure

</div>

1.  Create or edit the namespace object file.

2.  Add the following annotation:

    ``` yaml
    apiVersion: v1
    kind: Namespace
    metadata:
      annotations:
        quota.openshift.io/cluster-resource-override-enabled: "false"
    # ...
    ```

    where:

    `metadata.annotations.quota.openshift.io/cluster-resource-override-enabled.false`
    Specifies that overcommit is disabled for this namespace.

</div>

# Additional resources

- [Moving the Cluster Resource Override Operator pods](../../machine_management/creating-infrastructure-machinesets.xml#nodes-cluster-resource-override-move-infra_creating-infrastructure-machinesets)

- [Creating infrastructure machine sets](../../machine_management/creating-infrastructure-machinesets.xml#creating-infrastructure-machinesets)

- [Namespace-level resource overrides](../../nodes/clusters/nodes-cluster-overcommit.xml#nodes-cluster-resource-override-profiles_nodes-cluster-overcommit)

- [Create a namespace-level resource override](../../nodes/clusters/nodes-cluster-overcommit.xml#nodes-cluster-resource-override-profiles-creating_nodes-cluster-overcommit)

- [Cluster-level overcommit using the Cluster Resource Override Operator](../../nodes/clusters/nodes-cluster-overcommit.xml#nodes-cluster-resource-override-profiles_nodes-cluster-overcommit)

- [Setting deployment resources](../../applications/deployments/managing-deployment-processes.xml#deployments-triggers_deployment-operations)

- [Disabling or enforcing CPU limits using CPU CFS quotas](../../nodes/clusters/nodes-cluster-overcommit.xml#nodes-cluster-overcommit-node-enforcing_nodes-cluster-overcommit)

- [Reserving resources for system processes](../../nodes/clusters/nodes-cluster-overcommit.xml#nodes-cluster-overcommit-node-resources_nodes-cluster-overcommit)

- [Understanding how to reserve memory across quality of service tiers](../../nodes/clusters/nodes-cluster-overcommit.xml#qos-about-reserve_nodes-cluster-overcommit)

- [Allocating resources for nodes](../../nodes/nodes/nodes-nodes-resources-configuring.xml#nodes-nodes-resources-configuring-setting_nodes-nodes-resources-configuring)
