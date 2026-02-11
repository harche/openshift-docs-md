Logging for Red Hat OpenShift collects operations and application logs from your cluster and enriches the data with Kubernetes pod and project metadata. All supported modifications to the log collector are performed though the `spec.collection` stanza in the `ClusterLogForwarder` custom resource (CR).

# Creating a LogFileMetricExporter resource

To generate metrics from the logs produced by running containers, you must create a `LogFileMetricExporter` custom resource (CR).

If you do not create the `LogFileMetricExporter` CR, you might see a **No datapoints found** message in the OpenShift Container Platform web console dashboard for **Produced Logs**.

<div>

<div class="title">

Prerequisites

</div>

- You have administrator permissions.

- You have installed the Red Hat OpenShift Logging Operator.

- You have installed the OpenShift CLI (`oc`).

</div>

<div>

<div class="title">

Procedure

</div>

1.  Create a `LogFileMetricExporter` CR as a YAML file:

    <div class="formalpara">

    <div class="title">

    Example `LogFileMetricExporter` CR

    </div>

    ``` yaml
    apiVersion: logging.openshift.io/v1alpha1
    kind: LogFileMetricExporter
    metadata:
      name: instance
      namespace: openshift-logging
    spec:
      nodeSelector: {}
      resources:
        limits:
          cpu: 500m
          memory: 256Mi
        requests:
          cpu: 200m
          memory: 128Mi
      tolerations: []
    # ...
    ```

    </div>

    - Optional: The `nodeSelector` stanza defines which pods are scheduled on which nodes.

    - The `resources` stanza defines resource requirements for the `LogFileMetricExporter` CR.

    - Optional: The `tolerations` stanza defines the tolerations that the pods accept.

2.  Apply the `LogFileMetricExporter` CR by running the following command:

    ``` terminal
    $ oc apply -f <filename>.yaml
    ```

</div>

# Configure log collector CPU and memory limits

Use the log collector to adjust the CPU and memory limits.

<div>

<div class="title">

Procedure

</div>

- Edit the `ClusterLogForwarder` custom resource (CR):

  ``` terminal
  $ oc -n openshift-logging edit ClusterLogging instance
  ```

  ``` yaml
  apiVersion: observability.openshift.io/v1
  kind: ClusterLogForwarder
  metadata:
    name: instance
    namespace: openshift-logging
  spec:
    collector:
      resources:
        limits:
          memory: 736Mi
        requests:
          cpu: 100m
          memory: 736Mi
  # ...
  ```

  - Specify the CPU and memory limits and requests as needed. The values shown are the default values.

</div>

# Configuring input receivers

The Red Hat OpenShift Logging Operator deploys a service for each configured input receiver so that clients can write to the collector. This service exposes the port specified for the input receiver. For log forwarder `ClusterLogForwarder` CR deployments, the service name is in the `<clusterlogforwarder_resource_name>-<input_name>` format.

## Configuring the collector to receive audit logs as an HTTP server

You can configure your log collector to listen for HTTP connections to only receive audit logs by specifying `http` as a receiver input in the `ClusterLogForwarder` custom resource (CR).

> [!IMPORTANT]
> HTTP receiver input is only supported for the following scenarios:
>
> - Logging is installed on hosted control planes.
>
> - When logs originate from a Red Hat-supported product that is installed on the same cluster as the Red Hat OpenShift Logging Operator. For example:
>
>   - OpenShift Virtualization

<div>

<div class="title">

Prerequisites

</div>

- You have administrator permissions.

- You have installed the OpenShift CLI (`oc`).

- You have installed the Red Hat OpenShift Logging Operator.

- You have created a `ClusterLogForwarder` CR.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Modify the `ClusterLogForwarder` CR to add configuration for the `http` receiver input:

    <div class="formalpara">

    <div class="title">

    Example `ClusterLogForwarder` CR

    </div>

    ``` yaml
    apiVersion: observability.openshift.io/v1
    kind: ClusterLogForwarder
    metadata:
    # ...
    spec:
      inputs:
      - name: http-receiver
        type: receiver
        receiver:
          type: http
          port: 8443
          http:
            format: kubeAPIAudit
      outputs:
      - name: default-lokistack
        lokiStack:
          authentication:
            token:
              from: serviceAccount
          target:
            name: logging-loki
            namespace: openshift-logging
        tls:
          ca:
            key: service-ca.crt
            configMapName: openshift-service-ca.crt
        type: lokiStack
    # ...
      pipelines:
        - name: http-pipeline
          inputRefs:
            - http-receiver
          outputRefs:
            - <output_name>
    # ...
    ```

    </div>

    - Specify a name for your input receiver.

    - Specify the input receiver type as `http`.

    - Optional: Specify the port that the input receiver listens on. This must be a value between `1024` and `65535`. The default value is `8443`.

    - Currently, only the `kube-apiserver` webhook format is supported for `http` input receivers.

    - Configure a pipeline for your input receiver.

2.  Apply the changes to the `ClusterLogForwarder` CR by running the following command:

    ``` terminal
    $ oc apply -f <filename>.yaml
    ```

</div>

<div>

<div class="title">

Verification

</div>

1.  Verify that the collector is listening on the service that has a name in the `<clusterlogforwarder_resource_name>-<input_name>` format by running the following command:

    ``` terminal
    $ oc get svc
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` terminal
    NAME                      TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)            AGE
    collector                 ClusterIP   172.30.85.239    <none>        24231/TCP          3m6s
    collector-http-receiver   ClusterIP   172.30.205.160   <none>        8443/TCP           3m6s
    ```

    </div>

    In this example output, the service name is `collector-http-receiver`.

2.  Extract the certificate authority (CA) certificate file by running the following command:

    ``` terminal
    $ oc extract cm/openshift-service-ca.crt -n <namespace>
    ```

3.  Use the `curl` command to send logs by running the following command:

    ``` terminal
    $ curl --cacert <openshift_service_ca.crt> https://collector-http-receiver.<namespace>.svc:8443 -XPOST -d '{"<prefix>":"<msessage>"}'
    ```

    Replace `<openshift_service_ca.crt>` with the extracted CA certificate file.

    > [!NOTE]
    > You can only forward logs within a cluster by following the verification steps.

</div>

## Configuring the collector to listen for connections as a syslog server

You can configure your log collector to collect journal format infrastructure logs by specifying `syslog` as a receiver input in the `ClusterLogForwarder` custom resource (CR).

> [!IMPORTANT]
> Syslog receiver input is only supported for the following scenarios:
>
> - Logging is installed on hosted control planes.
>
> - When logs originate from a Red Hat-supported product that is installed on the same cluster as the Red Hat OpenShift Logging Operator. For example:
>
>   - Red Hat OpenStack Services on OpenShift (RHOSO)
>
>   - OpenShift Virtualization

<div>

<div class="title">

Prerequisites

</div>

- You have administrator permissions.

- You have installed the OpenShift CLI (`oc`).

- You have installed the Red Hat OpenShift Logging Operator.

- You have created a `ClusterLogForwarder` CR.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Grant the `collect-infrastructure-logs` cluster role to the service account by running the following command:

    <div class="formalpara">

    <div class="title">

    Example binding command

    </div>

    ``` terminal
    $ oc adm policy add-cluster-role-to-user collect-infrastructure-logs -z logcollector
    ```

    </div>

2.  Modify the `ClusterLogForwarder` CR to add configuration for the `syslog` receiver input:

    <div class="formalpara">

    <div class="title">

    Example `ClusterLogForwarder` CR

    </div>

    ``` yaml
    apiVersion: observability.openshift.io/v1
    kind: ClusterLogForwarder
    metadata:
    # ...
    spec:
      serviceAccount:
        name: <service_account_name>
      inputs:
        - name: syslog-receiver
          type: receiver
          receiver:
            type: syslog
            port: 10514
      outputs:
      - name: default-lokistack
        lokiStack:
          authentication:
            token:
              from: serviceAccount
          target:
            name: logging-loki
            namespace: openshift-logging
        tls:
          ca:
            key: service-ca.crt
            configMapName: openshift-service-ca.crt
        type: lokiStack
    # ...
      pipelines:
        - name: syslog-pipeline
          inputRefs:
            - syslog-receiver
          outputRefs:
            - <output_name>
    # ...
    ```

    </div>

    - Specify a name for your input receiver.

    - Specify the input receiver type as `syslog`.

    - Optional: Specify the port that the input receiver listens on. This must be a value between `1024` and `65535`.

    - Configure a pipeline for your input receiver.

3.  Apply the changes to the `ClusterLogForwarder` CR by running the following command:

    ``` terminal
    $ oc apply -f <filename>.yaml
    ```

</div>

<div>

<div class="title">

Verification

</div>

- Verify that the collector is listening on the service that has a name in the `<clusterlogforwarder_resource_name>-<input_name>` format by running the following command:

  ``` terminal
  $ oc get svc
  ```

  <div class="formalpara">

  <div class="title">

  Example output

  </div>

  ``` terminal
  NAME                        TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)            AGE
  collector                   ClusterIP   172.30.85.239    <none>        24231/TCP          33m
  collector-syslog-receiver   ClusterIP   172.30.216.142   <none>        10514/TCP          2m20s
  ```

  </div>

  In this example output, the service name is `collector-syslog-receiver`.

</div>
