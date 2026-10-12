Prepare your hosting cluster environment before deploying a virtualized control plane cluster. This includes installing and configuring KubeVirt Redfish and creating the control plane VMs.

# Install KubeVirt Redfish

Install KubeVirt Redfish on your OpenShift Virtualization cluster by applying a series of custom resources (CRs). These CRs create the namespace, permissions, configuration, and deployment required to expose VMs through the Redfish API.

- You have a OpenShift Container Platform cluster with OpenShift Virtualization installed.

- You installed the OpenShift CLI (`oc`).

- You logged in to OpenShift Container Platform as a user with `cluster-admin` privileges.

1.  Create the `Namespace` CR for KubeVirt Redfish by creating a YAML file with content such as the following example:

    ``` yaml
    apiVersion: v1
    kind: Namespace
    metadata:
      name: kubevirt-redfish
      labels:
        app.kubernetes.io/name: kubevirt-redfish
    ```

2.  Apply the resource by running the following command:

    ``` terminal
    $ oc apply -f namespace.yaml
    ```

3.  Create the `ServiceAccount` CR by creating a YAML file with content such as the following example:

    ``` yaml
    apiVersion: v1
    kind: ServiceAccount
    metadata:
      name: kubevirt-redfish
      namespace: kubevirt-redfish
      labels:
        app.kubernetes.io/name: kubevirt-redfish
        app.kubernetes.io/component: rbac
    ```

4.  Apply the resource by running the following command:

    ``` terminal
    $ oc apply -f serviceaccount.yaml
    ```

5.  Create the `ClusterRole` CR with required permissions by creating a YAML file with content such as the following example:

    ``` yaml
    apiVersion: rbac.authorization.k8s.io/v1
    kind: ClusterRole
    metadata:
      name: kubevirt-redfish-role
      labels:
        app.kubernetes.io/name: kubevirt-redfish
        app.kubernetes.io/component: rbac
    rules:
      - apiGroups: ["kubevirt.io"]
        resources: ["virtualmachines", "virtualmachineinstances"]
        verbs: ["get", "list", "watch", "update", "patch"]
      - apiGroups: ["kubevirt.io"]
        resources: ["virtualmachines/status", "virtualmachineinstances/status"]
        verbs: ["get", "list", "watch", "patch"]
      - apiGroups: ["kubevirt.io"]
        resources: ["virtualmachines/restart", "virtualmachines/start", "virtualmachines/stop"]
        verbs: ["create"]
      - apiGroups: ["subresources.kubevirt.io"]
        resources: ["virtualmachineinstances/pause", "virtualmachineinstances/unpause"]
        verbs: ["create", "update"]
      - apiGroups: [""]
        resources: ["pods", "services", "configmaps", "secrets"]
        verbs: ["get", "list", "watch", "create", "update", "delete"]
      - apiGroups: [""]
        resources: ["namespaces"]
        verbs: ["get", "list"]
      - apiGroups: ["cdi.kubevirt.io"]
        resources: ["datavolumes", "volumeimportsources"]
        verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
      - apiGroups: [""]
        resources: ["persistentvolumeclaims"]
        verbs: ["get", "list", "create", "update", "patch", "delete", "watch"]
      - apiGroups: ["storage.k8s.io"]
        resources: ["storageclasses"]
        verbs: ["get", "list"]
    ```

6.  Apply the resource by running the following command:

    ``` terminal
    $ oc apply -f clusterrole.yaml
    ```

7.  Create the `ClusterRoleBinding` CR by creating a YAML file with content such as the following example:

    ``` yaml
    apiVersion: rbac.authorization.k8s.io/v1
    kind: ClusterRoleBinding
    metadata:
      name: kubevirt-redfish-binding
      labels:
        app.kubernetes.io/name: kubevirt-redfish
        app.kubernetes.io/component: rbac
    roleRef:
      apiGroup: rbac.authorization.k8s.io
      kind: ClusterRole
      name: kubevirt-redfish-role
    subjects:
      - kind: ServiceAccount
        name: kubevirt-redfish
        namespace: kubevirt-redfish
    ```

8.  Apply the resource by running the following command:

    ``` terminal
    $ oc apply -f clusterrolebinding.yaml
    ```

9.  Create a `Secret` CR to enable the Redfish API to manage specific VMs:

    1.  Generate a `bcrypt` hashed password for the Redfish API by running the following command in a Linux terminal:

        ``` terminal
        $ htpasswd -nbB "" '<password>' | cut -d: -f2
        ```

        - `<password>` is the password you want to use for the Redfish API.

          The output is a `bcrypt` hashed password beginning with `$2a$`, `$2b$`, or `$2y$`.

          <div class="note">

          In earlier Technology Preview releases, plain text passwords were used. Use `bcrypt` hashed passwords for improved security.

          </div>

    2.  Create the `Secret` CR containing the configuration with content such as the following example. Edit the `config.yaml` section to match your environment:

        ``` yaml
        apiVersion: v1
        kind: Secret
        metadata:
          name: kubevirt-redfish-secret
          namespace: kubevirt-redfish
          labels:
            app.kubernetes.io/name: kubevirt-redfish
            app.kubernetes.io/component: config
        type: Opaque
        stringData:
          config.yaml: |
            server:
              host: "0.0.0.0"
              port: 8443
              tls:
                enabled: false
            system_id_convention: "enhanced"
            chassis:
              - name: "<chassis_name>"
                namespace: "<vm_namespace>"
                service_account: "kubevirt-redfish"
                vm_selector:
                  labels:
                    redfish-enabled: "true"
            authentication:
              users:
                - username: "admin"
                  password:
                    hash: "<bcrypt_password>"
                  chassis: ["<chassis_name>"]
            datavolume:
              storage_class: "<storage_class>"
              storage_size: "3Gi"
        ```

        where:

        `system_id_convention`
        Specifies the format for Redfish system IDs. The recommended setting is `enhanced` to use `<namespace>.<vm-name>` format. The `legacy` setting uses `<vm-name>` only.

        `chassis`
        Specifies the namespaces where VMs are deployed. Replace `<chassis_name>` with a name for this chassis configuration and `<vm_namespace>` with the namespace containing your VMs. The `vm_selector` labels identify which VMs in the namespace are exposed through Redfish. Only VMs with matching labels are visible. You can configure multiple chassis entries to expose different subsets of VMs in the same namespace, each with different authentication users.

        `authentication`
        Specifies the username and password required to validate requests to the Redfish API. Replace `<bcrypt_password>` with the `bcrypt` hashed password that you generated.

        `datavolume`
        Specifies storage for virtual media operations. KubeVirt Redfish uses this storage to create a data volume, download the installation ISO into that volume, and attach the volume to the VM as virtual media. Replace `<storage_class>` with a storage class that points to a shared storage location accessible from all nodes in the hosting cluster. Do not use a node-local storage class such as LVM Storage for this volume. For more information about storage options, see *Storage requirements* in "Prerequisites for virtualized control planes".

10. Apply the resource by running the following command:

    ``` terminal
    $ oc apply -f secret.yaml
    ```

    <div class="warning">

    The credentials defined in this `Secret` CR enable full management control over the VMs exposed through KubeVirt Redfish, independently of any OpenShift Container Platform privileges.

    </div>

11. Create the `Deployment` CR by creating a YAML file with content such as the following example:

    ``` yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: kubevirt-redfish
      namespace: kubevirt-redfish
      labels:
        app.kubernetes.io/name: kubevirt-redfish
        app.kubernetes.io/component: server
    spec:
      replicas: 1
      selector:
        matchLabels:
          app.kubernetes.io/name: kubevirt-redfish
          app.kubernetes.io/component: server
      template:
        metadata:
          labels:
            app.kubernetes.io/name: kubevirt-redfish
            app.kubernetes.io/component: server
        spec:
          serviceAccountName: kubevirt-redfish
          securityContext:
            runAsNonRoot: true
          containers:
            - name: kubevirt-redfish
              image: registry.redhat.io/container-native-virtualization/kubevirt-redfish-rhel9:v4.17
              imagePullPolicy: Always
              ports:
                - name: http
                  containerPort: 8443
                  protocol: TCP
              env:
                - name: CONFIG_PATH
                  value: "/app/config/config.yaml"
                - name: LOG_LEVEL
                  value: "info"
              resources:
                requests:
                  memory: "512Mi"
                  cpu: "100m"
                limits:
                  memory: "2Gi"
                  cpu: "500m"
              livenessProbe:
                httpGet:
                  path: /redfish/v1/
                  port: 8443
                  scheme: HTTP
                initialDelaySeconds: 30
                periodSeconds: 10
              readinessProbe:
                httpGet:
                  path: /redfish/v1/
                  port: 8443
                  scheme: HTTP
                initialDelaySeconds: 5
                periodSeconds: 5
              securityContext:
                runAsNonRoot: true
                allowPrivilegeEscalation: false
                capabilities:
                  drop:
                    - ALL
              volumeMounts:
                - name: config-volume
                  mountPath: /app/config
                  readOnly: true
          volumes:
            - name: config-volume
              secret:
                secretName: kubevirt-redfish-secret
    ```

    where:

    - The `image` field specifies the KubeVirt Redfish container image.

12. Apply the resource by running the following command:

    ``` terminal
    $ oc apply -f deployment.yaml
    ```

13. Create the `Service` CR by creating a YAML file with content such as the following example:

    ``` yaml
    apiVersion: v1
    kind: Service
    metadata:
      name: kubevirt-redfish
      namespace: kubevirt-redfish
      labels:
        app.kubernetes.io/name: kubevirt-redfish
        app.kubernetes.io/component: server
    spec:
      type: ClusterIP
      ports:
        - name: http
          port: 8443
          targetPort: 8443
          protocol: TCP
      selector:
        app.kubernetes.io/name: kubevirt-redfish
        app.kubernetes.io/component: server
    ```

14. Apply the resource by running the following command:

    ``` terminal
    $ oc apply -f service.yaml
    ```

15. Create the `Route` CR to expose the Redfish API externally by creating a YAML file with content such as the following example:

    ``` yaml
    apiVersion: route.openshift.io/v1
    kind: Route
    metadata:
      name: kubevirt-redfish
      namespace: kubevirt-redfish
      labels:
        app.kubernetes.io/name: kubevirt-redfish
        app.kubernetes.io/component: server
    spec:
      port:
        targetPort: http
      to:
        kind: Service
        name: kubevirt-redfish
        weight: 100
      tls:
        termination: edge
        insecureEdgeTerminationPolicy: Redirect
    ```

16. Apply the resource by running the following command:

    ``` terminal
    $ oc apply -f route.yaml
    ```

<!-- -->

1.  Verify that the pods are running by running the following command:

    ``` terminal
    $ oc get pods -n kubevirt-redfish
    ```

    <div class="formalpara-title">

    **Example output**

    </div>

    ``` terminal
    NAME                                READY   STATUS    RESTARTS   AGE
    kubevirt-redfish-587cd94988-xthml   1/1     Running   0          2m
    ```

2.  Get the route hostname by running the following command:

    ``` terminal
    $ oc get route kubevirt-redfish -n kubevirt-redfish -o jsonpath='{.spec.host}'
    ```

3.  Test the Redfish endpoint by running the following command:

    ``` terminal
    $ curl -sk -u "admin:<password>" https://<route_hostname>/redfish/v1/
    ```

    A successful response returns JSON with the Redfish service root:

    ``` json
    {
      "@odata.id": "/redfish/v1",
      "@odata.type": "#ServiceRoot.v1_0_0.ServiceRoot",
      "Id": "RootService",
      "Name": "Root Service",
      "Systems": {
        "@odata.id": "/redfish/v1/Systems"
      }
    }
    ```

# Create control plane VMs

Create VMs on the hosting cluster that will become the control plane nodes for your virtualized control plane cluster.

- KubeVirt Redfish is installed and configured on the hosting cluster.

- The hosting cluster has a network configured to provide Layer 2 connectivity between VMs.

- Logical Volume Manager (LVM) Storage is installed on the hosting cluster.

1.  Create a `VirtualMachine` CR for each control plane node by creating a YAML file with content such as the following example:

    ``` yaml
    apiVersion: kubevirt.io/v1
    kind: VirtualMachine
    metadata:
      name: control-plane-0
      namespace: <vm_namespace>
      labels:
        redfish-enabled: "true"
        vcp-cluster: <cluster_name>
    spec:
      runStrategy: Halted
      dataVolumeTemplates:
        - metadata:
            name: control-plane-0-disk
          spec:
            source:
              blank: {}
            storage:
              accessModes:
                - ReadWriteOnce
              volumeMode: Block
              resources:
                requests:
                  storage: 120Gi
              storageClassName: <storage_class>
      template:
        metadata:
          labels:
            redfish-enabled: "true"
            vcp-cluster: <cluster_name>
        spec:
          evictionStrategy: None
          affinity:
            podAntiAffinity:
              requiredDuringSchedulingIgnoredDuringExecution:
                - labelSelector:
                    matchLabels:
                      vcp-cluster: <cluster_name>
                  topologyKey: kubernetes.io/hostname
          readinessProbe:
            guestAgentPing: {}
            initialDelaySeconds: 120
            periodSeconds: 20
            timeoutSeconds: 10
            failureThreshold: 3
            successThreshold: 3
          domain:
            rebootPolicy: Terminate
            cpu:
              cores: 8
            memory:
              guest: 16Gi
            devices:
              disks:
                - name: rootdisk
                  disk:
                    bus: virtio
                - name: cloudinitdisk
                  disk:
                    bus: virtio
              interfaces:
                - name: default
                  macAddress: "52:54:00:00:00:01"
                  bridge: {}
          networks:
            - name: default
              multus:
                networkName: <network_attachment_definition>
          volumes:
            - name: rootdisk
              dataVolume:
                name: control-plane-0-disk
            - name: cloudinitdisk
              cloudInitNoCloud:
                userData: |
                  #cloud-config
                  hostname: control-plane-0
                  user: core
    ```

    where:

    - `<vm_namespace>` specifies the namespace for the VMs. Must match the namespace specified in the KubeVirt Redfish chassis configuration.

    - `redfish-enabled: "true"` is an example label. The label must match the `vm_selector` labels in the KubeVirt Redfish configuration so the VM is exposed through the Redfish API. You can use any label key and value, as long as both the VM and the KubeVirt Redfish configuration use the same label.

    - `vcp-cluster: <cluster_name>` identifies which target cluster a VM belongs to. Replace `<cluster_name>` with the name of your target cluster. This label is used by anti-affinity rules and the pod disruption budget to scope operations to a single target cluster. This is important when a hosting cluster runs VMs for multiple target clusters.

    - `evictionStrategy: None` prevents the hosting cluster from attempting to live-migrate control plane VMs during node drain operations. Live migration is not supported for virtualized control plane VMs.

    - `affinity.podAntiAffinity` distributes control plane VMs across different physical nodes so that a single node failure affects only one VM. The label selector uses the `vcp-cluster` label to scope anti-affinity to VMs belonging to the same target cluster.

    - `readinessProbe.guestAgentPing` verifies that the QEMU guest agent inside the VM is responsive. The hosting cluster uses this probe to determine whether the VM is healthy before allowing operations that affect other VMs.

    - `runStrategy: Halted` specifies that VMs must be powered off initially. The installation powers them on by using the Redfish API.

    - `rebootPolicy: Terminate` specifies the reboot behavior required for Redfish API boot override operations. Ensures the VM terminates cleanly when boot media changes.

      <div class="note">

      The `RebootPolicy` feature gate enables the `rebootPolicy` field in `VirtualMachine` CR specifications. In OpenShift Virtualization 5.0, this feature gate is enabled by default.

      The `rebootPolicy: Terminate` configuration is required when deploying a virtualized control plane cluster.

      </div>

    - `cores: 8` and `guest: 16Gi` specify the minimum recommended resources for control plane nodes.

    - `dataVolumeTemplates` creates a blank root disk for the VM. The `120Gi` value matches the control plane VM storage requirements.

    - `<storage_class>` specifies the LVM Storage `StorageClass` on the hosting cluster, for example `lvms-vg1`.

    - `macAddress` specifies a fixed MAC address for the VM network interface. Use this same address for the `bootMACAddress` field in the installation configuration. Assign a unique MAC address to each control plane VM.

    - `<network_attachment_definition>` specifies the name of a `NetworkAttachmentDefinition` configured on your hosting cluster. All control plane VMs must share the same L2 network segment. Common options include localnet, Linux bridge, or OVN Layer 2 networks.

2.  Apply the resource by running the following command:

    ``` terminal
    $ oc apply -f control-plane-0.yaml
    ```

    Create further VMs for `control-plane-1` and `control-plane-2` using the same specification, adjusting the `metadata.name`, `dataVolumeTemplates[].metadata.name`, `macAddress`, and cloud-init `hostname` for each VM.

3.  Create a `PodDisruptionBudget` to prevent the hosting cluster from evicting more than one control plane VM at a time:

    ``` yaml
    apiVersion: policy/v1
    kind: PodDisruptionBudget
    metadata:
      name: vcp-control-plane-pdb
      namespace: <vm_namespace>
    spec:
      minAvailable: 2
      selector:
        matchLabels:
          vcp-cluster: <cluster_name>
    ```

    where:

    - `minAvailable: 2` ensures that at least two control plane VMs remain running during node drain operations, which preserves `etcd` quorum. You must use `minAvailable` instead of `maxUnavailable` because the `VirtualMachineInstance` controller does not implement the Kubernetes scale subresource. A PDB with `maxUnavailable` cannot determine the expected pod count for VMs, which causes it to block all evictions.

    - The label selector uses the `vcp-cluster` label to scope the budget to VMs belonging to the same target cluster.

4.  Apply the resource by running the following command:

    ``` terminal
    $ oc apply -f vcp-control-plane-pdb.yaml
    ```

<!-- -->

1.  Verify that the VMs are created and powered off by running the following command:

    ``` terminal
    $ oc get vm -n <vm_namespace>
    ```

    - `<vm_namespace>` is the namespace of the VMs.

      <div class="formalpara-title">

      **Example output**

      </div>

      ``` terminal
      NAME               AGE   STATUS    READY
      control-plane-0    1m    Stopped   False
      control-plane-1    1m    Stopped   False
      control-plane-2    1m    Stopped   False
      ```

2.  Verify that KubeVirt Redfish can discover the VMs by querying the Redfish API:

    ``` terminal
    $ curl -sk -u "<username>:<password>" \
        https://<kubevirt_redfish_route>/redfish/v1/Systems
    ```

# Additional resources

- [Recommended resources for topologies](../installing/installing_with_agent_based_installer/preparing-to-install-with-agent-based-installer.xml#agent-based-installer-recommended-resources_preparing-to-install-with-agent-based-installer)

- [Connecting a virtual machine to a secondary localnet user-defined network](../virt/vm_networking/virt-connecting-vm-to-secondary-udn.xml#virt-connecting-vm-to-secondary-udn)
