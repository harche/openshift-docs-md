The oc-mirror is an OpenShift CLI (`oc`) that mirrors OpenShift Container Platform content and other images to a mirror registry.

These release notes track the development of oc-mirror.

# Release notes for oc-mirror v2 2.0.0

Review new features for oc-mirror v2 2.0.0.

Issued: 27 October 2026

## New features and enhancements

Multi-architecture filtering with sparse manifests
With this release, oc-mirror v2 supports multi-architecture filtering by using sparse manifests. You can add a `platforms` field to your `ImageSetConfiguration` file to mirror only the platforms that your cluster requires. Filtering applies to images in the platform release payload, Operator catalogs, Helm charts, and additional images. This filtering preserves the digest of the original manifest list, so that the image references and signatures remain valid. The `platforms` field replaces the deprecated `architectures` field.

> [!NOTE]
> Your target registry must support sparse manifests.

Image set mirroring by using the OpenShift Mirror Console
With this release, you can build your image sets by using the OpenShift Mirror Console without manually editing YAML files. You build an `ImageSetConfiguration` file that includes platform channels, Operator catalogs, Helm charts, and additional images, and start mirror operations by using that file. In the OpenShift Mirror Console, you can also perform the following tasks:

- Preview, save, or download the `ImageSetConfiguration` file

- Load an existing `ImageSetConfiguration` file

- Synchronize Operator catalog digests

- Review the operation history
