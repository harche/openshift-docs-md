Sysctl settings are exposed through Kubernetes, allowing users to modify certain kernel parameters at runtime. Only sysctls that are namespaced can be set independently on pods. If a sysctl is not namespaced, called *node-level*, you must use another method of setting the sysctl, such as by using the Node Tuning Operator.

Network sysctls are a special category of sysctl. Network sysctls include:

- System-wide sysctls, for example `net.ipv4.ip_local_port_range`, that are valid for all networking. You can set these independently for each pod on a node.

- Interface-specific sysctls, for example `net.ipv4.conf.IFNAME.accept_local`, that only apply to a specific additional network interface for a given pod. You can set these independently for each additional network configuration. You set these by using a configuration in the `tuning-cni` after the network interfaces are created.

Moreover, only those sysctls considered *safe* are whitelisted by default; you can manually enable other *unsafe* sysctls on the node to be available to the user.

If you are setting the sysctl and it is node-level, you can find information on this procedure in the section [Using the Node Tuning Operator](../../scalability_and_performance/using-node-tuning-operator.xml#using-node-tuning-operator).

# About sysctls

In Linux, the sysctl interface allows an administrator to modify kernel parameters at runtime. Parameters are available from the `/proc/sys/` virtual process file system. The parameters cover various subsystems, such as:

- kernel (common prefix: `kernel.`)

- networking (common prefix: `net.`)

- virtual memory (common prefix: `vm.`)

- MDADM (common prefix: `dev.`)

More subsystems are described in [Kernel documentation](https://www.kernel.org/doc/Documentation/sysctl/README). To get a list of all parameters, run:

``` terminal
$ sudo sysctl -a
```

# Namespaced and node-level sysctls

A number of sysctls are *namespaced* in the Linux kernels. This means that you can set them independently for each pod on a node. Being namespaced is a requirement for sysctls to be accessible in a pod context within Kubernetes.

The following sysctls are known to be namespaced:

- `kernel.shm*`

- `kernel.msg*`

- `kernel.sem`

- `fs.mqueue.*`

Additionally, most of the sysctls in the `net.*` group are known to be namespaced. Their namespace adoption differs based on the kernel version and distributor.

Sysctls that are not namespaced are called *node-level* and must be set manually by the cluster administrator, either by means of the underlying Linux distribution of the nodes, such as by modifying the `/etc/sysctls.conf` file, or by using a daemon set with privileged containers. You can use the Node Tuning Operator to set *node-level* sysctls.

> [!NOTE]
> Consider marking nodes with special sysctls as tainted. Only schedule pods onto them that need those sysctl settings. Use the taints and toleration feature to mark the nodes.

# Safe and unsafe sysctls

Sysctls are grouped into *safe* and *unsafe* sysctls.

For system-wide sysctls to be considered safe, they must be namespaced. A namespaced sysctl ensures there is isolation between namespaces and therefore pods. If you set a sysctl for one pod it must not add any of the following:

- Influence any other pod on the node

- Harm the node health

- Gain CPU or memory resources outside of the resource limits of a pod

> [!NOTE]
> Being namespaced alone is not sufficient for the sysctl to be considered safe.

Any sysctl that is not added to the allowed list on OpenShift Container Platform is considered unsafe for OpenShift Container Platform.

Unsafe sysctls are not allowed by default. For system-wide sysctls the cluster administrator must manually enable them on a per-node basis. Pods with disabled unsafe sysctls are scheduled but do not launch.

> [!NOTE]
> You cannot manually enable interface-specific unsafe sysctls.

OpenShift Container Platform adds the following system-wide and interface-specific safe sysctls to an allowed safe list:

| sysctl | Description |
|----|----|
| `kernel.shm_rmid_forced` | When set to `1`, all shared memory objects in current IPC namespace are automatically forced to use IPC_RMID. For more information, see [shm_rmid_forced](https://docs.kernel.org/admin-guide/sysctl/kernel.html?highlight=shm_rmid_forced#shm-rmid-forced). |
| `net.ipv4.ip_local_port_range` | Defines the local port range that is used by TCP and UDP to choose the local port. The first number is the first port number, and the second number is the last local port number. If possible, it is better if these numbers have different parity (one even and one odd value). They must be greater than or equal to `ip_unprivileged_port_start`. The default values are `32768` and `60999` respectively. For more information, see [ip_local_port_range](https://docs.kernel.org/networking/ip-sysctl.html?highlight=ip_local_port_range#ip-variables). |
| `net.ipv4.tcp_syncookies` | When `net.ipv4.tcp_syncookies` is set, the kernel handles TCP SYN packets normally until the half-open connection queue is full, at which time, the SYN cookie functionality kicks in. This functionality allows the system to keep accepting valid connections, even if under a denial-of-service attack. For more information, see [tcp_syncookies](https://docs.kernel.org/networking/ip-sysctl.html?highlight=tcp_syncookies#tcp-variables). |
| `net.ipv4.ping_group_range` | This restricts `ICMP_PROTO` datagram sockets to users in the group range. The default is `1 0`, meaning that nobody, not even root, can create ping sockets. For more information, see [ping_group_range](https://docs.kernel.org/networking/ip-sysctl.html?highlight=ping_group_range#ip-variables). |
| `net.ipv4.ip_unprivileged_port_start` | This defines the first unprivileged port in the network namespace. To disable all privileged ports, set this to `0`. Privileged ports must not overlap with the `ip_local_port_range`. For more information, see [ip_unprivileged_port_start](https://docs.kernel.org/networking/ip-sysctl.html?highlight=ip_unprivileged_port_start#ip-variables#ip-variables). |
| `net.ipv4.ip_local_reserved_ports` | Specify a range of comma-separated local ports that you want to reserve for applications or services. |
| `net.ipv4.tcp_keepalive_time` | Specify the interval in seconds before the first `keepalive` probe should be sent after a connection has become idle. |
| `net.ipv4.tcp_fin_timeout` | Specify the time in seconds that a connection remains in the `FIN-WAIT-2` state before it is aborted. |
| `net.ipv4.tcp_keepalive_intvl` | Specify the interval in seconds between the `keepalive` probes. This value is multiplied by the `tcp_keepalive_probes` value to determine the total time required before it is decided that the connection is broken. |
| `net.ipv4.tcp_keepalive_probes` | Specify how many `keepalive` probes to send until it is determined that the connection is broken. |

System-wide safe sysctls

<table>
<caption>Interface-specific safe sysctls</caption>
<colgroup>
<col style="width: 30%" />
<col style="width: 70%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;">sysctl</th>
<th style="text-align: left;">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;"><p><code>net.ipv4.conf.IFNAME.accept_redirects</code></p></td>
<td style="text-align: left;"><p>Accept IPv4 ICMP redirect messages.</p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>net.ipv4.conf.IFNAME.accept_source_route</code></p></td>
<td style="text-align: left;"><p>Accept IPv4 packets with strict source route (SRR) option.</p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>net.ipv4.conf.IFNAME.arp_accept</code></p></td>
<td style="text-align: left;"><p>Define behavior for gratuitous ARP frames with an IPv4 address that is not already present in the ARP table:</p>
<ul>
<li><p><code>0</code> - Do not create new entries in the ARP table.</p></li>
<li><p><code>1</code> - Create new entries in the ARP table.</p></li>
</ul></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>net.ipv4.conf.IFNAME.arp_notify</code></p></td>
<td style="text-align: left;"><p>Define mode for notification of IPv4 address and device changes.</p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>net.ipv4.conf.IFNAME.disable_policy</code></p></td>
<td style="text-align: left;"><p>Disable IPSEC policy (SPD) for this IPv4 interface.</p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>net.ipv4.conf.IFNAME.secure_redirects</code></p></td>
<td style="text-align: left;"><p>Accept ICMP redirect messages only to gateways listed in the interface’s current gateway list.</p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>net.ipv4.conf.IFNAME.send_redirects</code></p></td>
<td style="text-align: left;"><p>Send redirects is enabled only if the node acts as a router. That is, a host should not send an ICMP redirect message. It is used by routers to notify the host about a better routing path that is available for a particular destination.</p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>net.ipv6.conf.IFNAME.accept_ra</code></p></td>
<td style="text-align: left;"><p>Accept IPv6 Router advertisements; autoconfigure using them. It also determines whether or not to transmit router solicitations. Router solicitations are transmitted only if the functional setting is to accept router advertisements.</p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>net.ipv6.conf.IFNAME.accept_redirects</code></p></td>
<td style="text-align: left;"><p>Accept IPv6 ICMP redirect messages.</p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>net.ipv6.conf.IFNAME.accept_source_route</code></p></td>
<td style="text-align: left;"><p>Accept IPv6 packets with SRR option.</p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>net.ipv6.conf.IFNAME.arp_accept</code></p></td>
<td style="text-align: left;"><p>Define behavior for gratuitous ARP frames with an IPv6 address that is not already present in the ARP table:</p>
<ul>
<li><p><code>0</code> - Do not create new entries in the ARP table.</p></li>
<li><p><code>1</code> - Create new entries in the ARP table.</p></li>
</ul></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>net.ipv6.conf.IFNAME.arp_notify</code></p></td>
<td style="text-align: left;"><p>Define mode for notification of IPv6 address and device changes.</p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>net.ipv6.neigh.IFNAME.base_reachable_time_ms</code></p></td>
<td style="text-align: left;"><p>This parameter controls the hardware address to IP mapping lifetime in the neighbour table for IPv6.</p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>net.ipv6.neigh.IFNAME.retrans_time_ms</code></p></td>
<td style="text-align: left;"><p>Set the retransmit timer for neighbor discovery messages.</p></td>
</tr>
</tbody>
</table>

> [!NOTE]
> When setting these values using the `tuning` CNI plugin, use the value `IFNAME` literally. The interface name is represented by the `IFNAME` token, and is replaced with the actual name of the interface at runtime.

# Updating the interface-specific safe sysctls list

OpenShift Container Platform includes a predefined list of safe interface-specific `sysctls`. You can modify this list by updating the `cni-sysctl-allowlist` in the `openshift-multus` namespace.

> [!IMPORTANT]
> The support for updating the interface-specific safe sysctls list is a Technology Preview feature only. Technology Preview features are not supported with Red Hat production service level agreements (SLAs) and might not be functionally complete. Red Hat does not recommend using them in production. These features provide early access to upcoming product features, enabling customers to test functionality and provide feedback during the development process.
>
> For more information about the support scope of Red Hat Technology Preview features, see [Technology Preview Features Support Scope](https://access.redhat.com/support/offerings/techpreview/).

Follow this procedure to modify the predefined list of safe `sysctls`. This procedure describes how to extend the default allow list.

<div>

<div class="title">

Procedure

</div>

1.  View the existing predefined list by running the following command:

    ``` terminal
    $ oc get cm -n openshift-multus cni-sysctl-allowlist -oyaml
    ```

    <div class="formalpara">

    <div class="title">

    Expected output

    </div>

    ``` terminal
    apiVersion: v1
    data:
      allowlist.conf: |-
        ^net.ipv4.conf.IFNAME.accept_redirects$
        ^net.ipv4.conf.IFNAME.accept_source_route$
        ^net.ipv4.conf.IFNAME.arp_accept$
        ^net.ipv4.conf.IFNAME.arp_notify$
        ^net.ipv4.conf.IFNAME.disable_policy$
        ^net.ipv4.conf.IFNAME.secure_redirects$
        ^net.ipv4.conf.IFNAME.send_redirects$
        ^net.ipv6.conf.IFNAME.accept_ra$
        ^net.ipv6.conf.IFNAME.accept_redirects$
        ^net.ipv6.conf.IFNAME.accept_source_route$
        ^net.ipv6.conf.IFNAME.arp_accept$
        ^net.ipv6.conf.IFNAME.arp_notify$
        ^net.ipv6.neigh.IFNAME.base_reachable_time_ms$
        ^net.ipv6.neigh.IFNAME.retrans_time_ms$
    kind: ConfigMap
    metadata:
      annotations:
        kubernetes.io/description: |
          Sysctl allowlist for nodes.
        release.openshift.io/version: 4.17.0-0.nightly-2022-11-16-003434
      creationTimestamp: "2022-11-17T14:09:27Z"
      name: cni-sysctl-allowlist
      namespace: openshift-multus
      resourceVersion: "2422"
      uid: 96d138a3-160e-4943-90ff-6108fa7c50c3
    ```

    </div>

2.  Edit the list by using the following command:

    ``` terminal
    $ oc edit cm -n openshift-multus cni-sysctl-allowlist -oyaml
    ```

    For example, to allow you to be able to implement stricter reverse path forwarding you need to add `^net.ipv4.conf.IFNAME.rp_filter$` and `^net.ipv6.conf.IFNAME.rp_filter$` to the list as shown here:

    ``` terminal
    # Please edit the object below. Lines beginning with a '#' will be ignored,
    # and an empty file will abort the edit. If an error occurs while saving this file will be
    # reopened with the relevant failures.
    #
    apiVersion: v1
    data:
      allowlist.conf: |-
        ^net.ipv4.conf.IFNAME.accept_redirects$
        ^net.ipv4.conf.IFNAME.accept_source_route$
        ^net.ipv4.conf.IFNAME.arp_accept$
        ^net.ipv4.conf.IFNAME.arp_notify$
        ^net.ipv4.conf.IFNAME.disable_policy$
        ^net.ipv4.conf.IFNAME.secure_redirects$
        ^net.ipv4.conf.IFNAME.send_redirects$
        ^net.ipv4.conf.IFNAME.rp_filter$
        ^net.ipv6.conf.IFNAME.accept_ra$
        ^net.ipv6.conf.IFNAME.accept_redirects$
        ^net.ipv6.conf.IFNAME.accept_source_route$
        ^net.ipv6.conf.IFNAME.arp_accept$
        ^net.ipv6.conf.IFNAME.arp_notify$
        ^net.ipv6.neigh.IFNAME.base_reachable_time_ms$
        ^net.ipv6.neigh.IFNAME.retrans_time_ms$
        ^net.ipv6.conf.IFNAME.rp_filter$
    ```

3.  Save the changes to the file and exit.

    > [!NOTE]
    > The removal of `sysctls` is also supported. Edit the file, remove the `sysctl` or `sysctls` then save the changes and exit.

</div>

<div class="formalpara">

<div class="title">

Verification

</div>

Follow this procedure to enforce stricter reverse path forwarding for IPv4. For more information on reverse path forwarding see [Reverse Path Forwarding ](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/6/html/security_guide/sect-security_guide-server_security-reverse_path_forwarding).

</div>

1.  Create a network attachment definition, such as `reverse-path-fwd-example.yaml`, with the following content:

    ``` yaml
    apiVersion: "k8s.cni.cncf.io/v1"
    kind: NetworkAttachmentDefinition
    metadata:
      name: tuningnad
      namespace: default
    spec:
      config: '{
        "cniVersion": "0.4.0",
        "name": "tuningnad",
        "plugins": [{
          "type": "bridge"
          },
          {
          "type": "tuning",
          "sysctl": {
             "net.ipv4.conf.IFNAME.rp_filter": "1"
            }
        }
      ]
    }'
    ```

2.  Apply the yaml by running the following command:

    ``` terminal
    $ oc apply -f reverse-path-fwd-example.yaml
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` terminal
    networkattachmentdefinition.k8.cni.cncf.io/tuningnad created
    ```

    </div>

3.  Create a pod such as `examplepod.yaml` using the following YAML:

    ``` yaml
    apiVersion: v1
    kind: Pod
    metadata:
      name: example
      labels:
        app: httpd
      namespace: default
      annotations:
        k8s.v1.cni.cncf.io/networks: tuningnad
    spec:
      securityContext:
        runAsNonRoot: true
        seccompProfile:
          type: RuntimeDefault
      containers:
        - name: httpd
          image: 'image-registry.openshift-image-registry.svc:5000/openshift/httpd:latest'
          ports:
            - containerPort: 8080
          securityContext:
            allowPrivilegeEscalation: false
            capabilities:
              drop:
                - ALL
    ```

    - Specify the name of the configured `NetworkAttachmentDefinition`.

4.  Apply the yaml by running the following command:

    ``` terminal
    $ oc apply -f examplepod.yaml
    ```

5.  Verify that the pod is created by running the following command:

    ``` terminal
    $ oc get pod
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` terminal
    NAME      READY   STATUS    RESTARTS   AGE
    example   1/1     Running   0          47s
    ```

    </div>

6.  Log in to the pod by running the following command:

    ``` terminal
    $ oc rsh example
    ```

7.  Verify the value of the configured sysctl flag. For example, find the value `net.ipv4.conf.net1.rp_filter` by running the following command:

    ``` terminal
    sh-4.4# sysctl net.ipv4.conf.net1.rp_filter
    ```

    <div class="formalpara">

    <div class="title">

    Expected output

    </div>

    ``` terminal
    net.ipv4.conf.net1.rp_filter = 1
    ```

    </div>

<div>

<div class="title">

Additional resources

</div>

- [Linux networking documentation](https://docs.kernel.org/networking/ip-sysctl.html)

</div>

# Starting a pod with safe sysctls

You can set sysctls on pods using the pod’s `securityContext`. The `securityContext` applies to all containers in the same pod.

Safe sysctls are allowed by default.

This example uses the pod `securityContext` to set the following safe sysctls:

- `kernel.shm_rmid_forced`

- `net.ipv4.ip_local_port_range`

- `net.ipv4.tcp_syncookies`

- `net.ipv4.ping_group_range`

> [!WARNING]
> To avoid destabilizing your operating system, modify sysctl parameters only after you understand their effects.

Use this procedure to start a pod with the configured sysctl settings.

> [!NOTE]
> In most cases you modify an existing pod definition and add the `securityContext` spec.

<div>

<div class="title">

Procedure

</div>

1.  Create a YAML file `sysctl_pod.yaml` that defines an example pod and add the `securityContext` spec, as shown in the following example:

    ``` yaml
    apiVersion: v1
    kind: Pod
    metadata:
      name: sysctl-example
      namespace: default
    spec:
      containers:
      - name: podexample
        image: centos
        command: ["bin/bash", "-c", "sleep INF"]
        securityContext:
          runAsUser: 2000
          runAsGroup: 3000
          allowPrivilegeEscalation: false
          capabilities:
            drop: ["ALL"]
      securityContext:
        runAsNonRoot: true
        seccompProfile:
          type: RuntimeDefault
        sysctls:
        - name: kernel.shm_rmid_forced
          value: "1"
        - name: net.ipv4.ip_local_port_range
          value: "32770       60666"
        - name: net.ipv4.tcp_syncookies
          value: "0"
        - name: net.ipv4.ping_group_range
          value: "0           200000000"
    ```

    - `runAsUser` controls which user ID the container is run with.

    - `runAsGroup` controls which primary group ID the containers is run with.

    - `allowPrivilegeEscalation` determines if a pod can request to allow privilege escalation. If unspecified, it defaults to true. This boolean directly controls whether the `no_new_privs` flag gets set on the container process.

    - `capabilities` permit privileged actions without giving full root access. This policy ensures all capabilities are dropped from the pod.

    - `runAsNonRoot: true` requires that the container will run with a user with any UID other than 0.

    - `RuntimeDefault` enables the default seccomp profile for a pod or container workload.

2.  Create the pod by running the following command:

    ``` terminal
    $ oc apply -f sysctl_pod.yaml
    ```

3.  Verify that the pod is created by running the following command:

    ``` terminal
    $ oc get pod
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` terminal
    NAME              READY   STATUS            RESTARTS   AGE
    sysctl-example    1/1     Running           0          14s
    ```

    </div>

4.  Log in to the pod by running the following command:

    ``` terminal
    $ oc rsh sysctl-example
    ```

5.  Verify the values of the configured sysctl flags. For example, find the value `kernel.shm_rmid_forced` by running the following command:

    ``` terminal
    sh-4.4# sysctl kernel.shm_rmid_forced
    ```

    <div class="formalpara">

    <div class="title">

    Expected output

    </div>

    ``` terminal
    kernel.shm_rmid_forced = 1
    ```

    </div>

</div>

# Starting a pod with unsafe sysctls

A pod with unsafe sysctls fails to launch on any node unless the cluster administrator explicitly enables unsafe sysctls for that node. As with node-level sysctls, use the taints and toleration feature or labels on nodes to schedule those pods onto the right nodes.

The following example uses the pod `securityContext` to set a safe sysctl `kernel.shm_rmid_forced` and two unsafe sysctls, `net.core.somaxconn` and `kernel.msgmax`. There is no distinction between *safe* and *unsafe* sysctls in the specification.

> [!WARNING]
> To avoid destabilizing your operating system, modify sysctl parameters only after you understand their effects.

The following example illustrates what happens when you add safe and unsafe sysctls to a pod specification:

<div>

<div class="title">

Procedure

</div>

1.  Create a YAML file `sysctl-example-unsafe.yaml` that defines an example pod and add the `securityContext` specification, as shown in the following example:

    ``` yaml
    apiVersion: v1
    kind: Pod
    metadata:
      name: sysctl-example-unsafe
    spec:
      containers:
      - name: podexample
        image: centos
        command: ["bin/bash", "-c", "sleep INF"]
        securityContext:
          runAsUser: 2000
          runAsGroup: 3000
          allowPrivilegeEscalation: false
          capabilities:
            drop: ["ALL"]
      securityContext:
        runAsNonRoot: true
        seccompProfile:
          type: RuntimeDefault
        sysctls:
        - name: kernel.shm_rmid_forced
          value: "0"
        - name: net.core.somaxconn
          value: "1024"
        - name: kernel.msgmax
          value: "65536"
    ```

2.  Create the pod using the following command:

    ``` terminal
    $ oc apply -f sysctl-example-unsafe.yaml
    ```

3.  Verify that the pod is scheduled but does not deploy because unsafe sysctls are not allowed for the node using the following command:

    ``` terminal
    $ oc get pod
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` terminal
    NAME                       READY             STATUS            RESTARTS   AGE
    sysctl-example-unsafe      0/1               SysctlForbidden   0          14s
    ```

    </div>

</div>

# Enabling unsafe sysctls

A cluster administrator can allow certain unsafe sysctls for very special situations such as high performance or real-time application tuning.

If you want to use unsafe sysctls, a cluster administrator must enable them individually for a specific type of node. The sysctls must be namespaced.

You can further control which sysctls are set in pods by specifying lists of sysctls or sysctl patterns in the `allowedUnsafeSysctls` field of the Security Context Constraints.

- The `allowedUnsafeSysctls` option controls specific needs such as high performance or real-time application tuning.

> [!WARNING]
> Due to their nature of being unsafe, the use of unsafe sysctls is at-your-own-risk and can lead to severe problems, such as improper behavior of containers, resource shortage, or breaking a node.

<div>

<div class="title">

Procedure

</div>

1.  List existing MachineConfig objects for your OpenShift Container Platform cluster to decide how to label your machine config by running the following command:

    ``` terminal
    $ oc get machineconfigpool
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` terminal
    NAME     CONFIG                                             UPDATED   UPDATING   DEGRADED   MACHINECOUNT   READYMACHINECOUNT   UPDATEDMACHINECOUNT   DEGRADEDMACHINECOUNT   AGE
    master   rendered-master-bfb92f0cd1684e54d8e234ab7423cc96   True      False      False      3              3                   3                     0                      42m
    worker   rendered-worker-21b6cb9a0f8919c88caf39db80ac1fce   True      False      False      3              3                   3                     0                      42m
    ```

    </div>

2.  Add a label to the machine config pool where the containers with the unsafe sysctls will run by running the following command:

    ``` terminal
    $ oc label machineconfigpool worker custom-kubelet=sysctl
    ```

3.  Create a YAML file `set-sysctl-worker.yaml` that defines a `KubeletConfig` custom resource (CR):

    ``` yaml
    apiVersion: machineconfiguration.openshift.io/v1
    kind: KubeletConfig
    metadata:
      name: custom-kubelet
    spec:
      machineConfigPoolSelector:
        matchLabels:
          custom-kubelet: sysctl
      kubeletConfig:
        allowedUnsafeSysctls:
          - "kernel.msg*"
          - "net.core.somaxconn"
    ```

    - Specify the label from the machine config pool.

    - List the unsafe sysctls you want to allow.

4.  Create the object by running the following command:

    ``` terminal
    $ oc apply -f set-sysctl-worker.yaml
    ```

5.  Wait for the Machine Config Operator to generate the new rendered configuration and apply it to the machines by running the following command:

    ``` terminal
    $ oc get machineconfigpool worker -w
    ```

    After some minutes the `UPDATING` status changes from True to False:

    ``` terminal
    NAME     CONFIG                                             UPDATED   UPDATING   DEGRADED   MACHINECOUNT   READYMACHINECOUNT   UPDATEDMACHINECOUNT   DEGRADEDMACHINECOUNT   AGE
    worker   rendered-worker-f1704a00fc6f30d3a7de9a15fd68a800   False     True       False      3              2                   2                     0                      71m
    worker   rendered-worker-f1704a00fc6f30d3a7de9a15fd68a800   False     True       False      3              2                   3                     0                      72m
    worker   rendered-worker-0188658afe1f3a183ec8c4f14186f4d5   True      False      False      3              3                   3                     0                      72m
    ```

6.  Create a YAML file `sysctl-example-safe-unsafe.yaml` that defines an example pod and add the `securityContext` spec, as shown in the following example:

    ``` yaml
    apiVersion: v1
    kind: Pod
    metadata:
      name: sysctl-example-safe-unsafe
    spec:
      containers:
      - name: podexample
        image: centos
        command: ["bin/bash", "-c", "sleep INF"]
        securityContext:
          runAsUser: 2000
          runAsGroup: 3000
          allowPrivilegeEscalation: false
          capabilities:
            drop: ["ALL"]
      securityContext:
        runAsNonRoot: true
        seccompProfile:
          type: RuntimeDefault
        sysctls:
        - name: kernel.shm_rmid_forced
          value: "0"
        - name: net.core.somaxconn
          value: "1024"
        - name: kernel.msgmax
          value: "65536"
    ```

7.  Create the pod by running the following command:

    ``` terminal
    $ oc apply -f sysctl-example-safe-unsafe.yaml
    ```

    <div class="formalpara">

    <div class="title">

    Expected output

    </div>

    ``` terminal
    Warning: would violate PodSecurity "restricted:latest": forbidden sysctls (net.core.somaxconn, kernel.msgmax)
    pod/sysctl-example-safe-unsafe created
    ```

    </div>

8.  Verify that the pod is created by running the following command:

    ``` terminal
    $ oc get pod
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` terminal
    NAME                         READY   STATUS    RESTARTS   AGE
    sysctl-example-safe-unsafe   1/1     Running   0          19s
    ```

    </div>

9.  Log in to the pod by running the following command:

    ``` terminal
    $ oc rsh sysctl-example-safe-unsafe
    ```

10. Verify the values of the configured sysctl flags. For example, find the value `net.core.somaxconn` by running the following command:

    ``` terminal
    sh-4.4# sysctl net.core.somaxconn
    ```

    <div class="formalpara">

    <div class="title">

    Expected output

    </div>

    ``` terminal
    net.core.somaxconn = 1024
    ```

    </div>

</div>

The unsafe sysctl is now allowed and the value is set as defined in the `securityContext` spec of the updated pod specification.

# Additional resources

- [Configuring system controls by using the tuning CNI](../../networking/configuring_network_settings/configure-syscontrols-interface-tuning-cni.xml#nw-configuring-tuning-cni_configure-syscontrols-interface-tuning-cni)

- [Using the Node Tuning Operator](../../scalability_and_performance/using-node-tuning-operator.xml#using-node-tuning-operator)
