Operator Lifecycle Manager (OLM) v1 supports cluster extension lifecycle management in internet-disconnected environments. This feature helps cluster administrators run mission-critical production workloads in high-security, disconnected clusters.

# About disconnected support and the oc-mirror plugin in OLM v1

After you use the oc-mirror plugin for the OpenShift CLI (`oc`) to mirror images to a mirror registry, OLM v1 relies on specific resource sets to function.

Depending on your oc-mirror plugin version, OLM v1 uses one of the following resource sets:

oc-mirror plugin v1
Automatically generates `ImageContentSourcePolicy` resources and requires manually created `ClusterCatalog` resources.

oc-mirror plugin v2
Automatically generates `ImageDigestMirrorSet`, `ImageTagMirrorSet`, and `ClusterCatalog` resources.

<div class="note">

The oc-mirror plugin v2 is the recommended version for mirroring.

</div>

- [Mirroring images for a disconnected installation using the oc-mirror plugin v1](../../disconnected/installing-mirroring-disconnected.xml#installing-mirroring-disconnected)

- [Mirroring images for a disconnected installation using the oc-mirror plugin v2](../../disconnected/about-installing-oc-mirror-v2.xml#about-installing-oc-mirror-v2)
