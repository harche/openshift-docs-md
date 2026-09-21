OpenShift Container Platform provides methods for communicating from outside the cluster with services running in the cluster. This method uses load balancers on Amazon Web Services (AWS), specifically a Network Load Balancer (NLB) or a Classic Load Balancer (CLB). Both types of load balancers can forward the IP address of the client to the node, but a CLB requires proxy protocol support, which OpenShift Container Platform automatically enables.

There are two ways to switch an Ingress Controller from using a CLB to using an NLB. Use only one of these approaches for a given Ingress Controller; do not combine them.

1.  Force replace the Ingress Controller that is currently using a CLB. This deletes the `IngressController` object and an outage occurs while the new DNS records propagate and the NLB is being provisioned.

2.  Edit the existing `IngressController` to set `spec.endpointPublishingStrategy.loadBalancer.providerParameters.aws.type` to `NLB`. Starting in OpenShift Container Platform 4.22, the cloud controller does not reprovision the load balancer automatically. The `IngressController` displays a `Progressing` condition stating that you must delete the router `Service` in the `openshift-ingress` namespace so that a new load balancer can be created. That interruption can change the load balancer hostname and IP addresses. Complete the subnets update procedure to read the `Progressing` condition and delete the router `Service`.

You can configure these load balancers on a new or existing AWS cluster.

# Configuring Classic Load Balancer timeouts on AWS

To prevent connection drops for long-running processes in OpenShift Container Platform, configure custom timeout periods for specific routes or Ingress Controllers.

Ensure these settings account for the Amazon Web Services Classic Load Balancer (CLB) default timeout of 60 seconds to maintain stable network traffic.

If the timeout period of the CLB is shorter than the route timeout or Ingress Controller timeout, the load balancer can prematurely terminate the connection. You can prevent this problem by increasing both the timeout period of the route and CLB.

## Configuring route timeouts

You can configure the default timeouts for an existing route when you have services in need of a low timeout, which is required for Service Level Availability (SLA) purposes, or a high timeout, for cases with a slow back end.

<div class="important">

If you configured a user-managed external load balancer in front of your OpenShift Container Platform cluster, ensure that the timeout value for the user-managed external load balancer is higher than the timeout value for the route. This configuration prevents network congestion issues over the network that your cluster uses.

</div>

- You deployed an Ingress Controller on a running cluster.

<!-- -->

- Using the `oc annotate` command, add the timeout to the route:

  ``` terminal
  $ oc annotate route <route_name> \
      --overwrite haproxy.router.openshift.io/timeout=<timeout><time_unit>
  ```

- `<timeout>`: Supported time units are microseconds (us), milliseconds (ms), seconds (s), minutes (m), hours (h), or days (d).

  The following example sets a timeout of two seconds on a route named `myroute`:

  ``` terminal
  $ oc annotate route myroute --overwrite haproxy.router.openshift.io/timeout=2s
  ```

## Configuring Classic Load Balancer timeouts

You can configure the default timeouts for a Classic Load Balancer (CLB) to extend idle connections.

- You must have a deployed Ingress Controller on a running cluster.

1.  Set an Amazon Web Services connection idle timeout of five minutes for the default `ingresscontroller` by running the following command:

    ``` terminal
    $ oc -n openshift-ingress-operator patch ingresscontroller/default \
        --type=merge --patch='{"spec":{"endpointPublishingStrategy": \
        {"type":"LoadBalancerService", "loadBalancer": \
        {"scope":"External", "providerParameters":{"type":"AWS", "aws": \
        {"type":"Classic", "classicLoadBalancer": \
        {"connectionIdleTimeout":"5m"}}}}}}}'
    ```

2.  Optional: Restore the default value of the timeout by running the following command:

    ``` terminal
    $ oc -n openshift-ingress-operator patch ingresscontroller/default \
        --type=merge --patch='{"spec":{"endpointPublishingStrategy": \
        {"loadBalancer":{"providerParameters":{"aws":{"classicLoadBalancer": \
        {"connectionIdleTimeout":null}}}}}}}'
    ```

    <div class="note">

    You must specify the `scope` field when you change the connection timeout value unless the current scope is already set. When you set the `scope` field, you do not need to do so again if you restore the default timeout value.

    </div>

# Configuring ingress cluster traffic on AWS using a Network Load Balancer

To enable high-performance communication between external services and your OpenShift Container Platform cluster, configure an Amazon Web Services Network Load Balancer (NLB). You can set up an NLB on a new or existing AWS cluster to manage ingress traffic with low latency.

# Dual-stack networking for the Ingress Controller load balancer on AWS

On Amazon Web Services, an Ingress Controller must use a publishing `Service` type Network Load Balancer (NLB) to enable publishing over IPv4 and IPv6 when the cluster runs AWS dual-stack networking. A Classic Load Balancer (CLB) does not support the dual-stack publishing path.

<div class="important">

Dual-stack networking for OpenShift Container Platform on Amazon Web Services is a Technology Preview feature only. Technology Preview features are not supported with Red Hat production service level agreements (SLAs) and might not be functionally complete. Red Hat does not recommend using them in production. These features provide early access to upcoming product features, enabling customers to test functionality and provide feedback during the development process.

For more information about the support scope of Red Hat Technology Preview features, see [Technology Preview Features Support Scope](https://access.redhat.com/support/offerings/techpreview/).

</div>

If your Ingress Controller uses an NLB and the cluster-scoped `Infrastructure` resource named `cluster` contains `DualStackIPv4Primary` or `DualStackIPv6Primary` in the `status.platformStatus.aws.ipFamily` field, the Ingress Operator sets the Ingress Controller load balancer `Service` to dual-stack IP families.

The `Service` lists IPv4 first for `DualStackIPv4Primary` and IPv6 first for `DualStackIPv6Primary`.

If the Ingress Controller uses a CLB and the cluster runs AWS dual-stack networking, the publishing load balancer stays IPv4-only. To expose the Ingress Controller over IPv4 and IPv6, you must configure the Ingress Controller to use an NLB.

## Switching the Ingress Controller from using a Classic Load Balancer to a Network Load Balancer

To improve performance and reduce latency for cluster traffic in OpenShift Container Platform on Amazon Web Services, switch an Ingress Controller using a Classic Load Balancer (CLB) to one that uses a Network Load Balancer (NLB).

Switching between these load balancers does not delete the `IngressController` object.

<div class="warning">

This procedure might cause an outage that can last several minutes due to new DNS records propagation, new load balancers provisioning, and other factors. IP addresses and canonical names of the Ingress Controller load balancer might change after applying this procedure.

</div>

1.  Modify the existing Ingress Controller that you want to switch to by using an NLB. This example assumes that your default Ingress Controller has an `External` scope and no other customizations:

    <div class="formalpara-title">

    **Example `ingresscontroller.yaml` file**

    </div>

    ``` yaml
    apiVersion: operator.openshift.io/v1
    kind: IngressController
    metadata:
      creationTimestamp: null
      name: default
      namespace: openshift-ingress-operator
    spec:
      endpointPublishingStrategy:
        loadBalancer:
          scope: External
          providerParameters:
            type: AWS
            aws:
              type: NLB
        type: LoadBalancerService
    ```

    <div class="note">

    If you do not specify a value for the `spec.endpointPublishingStrategy.loadBalancer.providerParameters.aws.type` field, the Ingress Controller uses the `spec.loadBalancer.platform.aws.type` value from the cluster `Ingress` configuration that was set during installation.

    </div>

    <div class="tip">

    If your Ingress Controller has other customizations that you want to update, such as changing the domain, consider force replacing the Ingress Controller definition file instead.

    </div>

2.  Apply the changes to the Ingress Controller YAML file by running the command:

    ``` terminal
    $ oc apply -f ingresscontroller.yaml
    ```

3.  Check that the `Progressing` condition of the Ingress Controller is set to `True` by running the following command:

    ``` terminal
    $ oc get ingresscontroller default -n openshift-ingress-operator -o jsonpath='{.status.conditions[?(@.type=="Progressing")]}'
    ```

4.  Delete the service associated with the Ingress Controller by running the following command:

    ``` terminal
    $ oc -n openshift-ingress delete svc/router-<name>
    ```

    - Replace `<name>` with the specific instance name of your Ingress Controller.

      Expect several minutes of outages while the Ingress Controller updates.

- Confirm that the Ingress Controller updated successfully by running the following command:

  ``` terminal
  $ oc get ingresscontroller -n openshift-ingress-operator default -o jsonpath="{.status.conditions}" | yq -PC
  ```

## Switching the Ingress Controller from using a Network Load Balancer to a Classic Load Balancer

To support specific networking configurations in OpenShift Container Platform on Amazon Web Services, switch an Ingress Controller using a Network Load Balancer (NLB) to one that uses a Classic Load Balancer (CLB).

Switching between these load balancers does not delete the `IngressController` object.

<div class="warning">

This procedure might cause an outage that can last several minutes due to new DNS records propagation, new load balancers provisioning, and other factors. IP addresses and canonical names of the Ingress Controller load balancer might change after applying this procedure.

</div>

1.  Modify the existing Ingress Controller that you want to switch to using a CLB. This example assumes that your default Ingress Controller has an `External` scope and no other customizations:

    <div class="formalpara-title">

    **Example `ingresscontroller.yaml` file**

    </div>

    ``` yaml
    apiVersion: operator.openshift.io/v1
    kind: IngressController
    metadata:
      creationTimestamp: null
      name: default
      namespace: openshift-ingress-operator
    spec:
      endpointPublishingStrategy:
        loadBalancer:
          scope: External
          providerParameters:
            type: AWS
            aws:
              type: Classic
        type: LoadBalancerService
    ```

    <div class="note">

    If you do not specify a value for the `spec.endpointPublishingStrategy.loadBalancer.providerParameters.aws.type` field, the Ingress Controller uses the `spec.loadBalancer.platform.aws.type` value from the cluster `Ingress` configuration that was set during installation.

    </div>

    <div class="tip">

    If your Ingress Controller has other customizations that you want to update, such as changing the domain, consider force replacing the Ingress Controller definition file instead.

    </div>

2.  Apply the changes to the Ingress Controller YAML file by running the command:

    ``` terminal
    $ oc apply -f ingresscontroller.yaml
    ```

3.  Check that the `Progressing` condition of the Ingress Controller is set to `True` by running the following command:

    ``` terminal
    $ oc get ingresscontroller default -n openshift-ingress-operator -o jsonpath='{.status.conditions[?(@.type=="Progressing")]}'
    ```

4.  Delete the service associated with the Ingress Controller by running the following command:

    ``` terminal
    $ oc -n openshift-ingress delete svc/router-<name>
    ```

    - Replace `<name>` with the specific instance name of your Ingress Controller.

      Expect several minutes of outages while the Ingress Controller updates.

- Confirm that the Ingress Controller updated successfully by running the following command:

  ``` terminal
  $ oc get ingresscontroller -n openshift-ingress-operator default -o jsonpath="{.status.conditions}" | yq -PC
  ```

## Replacing Ingress Controller Classic Load Balancer with Network Load Balancer

To improve performance and reduce latency for traffic in OpenShift Container Platform on Amazon Web Services, replace an Ingress Controller using a Classic Load Balancer (CLB) with one that uses a Network Load Balancer (NLB).

<div class="warning">

This procedure might cause an outage that can last several minutes due to new DNS records propagation, new load balancers provisioning, and other factors. IP addresses and canonical names of the Ingress Controller load balancer might change after applying this procedure.

</div>

1.  Create a file with a new default Ingress Controller. The following example assumes that your default Ingress Controller has an `External` scope and no other customizations:

    <div class="formalpara-title">

    **Example `ingresscontroller.yml` file**

    </div>

    ``` yaml
    apiVersion: operator.openshift.io/v1
    kind: IngressController
    metadata:
      creationTimestamp: null
      name: default
      namespace: openshift-ingress-operator
    spec:
      endpointPublishingStrategy:
        loadBalancer:
          scope: External
          providerParameters:
            type: AWS
            aws:
              type: NLB
        type: LoadBalancerService
    ```

    If your default Ingress Controller has other customizations, ensure that you modify the file accordingly.

    <div class="tip">

    If your Ingress Controller has no other customizations and you are only updating the load balancer type, consider following the procedure detailed in "Switching the Ingress Controller from using a Classic Load Balancer to a Network Load Balancer".

    </div>

2.  Force replace the Ingress Controller YAML file:

    ``` terminal
    $ oc replace --force --wait -f ingresscontroller.yml
    ```

    Wait until the Ingress Controller is replaced. Expect several of minutes of outages.

## Configuring an Ingress Controller Network Load Balancer on an existing AWS cluster

To improve performance for high-traffic workloads in OpenShift Container Platform, configure an Ingress Controller backed by an Amazon Web Services Network Load Balancer (NLB) on an existing cluster.

You can create an Ingress Controller backed by an Amazon Web Services Network Load Balancer (NLB) on an existing cluster.

- You installed an AWS cluster.

- `PlatformStatus` of the infrastructure resource must be AWS.

  - To verify that the `PlatformStatus` is AWS, run the following command:

    ``` terminal
    $ oc get infrastructure/cluster -o jsonpath='{.status.platformStatus.type}'
    AWS
    ```

1.  Create the Ingress Controller manifest:

    ``` terminal
     $ cat ingresscontroller-aws-nlb.yaml
    ```

    <div class="formalpara-title">

    **Example output**

    </div>

    ``` yaml
    apiVersion: operator.openshift.io/v1
    kind: IngressController
    metadata:
      name: <ingress_controller_name>
      namespace: openshift-ingress-operator
    spec:
      domain: <unique_ingress_domain
      endpointPublishingStrategy:
        type: LoadBalancerService
        loadBalancer:
          scope: External
          providerParameters:
            type: AWS
            aws:
              type: NLB
    ```

    where:

    `<ingress_controller_name>`
    Specifies a unique name for the Ingress Controller.

    `<unique_ingress_domain>`
    Specifies a domain name that is unique among all Ingress Controllers in the cluster. This variable must be a subdomain of the DNS name `<clustername>.<domain>`.

    `scope`
    Specifies the type of NLB, either `External` to use an external NLB or `Internal` to use an internal NLB.

2.  Create the resource in the cluster:

    ``` terminal
    $ oc create -f ingresscontroller-aws-nlb.yaml
    ```

    <div class="important">

    Before you can configure an Ingress Controller NLB on a new AWS cluster, you must complete the creating the installation configuration file procedure. For more information, see "Creating the installation configuration file".

    </div>

## Configuring an Ingress Controller Network Load Balancer on a new AWS cluster

You can create an Ingress Controller backed by an Amazon Web Services Network Load Balancer (NLB) on a new cluster in situations where you need more transparent networking capabilities.

- Create and edit the `install-config.yaml` file. For instructions, see "Creating the installation configuration file" in the *Additonal resources* section.

1.  Change to the directory that contains the installation program and create the manifests:

    ``` terminal
    $ ./openshift-install create manifests --dir <installation_directory>
    ```

    - For `<installation_directory>`, specify the name of the directory that contains the `install-config.yaml` file for your cluster.

2.  Create a file that is named `cluster-ingress-default-ingresscontroller.yaml` in the `<installation_directory>/manifests/` directory:

    ``` terminal
    $ touch <installation_directory>/manifests/cluster-ingress-default-ingresscontroller.yaml
    ```

    `<installation_directory>`
    Specifies the directory name that contains the `manifests/` directory for your cluster.

3.  Check the several network configuration files that exist in the `manifests/` directory by entering the following command:

    ``` terminal
    $ ls <installation_directory>/manifests/cluster-ingress-default-ingresscontroller.yaml
    ```

    <div class="formalpara-title">

    **Example output**

    </div>

    ``` terminal
    cluster-ingress-default-ingresscontroller.yaml
    ```

4.  Open the `cluster-ingress-default-ingresscontroller.yaml` file in an editor and enter a custom resource (CR) that describes the Operator configuration you want:

    ``` yaml
    apiVersion: operator.openshift.io/v1
    kind: IngressController
    metadata:
      creationTimestamp: null
      name: default
      namespace: openshift-ingress-operator
    spec:
      endpointPublishingStrategy:
        loadBalancer:
          scope: External
          providerParameters:
            type: AWS
            aws:
              type: NLB
        type: LoadBalancerService
    ```

5.  Save the `cluster-ingress-default-ingresscontroller.yaml` file and quit the text editor.

6.  Optional: Back up the `manifests/cluster-ingress-default-ingresscontroller.yaml` file because the installation program deletes the `manifests/` directory during cluster creation.

## Choosing subnets while creating a LoadBalancerService Ingress Controller

To manually control network placement for Ingress Controllers in an existing cluster, specify the load balancer subnets in your configuration. This method provides precise control over your infrastructure by overriding the default automatic subnet discovery method used by Amazon Web Services.

- You must have an installed AWS cluster.

- You must know the names or IDs of the subnets to which you intend to map your `IngressController`.

1.  Create a custom resource (CR) YAML file, such as `sample-ingress.yaml`, and specifying the following content for the file:

    ``` yaml
    apiVersion: operator.openshift.io/v1
    kind: IngressController
    metadata:
      namespace: openshift-ingress-operator
      name: <name>
    spec:
      domain: <domain>
      endpointPublishingStrategy:
        type: LoadBalancerService
        loadBalancer:
          scope: External
      dnsManagementPolicy: Managed
    # ...
    ```

2.  Add subnets to the CR file:

    ``` yaml
    apiVersion: operator.openshift.io/v1
    kind: IngressController
    metadata:
      name:  <name>
      namespace: openshift-ingress-operator
    spec:
      domain: <domain>
      endpointPublishingStrategy:
        type: LoadBalancerService
        loadBalancer:
          scope: External
          providerParameters:
            type: AWS
            aws:
              type: Classic
              classicLoadBalancer:
                subnets:
                  ids:
                  - <subnet>
                  - <subnet>
                  - <subnet>
    dnsManagementPolicy: Managed
    ```

    where:

    `name`
    Specifies a name for the `IngressController`.

    `domain`
    Specifies the DNS name serviced by the `IngressController`.

    `classicLoadBalancer`
    Specifies the type of load balancer, either `classicLoadBalancer` if using a CLB or `networkLoadBalancer` field if using an NLB.

    `ids`
    Specifies a subnet by name using the `names` field instead of specifying the subnet by ID. This field is optional.

    `<subnet>`
    Specifies the subnet IDs (or names if you using `names`).

    <div class="important">

    You can specify a maximum of one subnet per availability zone. Only provide public subnets for external Ingress Controllers and private subnets for internal Ingress Controllers.

    </div>

3.  Save and apply the CR file by using the OpenShift CLI (`oc`):

    ``` terminal
    $  oc apply -f sample-ingress.yaml
    ```

4.  Confirm the load balancer was provisioned successfully by checking the `IngressController` conditions.

    ``` terminal
    $ oc get ingresscontroller -n openshift-ingress-operator <name> -o jsonpath="{.status.conditions}" | yq -PC
    ```

## Updating the subnets on an existing Ingress Controller

You can update an `IngressController` with manually specified load balancer subnets in OpenShift Container Platform to avoid any disruptions, to maintain the stability of your services, and to ensure that your network configuration aligns with your specific requirements.

The example in the procedure shows you how to select and apply new subnets, verify the configuration changes, and confirm successful load balancer provisioning.

<div class="warning">

This procedure may cause an outage that can last several minutes due to new DNS records propagation, new load balancers provisioning, and other factors. IP addresses and canonical names of the Ingress Controller load balancer might change after applying this procedure.

</div>

1.  Modify the existing IngressController by specifying the new subnets:

    ``` yaml
    apiVersion: operator.openshift.io/v1
    kind: IngressController
    metadata:
      name:  <name>
      namespace: openshift-ingress-operator
    spec:
      domain: <domain>
      endpointPublishingStrategy:
        type: LoadBalancerService
        loadBalancer:
          scope: External
          providerParameters:
            type: AWS
            aws:
              type: Classic
              classicLoadBalancer:
                subnets:
                  ids:
                  - <updated_subnet>
                  - <updated_subnet>
                  - <updated_subnet>
    # ...
    ```

    where:

    `<name>`
    Specifies a name for the `IngressController`.

    `<domain>`
    Specifies the DNS name serviced by the `IngressController`.

    `type`
    Specifies the updated subnet IDs (or names if you using `names`).

    `classicLoadBalancer`
    You can also use the `networkLoadBalancer` field if using an NLB.

    `ids`
    Specifies the subnet by name using the `names` field instead of specifying the subnet by ID. This parameter is optional.

    `<updated_subnet>`
    Specifies the updated subnet IDs (or names if you are using `names`).

    <div class="important">

    You can specify a maximum of one subnet per availability zone. Only provide public subnets for external Ingress Controllers and private subnets for internal Ingress Controllers.

    </div>

2.  Examine the `Progressing` condition on the `IngressController` for instructions on how to apply the subnet updates by running the following command:

    ``` terminal
    $ oc get ingresscontroller -n openshift-ingress-operator subnets -o jsonpath="{.status.conditions[?(@.type==\"Progressing\")]}" | yq -PC
    ```

    <div class="formalpara-title">

    **Example output**

    </div>

    ``` terminal
    lastTransitionTime: "2024-11-25T20:19:31Z"
    message: 'One or more status conditions indicate progressing: LoadBalancerProgressing=True (OperandsProgressing: One or more managed resources are progressing: The IngressController subnets were changed from [...] to [...].  To effectuate this change, you must delete the service: `oc -n openshift-ingress delete svc/router-<name>`; the service load-balancer will then be deprovisioned and a new one created. This will most likely cause the new load-balancer to have a different host name and IP address and cause disruption. To return to the previous state, you can revert the change to the IngressController: [...]'
    reason: IngressControllerProgressing
    status: "True"
    type: Progressing
    ```

3.  To apply the update, delete the service associated with the Ingress controller by running the following command:

    ``` terminal
    $ oc -n openshift-ingress delete svc/router-<name>
    ```

- To confirm that the load balancer was provisioned successfully, check the `IngressController` conditions by running the following command:

  ``` terminal
  $ oc get ingresscontroller -n openshift-ingress-operator <name> -o jsonpath="{.status.conditions}" | yq -PC
  ```

## Configuring AWS Elastic IP (EIP) addresses for a Network Load Balancer (NLB)

You can specify static IPs, otherwise known as elastic IPs, for your network load balancer (NLB) in the Ingress Controller. This is useful in situations where you want to configure appropriate firewall rules for your cluster network.

- You must have an installed Amazon Web Services cluster.

- You must know the names or IDs of the subnets to which you intend to map your `IngressController`.

1.  Create a YAML file that contains the following example content:

    ``` yaml
    apiVersion: operator.openshift.io/v1
    kind: IngressController
    metadata:
      namespace: openshift-ingress-operator
      name: <name>
    spec:
      domain: <domain>
      endpointPublishingStrategy:
        loadBalancer:
          scope: External
          type: LoadBalancerService
          providerParameters:
            type: AWS
            aws:
              type: NLB
              networkLoadBalancer:
                subnets:
                  ids:
                  - <subnet_ID>
                  names:
                  - <subnet_A>
                  - <subnet_B>
                eipAllocations:
                - <eipalloc_A>
                - <eipalloc_B>
                - <eipalloc_C>
    ```

    where:

    `<name>`
    Specifies a name for the Ingress Controller.

    `<domain>`
    Specifies the DNS name serviced by the Ingress Controller.

    `scope`
    Specifies a scope for the EIPs. The scope must be set to the value `External` and be Internet-facing in order to allocate EIPs.

    \`subnets
    Specifies the IDs and names for your subnets. The total number of IDs and names must be equal to your allocated EIPs.

    `eipAllocations`
    Specifies the EIP addresses.

    <div class="important">

    You can specify a maximum of one subnet per availability zone. Only provide public subnets for external Ingress Controllers. You can associate one EIP address per subnet.

    </div>

2.  Save and apply the CR file by entering the following command:

    ``` terminal
    $  oc apply -f sample-ingress.yaml
    ```

<!-- -->

1.  Confirm the load balancer was provisioned successfully by checking the `IngressController` conditions by running the following command:

    ``` terminal
    $ oc get ingresscontroller -n openshift-ingress-operator <name> -o jsonpath="{.status.conditions}" | yq -PC
    ```

# BYO security groups for AWS Network Load Balancers

The AWS Cloud Controller Manager (CCM) supports attaching your Bring Your Own (BYO) security groups to Network Load Balancers (NLBs). The NLBs must have been created for Kubernetes `Service` resources of type `LoadBalancer`.

By default, the CCM automatically creates and manages a dedicated security group for each NLB. With BYO security groups, you specify your own security groups so you can access the following capabilities:

- Provides full control over ingress and egress rules.

- Enables advanced use cases such as shared security policies and custom compliance rules.

When a BYO security group annotation is set at NLB creation time, the CCM skips creating a managed security group entirely. The CCM then associates the NLB with the provided custom security groups.

When a BYO security group annotation is attached after the NLB was provisioned with a managed group, the CCM removes the managed security group and replaces it with the requested BYO security groups.

<div class="important">

The CCM does not add, modify, or delete any rules on BYO security groups. You are responsible for configuring BYO security groups correctly according to their use cases.

</div>

Before you provide your BYO security groups to NLBs, read the following considerations:

- For the BYO security group feature to work, you must ensure that `NLBSecurityGroupMode = Managed` is set in the AWS CCM config file. By default, the installation program sets this configuration for a new cluster installation. If the configuration is not set, the CCM cannot manage security groups for AWS NLBs.

- When using BYO security groups, you must take full responsibility for managing all ingress and egress rules according to their use cases and setup. The CCM does not automatically add rules to BYO security groups.

- BYO security groups must be in the same VPC as the NLB.

- You cannot associate BYO security groups to pre-existing NLBs that were created without security groups. This limitation exists for AWS NLBs. To resolve this limitation, you must delete the NLB, recreate it, and configure it to minimize disruption during a cluster upgrade.

The following list details considerations for when upgrading your cluster to OpenShift Container Platform 4.17:

- For Identity and Access Management (IAM) permissions, verify that the IAM role for a control plane node includes the `elasticloadbalancing:SetSecurityGroups` permission. The upgrade operation does not automatically modify IAM policies.

- For existing NLBs with managed security groups, these groups continue to work as expected. The managed security group mode is preserved, and no action is required.

- For existing NLBs without security groups, if NLBs were created before managed security group mode was available, they continue to operate without security groups. To enable BYO or managed security groups on these NLBs, you must delete and recreate the service.

## Creating a service with an NLB by using BYO security groups

To create an NLB with BYO security groups, add the annotation `service.beta.kubernetes.io/aws-load-balancer-security-groups` with one or more security group IDs to the service manifest file.

1.  You checked that the AWS Identity and Access Management (IAM) role for each control plane node of your cluster includes the `elasticloadbalancing:SetSecurityGroups` permission.

    1.  For new clusters installed on installer-provisioned infrastructure, the installation program adds this role to each control plane node.

    2.  For user-provisioned infrastructure, you must add the permission to the IAM role of each control plane. The following configuration adds the permission to the IAM role in a JSON file:

        ``` json
        {
          "Effect": "Allow",
          "Action": [
            "elasticloadbalancing:SetSecurityGroups"
          ],
          "Resource": "*"
        }
        ```

2.  You checked that the NLB security group is enabled in the AWS CCM configuration. For example:

    ``` txt
    [Global]
    NLBSecurityGroupMode = Managed
    ```

3.  To create an NLB with BYO security groups, add the annotation `service.beta.kubernetes.io/aws-load-balancer-security-groups` with one or more security group IDs to the service manifest:

    ``` yaml
    apiVersion: v1
    kind: Service
    metadata:
      name: my-nlb-service
      namespace: my-namespace
      annotations:
        service.beta.kubernetes.io/aws-load-balancer-type: nlb
        service.beta.kubernetes.io/aws-load-balancer-security-groups: "<security_group_id1>,<security_group_id2>"
    spec:
      selector:
        app: my-app
      ports:
        - port: 443
          targetPort: 8443
          protocol: TCP
      type: LoadBalancer
    # ...
    ```

## Switching the management service for security groups

You can switch an existing Network Load Balancer (NLB) from a CCM-managed security group to a Bring Your Own (BYO) security group.

- You have provisioned security groups for your service NLB.

<!-- -->

- To switch from a CCM-managed security group to a BYO security group, complete the following steps.

  - Create your BYO security group in the same VPC as the cluster and configure the appropriate ingress rules.

  - Add the annotation `service.beta.kubernetes.io/aws-load-balancer-security-groups` with one or more security group IDs to the service manifest by entering the following command:

    ``` terminal
    $ oc annotate svc <nlb_service> \
      service.beta.kubernetes.io/aws-load-balancer-security-groups=<security_group_ID>
    ```

    Replace `<nlb_service>` with the name of your service and `<security_group_ID>` with your security group ID.

    <div class="note">

    After you complete the switch operation, the CCM completes the following tasks:

    - Detects the annotation change and updates the NLB security group configuration associating it with the requested BYO security group.

    - Automatically deletes the old managed security group. This happens because the security group is cluster-owned and is no longer needed.

    </div>

## Reverting the management service for security groups

You can revert from a Bring Your Own (BYO) security group back to a CCM-managed security group.

- You have provisioned security groups for your service NLB.

<!-- -->

- To revert from a BYO security group to a CCM-managed security group, remove the annotation from your service by entering the following command:

  ``` terminal
  $ oc annotate svc <nlb_service> \
    service.beta.kubernetes.io/aws-load-balancer-security-groups-
  ```

  Replace `<nlb_service>` with the name of your service.

  <div class="note">

  After you complete the revert operation, the CCM creates and attaches a new managed security group to the NLB. The CCM then detaches the BYO security group from the NLB. The CCM does not delete the BYO security group from your AWS customer account as the group is not a cluster-owned resource. You must manually delete the security group.

  </div>

## Updating BYO security groups

As a postinstallation task, you can add, remove, or swap Bring Your Own (BYO) security groups that are attached to an Network Load Balancer (NLB). This means that you can update ingress and egress rules dynamically and align network access policies across your load balancers.

- To modify BYO security groups, update the annotation value with the new security group IDs by entering the following command:

  ``` terminal
  $ oc annotate svc <nlb_service> \
    service.beta.kubernetes.io/aws-load-balancer-security-groups=<security_group_name> \
    --overwrite
  ```

  Replace `<nlb_service>` with the name of your NLB service and `<security_group_name>` with the name of your security group.

  After the command successfully executes, the CCM detects the change and updates the NLB with the new security groups.

# Additional resources

- [Converting to a dual-stack cluster network](../../../networking/ovn_kubernetes_network_provider/converting-to-dual-stack.xml#nw-dual-stack-convert_converting-to-dual-stack)

- [Enabling features using feature gates](../../../nodes/clusters/nodes-cluster-enabling-features.xml#nodes-cluster-enabling-features)

- [Creating the installation configuration file](../../../installing/installing_aws/ipi/installing-aws-customizations.xml#installation-initializing_installing-aws-customizations)

- [Infrastructure cluster configuration API](../../../rest_api/config_apis/infrastructure-config-openshift-io-v1.xml#infrastructure-config-openshift-io-v1)

- [Installing a cluster on AWS with network customizations](../../../installing/installing_aws/ipi/installing-aws-customizations.xml#installing-aws-customizations)

- [Network Load Balancer support on AWS](https://kubernetes.io/docs/concepts/services-networking/service/#aws-nlb-support)

- [Configure proxy protocol support for your Classic Load Balancer](https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/enable-proxy-protocol.html)
