When problems occur on your OpenShift Container Platform cluster, you want to determine exactly what is happening, so that you can fix the issue as soon as possible. The MCP server for Red Hat OpenShift feature provides an AI tool to quickly and easily diagnose your OpenShift Container Platform cluster.

# AI safety

Because MCP server for Red Hat OpenShift grants AI agents access to cluster resources, you must follow safety practices to protect your cluster from unauthorized actions, data exposure, and prompt injection risks.

> [!IMPORTANT]
> This feature uses AI technology. Do not include any personal information or other sensitive information in your input. Interactions may be used to improve Red Hat’s products or services. Always review AI-generated content before using it.

## Data ownership

The MCP server for Red Hat OpenShift does not store any information or state of the cluster. If you opt in, there are several telemetry metrics that are collected to understand the overall usage levels of the MCP server for Red Hat OpenShift:

- Cluster:k8s_mcp_tool_calls:sum:

- Total count of all Model Context Protocol (MCP) tool invocations across the cluster

- Cluster:k8s_mcp_tool_errors:sum:

- Total count of all failed MCP tool invocations across the cluster

- Cluster:k8s_mcp_http_requests:sum:

- Total count of all HTTP requests received by the MCP server

These metrics do not collect specific details of the calls, requests, or errors themselves; they only provide aggregate overall sums of the usage.

To opt in, edit TOML config:

``` toml
[telemetry]
enabled = true
```

To opt out, edit TOML config:

``` toml
[telemetry]
enabled = false
```

## Required verification workflow: Human in the loop (HITL) enforcement

- It is recommended that you assess the AI agent’s proposed action in the MCP client.

- You should manually check suggested resource versions (for example, ensure the model is not suggesting deprecated APIs).

- It is recommended that you use a human approval mechanism in the AI client interface for "write" actions.

## Data privacy and redaction

The MCP server for Red Hat OpenShift has no internal mechanisms for PII and data redaction. To ensure that cluster information within allowed Custom Resources (CRs) complies with data privacy standards, deploy TrustyAI to monitor and sanitize outgoing payloads. For how to scope and limit MCP access to specific CRs, see "Revoke access to Custom Resources".

## Audit trail recommendation

The MCP server for Red Hat OpenShift is configured to append a user-agent string in audit logs to identify that requests were made by an AI agent through the MCP server. Ensure that authorization is enabled via OAuth or MCP gateway. For more information, see "Install MCP server for Red Hat OpenShift".

## Recommendations regarding 3rd-party MCP servers

For better security and control, it is recommended that third-party MCP hosts implement a HITL requirement to approve any "write" operations performed via the MCP server for Red Hat OpenShift.

## AI governance and guardrails

MCP gateway acts as a centralized control point and enforces strict governance over agent-tool interactions through centralized authentication and identity management, using correctly scoped tokens and OAuth 2.0 to ensure agents only possess the specific permissions required for any given task. The MCP gateway further secures the environment using identity-based tool filtering, which removes unauthorized tools from the tools/list discovery process entirely, thus preventing agents from attempting to access forbidden capabilities.

To mitigate AI-specific risks, the gateway should be deployed with safety guardrails. Guardrails would include inspecting traffic payloads for prompt injections and safety violations by integrating with external engines like Trusty AI or NVIDIA Nemo. Additionally, the MCP gateway ensures operational stability and accountability by implementing rate limiting to prevent agent-driven denial-of-service attacks and providing comprehensive audit logging to track and analyze all tool usage.

## Use MCP gateway for aggregation and controlling access

It is highly recommended to use the MCP gateway to aggregate and control access to the MCP servers, including managing authentication and authorization to the MCP servers. This also provides observability and governance of MCP tool usage. Additionally, the MCP gateway also includes integration with Trusty AI and NeMo guardrails, which screens requests and response traffic for PII, prompt injection, and unsafe content before it reaches MCP servers.

## Emergency removal of AI agent access

In an emergency, you can use any of the following possible actions to revoke access for the AI agent (via the MCP server):

For information about how to apply configuration changes, see "Applying configuration changes to the MCP server for Red Hat OpenShift".

- **Remove access to the offending tool** in `config.toml`.

  Only enable specific tools:

  ``` toml
  enabled_tools = ["pods_list", "pods_get", "pods_log"]
  ```

- **Disable specific tools** from enabled toolsets.

  Disable destructive tool calls in `config.toml`.

  ``` toml
  disabled_tools = ["resources_delete", "pods_delete"].
  ```

- **Create a production-safe configuration**.

  ``` toml
  read_only = true
  ```

- **Allow writes, but prevent deletions**.

  ``` toml
  disable_destructive = true
  ```

- **Uninstall the MCP server completely** by running the following command:

  ``` terminal
  $ oc delete mcpserver --all --all-namespaces
  ```

- **RBAC revocation**:

  Remove the user’s rolebinding or clusterrolebinding. For more information, see "Install MCP server for Red Hat OpenShift".

- **Remove access through the MCP gateway**

  To remove access through the gateway, you can delete the MCPServerRegistration CR by running the following command:

  ``` terminal
  $ oc delete mcpsr <name of registration>
  ```

<div>

<div class="title">

Additional resources

</div>

- [Revoke access to Custom Resources](../../ai_applications/mcp_server/mcp-server-overview.xml#ai-app-mcp-server-revoke-cr-access_mcp-server-overview)

- [Install the MCP server](../../ai_applications/mcp_server/mcp-server-overview.xml#ai-app-mcp-server-install-lifecycle-operator_mcp-server-overview)

- [Applying configuration changes to the MCP server for Red Hat OpenShift](../../ai_applications/mcp_server/mcp-server-overview.xml#ai-app-mcp-server-apply-config-changes_mcp-server-overview)

</div>

# Model Context Protocol overview

Model Context Protocol (MCP) is an open source standard that enables AI applications to securely connect to external data sources, tools, and workflows without custom integrations.

MCP is an open source standard for connecting AI applications to external systems.

Using MCP, AI applications, such as Claude Code or Cursor, can connect to the following items, enabling them to access key information and perform tasks:

- **Data sources**: for example, local files, databases

- **Tools**: for example, search engines, calculators

- **Workflows**: for example, specialized prompts

MCP works similarly to a USB-C port for AI applications. Just as USB-C provides a standardized way to connect electronic devices, MCP provides a standardized way to connect AI applications to external systems.

# MCP server overview

A Model Context Protocol (MCP) server exposes cluster data and operations to AI models in a structured, secure way, so that AI agents can diagnose and act on your cluster without needing direct access to APIs or databases.

## The Goals of an MCP server

The primary goal of an MCP server is to expose specific capabilities to an AI model in a structured, safe, and predictable way. Here are the key objectives an MCP server achieves:

- **Capability exposure**: The server defines exactly what the AI is allowed to do or see. It does this by exposing three specific things:

  - **Tools**: Executable functions that do things (for example, "Delete this file," "Post to Slack," or "Calculate mortgage").

  - **Resources**: Read-only data sources that provide context (for example, "Read the contents of README.md" or "Fetch the logs from the last hour").

  - **Prompts**: Predefined templates that guide the AI model’s behavior (for example, a "Code Reviewer" prompt that tells the AI exactly how to look for bugs in a specific language).

- **Abstraction of complexity**: An MCP server hides the complicated parts of an integration. The LLM does not need to know how to write a SQL query or use a specific GitHub API. The server handles the code, the formatting, and the technical unique complexities, giving the LLM a clean, standardized result.

- **Execution and action**: When an AI \[agent or client\] decides to use a tool, the MCP server executes using the specific tool. For example, runs a Python script, queries a database, or calls an external API.

- **Safety and security**: The server provides a layer of isolation. By running as a separate process, it can be restricted to only accessing specific folders or specific API endpoints. If the AI model attempts to undesired or unintended action, for example, tries to delete your entire hard drive, the server can deny the behavior based on its internal rules.

# MCP gateway overview

The primary goal of a Model Context Protocol (MCP) gateway is to standardize and simplify how AI models interact with external data and tools. Without a gateway, an AI model would need a custom integration for every single database, API, or local file system it needs to access.

## Aggregation and orchestration

A gateway connects to multiple MCP servers simultaneously. Instead of the LLM (Large Language Model) managing ten different connections, it communicates only with the gateway. The gateway then routes the LLM’s request to the specific server that holds the relevant information (for example, fetching Jira tickets from one server and Google Drive docs from another).

## Security and access control

The gateway acts as a security perimeter.

It manages:

- **Authentication**: Holding the API keys or tokens required for various servers.

- **Permissions**: Ensuring the AI model only accesses the specific data or tools that the user authorized.

- **Privacy**: Stripping sensitive information before it is sent back to the model provider.

## Protocol translation

The gateway ensures that the communication between the AI model and the servers follows the MCP standard. It translates the high-level "intent" of the AI model into the specific JSON-RPC calls that the MCP servers understand.

## Scalability

By decoupling the AI model from the data sources, you can add, remove, or update MCP servers without ever needing to change the core configuration of your AI application.

# MCP server for Red Hat OpenShift Prompting workflow

By understanding the Model Context Protocol (MCP) prompting workflow you can better troubleshoot issues and optimize how your prompts reach cluster resources through the MCP server, gateway, and a Large Language Model (LLM).

When you prompt an LLM, the execution happens according to the following steps:

1.  User types a prompt: "Are there any pods that keep restarting?".

2.  MCP Host (for example, Claude Desktop): receives your prompt. It looks at its connected MCP servers and sees one has a tool called pods_list.

3.  MCP gateway (If used): If you are in an enterprise environment, the Host talks to the gateway first. The gateway checks "Is this user allowed to access the cluster?" and "Is the cluster currently online?"

4.  MCP server: The gateway (or Host) sends the command to the server. The server runs the actual code (the API call to OpenShift), gets the data, and sends it back.

5.  LLM: Receives that raw data, "reads" it, and gives you the final summary.

# Install MCP server for Red Hat OpenShift

Install and configure the MCP server for Red Hat OpenShift to enable AI agents to securely diagnose and inspect your cluster.

To install the MCP server for Red Hat OpenShift feature, complete the following procedures.

<div>

<div class="title">

Prerequisites

</div>

- Access to OpenShift console with admin rights.

- Installed MCP-compatible client, such as Claude Code, Visual Studio Code (VS Code), Cursor, or OpenShift LightSpeed (OLS).

  Gemma 4 is also available for disconnected environments.

  > [!NOTE]
  > Cloud-only results do not apply to disconnected deployments.

- Red Hat OpenShift AI v3.5 installed on an OpenShift Container Platform v4.22 cluster.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Install the MCP gateway.

2.  Enable the MCP Lifecycle Operator.

3.  Deploy the MCP server from the MCP Catalog.

4.  Verify the MCP gateway deployment.

5.  Configure the MCP gateway.

6.  Connect a Model Context Protocol (MCP)-compatible client, such as Claude Code, to the MCP server.

7.  Configure RBAC enforcement.

8.  Revoke access to Custom Resources.

9.  Set up the MCP gateway authentication.

10. Set up MCP gateway authorization.

</div>

## Install the MCP gateway

Install the Model Context Protocol (MCP) gateway to provide a secure, centralized entry point that enforces authentication, authorization, and rate limiting for all MCP server traffic.

<div>

<div class="title">

Procedure

</div>

1.  Install the MCP gateway.

    For information about how to install the MCP gateway, see "Install the MCP gateway (Red Hat Connectivity Link)".

    After installation, the controller automatically creates the HTTPRoute for gateway access. The MCP gateway acts as a reverse proxy that aggregates multiple MCP servers into a single endpoint and provides a layer for authentication and rate limiting.

</div>

<div>

<div class="title">

Additional resources

</div>

- [Install the MCP gateway (Red Hat Connectivity Link)](https://docs.redhat.com/en/documentation/red_hat_connectivity_link/1.4/html/install_the_mcp_gateway/index)

</div>

## Enable the MCP Lifecycle Operator

To install the MCP server for Red Hat OpenShift feature, install the Model Context Protocol (MCP) server by using the MCP Lifecycle Operator.

> [!IMPORTANT]
> MCP Lifecycle Operator is a Technology Preview feature only. Technology Preview features are not supported with Red Hat production service level agreements (SLAs) and might not be functionally complete. Red Hat does not recommend using them in production. These features provide early access to upcoming product features, enabling customers to test functionality and provide feedback during the development process.
>
> For more information about the support scope of Red Hat Technology Preview features, see [Technology Preview Features Support Scope](https://access.redhat.com/support/offerings/techpreview/).

<div>

<div class="title">

Prerequisites

</div>

- MCP gateway is installed.

- Access to OpenShift console with admin rights.

</div>

<div>

<div class="title">

Procedure

</div>

- For information about installing by using MCP Lifecycle Operator, see "Enable MCP server lifecycle management (Red Hat OpenShift AI documentation)".

  > [!IMPORTANT]
  > To install the MCP Lifecycle Operator, you need to install Red Hat OpenShift AI v3.6.0-ae2, which is an Early Release version of the software.

  Red Hat OpenShift AI v3.6.0-ae2 is available in the console under **Software Catalog** → **AI/Machine Learning** → **Red Hat OpenShift AI**. Under **Channel**, select **beta**, and under **Version**, select **3.6.0-ae.2**.

</div>

<div>

<div class="title">

Additional resources

</div>

- [Enable MCP server lifecycle management (Red Hat OpenShift AI documentation)](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.5/html/working_with_the_mcp_catalog/enabling-mcp-lifecycle-management)

</div>

## Deploy the MCP server from the MCP Catalog

Deploy the MCP server for Red Hat OpenShift from the Model Context Protocol (MCP) Catalog in Red Hat OpenShift AI. The MCP Catalog creates the MCP server custom resource (CR), which the MCP Lifecycle Operator reconciles, configuring the deployment, service, and network policy automatically.

<div>

<div class="title">

Prerequisites

</div>

- MCP gateway is installed.

- MCP Lifecycle Operator is enabled.

</div>

<div>

<div class="title">

Procedure

</div>

- For information about deploying the MCP server from the MCP Catalog, see "Deploy MCP servers from the MCP Catalog (Red Hat OpenShift AI documentation)".

</div>

<div>

<div class="title">

Additional resources

</div>

- [Deploy MCP servers from the MCP Catalog (Red Hat OpenShift AI documentation)](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.5/html/working_with_the_mcp_catalog/deploying-and-managing-mcp-servers#deploying-mcp-servers-from-the-mcp-catalog_deploying-mcp-servers)

</div>

## Verify the MCP gateway deployment

Verify that the Model Context Protocol (MCP) gateway is deployed and running correctly before configuring routing, authentication, and authorization.

<div>

<div class="title">

Prerequisites

</div>

- Access to an OpenShift Container Platform console and you have `admin` rights.

- OpenShift CLI (`oc`) is installed.

- MCP gateway is installed.

- MCP Lifecycle Operator is enabled.

- The MCP server is installed.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Check the status of your deployment by running the following command:

    ``` terminal
    $ oc get pods -n gateway-namespace -l "app.kubernetes.io/name=mcp-gateway"
    ```

    > [!NOTE]
    > This example uses the namespace "gateway-namespace" for installing the gateway. If you install the gateway in a different namespace than "gateway-namespace", use that namespace instead throughout the procedure.

    <div class="formalpara">

    <div class="title">

    Example

    </div>

    ``` terminal
    NAME                                      READY   STATUS    RESTARTS   AGE
    mcp-gateway-controller-594b9649cf-zstfw   1/1     Running   0          22s
    ```

    </div>

2.  Ensure that the MCP gateway Extension exists by running the following command:

    ``` terminal
    $ oc get mcpgatewayextension -A
    ```

    <div class="formalpara">

    <div class="title">

    Example

    </div>

    ``` terminal
    NAMESPACE          NAME          READY   AGE
    gateway-namespace  mcp-gateway           105s
    ```

    </div>

3.  Verify the broker-router deployment by running the following command:

    ``` terminal
    $ oc logs -n gateway-namespace deployment/mcp-gateway
    ```

4.  Verify EnvoyFilter was created in the gateway namespace by running the following command:

    ``` terminal
    $ oc get envoyfilter -n gateway-namespace -l app.kubernetes.io/managed-by=mcp-gateway-controller
    ```

</div>

## Configure the MCP gateway

Configure the Model Context Protocol (MCP) gateway so that it can route client traffic to your MCP server and discover the tools the server exposes.

<div>

<div class="title">

Prerequisites

</div>

- Access to OpenShift console with admin rights.

- MCP gateway is installed.

- MCP Lifecycle Operator is enabled.

- The MCP server is installed.

- The MCP gateway deployment is verified.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Before creating the `HTTPRoute`, verify the exact name of your MCP server service by entering the following command:

    ``` terminal
    $ oc get svc -n openshift-mcp-server
    ```

    Ensure that the `backendRefs.name` field in the following manifest matches the `NAME` output of your service. For example, `openshift-mcp-server`.

2.  Create the HTTPRoute for the MCP server by running the following command:

    ``` terminal
    $ oc apply -f - <<EOF
    apiVersion: gateway.networking.k8s.io/v1
    kind: HTTPRoute
    metadata:
      name: mcp-api-key-server-route
      namespace: openshift-mcp-server
    spec:
      parentRefs:
      - group: gateway.networking.k8s.io
        kind: Gateway
        name: mcp-gateway
        namespace: gateway-namespace
        sectionName: mcp
      hostnames:
      - ${MCP_SERVER_HOST}
      rules:
      - matches:
        - path:
            type: PathPrefix
            value: /mcp
        backendRefs:
        - name: openshift-mcp-server
          port: 8080
    EOF
    ```

    `${MCP_SERVER_HOST}` is the hostname of your MCP gateway route (for example, mcp-gateway.apps.\<cluster-name\>.\<domain-name\>).

    This HTTPRoute enables the MCP gateway to route traffic to your MCP server instance and is referenced in the MCPServerRegistration resource.

3.  Create an MCP server Registration Resource by running the following command:

    ``` terminal
    $ oc apply -f - <<EOF
    apiVersion: mcp.kuadrant.io/v1alpha1
    kind: MCPServerRegistration
    metadata:
      name: my-mcp-server-reg
      namespace: openshift-mcp-server
    spec:
      prefix: "openshift_"
      targetRef:
        group: "gateway.networking.k8s.io"
        kind: "HTTPRoute"
        name: "mcp-api-key-server-route"
        namespace: openshift-mcp-server
    EOF
    ```

    - `metadata.name`: Provide a name for the MCP server registration object.

    - `metadata.namespace`: The namespace for the MCP server, which is `openshift-mcp-server`.

    - `spec.targetRef.name`: The name of your MCP server HTTPRoute. You can find this by running the command: `oc get httproute -n openshift-mcp-server`.

    - `spec.targetRef.namespace`: The namespace for the MCP server HTTPRoute, which is `openshift-mcp-server`.

4.  Verify the registration status by running the following commands:

    ``` terminal
    $ oc wait --for=condition=Ready mcpsr/my-mcp-server-reg -n openshift-mcp-server --timeout=120s
    $ oc get mcpsr -A
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` terminal
    NAMESPACE             NAME                PREFIX      TARGET                     PATH   READY   TOOLS   CREDENTIALS   AGE
    openshift-mcp-server  my-mcp-server-reg   myserver_   mcp-api-key-server-route   /mcp   True    4                     30s
    ```

    </div>

    The **READY** column should display `True` and the **TOOLS** column should show the number of tools discovered.

    If the status is not ready, check the MCP server Registration conditions for details by running the following command:

    ``` terminal
    $ oc describe mcpsr my-mcp-server-reg -n openshift-mcp-server
    ```

5.  Check the controller logs by running the following command:

    ``` terminal
    $ oc logs -n gateway-namespace deployment/mcp-gateway-controller
    ```

6.  Check the broker logs for tool discovery by running the following command:

    ``` terminal
    $ oc logs -n gateway-namespace deployment/mcp-gateway
    ```

7.  Verify that your MCP server tools are available through the MCP gateway:

    1.  Initialize the MCP session and capture session ID by using -D to dump headers to a file, and then reading the session ID by running the following command:

        ``` terminal
        $ curl -s -D /tmp/mcp_headers -X POST http://mcp-gateway.apps.<cluster-name>.<domain-name>:8001/mcp  \
          -H "Content-Type: application/json" \
          -d '{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "test-client", "version": "1.0.0"}}}'
        ```

        `<cluster-name>.<domain-name>` is the name and domain of your cluster.

    2.  Extract the MCP session ID from response headers by running the following commands:

        ``` terminal
        $ SESSION_ID=$(grep -i "mcp-session-id:" /tmp/mcp_headers | cut -d' ' -f2 | tr -d '\r')

        $ echo "MCP Session ID: $SESSION_ID"
        ```

    3.  List tools by using the session ID in the following command:

        ``` terminal
        $ curl -X POST http://mcp-gateway.apps.<cluster-name>.<domain-name>:8001/mcp \
          -H "Content-Type: application/json" \
          -H "mcp-session-id: $SESSION_ID" \
          -d '{"jsonrpc": "2.0", "id": 2, "method": "tools/list"}'
        ```

        `<cluster-name>.<domain-name>` is the name and domain of your cluster.

    4.  Clean up by running the following command:

        ``` terminal
        $ rm -f /tmp/mcp_headers
        ```

        You should now see your MCP server tools in the response, prefixed with your configured `prefix` value, such as `openshift_`.

</div>

## Connect a client to the MCP server

Connect a client that is compatible with the Model Context Protocol (MCP) to the MCP server so that an AI agent can interact with your cluster.

<div>

<div class="title">

Prerequisites

</div>

- Access to OpenShift console with admin rights.

- MCP gateway is installed.

- MCP Lifecycle Operator is enabled.

- The MCP server is installed.

- MCP gateway is configured and verified.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Add the following lines to your client configuration file:

    - For Claude Desktop: `claude_desktop_config.json` file

    - For Claude Code (CLI): `.mcp.json` file

      ``` json
      {
        "mcpServers": {
          "openshift": {
            "type": "http",
            "url": "<url of the mcp gateway>/mcp"
          }
        }
      }
      ```

      `<url of the mcp gateway>` is the hostname you configured during MCP gateway installation.

2.  Accept the CA certificate when prompted by the client.

</div>

## Configure RBAC enforcement

To control which cluster resources the Model Context Protocol (MCP) server can access, configure role-based access control (RBAC) so that AI agents are limited to only the resources they need.

By default, RBAC is enabled, and you can extend the ClusterRoles, ClusterRoleBindings, Roles, and Rolebindings.

<div>

<div class="title">

Prerequisites

</div>

- Access to OpenShift console with admin rights.

- MCP gateway is installed.

- MCP Lifecycle Operator is enabled.

- The MCP server is installed.

- MCP gateway is configured and verified.

- MCP-compatible client connected.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Configure RBAC enforcement by extending ClusterRoles, ClusterRoleBindings, Roles, and Rolebindings.

    Use the following example RBAC YAML file to extend ClusterRoles, ClusterRoleBindings, Roles, and Rolebindings:

    <div class="formalpara">

    <div class="title">

    Example RBAC settings YAML file

    </div>

    ``` yaml
      apiVersion: rbac.authorization.k8s.io/v1
      kind: ClusterRole
      metadata:
        name: acm-managed-clusters
      rules:
        ...
      ---
      apiVersion: rbac.authorization.k8s.io/v1
      kind: ClusterRoleBinding
      metadata:
        name: acm-managed-clusters
        ...
      ---
      apiVersion: rbac.authorization.k8s.io/v1
      kind: Role
      metadata:
        name: acm-cluster-proxy-discovery
        namespace: multicluster-engine
        ...
      ---
      apiVersion: rbac.authorization.k8s.io/v1
      kind: RoleBinding
      metadata:
        name: acm-cluster-proxy-discovery
        namespace: multicluster-engine
        ...
    ```

    </div>

2.  Apply the RBAC configuration by saving the preceding example to a file (for example, `rbac-values.yaml`), and then run the following command:

    ``` terminal
    $ oc apply -f rbac-values.yaml
    ```

</div>

## Revoke access to Custom Resources

To prevent AI agents from reading or exposing confidential cluster data, you can revoke Model Context Protocol (MCP) server access to sensitive Custom Resources (CRs), such as Secrets and ConfigMaps.

<div>

<div class="title">

Prerequisites

</div>

- Access to OpenShift console with admin rights.

- MCP gateway is installed.

- MCP Lifecycle Operator is enabled.

- The MCP server is installed.

- MCP gateway is configured and verified.

- MCP-compatible client connected.

- RBAC is configured.

</div>

<div>

<div class="title">

Procedure

</div>

- Edit the openshift-mcp-server ConfigMap to add the denied resource values by running the following command:

  ``` terminal
  $ oc edit cm openshift-mcp-server
  ```

  Use the following example file to revoke access to Secrets, ConfigMaps, and RBAC resources:

  <div class="formalpara">

  <div class="title">

  Example

  </div>

  ``` toml
  # Deny access to Secrets
  [[denied_resources]]
  group = ""
  version = "v1"
  kind = "Secret"

  # Deny access to ConfigMaps
  [[denied_resources]]
  group = ""
  version = "v1"
  kind = "ConfigMap"

  # Deny access to RBAC resources for additional security
  [[denied_resources]]
  group = "rbac.authorization.k8s.io"
  version = "v1"
  kind = "Role"

  [[denied_resources]]
  group = "rbac.authorization.k8s.io"
  version = "v1"
  kind = "RoleBinding"

  [[denied_resources]]
  group = "rbac.authorization.k8s.io"
  version = "v1"
  kind = "ClusterRole"

  [[denied_resources]]
  group = "rbac.authorization.k8s.io"
  version = "v1"
  kind = "ClusterRoleBinding"
  ```

  </div>

</div>

## Identity provider and OAuth integration

Integrate the MCP server for Red Hat OpenShift with an identity provider and OAuth so that users authenticate through single sign-on and the server accesses OpenShift Container Platform resources with their identity.

An *identity provider* (IdP) is a centralized service that creates, maintains, and manages user identity information and authenticates users to applications and systems. Instead of separate credentials per application, an IdP lets users authenticate once (single sign-on) and pass that verification securely to other services.

*OAuth* (specifically OAuth 2.0) is an open-standard authorization framework. It allows a third-party application to access a user’s resources on another service without exposing the user’s password. Instead of sharing login credentials, OAuth uses access tokens that grant specific, limited permissions (scopes).

The MCP gateway validates the OAuth token and passes it to the MCP server, which uses it to authenticate against the OpenShift Container Platform API. The server either passes the token through (default) or exchanges it depending on configuration: Controlled by `cluster_auth_mode` and whether a `[token_exchange]` block is configured..

There are two Identity and Access Management (IAM) platforms that you can use:

- Red Hat build of Keycloak

- Microsoft Entra ID

## Set up MCP gateway authentication

To ensure that only verified users can access MCP server for Red Hat OpenShift tools and cluster resources, set up OAuth-based authentication for the Model Context Protocol (MCP) gateway.

<div>

<div class="title">

Prerequisites

</div>

- Access to OpenShift console with admin rights.

- MCP gateway is installed.

- MCP Lifecycle Operator is enabled.

- The MCP server is installed.

- MCP gateway is configured and verified.

- MCP-compatible client connected.

- RBAC is configured.

- You have revoked access to specific Custom Resources (CRs) as needed.

- You have access to an identity provider (IdP): Entra ID or Keycloak.

- The OpenShift Container Platform cluster is configured to trust your IdP as an external OIDC provider (see "Enabling direct authentication with an external OIDC identity provider").

</div>

<div>

<div class="title">

Procedure

</div>

1.  Configure OAuth metadata discovery by setting environment variables on the MCP gateway broker-router deployment by running the following command:

    ``` terminal
    $ oc set env mcp-gateway/gateway-namespace -n mcp-system\
    OAUTH_RESOURCE_NAME="MCP Server" \
    OAUTH_RESOURCE="https://<mcp_gateway_host>/mcp" \
    OAUTH_AUTHORIZATION_SERVERS=<authorization_server_url> \
    OAUTH_BEARER_METHODS_SUPPORTED="header" \
    OAUTH_SCOPES_SUPPORTED=<oauth-scopes-supported>
    ```

    > [!NOTE]
    > These environment variables enable the OAuth 2.0 Protected Resource Metadata endpoint that clients use for authentication discovery.

    - For `<oauth-scopes-supported>` use either:

      - For Entra ID: "api://\<MCP_SERVER_CLIENT_ID\>/mcp-server"

      - For Keycloak: "mcp-server"

    - For `<authorization_server_url>` use either:

      - Entra ID: [https://login.microsoftonline.com/\<tenant-id\>/v2.0](https://login.microsoftonline.com/<tenant-id>/v2.0)

      - Keycloak: [https://\<keycloak_host\>/realms/\<realm\>](https://<keycloak_host>/realms/<realm>);

2.  Create the HTTPRoute for OAuth discovery by running the following command:

    ``` terminal
    $ oc apply -f - <<EOF
    apiVersion: gateway.networking.k8s.io/v1
    kind: HTTPRoute
    metadata:
      name: mcp-gateway-oauth-metadata
      namespace: gateway-namespace
    spec:
      parentRefs:
      - group: gateway.networking.k8s.io
        kind: Gateway
        name: mcp-gateway
        namespace: gateway-namespace
        sectionName: mcp
      hostnames:
      - ${MCP_GATEWAY_HOST}
      rules:
      - matches:
        - path:
            type: PathPrefix
            value: /.well-known/oauth-protected-resource
        backendRefs:
        - name: mcp-gateway
          port: 8080
    EOF
    ```

    `${MCP_GATEWAY_HOST}` is the fully qualified domain name for your MCP gateway (for example, `mcp.127-0-0-1.sslip.io`).

    This route enables clients to discover OAuth metadata, which is required for the authentication flow. Without this route, clients receive a 404 error when attempting OAuth discovery.

3.  Configure the IdP (Entra ID or Keycloak) App Registration:

    - For *Entra ID*:

      1.  In the Azure Portal or Entra admin center, go to your Entra ID App Registration.

      2.  Under **Expose an API**, add a custom scope named `mcp-server`.

      3.  Ensure that the following scopes are available: `openid`, `offline_access`, and `mcp-server`.

      4.  If required by your organization, grant admin consent for these scopes.

          For more information about configuring Entra ID app registrations, see "Microsoft Entra ID".

    - For *Keycloak*:

      1.  Ensure that the following required scopes exist in your Keycloak realm:

          - openid (built-in)

          - offline_access (built-in)

          - mcp-server (custom — create it if it does not exist)

      2.  In the admin console, go to **Realm Settings** \> **Client Registration** \> **Authenticated Access Policies**, and add these scopes to the realm’s DCR Allowed Client Scopes policy.

          For more information about Keycloak, see "Red Hat build of Keycloak".

4.  Configure certificate trust for JWT validation by mounting the IdP’s CA certificate into the Authorino deployment by running the following commands:

    > [!IMPORTANT]
    > Skip this step if the IdP uses a publicly trusted certificate.

    ``` terminal
    $ oc create configmap idp-ca --from-file=ca.crt=/path/to/idp-ca.crt -n kuadrant-system
    ```

    ``` terminal
    $ oc patch deployment authorino -n kuadrant-system --type=json -p='[
      {
        "op": "add",
        "path": "/spec/template/spec/volumes/-",
        "value": {"name": "idp-ca", "configMap": {"name": "idp-ca"}}
      },
      {
        "op": "add",
        "path": "/spec/template/spec/containers/0/volumeMounts/-",
        "value": {"name": "idp-ca", "mountPath": "/etc/ssl/certs/idp-ca.crt", "subPath": "ca.crt"}
      }
    ]'
    ```

    This ensures that Authorino can verify JWT token signatures from the IdP.

5.  Configure the MCP gateway authentication by applying the authentication policy that validates JWT tokens by running the following command:

    ``` terminal
    $ oc apply -f - <<EOF
    apiVersion: kuadrant.io/v1
    kind: AuthPolicy
    metadata:
      name: mcp-auth-policy
      namespace: gateway-namespace
    spec:
      targetRef:
        group: gateway.networking.k8s.io
        kind: Gateway
        name: mcp-gateway
        sectionName: mcp
      defaults:
        when:
          - predicate: "!request.path.contains('/.well-known')"
        rules:
          authentication:
            'idp':
              jwt:
                issuerUrl: <authorization_server_url>
          response:
            unauthenticated:
              code: 401
              headers:
                'WWW-Authenticate':
                  value: Bearer resource_metadata=https://<mcp_gateway_host>/.well-known/oauth-protected-resource/mcp
                body:
                  value: |
                    {
                      "error": "Unauthorized",
                      "message": "Authentication required."
                    }

            success:
              headers:
                authorization:
                  plain:
                    expression: "request.headers['authorization']"

    EOF
    ```

    - For `<authorization_server_url>` use either:

      - Entra ID: [http://login.microsoftonline.com/\<tenant-id\>/v2.0](http://login.microsoftonline.com/<tenant-id>/v2.0)

      - Keycloak: [https://\<keycloak_host\>/realms/\<realm\>](https://<keycloak_host>/realms/<realm>);

6.  Grant the authenticated user permissions on the cluster by creating a `ClusterRoleBinding` by using a file similar to the following:

    ``` yaml
    apiVersion: rbac.authorization.k8s.io/v1
    kind: ClusterRoleBinding
    metadata:
      name: oidc-mcp-cluster-reader
    roleRef:
      apiGroup: rbac.authorization.k8s.io
      kind: ClusterRole
      name: view
    subjects:
    - apiGroup: rbac.authorization.k8s.io
      kind: User
      name: <issuer_url>#<username>
    ```

    - `name`: The user subject, in the format `<issuer_url>#<username>`.

    - Adjust the `ClusterRole` (for example, `view`) to the level of access the user requires.

</div>

<div>

<div class="title">

Verification

</div>

1.  Verify OAuth Discovery by testing that the broker now serves OAuth discovery information by running the following command:

    ``` terminal
    curl ${MCP_GATEWAY_HOST}/.well-known/oauth-protected-resource
    ```

    For `${MCP_GATEWAY_HOST}` use your MCP gateway domain.

    The command should show OAuth 2.0 Protected Resource Metadata similar to the following:

    <div class="formalpara">

    <div class="title">

    Example

    </div>

    ``` terminal
    {
      "resource_name": "MCP Server",
      "resource": "http://mcp.127-0-0-1.sslip.io:8001/mcp",
      "authorization_servers": [
        "https://login.microsoftonline.com/<tenant-id>/v2.0"
      ],
      "bearer_methods_supported": [
        "header"
      ],
      "scopes_supported": [
        "mcp-server",
      ]
    }
    ```

    </div>

2.  Test that protected endpoints now require authentication by running the following command:

    ``` terminal
    $ curl -v ${MCP_GATEWAY_HOST}/mcp \
      -H "Content-Type: application/json" \
      -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}'
    ```

    - For `${MCP_GATEWAY_HOST}` use your MCP gateway domain.

      <div class="formalpara">

      <div class="title">

      Example

      </div>

      ``` terminal
      {
        "error": "Unauthorized",
        "message": "Authentication required."
      }
      ```

      </div>

</div>

<div>

<div class="title">

Additional resources

</div>

- [Enabling direct authentication with an external OIDC identity provider](../../authentication/external-auth.xml#external-auth)

- [Microsoft Entra ID](https://www.microsoft.com/en-us/security/business/identity-access/microsoft-entra-id)

- [Red Hat build of Keycloak](https://docs.redhat.com/en/documentation/red_hat_build_of_keycloak/)

</div>

## Set up MCP gateway authorization

Set up tool-level authorization for the Model Context Protocol (MCP) gateway to control which users can access specific MCP server tools, ensuring that each user can only use the operations permitted by their role.

<div>

<div class="title">

Prerequisites

</div>

- Access to OpenShift console with admin rights.

- MCP gateway is installed.

- MCP Lifecycle Operator is enabled.

- The MCP server is installed.

- MCP gateway is configured and verified.

- MCP-compatible client connected.

- RBAC is configured.

- You have revoked access to specific Custom Resources (CRs) as needed.

- MCP gateway authentication is configured.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Ensure that your identity provider includes necessary group/role claims in the issued JWT tokens.

    The issued OAuth token should include claims similar to:

    <div class="formalpara">

    <div class="title">

    Example

    </div>

    ``` json
    {
      "resource_access": {
        "mcp-ns/openshift-mcp-server": {
          "roles": ["pods_list", "events_list", "nodes_list", "deployments_get"]
        },
        "mcp-ns/geometry-mcp-server": {
          "roles": ["pods_list", "events_list", "nodes_list", "deployments_get"]
        }
      }
    }
    ```

    </div>

    - The namespace should match the namespace of the `MCPServerRegistration` CR.

    - The “roles” represent the allowed tools. In this example, pods_list, events_list, nodes_list, deployments_get.

2.  Configure tool-level authorization by applying an AuthPolicy that enforces tool-level access control by running the following command:

    ``` terminal
    $ oc apply -f - <<EOF
    apiVersion: kuadrant.io/v1
    kind: AuthPolicy
    metadata:
      name: mcp-tool-auth-policy
      namespace: openshift-mcp-server
    spec:
      targetRef:
        group: gateway.networking.k8s.io
        kind: Gateway
        name: mcp-gateway
        sectionName: mcp
      rules:
        authentication:
          'idp':
            jwt:
              issuerUrl: <authorization_server_url>
        authorization:
          'tool-access-check':
            patternMatching:
              patterns:
                - predicate: |
                    request.headers['x-mcp-toolname'] in (has(auth.identity.resource_access) && auth.identity.resource_access.exists(p, p == request.headers['x-mcp-servername']) ? auth.identity.resource_access[request.headers['x-mcp-servername']].roles : [])
        response:
          unauthenticated:
            headers:
              'WWW-Authenticate':
                value: Bearer resource_metadata=https://<mcp_gateway_host>/.well-known/oauth-protected-resource/mcp
            body:
              value: |
                {
                  "error": "Unauthorized",
                  "message": "MCP Tool Access denied: Authentication required."
                }
          unauthorized:
            body:
              value: |
                {
                  "error": "Forbidden",
                  "message": "MCP Tool Access denied: Insufficient permissions for this tool."
                }
    EOF
    ```

    - For `<authorization_server_url>` use either:

      - Entra ID: login.microsoftonline.com/\<tenant-id\>/v2.0

      - Keycloak: [https://\<keycloak_host\>/realms/\<realm\>](https://<keycloak_host>/realms/<realm>);

    - `spec.sectionName` targets the MCP server Listener.

    - `<cluster-name>.<domain-name>` is the name and domain of your cluster.

</div>

<div>

<div class="title">

Verification

</div>

1.  Test that authorization now controls tool access by setting up the MCP Inspector:

    1.  Start MCP Inspector (requires Node.js/npm) by running the following command:

        ``` terminal
        $ npx @modelcontextprotocol/inspector@latest &
        INSPECTOR_PID=$!
        ```

    2.  Wait for services to start by running the following command:

        ``` terminal
        $ sleep 3
        ```

    3.  Open MCP Inspector by going to the following URL: [http://localhost:6274/?transport=streamable-http&serverUrl=https://\<mcp_gateway_host\>/mcp](http://localhost:6274/?transport=streamable-http&serverUrl=https://<mcp_gateway_host>/mcp).

        Replace `<mcp_gateway_host>` with the fully qualified domain name of your MCP gateway

2.  To stop the services later, run the following command:

    ``` terminal
    $ kill $INSPECTOR_PID
    ```

3.  Authenticate using a user account configured with the required role claims in your identity provider.

4.  Try the following allowed tools:

    - `pods_list`

    - `events_list`

    - `nodes_list`

    - `deployments_get`

5.  Try this restricted tool: `pods_delete`

    Since this tool is restricted, you should get a 403 Forbidden error.

6.  Monitor authorization decisions:

    1.  Check the AuthPolicy status by running the following command:

        ``` terminal
        $ oc get authpolicy -A
        ```

    2.  View the authorization logs by running the following command:

        ``` terminal
        $ oc logs -n kuadrant-system -l authorino-resource=authorino
        ```

</div>

## Configuring MCP server authentication to the cluster

Configure how the MCP server for Red Hat OpenShift authenticates to the OpenShift Container Platform API server by passing the user’s token through or exchanging it for a token the cluster accepts, so that requests run with the user’s identity.

There are two methods:

- *Passthrough* (default): the server forwards the user’s token directly to the cluster. Used when the cluster accepts the user’s token as-is.

  `cluster_auth_mode` = "passthrough"

  This is the default when `cluster_auth_mode` is unset.

- *Token exchange*: the server exchanges the token for one the cluster accepts (audience mismatch), preserving per-user identity. Exchange happens within passthrough when a \[token_exchange\] block is present.

<div>

<div class="title">

Prerequisites

</div>

- Access to OpenShift console with admin rights.

- MCP gateway is installed.

- MCP Lifecycle Operator is enabled.

- The MCP server is installed.

- MCP gateway is configured and verified.

- MCP-compatible client connected.

- RBAC is configured.

- You have revoked access to specific Custom Resources (CRs) as needed.

- MCP gateway authentication is configured.

- For passthrough: the cluster trusts the IdP as an external OIDC provider.

</div>

<div>

<div class="title">

Procedure

</div>

- To set up passthrough token exchange, add the following content to the `config.toml` `ConfigMap`:

  ``` toml
  Keycloak (RFC 8693):
  [token_exchange]
  strategy = "rfc8693"
  audience = "openshift"
  scopes = ["mcp:openshift"]

  [token_exchange.client_auth]
  method = "client_secret_basic"
  client_id = "mcp-server"
  client_secret = "<client_secret>"
  Entra (On-Behalf-Of):
  [Token_exchange]
  strategy = "entra-obo"
  scopes = ["api://<downstream_api_app_id>/.default"]

  [token_exchange.client_auth]
  method = "private_key_jwt"   # certificate (recommended)
  client_id = "<client_id>"
  certificate_file = "/path/to/client.crt"
  private_key_file = "/path/to/client.key"
  ```

  > [!NOTE]
  > While `[token_exchange]` and `oauth_*/require_oauth` are reloadable, changes to the configuration do not take effect automatically. For information about how to apply configuration changes, see "Applying configuration changes to the MCP server for Red Hat OpenShift".

</div>

<div>

<div class="title">

Verification

</div>

- Confirm the server reaches the cluster API as the user, for example, a tool call that needs cluster access succeeds, or check the server logs for the auth mode/exchange.

</div>

<div>

<div class="title">

Additional resources

</div>

- [Applying configuration changes to the MCP server for Red Hat OpenShift](../../ai_applications/mcp_server/mcp-server-overview.xml#ai-app-mcp-server-apply-config-changes_mcp-server-overview)

</div>

# MCP server for Red Hat OpenShift prompting

Use Model Context Protocol (MCP) server prompts to query a Large Language Model (LLM) to identify and diagnose issues across your OpenShift Container Platform cluster.

> [!NOTE]
> To ensure that you get the best results when prompting be sure to:
>
> - Specify the namespace.
>
> - For Red Hat Advanced Cluster Management (ACM) for Kubernetes environments, specify the cluster.

## MCP prompts

MCP Prompts are predefined templates that guide AI assistants through specific workflows.

They combine:

- **Structured guidance**: Step-by-step instructions for common tasks

- **Parameterization**: Arguments that customize the prompt for specific contexts

- **Conversation templates**: Preformatted messages that guide the interaction

## Creating custom prompts

Define custom prompts in your `config.toml` file. Code changes and recompilation are not needed.

For information about how to apply configuration changes, see "Applying configuration changes to the MCP server for Red Hat OpenShift".

<div class="formalpara">

<div class="title">

Example custom prompts

</div>

``` toml
[[prompts]]
name = "check-pod-logs"
title = "Check Pod Logs"
description = "Quick way to check pod logs"

[[prompts.arguments]]
name = "pod_name"
description = "Name of the pod"
required = true

[[prompts.arguments]]
name = "namespace"
description = "Namespace of the pod"
required = false

[[prompts.messages]]
role = "user"
content = "Show me the logs for pod {{pod_name}} in {{namespace}}"

[[prompts.messages]]
role = "assistant"
content = "I'll retrieve and analyze the logs for you."
```

</div>

<table>
<caption>Configuration reference</caption>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<thead>
<tr>
<th colspan="2" style="text-align: left;">Prompt Fields</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;"><p>name (required)</p></td>
<td style="text-align: left;"><p>Unique identifier for the prompt</p></td>
</tr>
<tr>
<td style="text-align: left;"><p>title (optional)</p></td>
<td style="text-align: left;"><p>Human-readable display name</p></td>
</tr>
<tr>
<td style="text-align: left;"><p>description (required)</p></td>
<td style="text-align: left;"><p>Brief explanation of what the prompt does</p></td>
</tr>
<tr>
<td style="text-align: left;"><p>arguments (optional)</p></td>
<td style="text-align: left;"><p>List of parameters the prompt accepts</p></td>
</tr>
<tr>
<td style="text-align: left;"><p>messages (required)</p></td>
<td style="text-align: left;"><p>Conversation template with role/content pairs</p></td>
</tr>
<tr>
<td colspan="2" style="text-align: left;"><p>Argument Fields</p></td>
</tr>
<tr>
<td style="text-align: left;"><p>name (required)</p></td>
<td style="text-align: left;"><p>Argument identifier</p></td>
</tr>
<tr>
<td style="text-align: left;"><p>description (optional)</p></td>
<td style="text-align: left;"><p>Explanation of the argument’s purpose</p></td>
</tr>
<tr>
<td style="text-align: left;"><p>required (optional)</p></td>
<td style="text-align: left;"><p>Whether the argument must be provided (default: false)</p></td>
</tr>
<tr>
<td colspan="2" style="text-align: left;"><p>Argument Substitution</p></td>
</tr>
<tr>
<td colspan="2" style="text-align: left;"><p>Use {{argument_name}} placeholders in message content. The template engine replaces these with actual values when the prompt is called. If an optional argument is not provided, its placeholder is removed from the output.</p></td>
</tr>
</tbody>
</table>

## Built-in prompts

The MCP server for Red Hat OpenShift includes several built-in prompts that are always available:

`Cluster-health-check` performs a comprehensive health assessment of your OpenShift cluster.

Arguments:

- namespace (optional): Limit the health check to a specific namespace. Default: all namespaces.

- check_events (optional): Include recent warning/error events in the analysis. Values: true or false. Default: true.

What it checks:

- **Nodes**: Status and conditions (for example, Ready, MemoryPressure, DiskPressure)

- **Cluster Operators**: Available and degraded status

- **Pods**: Phase, container statuses, restart counts, and common issues (for example, CrashLoopBackOff, ImagePullBackOff)

- **Workload Controllers**: Deployments, StatefulSets, and DaemonSets replica status

- **Persistent Volume Claims**: Binding status

- **Events**: Recent warning and error events from the last hour

Example usage:

``` terminal
Check the health of my cluster
```

Or with specific parameters:

``` terminal
Check the health of namespace production
```

You can also skip event checking for faster results:

``` terminal
Check the health of my cluster without events
```

The prompt gathers comprehensive diagnostic data and presents it to the LLM for analysis, which provides:

- Overall health status (Healthy, Warning, or Critical)

- Critical issues requiring immediate attention

- Warnings and recommendations

- Summary by component

## Configuration file location

Place your prompts in the `config.toml` file used by the MCP server. Specify the config file path by using the `--config flag` when starting the server.

## Toolset prompts

Some toolsets contain prompts and enabling the toolset enables the prompt(s).

## Prompt merging

When both toolset and config prompts exist, config-defined prompts override toolset prompts with the same name. This allows administrators to customize built-in workflows. Prompts with unique names from both sources are available.

<div>

<div class="title">

Additional resources

</div>

- [Applying configuration changes to the MCP server for Red Hat OpenShift](../../ai_applications/mcp_server/mcp-server-overview.xml#ai-app-mcp-server-apply-config-changes_mcp-server-overview)

</div>

# Toolsets for MCP server for Red Hat OpenShift

A toolset is a named group of related capabilities — tools, and sometimes resources and prompts — that the MCP server for Red Hat OpenShift exposes. Agents use the tools in an enabled toolset to perform tasks.

There are two kinds of toolsets:

Core
The default, always-on, toolset that provides Kubernetes primitives (for example, `pods_list`, `pods_exec`). Other toolsets build on top of it.

Optional
These extend the server for specific domains (networking diagnostics, service mesh, and so on). They’re off by default and you enable them explicitly.

## Enabling toolsets

Enable only the toolsets that you need to keep the tool surface manageable while giving agents what they require for specific tasks. Enabling toolsets requires that you list the toolsets that you want in the toolsets setting in `config.toml`; the change is reloadable. However, reloadable does not mean automatic.

For information about how to apply configuration changes, see "Applying configuration changes to the MCP server for Red Hat OpenShift".

Some toolsets also require their own configuration under `[toolset_configs.<name>]`, and some bundle prompts or resources in addition to tools. For more information about enabling a particular toolset, see the "Additional information" column in the "Available toolsets" table.

## Viewing toolset tools

After you enable a toolset, the tools it provides become available to your connected MCP client. To see the available tools, view the tool list in your MCP client, which retrieves it by using the `tools/list` method.

## Available toolsets

<table>
<caption>Available toolsets</caption>
<colgroup>
<col style="width: 16%" />
<col style="width: 50%" />
<col style="width: 16%" />
<col style="width: 16%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;">Name</th>
<th style="text-align: left;">Description</th>
<th style="text-align: left;">Enabled by default</th>
<th style="text-align: left;">Additional information</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;"><p>core</p></td>
<td style="text-align: left;"><p>Kubernetes primitives (such as, <code>pods_list</code>, <code>pods_exec</code>)</p></td>
<td style="text-align: left;"><p>Yes</p></td>
<td style="text-align: left;"></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>ossm</code> (kiali)</p></td>
<td style="text-align: left;"><p>OpenShift Service Mesh/Kiali mesh tools</p>
<p>This toolset allows assistants to query OpenShift Service Mesh information, such as mesh status and traffic graphs, through Kiali from the MCP server for Red Hat OpenShift.</p></td>
<td style="text-align: left;"><p>No</p></td>
<td style="text-align: left;"><p>See "ossm (kiali) toolset".</p></td>
</tr>
<tr>
<td style="text-align: left;"><p>ovn-kubernetes/cni-diagnostics</p></td>
<td style="text-align: left;"><p>OVN/OVS/CNI networking diagnostics</p></td>
<td style="text-align: left;"><p>No</p></td>
<td style="text-align: left;"><p>See "Troubleshooting OVN-Kubernetes with the MCP server".</p></td>
</tr>
<tr>
<td style="text-align: left;"><p>netedge</p></td>
<td style="text-align: left;"><p>Network ingress and DNS (NIDS) troubleshooting</p>
<p>This toolset extends the MCP server for Red Hat OpenShift with read-only, AI-driven diagnostics for Network Ingress and DNS (NIDS) components.</p></td>
<td style="text-align: left;"><p>No</p></td>
<td style="text-align: left;"><p>See "AI-driven networking troubleshooting".</p></td>
</tr>
</tbody>
</table>

<div>

<div class="title">

Additional resources

</div>

- [Applying configuration changes to the MCP server for Red Hat OpenShift](../../ai_applications/mcp_server/mcp-server-overview.xml#ai-app-mcp-server-apply-config-changes_mcp-server-overview)

- [`ossm` (kiali) toolset](../../ai_applications/mcp_server/mcp-server-overview.xml#ai-app-mcp-server-toolsets-ossm_mcp-server-overview)

- [Troubleshooting OVN-Kubernetes with the MCP server](../../networking/ovn_kubernetes_network_provider/troubleshooting-ovn-kubernetes-with-mcp-server.xml#troubleshooting-ovn-kubernetes-with-mcp-server)

- [AI-driven networking troubleshooting](../../networking/ingress_load_balancing/configuring_ingress_cluster_traffic/configuring-ingress-cluster-traffic-ingress-controller.xml#ai-driven-networking-troubleshooting_configuring-ingress-cluster-traffic-ingress-controller)

</div>

## `OSSM` (Service Mesh) toolset

Enable and configure the `ossm` (Kiali) toolset so that an assistant can query a live OpenShift Service Mesh, and optionally change its configuration, by using tools that Kiali already provides.

The assistant does not connect to Kiali directly. It connects to the MCP server for Red Hat OpenShift, and that server calls Kiali with the caller’s token.

Enable the toolset as `ossm`. Tool names use the `ossm_` prefix.

<div>

<div class="title">

Prerequisites

</div>

- The MCP server for Red Hat OpenShift is installed.

- OpenShift Service Mesh is installed, and the MCP server can reach the Kiali route.

- The OpenShift identity that starts the MCP server can list namespaces and read the mesh resources the assistant should see.

</div>

<div>

<div class="title">

Procedure

</div>

1.  To enable the `ossm` toolset, add or update the `config.toml` file to include the `ossm` toolset:

    <div class="formalpara">

    <div class="title">

    Adding `ossm` toolset

    </div>

    ``` toml
    toolsets = ["core", "ossm"]
    ```

    </div>

2.  Configure the `ossm` toolset similar to the following:

    <div class="formalpara">

    <div class="title">

    Adding `ossm` toolset configuration

    </div>

    ``` toml
    [toolset_configs.kiali]
    url = "https://<kiali_route>"
    # insecure = true
    # certificate_authority = "/path/to/ca.crt"
    ```

    </div>

    > [!IMPORTANT]
    > If the table is missing or invalid, the server does not start.

    - The `ossm` toolset reads its settings from `[toolset_configs.kiali]`.

    - `url` is required.

      Use an `http://` or `https://` URL that includes a host. When `url` is `https://` and `insecure` is `false`, set `certificate_authority` to the CA file for the Kiali certificate. A relative CA path is resolved from the directory that contains the TOML file.

    - Outside production, `insecure = true` skips certificate verification.

    - `read_only = true` (default) hides `ossm_manage_istio_config`:

      To set the assistant’s permission to create, update, or delete the mesh configuration:

      - *Not allowed*: set `read_only` = `true`.

      - *Is allowed*: leave `read_only` unset, or set it to `false`.

        For information about how to apply configuration changes, see "Applying configuration changes to the MCP server for Red Hat OpenShift".

3.  Bind the caller’s identity to the operator-provided `kiali-viewer` (read) or `kiali` (read/write) `ClusterRole`.

    The server uses your existing Kubernetes credentials (from `kubeconfig` or in-cluster) to set a bearer token for Kiali calls. An HTTP Authorization header passed to the MCP HTTP endpoint is not required for Kiali; Kiali calls use the server’s configured token.

    Kiali enforces access with that token (namespace get/list and, for writes and logs, resource RBAC). Tools advertise this as RBAC metadata:

    - Bounded for tools whose Kubernetes checks are derivable from arguments or a finite kind enum (logs, resource details, Istio config read/write, metrics/traces namespace gate, traffic graph). On OpenShift Container Platform, resource/graph declarations also include `deploymentconfigs` and `routes` from the operator’s viewer role.

    - Unbounded for mesh-wide status and mesh cluster listing, where Kiali aggregates control-plane and observability backends that cannot be expressed as a finite Kubernetes requirement set.

4.  Optional: Set up multi-cluster support.

    Kiali can manage multiple clusters within an Istio service mesh. Most Kiali tools accept an optional `meshCluster` parameter to target a specific mesh cluster. When a tool does not name a cluster, Kiali uses the home cluster, which is the cluster where Kiali runs.

    To discover available mesh cluster names before calling other tools, use `ossm_list_mesh_clusters`. The name field from that response is the only valid value for `meshCluster`.

    `ossm` tools do not take an OpenShift `context`. Use the mesh cluster name from `ossm_list_mesh_clusters`. Core tools on the same MCP server still use `context` when multi-cluster mode is enabled.

</div>

<div>

<div class="title">

Additional resources

</div>

- [Applying configuration changes to the MCP server for Red Hat OpenShift](../../ai_applications/mcp_server/mcp-server-overview.xml#ai-app-mcp-server-apply-config-changes_mcp-server-overview)

</div>

## Toolset tools list

Each toolset in the MCP server for Red Hat OpenShift provides a set of tools that assistants call to perform tasks. These tables list the tools in each toolset and describe what each tool does.

Each tool name is shown as the assistant calls it.

<table>
<caption><code>ossm</code> tools</caption>
<colgroup>
<col style="width: 33%" />
<col style="width: 66%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;">Name</th>
<th style="text-align: left;">What it does</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;"><p><code>ossm_get_logs</code></p></td>
<td style="text-align: left;"><p>Returns logs for a pod or workload in a namespace.</p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>ossm_get_mesh_status</code></p></td>
<td style="text-align: left;"><p>Returns mesh health, including the control plane, data plane, observability backends, and how those components connect.</p>
<p>Use this first when you need a mesh-wide view.</p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>ossm_get_mesh_traffic_graph</code></p></td>
<td style="text-align: left;"><p>Returns service-to-service traffic, dependencies, and network metrics, such as throughput, response time, and mTLS.</p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>ossm_get_metrics</code></p></td>
<td style="text-align: left;"><p>Returns latency, traffic, throughput, and payload metrics for a service, workload, or application.</p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>ossm_get_pod_performance</code></p></td>
<td style="text-align: left;"><p>Compares a pod’s current CPU and memory use with its requests and limits.</p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>ossm_get_resource_details</code></p></td>
<td style="text-align: left;"><p>Lists applications, services, workloads, namespaces, or Argo CD applications, or returns details for one resource.</p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>ossm_get_trace_details</code></p></td>
<td style="text-align: left;"><p>Returns the call hierarchy of one distributed trace.</p>
<p>Use it after <code>ossm_list_traces</code>.</p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>ossm_list_mesh_clusters</code></p></td>
<td style="text-align: left;"><p>Lists the mesh clusters Kiali can access, and identifies the home cluster where Kiali runs.</p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>ossm_list_traces</code></p></td>
<td style="text-align: left;"><p>Lists distributed traces for a service.</p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>ossm_manage_istio_config</code></p></td>
<td style="text-align: left;"><p>Creates, updates, or deletes service mesh configuration, including Istio, Gateway API, and Inference API resources.</p>
<p>This tool is hidden when the server is read-only.</p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>ossm_manage_istio_config_read</code></p></td>
<td style="text-align: left;"><p>Lists service mesh configuration or returns one resource.</p>
<p>Valid and invalid objects are reported separately.</p></td>
</tr>
</tbody>
</table>

## Troubleshooting toolsets

Diagnose and resolve common problems that can occur when you enable and configure toolsets in MCP server for Red Hat OpenShift.

Use the following table to troubleshoot the `ossm` toolset.

<table>
<caption>Troubleshooting the <code>ossm</code> toolset</caption>
<colgroup>
<col style="width: 25%" />
<col style="width: 75%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;">Issue</th>
<th style="text-align: left;">Resolution</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;"><p>Missing Kiali configuration when the <code>ossm</code> toolset is enabled.</p></td>
<td style="text-align: left;"><p>Set <code>[toolset_configs.kiali].url</code> in <code>config.toml</code>.</p></td>
</tr>
<tr>
<td style="text-align: left;"><p>Invalid URL.</p></td>
<td style="text-align: left;"><p>Ensure <code>[toolset_configs.kiali].url</code> is a valid <code>http(s)://host</code> URL.</p></td>
</tr>
<tr>
<td style="text-align: left;"><p>TLS certificate validation.</p></td>
<td style="text-align: left;"><p>* If <code>[toolset_configs.kiali].url</code> uses HTTPS and <code>[toolset_configs.kiali].insecure</code> is false, you must set <code>[toolset_configs.kiali].certificate_authority</code> with the path to the CA certificate file. Relative paths are resolved relative to the directory containing the config file.</p>
<p>* For non-production environments you can set <code>[toolset_configs.kiali].insecure = true</code> to skip certificate verification.</p></td>
</tr>
<tr>
<td style="text-align: left;"><p>The server does not start after you enable `ossm</p></td>
<td style="text-align: left;"><p>Set <code>[toolset_configs.kiali].url</code>.</p></td>
</tr>
<tr>
<td style="text-align: left;"><p>The URL is rejected.</p></td>
<td style="text-align: left;"><p>Use an <code>http://</code> or <code>https://</code> URL that includes a host.</p></td>
</tr>
<tr>
<td style="text-align: left;"><p>HTTPS fails certificate verification.</p></td>
<td style="text-align: left;"><p>Set <code>certificate_authority</code> to the CA file, or, outside production, set <code>insecure = true</code>.</p></td>
</tr>
<tr>
<td style="text-align: left;"><p>A tool returns no data or an authorization error.</p></td>
<td style="text-align: left;"><p>The token presented to Kiali cannot read that namespace or resource. Bind the identity to <code>kiali-viewer</code> or <code>kiali</code>.</p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>ossm_manage_istio_config</code> is not offered.</p></td>
<td style="text-align: left;"><p>The server is running with <code>read_only = true</code>.</p></td>
</tr>
</tbody>
</table>

# Upgrading the MCP server and monitoring the rollout

To upgrade the Model Context Protocol (MCP) server, update the container image reference in the `MCPServer` custom resource (CR). The MCP Lifecycle Operator then rolls out the new server version and reports progress through the CR status conditions.

> [!NOTE]
> To use Transport Layer Security (TLS) features, you must also be running the corresponding version of the MCP Lifecycle Operator. Upgrade the Lifecycle Operator before you update the server image in the `MCPServer` CR.

Upgrading also supports the new version of the MCP specification, cleans up and improves various toolsets, allows for running the metrics endpoint on a separate port, and makes improvements to the auth/tokenexchange flows.

<div>

<div class="title">

Prerequisites

</div>

- The MCP Lifecycle Operator is installed and, if you require TLS features, upgraded to the version that supports them. See "Enable MCP server lifecycle management" (Red Hat OpenShift AI documentation).

</div>

<div>

<div class="title">

Procedure

</div>

1.  Edit the `MCPServer` CR to point to the new server image:

    ``` yaml
    apiVersion: mcp.openshift.io/v1alpha1
    kind: MCPServer
    metadata:
        name: openshift-mcp-server
    spec:
        source:
            containerImage:
                ref: <new_image_reference>
    ```

    - `spec.source.containerImage.ref`: The container image reference for the target MCP server version, for example `registry.redhat.io/openshift-mcp/openshift-mcp-server-rhel9:495310209578a754f3383016486fa8f611de7452`.

2.  Apply the change by running the following command:

    ``` terminal
    $ oc apply -f mcpserver.yaml
    ```

</div>

<div>

<div class="title">

Verification

</div>

- Monitor the rollout by running the following command:

  ``` terminal
  $ oc get mcpserver openshift-mcp-server -o yaml
  ```

  `status.conditions` should progress through `Accepted`, indicating that the configuration is valid, then `Available` indicating that the deployment is running, but no handshake yet, and finally when `Verified` is true, the protocol handshake succeeded, and the MCP server is functional again.

</div>

<div>

<div class="title">

Additional resources

</div>

- [Enable MCP server lifecycle management (Red Hat OpenShift AI documentation)](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.5/html/working_with_the_mcp_catalog/enabling-mcp-lifecycle-management)

</div>

# Using metrics to monitor the MCP server for Red Hat OpenShift

The MCP server for Red Hat OpenShift exposes metrics that you can collect with OpenTelemetry Protocol (OTLP) export or Prometheus to monitor server health, request rates, and toolset activity.

| Mechanism | Direction | Method | Endpoint/config |
|----|----|----|----|
| OTLP export | Push | Server pushes metrics every 30 seconds to a configured OTLP endpoint | `[telemetry]` in `config.toml` |
| Prometheus | Pull | Prometheus scrapes the server | `/metrics` endpoint and ServiceMonitor |

Available metric capturing methods

> [!NOTE]
> The MCP server also exposes a Prometheus-compatible `/metrics` endpoint in OpenMetrics format on its HTTP port. If you prefer pull-based collection, create a ServiceMonitor that targets the server’s metrics port. Use the labels:
>
> - app: `mcp-server` and `mcp-server`: `<name of MCP server in the MCPServer CR>`
>
> - port: `mcp`
>
> For more information, see "About OpenShift Container Platform monitoring".

| Metric | Type | Description |
|----|----|----|
| `k8s_mcp_tool_calls_total` | Counter | Total MCP tool calls (labeled by `tool_name`) |
| `k8s_mcp_tool_errors_total` | Counter | Total MCP tool errors (labeled by `tool_name`) |
| `k8s_mcp_tool_duration_seconds` | Histogram | Tool call duration in seconds |
| `k8s_mcp_http_requests_total` | Counter | HTTP requests (labeled by `method`/`path`/`status` class) |
| `k8s_mcp_server_info` | Gauge | Server info (labeled by version, `go_version`) |

Available metrics

<div>

<div class="title">

Prerequisites

</div>

- MCP server for Red Hat OpenShift is installed and running.

</div>

<div>

<div class="title">

Procedure

</div>

1.  In the MCP server `config.toml` file, add a `[telemetry]` section that sets the OTLP endpoint and transport protocol as per the following example:

    ``` toml
    [telemetry]
    endpoint = "http://<otlp_endpoint>:4317"
    protocol = "grpc"
    ```

    - `endpoint`: The URL of your OTLP backend. Telemetry is enabled automatically when you set `endpoint`.

    - `protocol`: Either `grpc` (the default, on port 4317) or `http/protobuf` (on port 4318). Set the port to match the protocol.

2.  Optional: For a secure (TLS) endpoint, use an https:// URL and, for a self-signed CA, provide the CA certificate.

3.  Apply the updated configuration and restart or redeploy the MCP server so that it loads the new `[telemetry]` settings.

    For information about how to apply configuration changes, see "Applying configuration changes to the MCP server for Red Hat OpenShift".

</div>

<div>

<div class="title">

Verification

</div>

- Confirm that metrics arrive in your OTLP backend. The server exports metrics every 30 seconds, so allow at least that much time before checking.

</div>

<div>

<div class="title">

Additional resources

</div>

- [About OpenShift Container Platform monitoring](../../observability/monitoring/about-ocp-monitoring.xml#about-ocp-monitoring)

- [Applying configuration changes to the MCP server for Red Hat OpenShift](../../ai_applications/mcp_server/mcp-server-overview.xml#ai-app-mcp-server-apply-config-changes_mcp-server-overview)

</div>

# Configuration reference

To configure the MCP server for Red Hat OpenShift, review how the server resolves settings from environment variables and the `config.toml` file, and which configuration options changed in this release.

In the MCP Lifecycle Operator-managed deployment, the server reads configuration from a `config.toml` file that is mounted from a `ConfigMap` (or `Secret` for sensitive values). To change the configuration, edit the `ConfigMap` or `Secret`. Whether a change takes effect without a restart depends on whether the option is reloadable, as listed in the following "Vector changes" table and the "What Requires a Restart" section. Reloadable options apply after you initiate a reload (`SIGHUP`); non-reloadable options require you to restart the server.

For information about how to apply configuration changes, see "Applying configuration changes to the MCP server for Red Hat OpenShift".

The loading precedence for configuration, from highest to lowest, is the environment variable (which is `MCP_CONFIG_PATH`), then the `config.toml` file, and then the default value. Command-line flags are used only for startup (`--config`, `--config-dir`, `--version`), not for runtime configuration.

Note that the environment variable is supported both through `spec.config.env` and `spec.config.envFrom`.

Startup config logging
The server logs the effective config (and where each value came from) at startup.

Removed and renamed config options
Several config options have been removed or renamed in OpenShift Container Platform 5.0 in comparison with 4.22. For a list of which options are removed or renamed, see the following tables.

| Dropped flag | Replacement |
|----|----|
| `--port` | `port` in TOML |
| `--bind-address` | `bind_address` |
| `--metrics-port` | `metrics_port` |
| `--log-level` | `log_level` |
| `--log-file` | `log_file` |
| `--kubeconfig` | `kubeconfig` (\$KUBECONFIG remains client-go fallback when kubeconfig is empty) |
| `--list-output` | `list_output` |
| `--read-only` | `read_only` |
| `--disable-destructive` | `disable_destructive` |
| `--stateless` | `stateless` |
| `--toolsets` | `toolsets` |
| `--cluster-provider` | `cluster_provider_strategy` |
| `--disable-multi-cluster` | `cluster_provider_strategy` = "disabled" |
| `--tls-cert`/`--tls-key` | `tls_cert`/`tls_key` |
| `--require-tls` | `require_tls` |
| Hidden OAuth flags (`--require-oauth`, `--authorization-url`, …​) | matching TOML keys |

Removed CLI flags

| Legacy setting           | Replacement                                 |
|--------------------------|---------------------------------------------|
| token_exchange_strategy  | token_exchange.strategy                     |
| sts_audience             | token_exchange.audience                     |
| sts_scopes               | token_exchange.scopes                       |
| sts_subject_token_type   | token_exchange.subject_token_type           |
| sts_requested_token_type | token_exchange.requested_token_type         |
| sts_client_id            | token_exchange.client_auth.client_id        |
| sts_client_secret        | token_exchange.client_auth.client_secret    |
| sts_auth_style           | token_exchange.client_auth.method           |
| sts_client_cert_file     | token_exchange.client_auth.certificate_file |
| sts_client_key_file      | token_exchange.client_auth.private_key_file |
| sts_federated_token_file | token_exchange.client_auth.token_file       |

Removed/renamed TOML keys

| Legacy name         | New name        |
|---------------------|-----------------|
| K8S_MCP_CONFIG_PATH | MCP_CONFIG_PATH |

Bootstrap env rename

| TOML | Environment | Reload |
|----|----|----|
| `log_level`, `log_file` | — | Yes |
| `port`, `bind_address`, `metrics_port`, `stateless`, `disable_localhost_protection`, `server_instructions`, `apps_enabled` | — | No |
| `list_output` | — | Yes |
| `kubeconfig`, `cluster_provider_strategy` | — | No |
| `cluster_auth_mode`, `denied_resources`, `read_only`, `disable_destructive`, `validation_enabled`, experimental_enable_target_compatibility_tool_filters | — | Yes |
| `toolsets`, `enabled_tools`, `disabled_tools`, `tool_overrides`, `prompts`, `confirmation_*` | — | Yes |
| `tls_cert`, `tls_key`, `require_tls` | — | No |
| `tls_min_version` | `TLS_MIN_VERSION` | No (inbound) |
| `tls_cipher_suites` | `TLS_CIPHER_SUITES` | No (inbound) |
| `http.read_header_timeout` | — | No |
| `http.max_body_bytes`, `http.rate_limit_rps`, `http.rate_limit_burst` | — | Yes |
| `require_oauth`, `oauth_*`, `authorization_url`, `skip_jwt_verification`, `disable_dynamic_client_registration`, `server_url`, `certificate_authority`, `trust_proxy_headers`, `token_exchange.*` | — | Yes |
| `telemetry.*` | matching `OTEL_*` | No |
| `kube_client_qps`, `kube_client_burst` | `KUBE_CLIENT_QPS`, `KUBE_CLIENT_BURST` | No |
| `kubeconfig_debounce_window`, `cluster_state_*`, `workspace_*` | matching \*\_MS | No |
| `toolset_configs` | — | Yes |
| `cluster_provider_configs` | — | No |

Vector changes

<div class="note">

<div class="title">

</div>

- — means that vector is off.

- Reload = yes means a SIGHUP that changes the value takes effect.

- Reload = no means a SIGHUP that would change the value is rejected and the process exits.

</div>

<div>

<div class="title">

Additional resources

</div>

- [What Requires a Restart](https://github.com/containers/kubernetes-mcp-server/blob/main/docs/configuration.md#what-requires-a-restart)

- [Applying configuration changes to the MCP server for Red Hat OpenShift](../../ai_applications/mcp_server/mcp-server-overview.xml#ai-app-mcp-server-apply-config-changes_mcp-server-overview)

</div>

# Applying configuration changes to the MCP server for Red Hat OpenShift

Changes to the MCP server for Red Hat OpenShift configuration do not take effect automatically. After you edit the `ConfigMap` or `Secret`, reload the server to apply reloadable options, or restart it to apply non-reloadable options.

<div>

<div class="title">

Prerequisites

</div>

- The MCP server for Red Hat OpenShift is installed and running.

- You have access to the cluster with the `oc` CLI.

- You have permissions to edit the `ConfigMap` (or `Secret`) and to run `oc exec` on the MCP server pod.

- You know whether the configuration option you are changing is reloadable (see "Configuration reference").

</div>

<div>

<div class="title">

Procedure

</div>

1.  Edit the `ConfigMap` (or `Secret` for sensitive values).

2.  Depending on the option:

    - For *reloadable* options, send `SIGHUP` by running the following command to avoid a restart:

      ``` terminal
      oc exec [-n <namespace>] <mcp-server-pod-name> -- kill -HUP 1
      ```

      `<namespace>` is the namespace for the MCP server, and `<mcp-server-pod-name>` is the MCP server pod.

      > [!IMPORTANT]
      > If the new configuration is invalid, the reload fails and the process exits. Ensure that your configuration is valid to avoid a restart of the pod.

    - For *non-reloadable* options, restart or redeploy.

</div>

<div class="formalpara">

<div class="title">

Verification

</div>

After a reload, the server logs its effective configuration, so you can confirm the change loaded by checking the server logs.

</div>
