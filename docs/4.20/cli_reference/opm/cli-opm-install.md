# About the opm CLI

The `opm` CLI tool is provided by the Operator Framework for use with the Operator bundle format. This tool allows you to create and maintain catalogs of Operators from a list of Operator bundles that are similar to software repositories. The result is a container image which can be stored in a container registry and then installed on a cluster.

A catalog contains a database of pointers to Operator manifest content that can be queried through an included API that is served when the container image is run. On OpenShift Container Platform, Operator Lifecycle Manager (OLM) can reference the image in a catalog source, defined by a `CatalogSource` object, which polls the image at regular intervals to enable frequent updates to installed Operators on the cluster.

- See [Operator Framework packaging format](../../operators/understanding/olm-packaging-format.xml#olm-bundle-format_olm-packaging-format) for more information about the bundle format.

# Installing the opm CLI

You can install the `opm` CLI tool on your Linux, macOS, or Windows workstation.

- For Red Hat Enterprise Linux (RHEL) 9.0 and later, you must provide the following packages:

  - `podman` version 1.9.3+ (version 2.0+ recommended)

  - `glibc` version 2.28+

1.  Navigate to the [OpenShift mirror site](https://mirror.openshift.com/pub/openshift-v4/x86_64/clients/ocp/latest-4.17/) and download the latest version of the tarball that matches your operating system.

2.  Unpack the archive.

    - For Linux or macOS:

      ``` terminal
      $ tar xvf <file>
      ```

    - For Windows, unzip the archive with a ZIP program.

3.  Place the file anywhere in your `PATH`.

    - For Linux or macOS:

      1.  Check your `PATH`:

          ``` terminal
          $ echo $PATH
          ```

      2.  Move the file. For example:

          ``` terminal
          $ sudo mv ./opm /usr/local/bin/
          ```

    - For Windows:

      1.  Check your `PATH`:

          ``` terminal
          C:\> path
          ```

      2.  Move the file:

          ``` terminal
          C:\> move opm.exe <directory>
          ```

- After you install the `opm` CLI, verify that it is available:

  ``` terminal
  $ opm version
  ```

# Additional resources

- See [Managing custom catalogs](../../operators/admin/olm-managing-custom-catalogs.xml#olm-managing-custom-catalogs) for `opm` procedures including creating, updating, and pruning catalogs.
