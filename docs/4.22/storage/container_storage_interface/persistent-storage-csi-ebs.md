# Overview

OpenShift Container Platform is capable of provisioning persistent volumes (PVs) using the [AWS EBS CSI driver](https://github.com/openshift/aws-ebs-csi-driver).

Familiarity with [persistent storage](../../storage/understanding-persistent-storage.xml#understanding-persistent-storage) and [configuring CSI volumes](../../storage/container_storage_interface/persistent-storage-csi.xml#persistent-storage-csi) is recommended when working with a Container Storage Interface (CSI) Operator and driver.

To create CSI-provisioned PVs that mount to AWS EBS storage assets, OpenShift Container Platform installs the [AWS EBS CSI Driver Operator](https://github.com/openshift/aws-ebs-csi-driver-operator) (a Red Hat operator) and the AWS EBS CSI driver by default in the `openshift-cluster-csi-drivers` namespace.

- The *AWS EBS CSI Driver Operator* provides a StorageClass by default that you can use to create PVCs. You can disable this default storage class if desired (see [Managing the default storage class](../../storage/container_storage_interface/persistent-storage-csi-sc-manage.xml#persistent-storage-csi-sc-manage)). You also have the option to create the AWS EBS StorageClass as described in [Persistent storage using Amazon Elastic Block Store](../../storage/persistent_storage/persistent-storage-aws.xml#persistent-storage-aws).

- The *AWS EBS CSI driver* enables you to create and mount AWS EBS PVs.

<div class="note">

If you installed the AWS EBS CSI Operator and driver on an OpenShift Container Platform 4.5 cluster, you must uninstall the 4.5 Operator and driver before you update to OpenShift Container Platform 4.17.

</div>

# About CSI

The Container Storage Interface (CSI) enables storage vendors to deliver plugins through a standard interface without modifying Kubernetes core code, replacing traditional embedded storage drivers.

CSI Operators give OpenShift Container Platform users storage options, such as volume snapshots, that are not possible with in-tree volume plugins.

<div class="important">

OpenShift Container Platform defaults to using the CSI plugin to provision Amazon Elastic Block Store (Amazon EBS) storage.

</div>

For information about dynamically provisioning AWS EBS persistent volumes in OpenShift Container Platform, see [Persistent storage using Amazon Elastic Block Store](../../storage/persistent_storage/persistent-storage-aws.xml#persistent-storage-aws).

# User-managed encryption

The user-managed encryption feature allows you to provide keys during installation that encrypt OpenShift Container Platform node root volumes, and enables all managed storage classes to use these keys to encrypt provisioned storage volumes. You must specify the custom key in the `platform.<cloud_type>.defaultMachinePlatform` field in the install-config YAML file.

This features supports the following storage types:

- Amazon Web Services (AWS) Elastic Block storage (EBS)

- Microsoft Azure Disk storage

- Google Cloud Platform (GCP) persistent disk (PD) storage

- IBM Virtual Private Cloud (VPC) Block storage

<div class="note">

If there is no encrypted key defined in the storage class, only set `encrypted: "true"` in the storage class. The AWS EBS CSI driver uses the AWS managed alias/aws/ebs, which is created by Amazon EBS automatically in each region by default to encrypt provisioned storage volumes. In addition, the managed storage classes all have the `encrypted: "true"` setting.

</div>

For information about installing with user-managed encryption for Amazon EBS, see [Installation configuration parameters](../../installing/installing_aws/ipi/installing-aws-customizations.xml#installation-configuration-parameters_installing-aws-customizations).

# Support for European Sovereign Cloud (EUSC) region

European Sovereign Cloud (EUSC) region acts as a "digital fortress" built within a specific country’s borders. Sovereign Clouds are specifically designed to meet strict legal, jurisdictional, and security requirements of a particular nation or entity.

In the context of storage, EUSC ensures that all data, including primary storage, backups, and the resulting metadata, resides physically within the specific nation’s borders and remains exclusively under its legal jurisdiction.

For OpenShift Container Platform 4.22, and later, only AWS Elastic Block Storage supports EUSC. AWS Elastic File Storage (EFS) is not supported.

<div class="important">

EUSC is a Technology Preview feature only. Technology Preview features are not supported with Red Hat production service level agreements (SLAs) and might not be functionally complete. Red Hat does not recommend using them in production. These features provide early access to upcoming product features, enabling customers to test functionality and provide feedback during the development process.

For more information about the support scope of Red Hat Technology Preview features, see [Technology Preview Features Support Scope](https://access.redhat.com/support/offerings/techpreview/).

</div>

For information about installing an OpenShift Container Platform cluster into the AWS EUSC, see Section *AWS EUSC region* under *Installing*.

- [Persistent storage using Amazon Elastic Block Store](../../storage/persistent_storage/persistent-storage-aws.xml#persistent-storage-aws)

- [Configuring CSI volumes](../../storage/container_storage_interface/persistent-storage-csi.xml#persistent-storage-csi)
