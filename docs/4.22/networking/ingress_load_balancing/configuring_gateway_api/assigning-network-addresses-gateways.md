You can configure network addresses for your gateway to provide a predictable entry point for external and internal traffic. This ensures that clients can reliably resolve and route requests to your load balancers. Gateway API uses addresses to define the specific network locations that are assigned to your `Gateway` resource.

In OpenShift Container Platform, you rely on the gateway controller to automatically provision and bind the necessary network addresses, such as an external or internal load balancer IP, to your gateway. The controller then populates the `status.addresses` field of the `Gateway` resource with the assigned addresses once they are available.

To successfully assign network addresses to your gateway, complete the following tasks:

- Understand gateway address assignment and types to plan your DNS and load balancer configuration.

- Configure automatic address assignment for a gateway to successfully deploy it without violating manual address constraints.

- Configure an internal load balancer to restrict your gateway traffic to your private network.

- Review cloud provider annotations to ensure your internal load balancer provisions correctly on your specific infrastructure.

# Understand gateway address assignment and types

OpenShift Container Platform automatically handles address assignment by provisioning a `LoadBalancer` service when you create a `Gateway` resource. The network address assigned to your gateway corresponds to the IP address or hostname of this underlying load balancer.

<div class="important">

Do not define the `spec.addresses` field. Manually requesting specific network addresses is not currently supported in OpenShift Container Platform. If you attempt to request a specific address manually, the gateway enters an error state.

The `status.addresses` field is populated automatically by the gateway controller. This field lists the actual, active network address assigned to your gateway by the load balancing infrastructure.

</div>

## Address types

When the controller dynamically assigns an address to your gateway and populates the `status.addresses` field, it uses one of the following primary types to reflect the underlying load balancer:

`Hostname`
Represents a DNS-based ingress point. This concept is typically used for cloud load balancers where a DNS name exposes the load balancer.

`IPAddress`
A textual representation of a numeric IP address (IPv4 or IPv6) assigned by the load balancing infrastructure.

# Configure automatic address assignment for a gateway

When you create a gateway resource, you must configure it for automatic address provisioning to successfully deploy the gateway without violating OpenShift Container Platform manual address constraints. By intentionally omitting the addresses field, you allow the controller to seamlessly provision and bind the necessary external network addresses to your gateway.

- You have access to the cluster as a user with the `cluster-admin` role.

- You have installed the OpenShift CLI (`oc`).

- You have an existing `GatewayClass` resource, such as `openshift-default`.

1.  Create a YAML file, such as `hello-gateway.yaml`, that defines your `Gateway` object without the addresses field:

    ``` yaml
    apiVersion: gateway.networking.k8s.io/v1
    kind: Gateway
    metadata:
      name: sample-gateway
      namespace: openshift-ingress
    spec:
      gatewayClassName: openshift-default
      listeners:
      - name: http
        hostname: "*.gwapi.<cluster_domain>"
        port: 80
        protocol: HTTP
        allowedRoutes:
          namespaces:
            from: All
    ```

    - `metadata.name`: The name of your `Gateway` object. The name must consist of a maximum of 63 lowercase alphanumeric characters or hyphens (`-`). The name must also start and end with an alphanumeric character.

    - Replace `<cluster_domain>` with your actual cluster ingress domain (for example, `example.com`).

    - The `spec.addresses` field is omitted from this configuration to ensure automatic assignment.

    - The `gatewayClassName` dictates which controller provisions the address and populates the `status.addresses` field.

2.  Apply the `Gateway` configuration by running the following command:

    ``` terminal
    $ oc apply -f hello-gateway.yaml
    ```

3.  Verify that the controller automatically assigned an address to your gateway by running the following command:

    ``` terminal
    $ oc -n openshift-ingress get gateway sample-gateway
    ```

    <div class="formalpara-title">

    **Example output**

    </div>

    ``` terminal
    NAME             CLASS               ADDRESS             PROGRAMMED   AGE
    sample-gateway   openshift-default   <gateway_address>   True         6m16s
    ```

    The `ADDRESS` column in the output displays the dynamically provisioned network address for your gateway.

# Configure an internal load balancer for a gateway

By default, Gateway API provisions an external load balancer. To restrict your gateway traffic to your private network, you can configure Gateway API to provision an internal load balancer by adding a cloud-specific annotation to your `Gateway` custom resource (CR).

- You have access to the cluster as a user with the `cluster-admin` role.

- You have installed the OpenShift CLI (`oc`).

- You have configured a `GatewayClass` object.

1.  Create or edit your `Gateway` CR to include the cloud-specific annotation under `spec.infrastructure.annotations`.

    The following example provisions an internal load balancer for an AWS cluster:

    <div class="formalpara-title">

    **Example `Gateway` CR for an AWS internal load balancer**

    </div>

    ``` yaml
    apiVersion: gateway.networking.k8s.io/v1
    kind: Gateway
    metadata:
      name: mygateway
      namespace: openshift-ingress
    spec:
      gatewayClassName: openshift-default
      infrastructure:
        annotations:
        # Specifies the cloud provider annotation and value required to provision an internal load balancer:
          service.beta.kubernetes.io/aws-load-balancer-internal: "true"
      listeners:
      - name: https
        hostname: "*.example.com"
        port: 443
        protocol: HTTPS
        tls:
          mode: Terminate
          certificateRefs:
          - name: gateway-tls-secret
    # ...
    ```

2.  Apply the updated `Gateway` CR by running the following command:

    ``` terminal
    $ oc apply -f <gateway_filename>.yaml
    ```

- Verify that the load balancer service is provisioned and has an internal IP address by running the following command:

  ``` terminal
  $ oc -n openshift-ingress get svc
  ```

## Cloud provider annotations for internal load balancers

To provision an internal load balancer for clusters deployed in private environments, you must add specific annotations to the `spec.infrastructure.annotations` field of your `Gateway` custom resource (CR).

This configuration is supported on Amazon Web Services (AWS), Microsoft Azure, Google Cloud, Red Hat OpenStack Platform (RHOSP), and IBM Cloud. The following table details the required cloud-specific annotations and their corresponding values.

| Cloud Provider                      | Annotation                                                       | Value        |
|-------------------------------------|------------------------------------------------------------------|--------------|
| AWS                                 | `service.beta.kubernetes.io/aws-load-balancer-internal`          | `"true"`     |
| Azure                               | `service.beta.kubernetes.io/azure-load-balancer-internal`        | `"true"`     |
| Google Cloud                        | `cloud.google.com/load-balancer-type`                            | `"Internal"` |
| RHOSP                               | `service.beta.kubernetes.io/openstack-internal-load-balancer`    | `"true"`     |
| IBM Cloud/ IBM Power Virtual Server | `service.kubernetes.io/ibm-load-balancer-cloud-provider-ip-type` | `"private"`  |

Internal load balancer annotations by cloud provider
