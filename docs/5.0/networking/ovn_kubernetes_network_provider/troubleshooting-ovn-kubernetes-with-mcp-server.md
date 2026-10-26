You can troubleshoot OVN-Kubernetes networking issues in OpenShift Container Platform by enabling the Model Context Protocol (MCP) server `ovn-kubernetes` and `cni-diagnostics` toolsets and applying toolset permissions.

The MCP server for Red Hat OpenShift can diagnose OVN-Kubernetes connectivity issues in OpenShift Container Platform by collecting evidence across Kubernetes, OVN, Open vSwitch, and kernel networking layers with the `ovn-kubernetes` and `cni-diagnostics` toolsets.

> [!NOTE]
> The `ovn-kubernetes` and `cni-diagnostics` toolsets must only be enabled on clusters that use OVN-Kubernetes.

# Configure role based access control (RBAC) for OVN-Kubernetes and CNI diagnostics toolsets

Apply `ClusterRole` and `ClusterRoleBinding` resources so the MCP server for Red Hat OpenShift can list `ovnkube-node` pods, run OVN and OVS commands in them, and create privileged debug pods with host network access.

> [!IMPORTANT]
> The `ovn-kubernetes` tool uses `pods/exec` permissions on privileged `ovnkube-node` pods. The `cni-diagnostics` tool creates privileged debug pods with host network access. Grant these permissions only to trusted users, and monitor Kubernetes audit logs for unexpected tool usage.

<div>

<div class="title">

Prerequisites

</div>

- You have installed and configured the MCP server for Red Hat OpenShift.

- You have configured the MCP server with base RBAC.

- You have cluster administrator permissions.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Create `ClusterRole` and `ClusterRoleBinding` resources that grant the MCP server permissions to list `ovnkube-node` pods and execute OVN and OVS commands inside them:

    <div class="formalpara">

    <div class="title">

    Example of RBAC for the `ovn-kubernetes` toolset

    </div>

    ``` yaml
    apiVersion: rbac.authorization.k8s.io/v1
    kind: ClusterRole
    metadata:
      name: ovn-kubernetes-mcp-user
    rules:
      - apiGroups: [""]
        resources: ["namespaces"]
        verbs: ["get", "list"]
      - apiGroups: [""]
        resources: ["pods"]
        verbs: ["get", "list"]
      - apiGroups: [""]
        resources: ["pods/exec"]
        verbs: ["create"]
    ---
    apiVersion: rbac.authorization.k8s.io/v1
    kind: ClusterRoleBinding
    metadata:
      name: ovn-kubernetes-mcp-user-binding
    roleRef:
      apiGroup: rbac.authorization.k8s.io
      kind: ClusterRole
      name: ovn-kubernetes-mcp-user
    subjects:
      - kind: ServiceAccount
        name: <mcp_server_service_account>
        namespace: <mcp_server_namespace>
    ```

    </div>

    where: `<mcp_server_service_account>`:: Specifies the service account name used by the MCP server. `<mcp_server_namespace>`:: Specifies the namespace where the MCP server service account exists.

2.  Create `ClusterRole` and `ClusterRoleBinding` resources that grant the MCP server permissions for CNI diagnostics by using the following example:

    <div class="formalpara">

    <div class="title">

    Example RBAC for the `cni-diagnostics` toolset

    </div>

    ``` yaml
    apiVersion: rbac.authorization.k8s.io/v1
    kind: ClusterRole
    metadata:
      name: cni-diagnostics-mcp-user
    rules:
      - apiGroups: [""]
        resources: ["nodes"]
        verbs: ["get", "list"]
      - apiGroups: [""]
        resources: ["pods"]
        verbs: ["create", "get", "list", "delete"]
      - apiGroups: [""]
        resources: ["namespaces"]
        verbs: ["get", "list"]
      - apiGroups: [""]
        resources: ["pods/exec"]
        verbs: ["create"]
      - apiGroups: [""]
        resources: ["pods/log"]
        verbs: ["get"]
    ---
    apiVersion: rbac.authorization.k8s.io/v1
    kind: ClusterRoleBinding
    metadata:
      name: cni-diagnostics-mcp-user-binding
    roleRef:
      apiGroup: rbac.authorization.k8s.io
      kind: ClusterRole
      name: cni-diagnostics-mcp-user
    subjects:
      - kind: ServiceAccount
        name: <mcp_server_service_account>
        namespace: <mcp_server_namespace>
    ```

    </div>

    where:

    `<mcp_server_service_account>`
    Specifies the service account name used by the MCP server.

    `<mcp_server_namespace>`
    Specifies the namespace where the MCP server service account exists.

3.  Optional: If your MCP server uses OAuth or token exchange, update the `subjects` field in each `ClusterRoleBinding` to reference the user or group that requires access by using the following example:

    <div class="formalpara">

    <div class="title">

    Example `ClusterRoleBinding` subjects for OAuth or token exchange mode

    </div>

    ``` yaml
    apiVersion: rbac.authorization.k8s.io/v1
    kind: ClusterRoleBinding
    metadata:
      name: <binding_name>
    subjects:
      - kind: User
        name: <user_name>
        apiGroup: rbac.authorization.k8s.io
    ```

    </div>

    ``` yaml
    apiVersion: rbac.authorization.k8s.io/v1
    kind: ClusterRoleBinding
    metadata:
      name: <binding_name>
    subjects:
      - kind: Group
        name: <group_name>
        apiGroup: rbac.authorization.k8s.io
    ```

    where: `<binding_name>`:: Specifies the name of the `ClusterRoleBinding` resource, for example `ovn-kubernetes-mcp-user-binding`. `<user_name>`:: Specifies that the `ClusterRole` is bound to an individual user. Replace `<user_name>` with the user’s username. `<group_name>`:: Specifies that the `ClusterRole` is bound to all members of a group. Replace `<group_name>` with the group name.

4.  Apply the `ovn-kubernetes-mcp-rbac.yaml` manifests by running the following command:

    ``` terminal
    $ oc apply -f ovn-kubernetes-mcp-rbac.yaml
    ```

5.  Apply the `cni-diagnostics-mcp-rbac.yaml` manifests by running the following command:

    ``` terminal
    $ oc apply -f cni-diagnostics-mcp-rbac.yaml
    ```

</div>

# OVN-Kubernetes toolset reference

You can call `ovn-kubernetes` tools from an MCP client to inspect OVN and Open vSwitch state on OpenShift Container Platform.

Unless noted otherwise, OVN-layer tools default the pod namespace to `openshift-ovn-kubernetes`. Supply the `ovnkube-node` pod name. Discover pods with the `core` toolset `pods_list` tool and a label selector such as `app=ovnkube-node`.

| Tool | Key parameters and use |
|----|----|
| `ovn_show` | Set `database` to `nbdb` (`ovn-nbctl show`) or `sbdb` (`ovn-sbctl show`). |
| `ovn_get` | Requires `database` and `table`. `database` accepts only `nbdb` or `sbdb`. Optional `record`, `columns`, and `pattern` filters. |
| `ovn_lflow_list` | Optional `datapath` and `pattern` filters for Southbound logical flows. |
| `ovn_trace` | Requires `datapath` and `microflow`. Optional `mode`: `detailed`, `summary`, or `minimal`. |

OVN layer tools

Common Northbound tables for `ovn_get` include `Logical_Switch`, `Logical_Router`, `Logical_Switch_Port`, `Logical_Router_Port`, `ACL`, `Address_Set`, `Port_Group`, `Load_Balancer`, and `NAT`.

Common Southbound tables include `Chassis`, `Port_Binding`, `Datapath_Binding`, `Logical_Flow`, `MAC_Binding`, `Multicast_Group`, and `SB_Global`.

| Tool | Key parameters and use |
|----|----|
| `ovs_vsctl` | Set `action` to `show`, `list-br`, `list-ports`, or `list-ifaces`. For `list-ports` and `list-ifaces`, set `bridge` (for example, `br-int`). |
| `ovs_ofctl` | Set `action` to `dump-flows` and provide `bridge`. Optional `pattern` filters output lines. |
| `ovs_appctl` | Set `action` to `dpctl/dump-conntrack` or `ofproto/trace`. For `ofproto/trace`, set `bridge` and `flow`. |

OVS layer tools

For OVS-layer tools, set `namespace` to `openshift-ovn-kubernetes` and `name` to the `ovnkube-node` pod on the target node. Optional `head`, `tail`, and `apply_tail_first` parameters limit output size.

# CNI diagnostics toolset reference

You can call `cni-diagnostics` tools from an MCP client for kernel-level networking diagnostics and packet capture on OpenShift Container Platform nodes.

The following `cni-diagnostics` tools create ephemeral privileged debug pods on the target node for kernel-level networking diagnostics and packet capture. Pod-level `tcpdump` uses `pods/exec` on an existing pod. You can customize debug-pod images in the MCP server `config.toml` file.

| Tool | Key parameters and use |
|----|----|
| `get-conntrack` | Requires `node`. Optional `command` values include `-L`, `-C`, and `-S`. |
| `get-iptables` | Requires `node`. Optional `table` and `command` select the table and list style. |
| `get-nft` | Requires `node` and a `command` such as `list ruleset` or `list tables`. |
| `get-ip` | Requires `node` and `command` for `iproute2` queries. |

Kernel-level tools

| Tool | Key parameters and use |
|----|----|
| `tcpdump` | Set `target_type` to `node` or `pod`, and set `name` to the node or pod name. Optional `bpf_filter` and `packet_count` limit the capture. |
| `pwru` | Requires `node_name`. Optional `bpf_filter` and `output_limit_lines` limit the trace. Requires eBPF support. |

Network tools

> [!NOTE]
> Packet capture and eBPF tracing can increase CPU use on production nodes. Use BPF filters and limit packet or line counts to the minimum that you need.

# Additional resources

- [Deploy the MCP server from the MCP Catalog](../../ai_applications/mcp_server/mcp-server-overview.xml#ai-app-mcp-server-install-deploy-server-from-mcp-catalog_mcp-server-overview)

- [Configure RBAC enforcement](../../ai_applications/mcp_server/mcp-server-overview.xml#ai-app-mcp-server-configure-rbac_mcp-server-overview)

- [Troubleshooting OVN-Kubernetes](../../networking/ovn_kubernetes_network_provider/ovn-kubernetes-troubleshooting-sources.xml#ovn-kubernetes-troubleshooting-sources)

- [Tracing Openflow with ovnkube-trace](../../networking/ovn_kubernetes_network_provider/ovn-kubernetes-tracing-using-ovntrace.xml#ovn-kubernetes-tracing-using-ovntrace)

- [Implementation of connection health checks](../../networking/advanced_networking/verifying-connectivity-endpoint.xml#nw-pod-network-connectivity-implementation_verifying-connectivity-endpoint)

- [Verifying network connectivity for an endpoint](../../networking/advanced_networking/verifying-connectivity-endpoint.xml#nw-pod-network-connectivity-verify_verifying-connectivity-endpoint)
