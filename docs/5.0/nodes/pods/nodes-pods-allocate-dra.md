You can use Attribute-Based GPU Allocation to enable fine-tuned control over graphics processing unit (GPU) resource allocation in OpenShift Container Platform, allowing pods to request GPUs based on specific device attributes, including product name, GPU memory capacity, compute capability, vendor name and driver version. Having access to these attributes, which are exposed by a third-party Dynamic Resource Allocation (DRA) driver, allows OpenShift Container Platform to schedule a pod on a node that has the specific devices that the workload needs.

This workflow provides significant improvement in the device allocation workflow when compared to device plugins, which require per-container device requests, do not support device sharing, and do not support expression-based device filtering.

# About GPU attributes

You can use Attribute-Based GPU Allocation to enable pods to be scheduled on nodes that have specific graphics processing units (GPU). These attributes are advertised to the cluster by using a Dynamic Resource Allocation (DRA) driver, a third-party application that runs on each node in your cluster.

The DRA driver manages and exposes specialized resources within your cluster by interacting with the underlying hardware and advertising it to the OpenShift Container Platform control plane. You must install a DRA driver in your cluster. Installation of the DRA driver is beyond the scope of this documentation. Some DRA device drivers can also slice GPU memory, making it available to multiple workloads.

The DRA driver advertises several GPU device attributes that OpenShift Container Platform can use for precise GPU selection, including the following attributes:

Product Name
Pods can request an exact GPU model based on performance requirements or compatibility with applications. This ensures that workloads leverage the best-suited hardware for their tasks.

GPU Memory Capacity
Pods can request GPUs with a minimum or maximum memory capacity, such as 8 GB, 16 GB, or 40 GB. This is helpful with memory-intensive workloads such as large AI model training or data processing. This attribute enables applications to allocate GPUs that meet memory needs without overcommitting or underutilizing resources.

Compute Capability
Pods can request GPUs based on the compute capabilities of the GPU, such as the CUDA versions supported. Pods can target GPUs that are compatible with the application’s framework and leverage optimized processing capabilities.

Power and Thermal Profiles
Pods can request GPUs based on power usage or thermal characteristics, enabling power-sensitive or temperature-sensitive applications to operate efficiently. This is particularly useful in high-density environments where energy or cooling constraints are factors.

Device ID and Vendor ID
Pods can request GPUs based on the GPU’s hardware specifics, which allows applications that require specific vendors or device types to make targeted requests.

Driver Version
Pods can request GPUs that run a specific driver version, ensuring compatibility with application dependencies and maximizing GPU feature access.

# About GPU allocation objects and concepts

You can use the following Attribute-Based GPU Allocation objects and concepts to ensure that a workload is scheduled on a node with the graphics processing unit (GPU) specifications it needs. You should be familiar with these objects before proceeding.

Device class
A device class is a category of devices that pods can claim. Some device drivers contain their own device class. Alternatively, an administrator can create device classes. A device class contains a device selector, which is a [common expression language (CEL)](https://cel.dev/) expression that must evaluate to true if a device satisfies the request.

The following example `DeviceClass` object selects any device that is managed by the `driver.example.com` device driver:

<div class="formalpara-title">

**Example device class object**

</div>

``` yaml
apiVersion: resource.k8s.io/v1
kind: DeviceClass
metadata:
  name: example-device-class
spec:
  selectors:
  - cel:
      expression: |-
        device.driver == "driver.example.com"
```

where:

`spec.selectors`
Specifies a CEL expression for selecting a device.

Resource slice
A Dynamic Resource Allocation (DRA) developer uses a third-party DRA driver on each node to create and manage *resource slices*, which describe what resources are available in that cluster. A resource slice represents one or more GPU resources that are attached to nodes. The DRA can allocate either a full device or fixed-size partitions of full devices.

When a resource claim is created and used in a pod, OpenShift Container Platform uses the resource slices to find nodes that have the requested resources. After finding an eligible resource slice for the resource claim, the scheduler updates the resource claim with the allocation details, allocates resources to the resource claim, and schedules the pod onto a node that can access the resources.

To allow multiple resource claims to share one device, you can share that device by partitioning it into fixed logical devices or by using consumable capacity.

- **Define slices explicitly**

  You can use your DRA driver to partition a single physical hardware device into smaller, logical instances, such as Multi-Instance GPUs, based on workload demands. By partitioning devices, you can safely and efficiently share expensive accelerators across multiple pods.

  To allocate partitions, the DRA driver creates a *counter set*, which is a set of named *counters*. The counters represent the resources available on the physical device that are used by the logical devices advertised through resource slices.

  Logical devices can specify the `consumesCounters` list in the resource slice. Each entry contains a reference to a counter set and a set of named counters with the amounts they can consume.

  In the following example, the `resource-driver.example.com` DRA driver is sharing 40Gi of memory through the `gpu-0-counter-set` counter set in the `counter-slice` object. The `device-slice` object makes this memory available as a full device named *gpu-0* or either of two partitioned devices named *gpu-0-partition-0* and *gpu-0-partition-1*. Each device has a capacity and declares how much it consumes from the counter when allocated, either 40Gi for the full device or 20Gi of memory for each partition. You can allocate the memory by using either the full device or the partitions, but not both, enforcing mutual exclusivity between a full device and its partitions. When *gpu-0* is allocated, the GPU consumes all 40Gi from the counter set, leaving 0Gi for the partitions.

  <div class="formalpara-title">

  **Example resource slice object for a partitionable device**

  </div>

  ``` yaml
  apiVersion: resource.k8s.io/v1
  kind: ResourceSlice
  metadata:
    name: counter-slice
  spec:
    driver: "resource-driver.example.com"
    nodeName: dra-example-driver
    pool:
      generation: 1
      name: "my-pool"
      resourceSliceCount: 2
    sharedCounters:
    - name: gpu-0-counter-set
      counters:
        memory:
          value: 40Gi
  ---
  apiVersion: resource.k8s.io/v1
  kind: ResourceSlice
  metadata:
    name: device-slice
  spec:
    driver: "resource-driver.example.com"
    pool:
      generation: 1
      name: "my-pool"
      resourceSliceCount: 2
    nodeName: "my-node"
    devices:
    - name: gpu-0
      capacity:
        memory:
          value: 40Gi
      consumesCounters:
      - counterSet: gpu-0-counter-set
        counters:
          memory:
            value: 40Gi
    - name: gpu-0-partition-0
      capacity:
        memory:
          value: 20Gi
      consumesCounters:
      - counterSet: gpu-0-counter-set
        counters:
          memory:
            value: 20Gi
    - name: gpu-0-partition-1
      capacity:
        memory:
          value: 20Gi
      consumesCounters:
      - counterSet: gpu-0-counter-set
        counters:
          memory:
            value: 20Gi
  ```

  where:

  `spec.driver`
  Specifies the name of the DRA driver, which you can specify in a device class.

  `spec.sharedCounters`
  Specifies the counter set and counters.

  `spec.devices`
  Specifies a list of devices that can be requested by pods.

  `spec.devices.name`
  Specifies the details of a single device.

  `spec.devices.consumesCounters`
  Specifies how much of a shared counter set the device consumes if allocated.

- **Share a device with consumable capacity**

  When you set the `allowMultipleAllocations` field to `true` in a resource slice for a device, you can allow that device to be consumed by multiple independent resource claims. This method, called *consumable capacity*, is more dynamic than manual partitioning. The scheduler manages how much of the device’s capacity each claim consumes.

  The following example resource slice configures consumable capacity to allow multiple resource claims to consume memory capacity from the same GPU device.

  <div class="formalpara-title">

  **Example resource slice for a device that allows multiple allocations and has consumable capacity**

  </div>

  ``` yaml
  kind: ResourceSlice
  apiVersion: resource.k8s.io/v1
  metadata:
    name: resourceslice
  spec:
    nodeName: worker-1
    pool:
      name: pool
      generation: 1
      resourceSliceCount: 1
    driver: dra.example.com
    devices:
    - name: gpu-0
      allowMultipleAllocations: true
      attributes:
        name:
          string: "gpu-0"
      capacity:
        memory:
          requestPolicy:
            default: 6Gi
            validRange:
              min: 2Gi
              max: 8Gi
              step: 2Gi
          value: 10Gi
  ```

  where:

  `spec.devices.allowMultipleAllocations`
  When `true`, specifies that the device can be allocated more than once, including to multiple resource claims and to multiple requests within a resource claim.

  `spec.devices.capacity.memory.requestPolicy`
  Specifies how the device’s memory capacity can be consumed. Contains the following parameters:

  - `default` defines the default consumed capacity if the resource claim does not specify this capacity. The default amount must be greater than or equal to the `min` value and less than or equal to the `max` value. The default amount and the `max` value, if set, must be multiples of `step`.

  - `validRange.min` defines the minimum capacity allowed for a consumption request. Requests below `min` are rounded up to `min`.

  - `validRange.max` defines the upper limit for capacity that a single request can consume. This must be less than or equal to the capacity `value`. If the requested or rounded amount exceeds `max`, the device cannot be allocated.

  - `validRange.step` defines the step size between valid capacity amounts within the range. If a request is between `min` and `max` but is not aligned with `step`, the scheduler rounds it up to the next valid amount. In this example, a request for `3Gi` is rounded to `4Gi`, which is one step above the minimum.

  `spec.devices.capacity.memory.value`
  Specifies the fixed total memory capacity of the device. The scheduler tracks consumed capacity separately and does not change this value.

Resource claim
Cluster administrators create resource claim objects to request specific resources, either a `ResourceClaim` that is used with one workload or a `ResourceClaimTemplate` that can be used with multiple workloads. These claims reference a device class and can include parameters to specify desired configurations or features of the hardware.

The administrator adds the resource claim to a pod specification. The scheduler then schedules that pod on a node in the cluster that has the requested GPU. For the device request in a resource claim, you must specify either a list of one or more device requests that the scheduler must meet or provide a prioritized list of requests for the scheduler to choose from.

If you use a `ResourceClaimTemplate` object in a pod specification, OpenShift Container Platform automatically generates a new `ResourceClaim` object for each pod or replica.

Each resource claim that OpenShift Container Platform generates from the template is bound to that specific pod. When the pod terminates, OpenShift Container Platform deletes the corresponding resource claim. An exclusively allocated device cannot be used simultaneously by another workload. If the device allows multiple allocations, independent resource claims can share that device by consuming part of its capacity.

You must specify either a request for a specific device that the scheduler must meet, or a provide a prioritized list of devices for the scheduler to choose from.

- **Resource claim template for partitioned devices**

  The following example resource claim template contains two sub-requests. Of these sub-requests, only one is selected by the scheduler. The scheduler tries to satisfy the sub-requests in the order in which they are listed. A CEL expression is used inside the sub-request for selecting a device.

  <div class="formalpara-title">

  **Example resource claim template object**

  </div>

  ``` yaml
  apiVersion: resource.k8s.io/v1
  kind: ResourceClaimTemplate
  metadata:
    namespace: gpu-claim
    name: gpu-devices
  spec:
    spec:
      devices:
        requests:
        - name: req-0
          firstAvailable:
          - name: 2g-10gb
            deviceClassName: example-device-class
            selectors:
            - cel:
                expression: "device.attributes['driver.example.com'].profile == '2g.10gb'"
          - name: 3g-20gb
            deviceClassName: example-device-class
            selectors:
            - cel:
                expression: "device.attributes['driver.example.com'].profile == '3g.20gb'"
  ```

  where:

  `spec.spec.devices.requests`
  Specifies a list of one or more requests for devices. The sub-request must include either `exactly` or `firstAvailable`.

  - `exactly`: Specifies a request for one or more identical devices. The devices must match the request exactly for the request to be satisfied. If the requested device is not available, the scheduler cannot create the pod.

  - `firstAvailable`: Specifies multiple requests for a device, of which only one device needs to be available before the scheduler can create the requesting pod. The scheduler checks the availability of the devices in the order listed and selects the first available device. The scheduler can create the pod if one requested devices is available.

  `spec.devices.requests.exactly.deviceClassName` or `spec.devices.requests.firstAvailable.deviceClassName`
  Specifies which device class to use with this request.

  `spec.devices.requests.exactly.selectors` or `spec.devices.requests.firstAvailable.selectors`
  Specifies CEL expressions to request specific devices from the specified device class.

- **Resource claim for partitioned devices**

  The following example resource claim uses a CEL expression to request one device in the `example-device-class` device class. Here, the `exactly` parameter indicates that a node with the specific requested device must be available before the scheduler can create the pod.

  <div class="formalpara-title">

  **Example resource claim object**

  </div>

  ``` yaml
  apiVersion: resource.k8s.io/v1
  kind: ResourceClaim
  metadata:
    namespace: gpu-claim
    name: gpu-devices
  spec:
    devices:
      requests:
      - name: req-0
        exactly:
          name: 2g-10gb
          deviceClassName: example-device-class
          selectors:
          - cel:
              expression: "device.attributes['driver.example.com'].profile == '2g.10gb'"
  ```

- **Resource claim template for consumable capacity**

  The following example resource claim template requests consumable capacity. This example includes one device request that the scheduler must satisfy for the claim to succeed.

  <div class="formalpara-title">

  **Example resource claim template object for consumable capacity**

  </div>

  ``` yaml
  apiVersion: resource.k8s.io/v1
  kind: ResourceClaimTemplate
  metadata:
    name: memory-claim-template
  spec:
    spec:
      devices:
        requests:
        - name: req-0
          exactly:
            deviceClassName: example-device-class
            capacity:
              requests:
                memory: 4Gi
  ```

- **Resource claim for consumable capacity**

  The following example resource claim requests a specific portion (4Gi) of that shared device’s consumable capacity.

  <div class="formalpara-title">

  **Example resource claim object**

  </div>

  ``` yaml
  apiVersion: resource.k8s.io/v1
  kind: ResourceClaim
  metadata:
    name: shared-gpu-claim
  spec:
    devices:
      requests:
        - name: gpu-request
          exactly:
            deviceClassName: gpu.example.com
            capacity:
              requests:
                memory: 4Gi
  ```

## About DRA admin access

When working with Dynamic Resource Allocation (DRA), as a cluster administrator you can gain privileged access to a device that is in use by other users, so that you can perform tasks such as monitoring the health and status of the device while ensuring that users can continue to use the device.

To gain admin access, an administrator must create a resource claim or resource claim template with the `adminAccess: true` parameter in a namespace that includes the `resource.kubernetes.io/admin-access: "true"` label. Non-administrator users cannot access namespaces with this label.

<div class="formalpara-title">

**Example namespace with admin access label**

</div>

``` yaml
apiVersion: v1
kind: Namespace
metadata:
  labels:
    resource.kubernetes.io/admin-access: "true"
# ...
```

In the following example, the administrator is granted access to the `2g-10gb` device:

<div class="formalpara-title">

**Example resource claim object with admin access**

</div>

``` yaml
apiVersion: resource.k8s.io/v1
kind: ResourceClaimTemplate
metadata:
  name: large-black-cat-claim-template
spec:
  devices:
    requests:
    - name: req-0
      exactly:
        allocationMode: All
        adminAccess: true
        deviceClassName: example-device-class
        selectors:
        - cel:
            expression: "device.attributes['driver.example.com'].profile == '2g.10gb'"
```

where:

`spec.devices.requests.exactly.adminAccess.true` or `spec.devices.requests.firstAvailable.adminAccess.true`
Specifies that the admin access mode is enabled for the specified device.

For information on adding a resource claim to a pod, see "Adding resource claims to pods".

- [Adding resource claims to pods](../../nodes/pods/nodes-pods-allocate-dra.xml#nodes-pods-allocate-dra-configure_nodes-pods-allocate-dra)

## About DRA device binding conditions

When working with Dynamic Resource Allocation (DRA), you can improve scheduling reliability by using *device binding conditions* to allow the scheduler to delay pod scheduling until specific external resources, such as fabric-attached GPUs or reprogrammable FPGAs, are confirmed to be ready.

For example, you can use device binding conditions to ensure that High-Performance Computing (HPC) workloads that require specialized network-attached devices are scheduled only on nodes where those devices are pre-attached and ready for use. Or, you could ensure that storage devices are ready for your storage-intensive applications before scheduling the workloads.

To configure device binding conditions, use your third-party DRA driver to publish the following fields in the `devices` section of a resource slice:

- `bindingConditions` is a list of condition types that must be `True` in the `status.devices` field of the associated resource claim before the pod can be bound. These conditions typically represent readiness signals, such as `DeviceAttached` or `DeviceInitialized`. You can specify a maximum of four condition types.

- `bindingFailureConditions` is a list of condition types that indicate a failure state. If any of these conditions is `True` in the `status.devices` field of the associated resource claim, the scheduler clears the allocation and reschedules the pod. You can specify a maximum of four condition types.

- `bindsToNode` sets a node selector inside the resource claim that external controllers can use to perform node-specific operations such as device attachment or preparation. If set to `True`, the scheduler records the selected node name in the `status.allocation.nodeSelector` field of the resource claim. This does not affect the pod’s `spec.nodeSelector` field.

All condition types listed in the `bindingConditions` and `bindingFailureConditions` fields are evaluated by the scheduler from the `status.conditions` field of a resource claim. External controllers are responsible for updating these conditions by using standard Kubernetes condition semantics, such as `type`, `status`, `reason`, `message`, or `lastTransitionTime`.

When the scheduler allocates a device that specifies binding conditions, it copies the `bindingConditions` and `bindingFailureConditions` fields from the resource slice into the matching entry in the `status.allocation.devices.results` field of the resource claim. The scheduler then evaluates those condition types against the entry in the `status.devices` field that has the same `driver`, `pool`, and `device` values. Until an entry matching the driver, pool, and device exists, the scheduler treats all binding conditions as pending. Each entry can contain a maximum of eight conditions.

The scheduler waits up to 600 seconds for all `bindingConditions` to become `True`. If the timeout is reached or any `bindingFailureConditions` is `True`, the scheduler clears the allocation and reschedules the pod.

## About device taints and tolerations

You can use device taints and tolerations with Dynamic Resource Allocation (DRA) to keep pods off of specific devices or restrict devices for specialized workloads.

You can use your DRA driver to taint a device by adding the taint to a `ResourceSlice` object. Consult your DRA driver documentation to learn if the driver uses taints and what their keys and values are.

For example, you can taint a device to reserve that device for specialized workloads. Or, if a device is not working or is offline for maintenance, you can prevent new pods from being scheduled on the device and remove any existing pods from the device.

The taint effect determines how the taint affects scheduling and existing workloads. You can use one of the following effects in the taint:

- The `NoSchedule` effect blocks new workloads from being added to the device, but leaves existing workloads in place.

- The `NoExecute` effect blocks new workloads from being added to the device and removes existing workloads. You can use the `tolerationSeconds` parameter in a toleration to control how long a workload can remain bound to a device before being evicted.

- The `None` effect is ignored by the scheduler. New workloads can be added to the device and existing workloads remain.

To allow pods to use a tainted device, add a matching toleration to a resource claim.

The following example resource claim contains a toleration for a typical `NoExecute` taint. In this example, associated pods tolerate the taint for up to 300 seconds after the taint is added, after which the pods are evicted.

``` yaml
apiVersion: resource.k8s.io/v1
kind: ResourceClaim
metadata:
  name: resilient-workload-claim
  namespace: default
spec:
  devices:
    requests:
    - name: req-0
      exactly:
        deviceClassName: example-device-class
        tolerations:
        - key: "dra.example.com/unhealthy"
          operator: "Equal"
          value: "Broken"
          effect: "NoExecute"
          tolerationSeconds: 300
```

# Adding resource claims to pods

You can use resource claims and resource claim templates with Attribute-Based GPU Allocation to allow you to request your workloads to be scheduled on nodes with specific graphics processing units (GPU).

Resource claims can be used with multiple pods, but resource claim templates can be used with only one pod. For more information, see "About GPU allocation objects and concepts".

The example in the following procedure creates a resource claim to schedule a pod on a node with the assign a specific GPU to and a resource claim to share a GPU between `container1` and `container2`.

- A Dynamic Resource Allocation (DRA) driver is installed. For more information on DRA, see ["Dynamic Resource Allocation"](https://kubernetes.io/docs/concepts/scheduling-eviction/dynamic-resource-allocation/) (Kubernetes documentation).

- A resource slice has been created.

- A resource claim and/or resource claim template has been created.

  <div class="formalpara-title">

  **Example resource claim object**

  </div>

  ``` yaml
  apiVersion: resource.k8s.io/v1
  kind: ResourceClaim
  metadata:
    namespace: gpu-claim
    name: gpu-devices
  spec:
    devices:
      requests:
      - name: req-0
        exactly:
          name: 2g-10gb
          deviceClassName: example-device-class
          selectors:
          - cel:
              expression: "device.attributes['driver.example.com'].profile == '2g.10gb'"
  ```

  <div class="formalpara-title">

  **Example resource claim template object**

  </div>

  ``` yaml
  apiVersion: resource.k8s.io/v1
  kind: ResourceClaimTemplate
  metadata:
    namespace: gpu-claim
    name: gpu-devices
  spec:
    spec:
      devices:
        requests:
        - name: req-0
          firstAvailable:
          - name: 2g-10gb
            deviceClassName: example-device-class
            selectors:
            - cel:
                expression: "device.attributes['driver.example.com'].profile == '2g.10gb'"
          - name: 3g-20gb
            deviceClassName: example-device-class
            selectors:
            - cel:
                expression: "device.attributes['driver.example.com'].profile == '3g.20gb'"
  ```

1.  Create a pod by creating a YAML file similar to the following:

    <div class="formalpara-title">

    **Example pod that is requesting resources**

    </div>

    ``` yaml
    apiVersion: v1
    kind: Pod
    metadata:
      namespace: gpu-allocate
      name: pod1
      labels:
        app: pod
    spec:
      restartPolicy: Never
      containers:
      - name: container0
        image: ubuntu:24.04
        command: ["sleep", "9999"]
        resources:
          claims:
          - name: gpu-claim-template
      - name: container1
        image: ubuntu:24.04
        command: ["sleep", "9999"]
        resources:
          claims:
          - name: gpu-claim
      - name: container2
        image: ubuntu:24.04
        command: ["sleep", "9999"]
        resources:
          claims:
          - name: gpu-claim
      resourceClaims:
      - name: gpu-claim-template
        resourceClaimTemplateName: gpu-devices-template
      - name: gpu-claim
        resourceClaimName: gpu-devices
    ```

    where:

    `spec.container.resource.claims`
    Specifies one or more resource claims to use with this container.

    `spec.resourceClaims`
    Specifies the resource claims that are required for the containers to start. Include an arbitrary name for the resource claim request and a resource claim, resource claim template, or both.

2.  Create the CRD object:

    ``` terminal
    $ oc create -f <file_name>.yaml
    ```

    For more information on configuring pod resource requests, see ["Dynamic Resource Allocation"](https://kubernetes.io/docs/concepts/scheduling-eviction/dynamic-resource-allocation/) (Kubernetes documentation).

<!-- -->

1.  Examine the pod status to confirm that the resource claim was used by running the following command:

    ``` terminal
    $ oc get pod <pod_name> -n <namespace_name> -o yaml
    ```

    Replace `<pod_name>` with the name of your pod and `<namespace_name>` with the name of your namespace.

    <div class="formalpara-title">

    **Example output**

    </div>

    ``` terminal
    kind: Pod
    apiVersion: v1
    metadata:
      name: pod1
    # ...
    status:
    # ...
      resourceClaimStatuses:
        - name: gpu-claim
          resourceClaimName: pod1-gpu-claim-l8bqt
    # ...
    ```

2.  Examine the resource claim object by running the following command:

    ``` terminal
    $ oc get resourceclaim <resourceclaim_name> -n <namespace_name> -o yaml
    ```

    Replace `<resourceclaim_name>` with the name of your claim and `<namespace_name>` with the name of your namespace.

    <div class="formalpara-title">

    **Example output**

    </div>

    ``` terminal
    apiVersion: resource.k8s.io/v1
    kind: ResourceClaim
    metadata:
      annotations:
        resource.kubernetes.io/pod-claim-name: gpu-claim
      name: pod1-gpu-claim-l8bqt
    # ...
    status:
      allocation:
        devices:
          results:
          - consumedCapacity:
              memory: 4Gi
            device: gpu-0
            driver: dra.example.com
            pool: pool
            request: gpu-request
            shareID: 265cc3ad-60d6-4f49-a9ac-9d5af08cb2d9
    # ...
    ```

    In this example, the scheduler allocated a share of the `gpu-0` device from the `dra.example.com` DRA driver. The `consumedCapacity` field shows how much of the device’s memory this claim consumed. The `shareID` field identifies this allocation share.

# Additional resources

- [Enabling features using feature gates](../../nodes/clusters/nodes-cluster-enabling-features.xml#nodes-cluster-enabling-features)
