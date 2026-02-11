Config maps allow you to decouple configuration artifacts from image content to keep containerized applications portable.

The following sections define config maps and how to create and use them.

# Understanding config maps

Many applications require configuration by using some combination of configuration files, command-line arguments, and environment variables. In OpenShift Container Platform, these configuration artifacts are decoupled from image content to keep containerized applications portable.

The `ConfigMap` object provides mechanisms to inject containers with configuration data while keeping containers agnostic of OpenShift Container Platform. A config map can be used to store fine-grained information like individual properties or coarse-grained information like entire configuration files or JSON blobs.

The `ConfigMap` object holds key-value pairs of configuration data that can be consumed in pods or used to store configuration data for system components such as controllers. For example:

<div class="formalpara-title">

**`ConfigMap` Object Definition**

</div>

``` yaml
kind: ConfigMap
apiVersion: v1
metadata:
  creationTimestamp: 2016-02-18T19:14:38Z
  name: example-config
  namespace: my-namespace
data:
  example.property.1: hello
  example.property.2: world
  example.property.file: |-
    property.1=value-1
    property.2=value-2
    property.3=value-3
binaryData:
  bar: L3Jvb3QvMTAw
```

- Contains the configuration data.

- Points to a file that contains non-UTF8 data, for example, a binary Java keystore file. Enter the file data in Base 64.

<div class="note">

You can use the `binaryData` field when you create a config map from a binary file, such as an image.

</div>

Configuration data can be consumed in pods in a variety of ways. A config map can be used to:

- Populate environment variable values in containers

- Set command-line arguments in a container

- Populate configuration files in a volume

Users and system components can store configuration data in a config map.

A config map is similar to a secret, but designed to more conveniently support working with strings that do not contain sensitive information.

## Config map restrictions

**A config map must be created before its contents can be consumed in pods.**

Controllers can be written to tolerate missing configuration data. Consult individual components configured by using config maps on a case-by-case basis.

**`ConfigMap` objects reside in a project.**

They can only be referenced by pods in the same project.

**The Kubelet only supports the use of a config map for pods it gets from the API server.**

This includes any pods created by using the CLI, or indirectly from a replication controller. It does not include pods created by using the OpenShift Container Platform node’s `--manifest-url` flag, its `--config` flag, or its REST API because these are not common ways to create pods.

- [Creating and using config maps](../nodes/pods/nodes-pods-configmaps.xml)

# Use cases: Consuming config maps in pods

The following sections describe some uses cases when consuming `ConfigMap` objects in pods.

## Populating environment variables in containers by using config maps

You can use config maps to populate individual environment variables in containers or to populate environment variables in containers from all keys that form valid environment variable names.

As an example, consider the following config map:

<div class="formalpara-title">

**`ConfigMap` with two environment variables**

</div>

``` yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: special-config
  namespace: default
data:
  special.how: very
  special.type: charm
```

- Name of the config map.

- The project in which the config map resides. Config maps can only be referenced by pods in the same project.

- Environment variables to inject.

<div class="formalpara-title">

**`ConfigMap` with one environment variable**

</div>

``` yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: env-config
  namespace: default
data:
  log_level: INFO
```

- Name of the config map.

- Environment variable to inject.

<!-- -->

- You can consume the keys of this `ConfigMap` in a pod using `configMapKeyRef` sections.

  <div class="formalpara-title">

  **Sample `Pod` specification configured to inject specific environment variables**

  </div>

  ``` yaml
  apiVersion: v1
  kind: Pod
  metadata:
    name: dapi-test-pod
  spec:
    securityContext:
      runAsNonRoot: true
      seccompProfile:
        type: RuntimeDefault
    containers:
      - name: test-container
        image: gcr.io/google_containers/busybox
        command: [ "/bin/sh", "-c", "env" ]
        env:
          - name: SPECIAL_LEVEL_KEY
            valueFrom:
              configMapKeyRef:
                name: special-config
                key: special.how
          - name: SPECIAL_TYPE_KEY
            valueFrom:
              configMapKeyRef:
                name: special-config
                key: special.type
                optional: true
        envFrom:
          - configMapRef:
              name: env-config
        securityContext:
          allowPrivilegeEscalation: false
          capabilities:
            drop: [ALL]
    restartPolicy: Never
  ```

  - Stanza to pull the specified environment variables from a `ConfigMap`.

  - Name of a pod environment variable that you are injecting a key’s value into.

  - Name of the `ConfigMap` to pull specific environment variables from.

  - Environment variable to pull from the `ConfigMap`.

  - Makes the environment variable optional. As optional, the pod will be started even if the specified `ConfigMap` and keys do not exist.

  - Stanza to pull all environment variables from a `ConfigMap`.

  - Name of the `ConfigMap` to pull all environment variables from.

    When this pod is run, the pod logs will include the following output:

        SPECIAL_LEVEL_KEY=very
        log_level=INFO

<div class="note">

`SPECIAL_TYPE_KEY=charm` is not listed in the example output because `optional: true` is set.

</div>

## Setting command-line arguments for container commands with config maps

You can use a config map to set the value of the commands or arguments in a container by using the Kubernetes substitution syntax `$(VAR_NAME)`.

As an example, consider the following config map:

``` yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: special-config
  namespace: default
data:
  special.how: very
  special.type: charm
```

- To inject values into a command in a container, you must consume the keys you want to use as environment variables. Then you can refer to them in a container’s command using the `$(VAR_NAME)` syntax.

  <div class="formalpara-title">

  **Sample pod specification configured to inject specific environment variables**

  </div>

  ``` yaml
  apiVersion: v1
  kind: Pod
  metadata:
    name: dapi-test-pod
  spec:
    securityContext:
      runAsNonRoot: true
      seccompProfile:
        type: RuntimeDefault
    containers:
      - name: test-container
        image: gcr.io/google_containers/busybox
        command: [ "/bin/sh", "-c", "echo $(SPECIAL_LEVEL_KEY) $(SPECIAL_TYPE_KEY)" ]
        env:
          - name: SPECIAL_LEVEL_KEY
            valueFrom:
              configMapKeyRef:
                name: special-config
                key: special.how
          - name: SPECIAL_TYPE_KEY
            valueFrom:
              configMapKeyRef:
                name: special-config
                key: special.type
        securityContext:
          allowPrivilegeEscalation: false
          capabilities:
            drop: [ALL]
    restartPolicy: Never
  ```

  - Inject the values into a command in a container using the keys you want to use as environment variables.

    When this pod is run, the output from the echo command run in the test-container container is as follows:

        very charm

## Injecting content into a volume by using config maps

You can inject content into a volume by using config maps.

<div class="formalpara-title">

**Example `ConfigMap` custom resource (CR)**

</div>

``` yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: special-config
  namespace: default
data:
  special.how: very
  special.type: charm
```

<div class="formalpara-title">

**Procedure**

</div>

You have a couple different options for injecting content into a volume by using config maps.

- The most basic way to inject content into a volume by using a config map is to populate the volume with files where the key is the file name and the content of the file is the value of the key:

  ``` yaml
  apiVersion: v1
  kind: Pod
  metadata:
    name: dapi-test-pod
  spec:
    securityContext:
      runAsNonRoot: true
      seccompProfile:
        type: RuntimeDefault
    containers:
      - name: test-container
        image: gcr.io/google_containers/busybox
        command: [ "/bin/sh", "-c", "cat", "/etc/config/special.how" ]
        volumeMounts:
        - name: config-volume
          mountPath: /etc/config
        securityContext:
          allowPrivilegeEscalation: false
          capabilities:
            drop: [ALL]
    volumes:
      - name: config-volume
        configMap:
          name: special-config
    restartPolicy: Never
  ```

  - File containing key.

    When this pod is run, the output of the cat command will be:

        very

- You can also control the paths within the volume where config map keys are projected:

  ``` yaml
  apiVersion: v1
  kind: Pod
  metadata:
    name: dapi-test-pod
  spec:
    securityContext:
      runAsNonRoot: true
      seccompProfile:
        type: RuntimeDefault
    containers:
      - name: test-container
        image: gcr.io/google_containers/busybox
        command: [ "/bin/sh", "-c", "cat", "/etc/config/path/to/special-key" ]
        volumeMounts:
        - name: config-volume
          mountPath: /etc/config
        securityContext:
          allowPrivilegeEscalation: false
          capabilities:
            drop: [ALL]
    volumes:
      - name: config-volume
        configMap:
          name: special-config
          items:
          - key: special.how
            path: path/to/special-key
    restartPolicy: Never
  ```

  - Path to config map key.

    When this pod is run, the output of the cat command will be:

        very
