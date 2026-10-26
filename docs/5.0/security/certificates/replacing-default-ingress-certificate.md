To allow external clients to connect securely to applications under the .apps subdomain in OpenShift Container Platform, you can replace the default wildcard ingress certificate with one issued by a trusted public CA.

# Understand the default ingress certificate

You can replace the default ingress certificate with a certificate from a public CA so that external clients connect securely to your applications.

The default ingress certificate in OpenShift Container Platform is a wildcard certificate that the Ingress Operator issues from an internal CA for the web console, CLI, and applications under the `.apps` subdomain.

# Ingress certificate renewal and rotation

After you replace the default ingress certificate, you need to renew or rotate it before it expires.

The Ingress Controller reads the certificate and key from a secret you created. When you renew the certificate, external certificate management tools or the cert-manager Operator replace the certificate and key contents inside that secret without changing the secret name.

Each node runs an agent called `kubelet`, which monitors secrets that pods on that node use. When the `kubelet` detects that the contents of the certificate secret changed, it updates the certificate files on the node. The Ingress Controller router pods on that node read these certificate files, detect the changes, and load the new certificate and key without restarting.

Because the router pods load the new certificate without restarting, OpenShift Container Platform doesn’t roll out a new router deployment. This automatic reload happens whether you manage certificates manually or use the cert-manager Operator to rotate them automatically.

# Replace the default ingress certificate

To secure the web console, CLI, and all applications under the `.apps` subdomain in OpenShift Container Platform, you can replace the default ingress certificate by creating a Transport Layer Security (TLS) secret with your wildcard certificate and updating the Ingress Controller and cluster proxy configuration.

> [!IMPORTANT]
> Replacing the default ingress certificate does not change the web console route certificate. To support HTTP/2, the Console Operator creates a self-signed certificate for the console route, so browsers still show certificate warnings. To use a trusted certificate, set the console route certificate in the `spec.componentRoutes` field to your custom certificate. For more information, see "Customizing the console route."

<div>

<div class="title">

Prerequisites

</div>

- You must have a wildcard certificate for the fully qualified `.apps` subdomain and its corresponding private key. Each should be in a separate PEM format file.

- The private key must be unencrypted. If your key is encrypted, decrypt it before importing it into OpenShift Container Platform.

- The certificate must include the `subjectAltName` extension showing `*.apps.<clustername>.<domain>`.

- The certificate file can contain one or more certificates in a chain. The file must list the wildcard certificate as the first certificate, followed by other intermediate certificates, and then ending with the root certificate authority (CA) certificate.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Copy the root CA certificate into an additional PEM format file.

2.  Create a config map that includes only the root CA certificate that signs the wildcard certificate:

    ``` terminal
    $ oc create configmap custom-ca \
         --from-file=ca-bundle.crt=</path/to/example-ca.crt> \
         -n openshift-config
    ```

    where:

    `</path/to/example-ca.crt>`
    specifies the path to the root CA certificate file on your local file system. For example, `/etc/pki/ca-trust/source/anchors`.

3.  Update the cluster-wide proxy configuration with the new config map:

    ``` terminal
    $ oc patch proxy/cluster \
         --type=merge \
         --patch='{"spec":{"trustedCA":{"name":"custom-ca"}}}'
    ```

    > [!NOTE]
    > If you update only the trusted CA for your cluster, the MCO updates the `/etc/pki/ca-trust/source/anchors/openshift-config-user-ca-bundle.crt` file. The Machine Config Controller (MCC) applies the trusted CA update to each node so that a node reboot is not required. However, with these changes, the Machine Config Daemon (MCD) restarts critical services on each node, such as kubelet and CRI-O (Container Runtime Interface for Open Container Initiative). These service restarts cause each node to briefly enter the `NotReady` state until the service is fully restarted.
    >
    > If you change any other parameter in the `openshift-config-user-ca-bundle.crt` file, such as `noproxy`, the MCO reboots each node in your cluster.

4.  Verify that all certificates that include `-----END CERTIFICATE-----` also end with one carriage return after that line.

5.  Create a secret that contains the wildcard certificate chain and key:

    ``` terminal
    $ oc create secret tls <secret> \
         --cert=</path/to/cert.crt> \
         --key=</path/to/cert.key> \
         -n openshift-ingress
    ```

    where:

    `<secret>`
    specifies the name of the secret that will contain the certificate chain and private key.

    `</path/to/cert.crt>`
    specifies the path to the certificate chain on your local file system.

    `</path/to/cert.key>`
    specifies the path to the private key associated with this certificate.

6.  Update the Ingress Controller configuration with the new secret:

    ``` terminal
    $ oc patch ingresscontroller.operator default \
         --type=merge -p \
         '{"spec":{"defaultCertificate": {"name": "<secret>"}}}' \
         -n openshift-ingress-operator
    ```

    where:

    `<secret>`
    specifies the name of the secret. Replace `<secret>` with the name you used for the secret.

</div>

# Additional resources

- [Ingress certificate renewal and rotation](../../security/certificates/replacing-default-ingress-certificate.xml#ingress-certificate-renewal-rotation_replacing-default-ingress)

- [Customizing the console route](../../web_console/customizing-the-web-console.xml#customizing-the-console-route_customizing-web-console)

- [Replacing the CA Bundle certificate](../../security/certificates/updating-ca-bundle.xml#ca-bundle-understanding_updating-ca-bundle)

- [Proxy certificate customization](../../security/certificate_types_descriptions/proxy-certificates.xml#proxy-cert-customization_proxy-certificates)
