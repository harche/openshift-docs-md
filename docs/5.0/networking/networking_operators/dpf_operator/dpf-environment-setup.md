Before installing the NVIDIA DPF Operator, you must set up the management cluster, configure worker nodes, and install and configure the required Operators.

# Set up the management cluster

The management cluster is a standard OpenShift Container Platform 4.17 cluster installed by using the Assisted Installer. This cluster hosts the DPF Operators and the hosted control planes for managing the hosted cluster on DPUs.

- You have access to the [Red Hat Hybrid Cloud Console](https://console.redhat.com/openshift/create).

- You have the OpenShift CLI (`oc`) installed.

1.  Go to the [Red Hat Hybrid Cloud Console cluster creation page](https://console.redhat.com/openshift/create) and create a cluster with control-plane nodes only. Select **Data center** → **Assisted Installer**.

2.  Optional: Configure jumbo MTU for each control plane node.

    1.  Under **Hosts' network configuration** in the Assisted Installer wizard, select **Static IP, bridges, and bonds**.

    2.  Set the **Static network configurations** section per node according to the following template, using the relevant MAC address and interface name for each node:

        ``` yaml
        interfaces:
          - ipv4:
              dhcp: true
              enabled: true
            mac-address: <xx:xx:xx:xx:xx:xx>
            mtu: 1500 # Set to 1500 for standard MTU or 9000 for jumbo frames
            name: <interface-name>
            state: up
            type: ethernet
        ```

        <div class="note">

        - You can alternatively configure MTU allocation on the DHCP server that allocates IPs to the control plane nodes.

        - If virtual machines are used for control-plane nodes, the MTU must be set on the bridge of the hypervisor used by the VMs.

        - When using MTU 9000, ensure the switch ports that connect the cluster’s control-plane nodes are set to handle jumbo frames.

        </div>

3.  Select the following operators to install with the cluster:

    - **Storage** → **Logical Volume Manager Storage**

    - **Platform Operations & Lifecycle** → **MultiCluster Engine**

    - **Scheduling** → **Node Feature Discovery**

4.  Click **Add hosts** to add hosts to the cluster. Only control plane nodes are required at this stage.

5.  After the installation completes, download the `KUBECONFIG` file and save it as `mgmt-kubeconfig`.

<!-- -->

1.  Set the `KUBECONFIG` environment variable:

    ``` terminal
    $ export KUBECONFIG="$(pwd)/mgmt-kubeconfig"
    ```

2.  Verify that all nodes are in a `Ready` state:

    ``` terminal
    $ oc get nodes
    ```

# Configure worker nodes for DPU operation

You must deploy the `dpu-worker-config` Helm chart to configure worker nodes with DPUs before adding those nodes to the management cluster. The `dpu-worker-config` Helm chart creates the `MachineConfigPool`, `dpu-worker-configuration` MachineConfig, and other required resources that configure the bridge, OVS services, and IP routing on worker nodes. The `MachineConfigPool` groups DPU-equipped worker nodes so that the Machine Config Operator can apply DPU-specific configurations to them.

The MachineConfig resource performs several configuration tasks required by DPF:

- **Bridge Configuration**: Creates a `br-ex` bridge interface that enables communication between the DPU and the hosted cluster control plane running on the management cluster. This name must match the `dpuNodeOOBBridgeName` value in the `DPFOperatorConfig` resource, or DPU provisioning fails. For more information refer to [DPF Operator Prerequisites](https://networking-docs.nvidia.com/dpf/26.4.1/host-network-configuration-prerequisites).

- **OVS Service Management**: Disables OpenShift’s default OVS services on x86 worker nodes. This is required for OVN-Kubernetes DPU Host mode operation, where networking functions are offloaded to the DPU rather than running on the host CPU.

- **IP Rules Configuration**: Sets routing rules required for pod-to-host control-plane traffic.

<!-- -->

- You have access to the cluster as a user with the `cluster-admin` role.

- You have installed the OpenShift CLI (`oc`).

- The Helm CLI (`helm`) is installed on your workstation.

- You have a pull secret file that includes credentials for `registry.redhat.io`. Helm reads its registry credentials from this file, which is separate from the container runtime configuration.

1.  Set the `OPENSHIFT_PULL_SECRET` environment variable to the path of your pull secret file:

    ``` terminal
    $ export OPENSHIFT_PULL_SECRET="/root/pull-secret.txt"
    ```

2.  Deploy the `dpu-worker-config` Helm chart to create the worker node MachineConfig:

    ``` terminal
    $ helm upgrade --install dpu-worker-config \
        oci://registry.redhat.io/dpu-kit-for-nvidia/dpu-worker-config-chart \
        --version 4.22.0 \
        --registry-config "${OPENSHIFT_PULL_SECRET}" \
        --namespace dpf-hcp-provisioner-system \
        --create-namespace \
        --disable-openapi-validation
    ```

- Verify that the `dpu-worker-config` Helm release is deployed:

  ``` terminal
  $ helm list -n dpf-hcp-provisioner-system
  ```

- Verify that the `MachineConfigPool` was created automatically:

  ``` terminal
  $ oc get mcp worker-dpu
  ```

  <div class="formalpara-title">

  **Example output**

  </div>

  ``` terminal
  NAME         CONFIG                                                 UPDATED   UPDATING   DEGRADED   MACHINECOUNT   READYMACHINECOUNT   UPDATEDMACHINECOUNT   DEGRADEDMACHINECOUNT   AGE
  worker-dpu   rendered-worker-dpu-b4a44cc606c2ffcf07067d1e943a8758   True      False      False      0              0                   0                     0                      2m
  ```

- Verify that the `dpu-worker-configuration` MachineConfig is created:

  ``` terminal
  $ oc get machineconfig dpu-worker-configuration
  ```

  <div class="formalpara-title">

  **Example output**

  </div>

  ``` terminal
  NAME                       GENERATEDBYCONTROLLER   IGNITIONVERSION   AGE
  dpu-worker-configuration                           3.2.0             2m
  ```

<div class="note">

The Machine Config Operator automatically reboots worker nodes to apply DPU-specific configurations after nodes with the `worker-dpu` label are added to the cluster.

</div>

# Create the DPF namespace

You must create a dedicated namespace for the DPF Operator and its components before installing the Operator.

- You have access to the cluster as a user with the `cluster-admin` role.

- You have installed the OpenShift CLI (`oc`).

<!-- -->

- Create the `dpf-operator-system` namespace:

  ``` terminal
  $ oc create namespace dpf-operator-system
  ```

<!-- -->

- Verify that the namespace was created:

  ``` terminal
  $ oc get namespace dpf-operator-system
  ```

# Required Operators

Before you install the DPF Operator, you must install the cert-manager Operator for Red Hat OpenShift, MetalLB Operator, Red Hat OpenShift GitOps, and NVIDIA Maintenance Operator.

The multicluster engine Operator and the Node Feature Discovery Operator can be installed during management cluster creation by using the Assisted Installer. After installation, configure those Operators, MetalLB, GitOps, and the Cluster Network Operator as described in "Configure the required Operators".

## Install the NVIDIA Maintenance Operator

The NVIDIA Maintenance Operator assists in performing maintenance tasks and gracefully draining DPU worker nodes. You install this operator by using Helm.

- You have access to the cluster as a user with the `cluster-admin` role.

- You have installed the OpenShift CLI (`oc`).

- You have installed the Helm CLI (`helm`).

1.  Create a Helm values file named `maintenance-operator-values.yaml` with the following content:

    ``` yaml
    operatorConfig:
      deploy: true
      maxParallelOperations: 60%
    operator:
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
              - matchExpressions:
                  - key: "node-role.kubernetes.io/master"
                    operator: Exists
              - matchExpressions:
                  - key: "node-role.kubernetes.io/control-plane"
                    operator: Exists
      tolerations:
        - key: node-role.kubernetes.io/master
          operator: Exists
          effect: NoSchedule
        - key: node-role.kubernetes.io/control-plane
          operator: Exists
          effect: NoSchedule
    ```

2.  Install the Operator by using Helm:

    ``` terminal
    $ helm upgrade --install maintenance-operator oci://ghcr.io/mellanox/maintenance-operator-chart \
      --namespace dpf-operator-system \
      --create-namespace \
      --disable-openapi-validation \
      --version 0.3.0 \
      --values maintenance-operator-values.yaml \
      --wait
    ```

- Verify that the Operator pod is running:

  ``` terminal
  $ oc get pods -n dpf-operator-system
  ```

  <div class="formalpara-title">

  **Example output**

  </div>

  ``` terminal
  maintenance-operator-585767f779-kps9c   1/1     Running   0          2d23h
  ```

<!-- -->

- [Installing the cert-manager Operator for Red Hat OpenShift](../../../security/cert_manager_operator/cert-manager-operator-install.xml#cert-manager-operator-install)

- [Installing the MetalLB Operator](../metallb-operator/metallb-operator-install.xml#metallb-operator-install)

- [Installing Red Hat OpenShift GitOps](https://docs.openshift.com/gitops/latest/installing_gitops/installing-openshift-gitops.html#installing-openshift-gitops)

- [DPF Operator prerequisites](https://networking-docs.nvidia.com/dpf/26.4.1/host-network-configuration-prerequisites)

# Configure the required Operators

After the required Operators are installed, configure Node Feature Discovery, MetalLB, GitOps, and Cluster Network Operator for the DPF environment. This procedure also verifies that the multicluster engine and hosted control planes components are ready.

- You have access to the cluster as a user with the `cluster-admin` role.

- You have installed the OpenShift CLI (`oc`).

- You have installed the cert-manager Operator for Red Hat OpenShift, MetalLB Operator, Red Hat OpenShift GitOps, and NVIDIA Maintenance Operator.

- You have installed the Logical Volume Manager Storage Operator, multicluster engine operator, and the Node Feature Discovery Operator. You can install them by using the Assisted Installer during cluster creation. For manual installation, see [Installing multicluster engine operator](https://docs.redhat.com/en/documentation/red_hat_advanced_cluster_management_for_kubernetes/2.17/html/install/index) and ensure that the hosted control planes component is enabled.

1.  Define the cluster variables used by Node Feature Discovery:

    ``` terminal
    $ export CLUSTER_NAME="doca-mgmt"
    $ export BASE_DOMAIN="example.com"
    $ export HOST_CLUSTER_API="api.${CLUSTER_NAME}.${BASE_DOMAIN}"
    ```

    where:

    `CLUSTER_NAME`
    Specifies the management cluster name.

    `BASE_DOMAIN`
    Specifies the management cluster base domain.

    `HOST_CLUSTER_API`
    Specifies the management cluster API endpoint.

2.  Create a file named `nfd-instance.yaml` with the following `NodeFeatureDiscovery` resource definition:

    ``` yaml
    apiVersion: nfd.openshift.io/v1
    kind: NodeFeatureDiscovery
    metadata:
      name: nfd-instance
      namespace: openshift-nfd
    spec:
      operand:
        workerEnvs:
          - name: KUBERNETES_SERVICE_HOST
            value: $HOST_CLUSTER_API
          - name: KUBERNETES_SERVICE_PORT
            value: "6443"
      workerConfig:
        configData: |
          sources:
            pci:
              deviceClassWhitelist:
                - "0200"
                - "03"
                - "12"
                - "0207"
              deviceLabelFields:
                - "vendor"
                - "device"
                - "class"
    ```

3.  Apply the file by using `envsubst` to substitute the environment variables:

    ``` terminal
    $ envsubst < nfd-instance.yaml | oc apply -f -
    ```

4.  Create a file named `nfd-rule.yaml` with the following `NodeFeatureRule` resource definition to detect worker nodes with DPUs and label them with a `dpu-enabled` label:

    ``` yaml
    apiVersion: nfd.openshift.io/v1alpha1
    kind: NodeFeatureRule
    metadata:
      name: dpu-detection-rule
      namespace: openshift-nfd
    spec:
      rules:
        - labels:
            dpu-enabled: ""
          matchFeatures:
            - feature: pci.device
              matchExpressions:
                device:
                  op: In
                  value:
                    - a2d6
                    - a2dc
                vendor:
                  op: In
                  value:
                    - 15b3
          name: DPU-detection-rule
    ```

5.  Apply the file:

    ``` terminal
    $ oc apply -f nfd-rule.yaml
    ```

6.  Ensure that the MetalLB Operator `Subscription` schedules Operator pods on control-plane nodes. When you install the MetalLB Operator, include the following `spec.config` settings, or patch an existing `Subscription` to add them:

    ``` yaml
    apiVersion: operators.coreos.com/v1alpha1
    kind: Subscription
    metadata:
      name: metallb-operator
      namespace: openshift-operators
    spec:
      channel: "stable"
      name: metallb-operator
      source: redhat-operators
      sourceNamespace: openshift-marketplace
      installPlanApproval: Automatic
      config:
        tolerations:
        - key: "node-role.kubernetes.io/control-plane"
          operator: "Exists"
          effect: "NoSchedule"
        affinity:
          nodeAffinity:
            requiredDuringSchedulingIgnoredDuringExecution:
              nodeSelectorTerms:
              - matchExpressions:
                - key: "node-role.kubernetes.io/control-plane"
                  operator: "Exists"
    ```

7.  Create a file named `metallb-config.yaml` with the following `MetalLB` resource definition:

    ``` yaml
    apiVersion: metallb.io/v1beta1
    kind: MetalLB
    metadata:
      name: metallb
      namespace: openshift-operators
    spec:
      nodeSelector:
        node-role.kubernetes.io/control-plane: ""
      speakerTolerations:
        - key: node-role.kubernetes.io/control-plane
          operator: Exists
          effect: NoSchedule
    ```

8.  Apply the MetalLB resource file:

    ``` terminal
    $ oc apply -f metallb-config.yaml
    ```

9.  Ensure that the Red Hat OpenShift GitOps `Subscription` includes the DPF-required environment variables. When you install the Operator, set the following `spec.config.env` values, or patch an existing `Subscription` to add them so that Argo CD can manage the `dpf-operator-system` namespace:

    ``` yaml
    apiVersion: operators.coreos.com/v1alpha1
    kind: Subscription
    metadata:
      name: openshift-gitops-operator
      namespace: openshift-gitops-operator
    spec:
      channel: gitops-1.21
      config:
        env:
        - name: ARGOCD_CLUSTER_CONFIG_NAMESPACES
          value: "openshift-gitops,dpf-operator-system"
        - name: CONTROLLER_CLUSTER_ROLE
          value: "cluster-admin"
        - name: SERVER_CLUSTER_ROLE
          value: "cluster-admin"
      installPlanApproval: Automatic
      name: openshift-gitops-operator
      source: redhat-operators
      sourceNamespace: openshift-marketplace
      startingCSV: openshift-gitops-operator.v1.21.3
    ```

10. Create a file named `argocd-instance.yaml` with the following `ArgoCD` resource definition:

    ``` yaml
    apiVersion: argoproj.io/v1beta1
    kind: ArgoCD
    metadata:
      name: argocd
      namespace: dpf-operator-system
    spec:
      nodePlacement:
        nodeSelector:
          node-role.kubernetes.io/control-plane: ""
        tolerations:
        - key: node-role.kubernetes.io/master
          operator: Exists
          effect: NoSchedule
        - key: node-role.kubernetes.io/control-plane
          operator: Exists
          effect: NoSchedule
      server:
        route:
          enabled: true
      controller: {}
      repo: {}
      applicationSet:
        enabled: false
      resourceExclusions: |
        - apiGroups:
          - packages.operators.coreos.com
          kinds:
          - PackageManifest
      sso:
        provider: dex
        dex:
          openShiftOAuth: true
      notifications:
        enabled: false
    ```

11. Apply the Argo CD file:

    ``` terminal
    $ oc apply -f argocd-instance.yaml
    ```

12. Wait for the ArgoCD Redis deployment to be ready:

    ``` terminal
    $ oc wait deployment argocd-redis -n dpf-operator-system \
      --for=condition=Available --timeout=120s
    ```

13. Enable global IP forwarding on the OVN-Kubernetes configuration:

    This command enables IP packet forwarding between different networks managed by OVN-Kubernetes.

    ``` terminal
    $ oc patch network.operator.openshift.io cluster --type=merge -p \
      '{"spec":{"defaultNetwork":{"ovnKubernetesConfig":{"gatewayConfig":{"ipForwarding":"Global"}}}}}'
    ```

- Verify that the `MultiClusterEngine` instance is created:

  ``` terminal
  $ oc get multiclusterengine mce
  ```

  <div class="formalpara-title">

  **Example output**

  </div>

  ``` terminal
  NAME   STATUS      AGE     CURRENTVERSION   DESIREDVERSION   MESSAGE
  mce    Available   4m58s   2.17.2           2.17.2           All components available
  ```

- Verify that the hosted control planes component is enabled:

  ``` terminal
  $ oc get multiclusterengine mce -o jsonpath='{.spec.overrides.components[?(@.name=="hypershift")].enabled}{"\n"}'
  ```

  <div class="note">

  If the previous command returns `false` or an empty result, hosted control planes is not enabled and DPU provisioning fails.

  To continue, you must enable the `hypershift` component on the `MultiClusterEngine` resource. In current multicluster engine Operator versions the component is named `hypershift`; earlier versions use `hypershift-preview`.

  - If the result is empty, no `hypershift` entry exists. Run the following command to add the entry and enable it:

    ``` terminal
    $ oc patch mce multiclusterengine --type=json \
        -p='[{"op":"add","path":"/spec/overrides/components/-","value":{"name":"hypershift","enabled":true}}]'
    ```

  - If the result is `false`, an entry exists but is disabled. Edit the resource and set the `hypershift` component to `enabled: true`:

    ``` terminal
    $ oc edit multiclusterengine mce
    ```

  </div>

  <div class="important">

  Do not use `oc patch --type=merge` to enable the component, because a merge patch replaces the entire `components` array and removes the other components. Use the JSON `add` patch when no entry exists, or `oc edit` when an entry exists but is disabled.

  </div>

- Verify that the `NodeFeatureDiscovery` instance and `NodeFeatureRule` are configured:

  ``` terminal
  $ oc get nodefeaturediscovery,nodefeaturerule -n openshift-nfd
  ```

- Verify that the `MetalLB` instance was created:

  ``` terminal
  $ oc get metallb -n openshift-operators
  ```

- Verify that the Argo CD pods are running:

  ``` terminal
  $ oc get pods -n dpf-operator-system -l app.kubernetes.io/part-of=argocd
  ```

- Verify that IP forwarding is set to `Global`:

  ``` terminal
  $ oc get network.operator.openshift.io cluster -o jsonpath='{.spec.defaultNetwork.ovnKubernetesConfig.gatewayConfig.ipForwarding}'
  ```

  <div class="formalpara-title">

  **Example output**

  </div>

  ``` terminal
  Global
  ```
