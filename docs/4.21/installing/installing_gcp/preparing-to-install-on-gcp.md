Before you install OpenShift Container Platform on Google Cloud, review the requirements, supported methods, and preparation steps to plan your installation.

# Prerequisites

- You reviewed details about the OpenShift Container Platform installation and update processes. For more information, see "Installation and update".

- You read the documentation on selecting a cluster installation method and preparing it for users. For more information, see "Selecting a cluster installation method and preparing it for users".

<!-- -->

- [Installation and update](../../architecture/architecture-installation.xml#architecture-installation)

- [Selecting a cluster installation method and preparing it for users](../../installing/overview/installing-preparing.xml#installing-preparing)

# Requirements for installing OpenShift Container Platform on Google Cloud

Before installing OpenShift Container Platform on Google Cloud, you must create a service account and configure a Google Cloud project by creating a project, enabling API services, configuring DNS, setting Google Cloud account limits, and selecting supported Google Cloud regions. For more information, see "Configuring a Google Cloud project".

If the cloud Identity and Access Management (IAM) APIs are not accessible in your environment, or if you do not want to store an administrator-level credential secret in the `kube-system` namespace, you can configure your cluster to use short-term credentials, manually create long-term credentials, or both. For more information, see "Configuring a Google Cloud cluster to use short-term credentials" and "Manually creating long-term credentials".

- [Configuring a Google Cloud project](../../installing/installing_gcp/installing-gcp-account.xml#installing-gcp-account)

- [Configuring a Google Cloud cluster to use short-term credentials](../../installing/installing_gcp/installing-gcp-customizations.xml#installing-gcp-with-short-term-creds_installing-gcp-customizations)

- [Manually creating long-term credentials](../../installing/installing_gcp/installing-gcp-customizations.xml#manually-create-iam_installing-gcp-customizations)

# Choosing a method to install OpenShift Container Platform on Google Cloud

You can install OpenShift Container Platform on installer-provisioned or user-provisioned infrastructure. The default installation type uses installer-provisioned infrastructure, where the installation program provisions the underlying infrastructure for the cluster. You can also install OpenShift Container Platform on infrastructure that you provision. If you do not use infrastructure that the installation program provisions, you must manage and maintain the cluster resources yourself. For more information about installer-provisioned and user-provisioned installation processes, see "Installation process".

- [Installation process](../../architecture/architecture-installation.xml#installation-process_architecture-installation)

## Installer-provisioned infrastructure installation methods

You can choose from several methods to install a cluster on Google Cloud by using installer-provisioned infrastructure, depending on your network requirements and environment constraints.

You can install a cluster on Google Cloud infrastructure that is provisioned by the OpenShift Container Platform installation program, by using one of the following methods:

- **[Installing a cluster quickly on Google Cloud](../../installing/installing_gcp/installing-gcp-default.xml#installing-gcp-default)**: You can install OpenShift Container Platform on Google Cloud infrastructure that is provisioned by the OpenShift Container Platform installation program. You can install a cluster quickly by using the default configuration options.

- **[Installing a customized cluster on Google Cloud](../../installing/installing_gcp/installing-gcp-customizations.xml#installing-gcp-customizations)**: You can install a customized cluster on Google Cloud infrastructure that the installation program provisions. You can customize your OpenShift Container Platform network configuration during installation, so that your cluster can coexist with your existing IP address allocations and adhere to your network requirements. The installation program allows for some customization to be applied at the installation stage. Many other customization options are available postinstallation.

- **[Installing a cluster on Google Cloud in a restricted network](../../installing/installing_gcp/installing-restricted-networks-gcp-installer-provisioned.xml#installing-restricted-networks-gcp-installer-provisioned)**: You can install OpenShift Container Platform on installer-provisioned infrastructure in Google Cloud by using an internal mirror of the installation release content. You can use this method to install a cluster that does not require an active internet connection to obtain the software components. While you can install OpenShift Container Platform by using the mirrored content, your cluster still requires internet access to use the Google Cloud APIs.

- **[Installing a cluster into an existing Virtual Private Cloud](../../installing/installing_gcp/installing-gcp-vpc.xml#installing-gcp-vpc)**: You can install OpenShift Container Platform on an existing Google Cloud Virtual Private Cloud (VPC). You can use this installation method if you have constraints set by the guidelines of your company, such as limits on creating new accounts or infrastructure.

- **[Installing a private cluster on an existing VPC](../../installing/installing_gcp/installing-gcp-private.xml#installing-gcp-private)**: You can install a private cluster on an existing Google Cloud VPC. You can use this method to deploy OpenShift Container Platform on an internal network that is not visible to the internet.

<!-- -->

- [Postinstallation configuration](../../post_installation_configuration/cluster-tasks.xml#post-install-cluster-tasks)

## User-provisioned infrastructure installation methods

You can choose from several methods to install a cluster on Google Cloud by using infrastructure that you provision, depending on your network requirements and environment constraints.

You can install a cluster on Google Cloud infrastructure that you provision, by using one of the following methods:

- **[Installing a cluster on Google Cloud with user-provisioned infrastructure](../../installing/installing_gcp/installing-gcp-user-infra.xml#installing-gcp-user-infra)**: You can install OpenShift Container Platform on Google Cloud infrastructure that you provide. You can use the provided Infrastructure Manager templates to assist with the installation.

- **[Installing a cluster with shared VPC on user-provisioned infrastructure in Google Cloud](../../installing/installing_gcp/installing-gcp-user-infra-vpc.xml#installing-gcp-user-infra-vpc)**: You can use the provided Infrastructure Manager templates to create Google Cloud resources in a shared VPC infrastructure.

- **[Installing a cluster on Google Cloud in a restricted network with user-provisioned infrastructure](../../installing/installing_gcp/installing-restricted-networks-gcp.xml#installing-restricted-networks-gcp)**: You can install OpenShift Container Platform on Google Cloud in a restricted network with user-provisioned infrastructure. By creating an internal mirror of the installation release content, you can install a cluster that does not require an active internet connection to obtain the software components. You can also use this installation method to ensure that your clusters only use container images that satisfy your organizational controls on external content.
