After installing OpenShift Container Platform, you can further expand and customize your cluster to your requirements, including storage configuration.

By default, containers operate by using the ephemeral storage or transient local storage. The ephemeral storage has a lifetime limitation. To store the data for a long time, you must configure persistent storage. You can configure storage by using one of the following methods:

Dynamic provisioning
You can dynamically provision storage on-demand by defining and creating storage classes that control different levels of storage, including storage access.

Static provisioning
You can use Kubernetes persistent volumes to make existing storage available to a cluster. Static provisioning can support various device configurations and mount options.

# Dynamic provisioning

Dynamic Provisioning allows you to create storage volumes on-demand, eliminating the need for cluster administrators to pre-provision storage. See [Dynamic provisioning](../storage/dynamic-provisioning.xml#dynamic-provisioning).

# Recommended configurable storage technology

The following table summarizes the recommended and configurable storage technologies for the given OpenShift Container Platform cluster application.

| Storage type          | Block            | File                     | Object                       |
|-----------------------|------------------|--------------------------|------------------------------|
| ROX<sup>1</sup>       | Yes<sup>4</sup>  | Yes<sup>4</sup>          | Yes                          |
| RWX<sup>2</sup>       | No               | Yes                      | Yes                          |
| Registry              | Configurable     | Configurable             | Recommended                  |
| Scaled registry       | Not configurable | Configurable             | Recommended                  |
| Metrics<sup>3</sup>   | Recommended      | Configurable<sup>5</sup> | Not configurable             |
| Elasticsearch Logging | Recommended      | Configurable<sup>6</sup> | Not supported<sup>6</sup>    |
| Loki Logging          | Not configurable | Not configurable         | Recommended                  |
| Apps                  | Recommended      | Recommended              | Not configurable<sup>7</sup> |

Recommended and configurable storage technology

<div class="note">

A scaled registry is an OpenShift image registry where two or more pod replicas are running.

</div>

## Specific application storage recommendations

<div class="important">

Testing shows issues with using the NFS server on Red Hat Enterprise Linux (RHEL) as a storage backend for core services. This includes the OpenShift Container Registry and Quay, Prometheus for monitoring storage, and Elasticsearch for logging storage. Therefore, using RHEL NFS to back PVs used by core services is not recommended.

Other NFS implementations in the marketplace might not have these issues. Contact the individual NFS implementation vendor for more information on any testing that was possibly completed against these OpenShift Container Platform core components.

</div>

### Registry

In a non-scaled/high-availability (HA) OpenShift image registry cluster deployment:

- The storage technology does not have to support RWX access mode.

- The storage technology must ensure read-after-write consistency.

- The preferred storage technology is object storage followed by block storage.

- File storage is not recommended for OpenShift image registry cluster deployment with production workloads.

### Scaled registry

In a scaled/HA OpenShift image registry cluster deployment:

- The storage technology must support RWX access mode.

- The storage technology must ensure read-after-write consistency.

- The preferred storage technology is object storage.

- Red Hat OpenShift Data Foundation, Amazon Simple Storage Service (Amazon S3), Google Cloud Storage (GCS), Microsoft Azure Blob Storage, and OpenStack Swift are supported.

- Object storage should be S3 or Swift compliant.

- For non-cloud platforms, such as vSphere and bare metal installations, the only configurable technology is file storage.

- Block storage is not configurable.

- The use of Network File System (NFS) storage with OpenShift Container Platform is supported. However, the use of NFS storage with a scaled registry can cause known issues. For more information, see the Red Hat Knowledgebase solution, [Is NFS supported for OpenShift cluster internal components in Production?](https://access.redhat.com/solutions/3428661).

### Metrics

In an OpenShift Container Platform hosted metrics cluster deployment:

- The preferred storage technology is block storage.

- Object storage is not configurable.

<div class="important">

It is not recommended to use file storage for a hosted metrics cluster deployment with production workloads.

</div>

### Logging

In an OpenShift Container Platform hosted logging cluster deployment:

- Loki Operator:

  - The preferred storage technology is S3 compatible Object storage.

  - Block storage is not configurable.

- OpenShift Elasticsearch Operator:

  - The preferred storage technology is block storage.

  - Object storage is not supported.

<div class="note">

As of logging version 5.4.3 the OpenShift Elasticsearch Operator is deprecated and is planned to be removed in a future release. Red Hat will provide bug fixes and support for this feature during the current release lifecycle, but this feature will no longer receive enhancements and will be removed. As an alternative to using the OpenShift Elasticsearch Operator to manage the default log storage, you can use the Loki Operator.

</div>

### Applications

Application use cases vary from application to application, as described in the following examples:

- Storage technologies that support dynamic PV provisioning have low mount time latencies, and are not tied to nodes to support a healthy cluster.

- Application developers are responsible for knowing and understanding the storage requirements for their application, and how it works with the provided storage to ensure that issues do not occur when an application scales or interacts with the storage layer.

## Other specific application storage recommendations

<div class="important">

It is not recommended to use RAID configurations on `Write` intensive workloads, such as `etcd`. If you are running `etcd` with a RAID configuration, you might be at risk of encountering performance issues with your workloads.

</div>

- Red Hat OpenStack Platform (RHOSP) Cinder: RHOSP Cinder tends to be adept in ROX access mode use cases.

- Databases: Databases (RDBMSs, NoSQL DBs, etc.) tend to perform best with dedicated block storage.

- The etcd database must have enough storage and adequate performance capacity to enable a large cluster. Information about monitoring and benchmarking tools to establish ample storage and a high-performance environment is described in *Recommended etcd practices*.

# Deploy Red Hat OpenShift Data Foundation

Red Hat OpenShift Data Foundation is a provider of agnostic persistent storage for OpenShift Container Platform supporting file, block, and object storage, either in-house or in hybrid clouds. As a Red Hat storage solution, Red Hat OpenShift Data Foundation is completely integrated with OpenShift Container Platform for deployment, management, and monitoring. For more information, see the [Red Hat OpenShift Data Foundation documentation](https://access.redhat.com/documentation/en-us/red_hat_openshift_data_foundation).

<div class="important">

OpenShift Data Foundation on top of Red Hat Hyperconverged Infrastructure (RHHI) for Virtualization, which uses hyperconverged nodes that host virtual machines installed with OpenShift Container Platform, is not a supported configuration. For more information about supported platforms, see the [Red Hat OpenShift Data Foundation Supportability and Interoperability Guide](https://access.redhat.com/articles/4731161).

</div>

| If you are looking for Red Hat OpenShift Data Foundation information about…​                                                             | See the following Red Hat OpenShift Data Foundation documentation:                                                                                                                                                                        |
|-----------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| What’s new, known issues, notable bug fixes, and Technology Previews                                                                    | [OpenShift Data Foundation 4.12 Release Notes](https://access.redhat.com/documentation/en-us/red_hat_openshift_data_foundation/4.12/html/4.12_release_notes)                                                                              |
| Supported workloads, layouts, hardware and software requirements, sizing and scaling recommendations                                    | [Planning your OpenShift Data Foundation 4.12 deployment](https://access.redhat.com/documentation/en-us/red_hat_openshift_data_foundation/4.12/html/planning_your_deployment)                                                             |
| Instructions on deploying OpenShift Data Foundation to use an external Red Hat Ceph Storage cluster                                     | [Deploying OpenShift Data Foundation 4.12 in external mode](https://access.redhat.com/documentation/en-us/red_hat_openshift_data_foundation/4.12/html/deploying_openshift_data_foundation_in_external_mode)                               |
| Instructions on deploying OpenShift Data Foundation to local storage on bare metal infrastructure                                       | [Deploying OpenShift Data Foundation 4.12 using bare metal infrastructure](https://access.redhat.com/documentation/en-us/red_hat_openshift_data_foundation/4.12/html/deploying_openshift_data_foundation_using_bare_metal_infrastructure) |
| Instructions on deploying OpenShift Data Foundation on Red Hat OpenShift Container Platform VMware vSphere clusters                     | [Deploying OpenShift Data Foundation 4.12 on VMware vSphere](https://access.redhat.com/documentation/en-us/red_hat_openshift_data_foundation/4.12/html/deploying_openshift_data_foundation_on_vmware_vsphere)                             |
| Instructions on deploying OpenShift Data Foundation using Amazon Web Services for local or cloud storage                                | [Deploying OpenShift Data Foundation 4.12 using Amazon Web Services](https://access.redhat.com/documentation/en-us/red_hat_openshift_data_foundation/4.12/html/deploying_openshift_data_foundation_using_amazon_web_services)             |
| Instructions on deploying and managing OpenShift Data Foundation on existing Red Hat OpenShift Container Platform Google Cloud clusters | [Deploying and managing OpenShift Data Foundation 4.12 using Google Cloud](https://access.redhat.com/documentation/en-us/red_hat_openshift_data_foundation/4.12/html/deploying_and_managing_openshift_data_foundation_using_google_cloud) |
| Instructions on deploying and managing OpenShift Data Foundation on existing Red Hat OpenShift Container Platform Azure clusters        | [Deploying and managing OpenShift Data Foundation 4.12 using Microsoft Azure](https://access.redhat.com/documentation/en-us/red_hat_openshift_data_foundation/4.12/html/deploying_openshift_data_foundation_using_microsoft_azure/index)  |
| Instructions on deploying OpenShift Data Foundation to use local storage on IBM Power® infrastructure                                   | [Deploying OpenShift Data Foundation on IBM Power®](https://access.redhat.com/documentation/en-us/red_hat_openshift_data_foundation/4.12/html-single/deploying_openshift_data_foundation_using_ibm_power/index)                           |
| Instructions on deploying OpenShift Data Foundation to use local storage on IBM Z® infrastructure                                       | [Deploying OpenShift Data Foundation on IBM Z® infrastructure](https://access.redhat.com/documentation/en-us/red_hat_openshift_data_foundation/4.12/html/deploying_openshift_data_foundation_using_ibm_z_infrastructure/index)            |
| Allocating storage to core services and hosted applications in Red Hat OpenShift Data Foundation, including snapshot and clone          | [Managing and allocating resources](https://access.redhat.com/documentation/en-us/red_hat_openshift_data_foundation/4.12/html/managing_and_allocating_storage_resources)                                                                  |
| Managing storage resources across a hybrid cloud or multicloud environment using the Multicloud Object Gateway (NooBaa)                 | [Managing hybrid and multicloud resources](https://access.redhat.com/documentation/en-us/red_hat_openshift_data_foundation/4.12/html/managing_hybrid_and_multicloud_resources)                                                            |
| Safely replacing storage devices for Red Hat OpenShift Data Foundation                                                                  | [Replacing devices](https://access.redhat.com/documentation/en-us/red_hat_openshift_data_foundation/4.12/html/replacing_devices)                                                                                                          |
| Safely replacing a node in a Red Hat OpenShift Data Foundation cluster                                                                  | [Replacing nodes](https://access.redhat.com/documentation/en-us/red_hat_openshift_data_foundation/4.12/html/replacing_nodes)                                                                                                              |
| Scaling operations in Red Hat OpenShift Data Foundation                                                                                 | [Scaling storage](https://access.redhat.com/documentation/en-us/red_hat_openshift_data_foundation/4.12/html/scaling_storage)                                                                                                              |
| Monitoring a Red Hat OpenShift Data Foundation 4.12 cluster                                                                             | [Monitoring Red Hat OpenShift Data Foundation 4.12](https://access.redhat.com/documentation/en-us/red_hat_openshift_data_foundation/4.12/html/monitoring_openshift_data_foundation)                                                       |
| Resolve issues encountered during operations                                                                                            | [Troubleshooting OpenShift Data Foundation 4.12](https://access.redhat.com/documentation/en-us/red_hat_openshift_data_foundation/4.12/html/troubleshooting_openshift_data_foundation)                                                     |
| Migrating your OpenShift Container Platform cluster from version 3 to version 4                                                         | [Migration](https://access.redhat.com/documentation/en-us/openshift_container_platform/4.12/html/migrating_from_version_3_to_4/index)                                                                                                     |
