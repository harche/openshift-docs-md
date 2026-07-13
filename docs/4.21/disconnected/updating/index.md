You can update a OpenShift Container Platform cluster in a disconnected environment where the cluster nodes cannot access the internet or where you want to manage update recommendations and release images locally for policy or performance purposes.

# Mirroring OpenShift Container Platform images

You can mirror OpenShift Container Platform images to a local container image registry to provide your disconnected cluster with the resources necessary for targeted updates. A single container image registry is sufficient to host mirrored images for several clusters in the disconnected network.

For more information about mirroring images onto a repository in your disconnected cluster, see the "Mirroring OpenShift Container Platform images" section.

- [Mirroring OpenShift Container Platform images](../../disconnected/updating/mirroring-image-repository.xml#mirroring-ocp-image-repository)

# Performing a cluster update in a disconnected environment

You can keep your disconnected OpenShift Container Platform environment up to date by performing a cluster update. This process can be managed locally either with or without the OpenShift Update Service (OSUS).

For more information about performing a cluster update in a disconnected environment with OSUS, see the "Updating a cluster in a disconnected environment using the OpenShift Update Service" section.

For more information about performing a cluster update in a disconnected environment without OSUS, see the "Updating a cluster in a disconnected environment without the OpenShift Update Service" section.

- [Updating a cluster in a disconnected environment using the OpenShift Update Service](../../disconnected/updating/disconnected-update-osus.xml#updating-disconnected-cluster-osus)

- [Updating a cluster in a disconnected environment without the OpenShift Update Service](../../disconnected/updating/disconnected-update.xml#updating-disconnected-cluster)

# Uninstalling the OpenShift Update Service from a cluster

You can uninstall a local copy of the OpenShift Update Service (OSUS) from your OpenShift Container Platform cluster when you no longer need to manage updates locally:

For more information about uninstalling the OpenShift Update Service from a cluster, see the "Uninstalling the OpenShift Update Service from a cluster" section.

- [Uninstalling the OpenShift Update Service from a cluster](../../disconnected/updating/uninstalling-osus.xml#uninstalling-osus)
