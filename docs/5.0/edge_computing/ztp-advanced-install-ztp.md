You can use `ClusterInstance` custom resources (CRs) to deploy custom functionality and configurations in your managed clusters at installation time.

# Customizing extra installation manifests in the GitOps ZTP pipeline

You can define a set of extra manifests for inclusion in the installation phase of the GitOps Zero Touch Provisioning (ZTP) pipeline. These manifests are linked to the `ClusterInstance` custom resources (CRs) and are applied to the cluster during installation. Including `MachineConfig` CRs at install time makes the installation process more efficient.

Extra manifests must be packaged in `ConfigMap` resources and referenced in the `extraManifestsRefs` field of the `ClusterInstance` CR.

- Create a Git repository where you manage your custom site configuration data. The repository must be accessible from the hub cluster and be defined as a source repository for the Argo CD application.

1.  Create a set of extra manifest CRs that the GitOps ZTP pipeline uses to customize the cluster installs.

2.  In your `/clusterinstance` directory, create a subdirectory with your extra manifests. The following example illustrates a sample folder structure:

    ``` text
    clusterinstance/
    ├── site1-sno-du.yaml
    ├── extra-manifest/
    │   ├── 01-example-machine-config.yaml
    │   ├── enable-crun-master.yaml
    │   └── enable-crun-worker.yaml
    └── kustomization.yaml
    ```

3.  Create or update the `kustomization.yaml` file to use `configMapGenerator` to package your extra manifests into a `ConfigMap`:

    ``` yaml
    apiVersion: kustomize.config.k8s.io/v1beta1
    kind: Kustomization
    resources:
      - site1-sno-du.yaml
    configMapGenerator:
      - name: extra-manifests-cm
        namespace: site1-sno-du
        files:
          - extra-manifest/01-example-machine-config.yaml
          - extra-manifest/enable-crun-master.yaml
          - extra-manifest/enable-crun-worker.yaml
    generatorOptions:
      disableNameSuffixHash: true
    ```

    - The `configMapGenerator.namespace` value must match the `ClusterInstance` namespace.

    - Setting `generatorOptions.disableNameSuffixHash` to `true` disables the hash suffix so the `ConfigMap` name is predictable.

4.  In your `ClusterInstance` CR, reference the `ConfigMap` in the `extraManifestsRefs` field:

    ``` yaml
    apiVersion: siteconfig.open-cluster-management.io/v1alpha1
    kind: ClusterInstance
    metadata:
      name: "site1-sno-du"
      namespace: "site1-sno-du"
    spec:
      clusterName: "site1-sno-du"
      networkType: "OVNKubernetes"
      extraManifestsRefs:
        - name: extra-manifests-cm
      # ...
    ```

    - The `extraManifestsRefs` field references the `ConfigMap` containing the extra manifests.

5.  Commit the `ClusterInstance` CR, extra manifest files, and `kustomization.yaml` to your Git repository and push the changes.

    During cluster provisioning, the SiteConfig Operator applies the CRs contained in the referenced `ConfigMap` resources as extra manifests.

    <div class="note">

    You can reference multiple `ConfigMap` resources in `extraManifestsRefs` to organize your manifests logically. For example, you might have separate `ConfigMap` resources for crun configuration, custom `MachineConfig` CRs, and other Day 0 configurations.

    </div>

# Customizing the br-ex bridge at installation time in the GitOps ZTP pipeline

By default, OpenShift Container Platform automatically configures the Open vSwitch (OVS) `br-ex` bridge on bare-metal nodes. For advanced networking requirements, you can override this default behavior by defining a customized `br-ex` bridge in an NMState configuration. When you configure the customized `br-ex` bridge as part of the GitOps Zero Touch Provisioning (ZTP) installation, the configuration is applied during cluster provisioning. This eliminates the need for the Day 2 migration procedure, which requires a node reboot.

To customize the `br-ex` bridge at installation time in the GitOps ZTP pipeline, you create a `MachineConfig` object that includes the customized `br-ex` bridge configuration, package it as a `ConfigMap`, and reference it in your `ClusterInstance` CR.

<div class="note">

The customized `br-ex` bridge configuration cannot be included directly in the `ClusterInstance` CR. Using a `MachineConfig` object as an extra manifest is currently the only supported method to configure a customized `br-ex` bridge at installation time.

</div>

- You configured a Git repository where you manage your custom site configuration data. The repository must be accessible from the hub cluster and be defined as a source repository for the Argo CD application.

- You created a `MachineConfig` object that includes your customized `br-ex` bridge NMState configuration. For detailed instructions on creating the NMState configuration and `MachineConfig` object, see "Creating a manifest object that includes a customized br-ex bridge".

1.  In your `/clusterinstance` directory, create an `extra-manifest` subdirectory and save the `MachineConfig` object to a file in this directory, for example, `extra-manifest/10-br-ex-master.yaml`.

2.  Create or update the `kustomization.yaml` file to use `configMapGenerator` to package the `MachineConfig` object into a `ConfigMap`:

    ``` yaml
    apiVersion: kustomize.config.k8s.io/v1beta1
    kind: Kustomization
    resources:
      - site1-sno-du.yaml
    configMapGenerator:
      - name: br-ex-extra-manifest
        namespace: site1-sno-du
        files:
          - extra-manifest/10-br-ex-master.yaml
    generatorOptions:
      disableNameSuffixHash: true
    ```

    - The `configMapGenerator.namespace` value must match the `ClusterInstance` namespace.

    - Setting `generatorOptions.disableNameSuffixHash` to `true` disables the hash suffix so the `ConfigMap` name is predictable.

3.  In your `ClusterInstance` CR, reference the `ConfigMap` in the `extraManifestsRefs` field:

    ``` yaml
    apiVersion: siteconfig.open-cluster-management.io/v1alpha1
    kind: ClusterInstance
    metadata:
      name: "site1-sno-du"
      namespace: "site1-sno-du"
    spec:
      clusterName: "site1-sno-du"
      networkType: "OVNKubernetes"
      extraManifestsRefs:
        - name: br-ex-extra-manifest
      # ...
    ```

4.  Commit the `ClusterInstance` CR, `MachineConfig` object, and `kustomization.yaml` file to your Git repository and push the changes.

    During cluster provisioning, the SiteConfig Operator applies the `MachineConfig` object as an extra manifest, and the customized `br-ex` bridge configuration is applied to each node without requiring a reboot.

- On the hub cluster, verify that the `ConfigMap` that contains the `MachineConfig` object exists by running the following command:

  ``` terminal
  $ oc get configmap br-ex-extra-manifest -n site1-sno-du
  ```

- After the cluster installation is complete, verify that the `MachineConfig` object exists on the managed cluster by running the following command:

  ``` terminal
  $ oc get machineconfig 10-br-ex-master
  ```

# Configuring cluster network MTU at installation time

You can explicitly set the cluster network maximum transmission unit (MTU) during installation by including a `Network` custom resource (CR) as an extra manifest in the GitOps Zero Touch Provisioning (ZTP) pipeline.

Setting the cluster network MTU with additional headroom during deployment prevents the need for a Day 2 MTU update that requires at least two rolling reboots of all cluster nodes.

During installation, the Cluster Network Operator (CNO) automatically calculates the cluster network MTU based on the primary network interface MTU. When you enable IPsec at installation time, the calculation includes both the OVN-Kubernetes overhead of 100 bytes and the IPsec overhead. If you plan to enable IPsec or another encapsulation technology as a Day 2 operation, the calculated MTU includes only the OVN-Kubernetes overhead and might be insufficient.

By explicitly setting the cluster network MTU at installation time, you can include additional headroom for those future needs and avoid a disruptive MTU migration.

<div class="important">

The cluster network MTU value must be lower than the machine network MTU by at least 100 bytes to account for OVN-Kubernetes overlay overhead. If you plan to enable IPsec as a Day 2 operation, allow an additional 46 bytes for IPsec headroom. For example, with a machine network MTU of `9100` bytes, set the cluster network MTU to `8900` bytes, which accounts for the following offset:

- OVN-Kubernetes overhead: 100 bytes

- IPsec headroom: 46 bytes

- Extra headroom: 54 bytes

- Total offset: 200 bytes

To avoid selecting an MTU value that a node cannot support, verify the maximum MTU (`maxmtu`) that the network interface accepts by running the `ip -d link` command.

</div>

- You have configured the hub cluster to provision managed clusters by using the GitOps ZTP pipeline.

- You have a Git repository where you manage your custom site configuration data. The repository must be accessible from the hub cluster and be defined as a source repository for the Argo CD application.

1.  In your `ClusterInstance` CR, set the machine network MTU on the network interface for all nodes.

    The following example configures a VLAN interface with MTU `9100`:

    ``` yaml
    apiVersion: siteconfig.open-cluster-management.io/v1alpha1
    kind: ClusterInstance
    metadata:
      name: "site1-sno-du"
      namespace: "site1-sno-du"
    spec:
      nodes:
        - hostName: "node1.example.com"
          nodeNetwork:
            interfaces:
              - name: "bond0.120"
                macAddress: "00:00:00:00:00:00"
            config:
              interfaces:
                - name: bond0.120
                  type: vlan
                  state: up
                  mtu: 9100
                  ipv4:
                    enabled: true
                    dhcp: false
                    address:
                      - ip: "192.168.120.15"
                        prefix-length: 25
                  vlan:
                    base-iface: bond0
                    id: 120
      # ...
    ```

2.  Create a `Network` CR manifest file named `set-cluster-mtu.yaml` that sets the cluster network MTU:

    ``` yaml
    apiVersion: operator.openshift.io/v1
    kind: Network
    metadata:
      name: cluster
    spec:
      defaultNetwork:
        ovnKubernetesConfig:
          mtu: 8900
    ```

    where:

    `mtu`
    Specifies the cluster network MTU value. This value must be at least 100 bytes less than the machine network MTU. In this example, the value is 200 bytes less than the machine network MTU of 9100 to allow headroom for IPsec and other future requirements.

3.  In your `clusterinstance` directory, place the manifest file in an extra manifests subdirectory:

    ``` text
    clusterinstance/
    ├── site1-sno-du.yaml
    ├── extra-manifest/
    │   └── set-cluster-mtu.yaml
    └── kustomization.yaml
    ```

4.  Create or update the `kustomization.yaml` file to package the extra manifest into a `ConfigMap`:

    ``` yaml
    apiVersion: kustomize.config.k8s.io/v1beta1
    kind: Kustomization
    resources:
      - site1-sno-du.yaml
    configMapGenerator:
      - name: cluster-mtu-extra-manifests
        namespace: site1-sno-du
        files:
          - extra-manifest/set-cluster-mtu.yaml
    generatorOptions:
      disableNameSuffixHash: true
    ```

5.  In your `ClusterInstance` CR, reference the `ConfigMap` in the `extraManifestsRefs` field:

    ``` yaml
    apiVersion: siteconfig.open-cluster-management.io/v1alpha1
    kind: ClusterInstance
    metadata:
      name: "site1-sno-du"
      namespace: "site1-sno-du"
    spec:
      clusterName: "site1-sno-du"
      networkType: "OVNKubernetes"
      extraManifestsRefs:
        - name: cluster-mtu-extra-manifests
      # ...
    ```

6.  Commit the `ClusterInstance` CR, the `set-cluster-mtu.yaml` manifest, and the `kustomization.yaml` to your Git repository and push the changes.

    During cluster provisioning, the SiteConfig Operator applies the `Network` CR as an extra manifest, and the CNO uses the specified MTU value instead of auto-calculating it.

- After the cluster installation is complete, verify the cluster network MTU by running the following command:

  ``` terminal
  $ oc get networks.operator.openshift.io cluster -o yaml
  ```

  <div class="formalpara-title">

  **Example output**

  </div>

  ``` yaml
  apiVersion: operator.openshift.io/v1
  kind: Network
  metadata:
    name: cluster
  # ...
  spec:
    # ...
    defaultNetwork:
      ovnKubernetesConfig:
        # ...
        mtu: 8900
  ```

<!-- -->

- [Customizing extra installation manifests in the GitOps ZTP pipeline](../edge_computing/ztp-advanced-install-ztp.xml#ztp-customizing-the-install-extra-manifests_ztp-advanced-install-ztp)

- [Creating a manifest object that includes a customized br-ex bridge](../installing/installing_bare_metal/ipi/ipi-install-installation-workflow.xml#creating-manifest-file-customized-br-ex-bridge_ipi-install-installation-workflow)

# Deleting a node by using the ClusterInstance CR

By using a `ClusterInstance` custom resource (CR), you can delete and reprovision a node. This method is more efficient than manually deleting the node.

- You have configured the hub cluster to generate the required installation and policy CRs.

- You have created a Git repository in which you can manage your custom site configuration data. The repository must be accessible from the hub cluster and be defined as the source repository for the Argo CD application.

1.  Update the `ClusterInstance` CR to add the `bmac.agent-install.openshift.io/remove-agent-and-node-on-delete=true` annotation to the `BareMetalHost` resource for the node, and push the changes to the Git repository:

    ``` yaml
    apiVersion: siteconfig.open-cluster-management.io/v1alpha1
    kind: ClusterInstance
    metadata:
      name: "example-cluster"
      namespace: "example-cluster"
    spec:
      # ...
      nodes:
        - hostName: "worker-node2.example.com"
          role: "worker"
          extraAnnotations:
            BareMetalHost:
              bmac.agent-install.openshift.io/remove-agent-and-node-on-delete: "true"
    # ...
    ```

2.  Verify that the `BareMetalHost` object is annotated by running the following command:

    ``` terminal
    $ oc get bmh -n <cluster_namespace> <bmh_name> -ojsonpath='' | jq -r '.annotations["bmac.agent-install.openshift.io/remove-agent-and-node-on-delete"]'
    ```

    <div class="formalpara-title">

    **Example output**

    </div>

    ``` terminal
    true
    ```

3.  Delete the `BareMetalHost` CR by configuring the `pruneManifests` field in the `ClusterInstance` CR to remove the target `BareMetalHost` resource:

    ``` yaml
    apiVersion: siteconfig.open-cluster-management.io/v1alpha1
    kind: ClusterInstance
    metadata:
      name: "example-cluster"
      namespace: "example-cluster"
    spec:
      # ...
      nodes:
        - hostName: "worker-node2.example.com"
          role: "worker"
          pruneManifests:
            - apiVersion: metal3.io/v1alpha1
              kind: BareMetalHost
    # ...
    ```

4.  Push the changes to the Git repository and wait for deprovisioning to start. The status of the `BareMetalHost` CR should change to `deprovisioning`. Wait for the `BareMetalHost` to finish deprovisioning, and be fully deleted.

<!-- -->

1.  Verify that the `BareMetalHost` and `Agent` CRs for the worker node have been deleted from the hub cluster by running the following commands:

    ``` terminal
    $ oc get bmh -n <cluster_namespace>
    ```

    ``` terminal
    $ oc get agent -n <cluster_namespace>
    ```

2.  Verify that the node record has been deleted from the spoke cluster by running the following command:

    ``` terminal
    $ oc get nodes
    ```

    <div class="note">

    If you are working with secrets, deleting a secret too early can cause an issue because ArgoCD needs the secret to complete resynchronization after deletion. Delete the secret only after the node cleanup, when the current ArgoCD synchronization is complete.

    </div>

3.  After the `BareMetalHost` object is successfully deleted, remove the worker node definition from the `spec.nodes` section in the `ClusterInstance` CR and push the changes to the Git repository.

<div class="formalpara-title">

**Next steps**

</div>

To reprovision a node, add the node definition back to the `spec.nodes` section in the `ClusterInstance` CR, push the changes to the Git repository, and wait for the synchronization to complete. This regenerates the `BareMetalHost` CR of the worker node and triggers the re-install of the node.

# Replacing a failed control plane node by using the ClusterInstance CR

You can replace a failed control plane node on a OpenShift Container Platform cluster by removing the failed node from the `ClusterInstance` custom resource (CR) and then adding a replacement node. Complete the replacement before a second control plane failure can lose quorum.

<div class="warning">

If you reuse the same hostname for the replacement node, you must remove the failed node before you add the replacement. If you use a different hostname, the failed node can be removed before or after the replacement is added. Replace only one control plane node at a time. Replacing two control plane nodes in parallel can lose `etcd` quorum and make the cluster unrecoverable.

</div>

- You have deployed the managed cluster by using a `ClusterInstance` CR.

- At least two of the three control plane nodes are in the `Ready` state so that `etcd` still has a quorum.

- You have a replacement bare-metal host with baseboard management controller (BMC) credentials. If you reuse the same hardware, you can keep the existing BMC secret.

- Control plane nodes do not host OpenShift Data Foundation object storage daemons (OSDs) or monitors.

- You have the `kubeconfig` file for the hub cluster and the `kubeconfig` file for the managed cluster.

1.  Identify the failed control plane node on the managed cluster by running the following command:

    ``` terminal
    $ oc --kubeconfig <managed_cluster_kubeconfig> get nodes
    ```

    where:

    `<managed_cluster_kubeconfig>`
    Specifies the `kubeconfig` file for the managed cluster.

    <div class="formalpara-title">

    **Example output**

    </div>

    ``` terminal
    NAME                           STATUS     ROLES                  AGE   VERSION
    control-plane-0.example.com    Ready      control-plane,master   10d   v1.33.0
    control-plane-1.example.com    Ready      control-plane,master   10d   v1.33.0
    control-plane-2.example.com    NotReady   control-plane,master   10d   v1.33.0
    compute-1.example.com          Ready      worker                 10d   v1.33.0
    ```

    The failed node reports `NotReady` or is missing from the list. Note the `hostName` value that matches that node in the `ClusterInstance` CR.

2.  In the `ClusterInstance` CR, add the `bmac.agent-install.openshift.io/remove-agent-and-node-on-delete` annotation to the failed node and apply the updated CR to the hub cluster:

    ``` yaml
    apiVersion: siteconfig.open-cluster-management.io/v1alpha1
    kind: ClusterInstance
    metadata:
      name: "example-cluster"
      namespace: "example-cluster"
    spec:
      # ...
      nodes:
        - hostName: "control-plane-2.example.com"
          role: "master"
          extraAnnotations:
            BareMetalHost:
              bmac.agent-install.openshift.io/remove-agent-and-node-on-delete: "true"
    # ...
    ```

3.  Verify that the `BareMetalHost` resource on the hub cluster has the annotation by running the following command:

    ``` terminal
    $ oc --kubeconfig <hub_cluster_kubeconfig> get bmh -n <cluster_namespace> <bmh_name> \
      -o jsonpath='{.metadata.annotations.bmac\.agent-install\.openshift.io/remove-agent-and-node-on-delete}{"\n"}'
    ```

    <div class="formalpara-title">

    **Example output**

    </div>

    ``` terminal
    true
    ```

    where:

    `<cluster_namespace>`
    Specifies the namespace of the `ClusterInstance` CR.

    `<bmh_name>`
    Specifies the name of the `BareMetalHost` resource, which matches the node `hostName` value.

4.  Configure the `pruneManifests` field for the failed node so that the `BareMetalHost` resource is deleted. Keep the deletion annotation and apply the updated CR to the hub cluster:

    ``` yaml
    apiVersion: siteconfig.open-cluster-management.io/v1alpha1
    kind: ClusterInstance
    metadata:
      name: "example-cluster"
      namespace: "example-cluster"
    spec:
      # ...
      nodes:
        - hostName: "control-plane-2.example.com"
          role: "master"
          extraAnnotations:
            BareMetalHost:
              bmac.agent-install.openshift.io/remove-agent-and-node-on-delete: "true"
          pruneManifests:
            - apiVersion: metal3.io/v1alpha1
              kind: BareMetalHost
    # ...
    ```

    The status of the `BareMetalHost` resource changes to `deprovisioning`. If the BMC is unreachable, deprovisioning can take significantly longer than a graceful removal. Wait until the `BareMetalHost` resource is fully deleted.

5.  Verify that the `BareMetalHost` resource is deleted from the hub cluster by running the following command:

    ``` terminal
    $ oc --kubeconfig <hub_cluster_kubeconfig> get bmh -n <cluster_namespace>
    ```

    where:

    `<hub_cluster_kubeconfig>`
    Specifies the `kubeconfig` file for the hub cluster.

    `<cluster_namespace>`
    Specifies the namespace of the `ClusterInstance` CR.

6.  Verify that the `Agent` resource for the failed node is deleted from the hub cluster by running the following command:

    ``` terminal
    $ oc --kubeconfig <hub_cluster_kubeconfig> get agent -n <cluster_namespace> \
      -o jsonpath='{range .items[*]}{.spec.hostname}{"\n"}{end}' | grep <failed_hostname>
    ```

    where:

    `<failed_hostname>`
    Specifies the `hostName` value of the failed node, for example `control-plane-2.example.com`.

    If the command returns no output, the `Agent` resource for the failed node has been deleted. If other `Agent` resources remain in the namespace for other nodes, that is expected.

    <div class="important">

    Wait for the `Agent` resource for the failed node to be deleted before adding the replacement node.

    </div>

7.  Verify that the failed node is no longer listed on the managed cluster by running the following command:

    ``` terminal
    $ oc --kubeconfig <managed_cluster_kubeconfig> get nodes
    ```

8.  Configure the replacement node in `spec.nodes`. Remove the `pruneManifests` field and the deletion annotation. Then complete one of the following actions:

    - To reuse the same hardware, keep the existing node entry and the same `hostName` value. Leave the BMC address, boot MAC address, and node network configuration unchanged.

    - To install replacement hardware, update at least the BMC address, BMC secret name, boot MAC address, and node network configuration. If the replacement uses a different `hostName` value, delete the failed node entry and add a new entry.

      The following example reuses the `control-plane-2.example.com` hostname on replacement hardware:

      ``` yaml
      apiVersion: siteconfig.open-cluster-management.io/v1alpha1
      kind: ClusterInstance
      metadata:
        name: "example-cluster"
        namespace: "example-cluster"
      spec:
        # ...
        nodes:
          - hostName: "control-plane-2.example.com"
            role: "master"
            bmcAddress: "redfish-virtualmedia+https://192.0.2.22/redfish/v1/Systems/System.Embedded.1"
            bmcCredentialsName:
              name: "control-plane-2-bmc-secret"
            bootMACAddress: "AA:BB:CC:DD:EE:22"
            bootMode: "UEFI"
            nodeNetwork:
              interfaces:
                - name: eno1
                  macAddress: "AA:BB:CC:DD:EE:22"
              config:
                interfaces:
                  - name: eno1
                    type: ethernet
                    state: up
                    macAddress: "AA:BB:CC:DD:EE:22"
                    ipv4:
                      enabled: true
                      address:
                        - ip: 192.0.2.12
                          prefix-length: 24
                    ipv6:
                      enabled: false
      # ...
      ```

9.  Create the BMC secret for the replacement node in the same namespace as the `ClusterInstance` CR. The `BareMetalHost` finalizer deletes the referenced `bmcSecret` when the old `BareMetalHost` resource is removed, so this step is required for both same-hardware and new-hardware replacements.

    ``` yaml
    apiVersion: v1
    kind: Secret
    metadata:
      name: "control-plane-2-bmc-secret"
      namespace: example-cluster
    stringData:
      username: "username"
      password: "password"
    type: Opaque
    ```

10. Apply the updated `ClusterInstance` CR and any new secret to the hub cluster. The SiteConfig Operator creates a new `BareMetalHost` resource. The Assisted Installer provisions the host and joins it to the cluster.

11. Monitor provisioning on the hub cluster by running the following command:

    ``` terminal
    $ oc --kubeconfig <hub_cluster_kubeconfig> get bmh -n <cluster_namespace>
    ```

    where:

    `<hub_cluster_kubeconfig>`
    Specifies the `kubeconfig` file for the hub cluster.

    `<cluster_namespace>`
    Specifies the namespace of the `ClusterInstance` CR.

    <div class="formalpara-title">

    **Example output**

    </div>

    ``` terminal
    NAME                           STATE          CONSUMER   ONLINE   ERROR   AGE
    control-plane-0.example.com    provisioned               true             10d
    control-plane-1.example.com    provisioned               true             10d
    control-plane-2.example.com    provisioning              true             5m
    ```

<!-- -->

1.  Verify that the replacement node is `Ready` on the managed cluster by running the following command:

    ``` terminal
    $ oc --kubeconfig <managed_cluster_kubeconfig> get nodes -l node-role.kubernetes.io/control-plane
    ```

    where:

    `<managed_cluster_kubeconfig>`
    Specifies the `kubeconfig` file for the managed cluster.

2.  Identify an `etcd` pod on a control plane node by running the following command:

    ``` terminal
    $ oc --kubeconfig <managed_cluster_kubeconfig> get pods -n openshift-etcd
    ```

3.  Verify that `etcd` has three healthy members by running the following command:

    ``` terminal
    $ oc --kubeconfig <managed_cluster_kubeconfig> rsh -n openshift-etcd <etcd_pod> \
      etcdctl member list -w table
    ```

    where:

    `<etcd_pod>`
    Specifies the name of an `etcd` pod on a control plane node.

4.  Verify that every `etcd` endpoint is healthy by running the following command:

    ``` terminal
    $ oc --kubeconfig <managed_cluster_kubeconfig> rsh -n openshift-etcd <etcd_pod> \
      etcdctl endpoint health --cluster
    ```

5.  Verify that the `etcd` and `kube-apiserver` Operators have finished reconciling by running the following command:

    ``` terminal
    $ oc --kubeconfig <managed_cluster_kubeconfig> get clusteroperators etcd kube-apiserver
    ```

    Wait until both Operators report `True` in the `AVAILABLE` column and `False` in the `PROGRESSING` column.

- [Migrating from SiteConfig CRs to ClusterInstance CRs](../edge_computing/ztp-migrate-clusterinstance.xml#ztp-migrate-clusterinstance)

- [SiteConfig Operator](https://docs.redhat.com/en/documentation/red_hat_advanced_cluster_management_for_kubernetes/2.17/html/multicluster_engine_operator_with_red_hat_advanced_cluster_management/siteconfig-intro)

- [ClusterInstance API](https://docs.redhat.com/en/documentation/red_hat_advanced_cluster_management_for_kubernetes/2.17/html-single/apis/index#clusterinstance-api)
