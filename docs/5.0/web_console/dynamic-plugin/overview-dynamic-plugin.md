The OpenShift Container Platform web console loads and interprets dynamic plugins from remote sources at runtime. One way to deliver and expose dynamic plugins to the console is through OLM Operators. The Operator creates a deployment on the platform with an HTTP server to host the plugin and exposes the plugin using a Kubernetes service.

You can use dynamic plugins to add custom pages and other extensions to your console user interface at runtime. The `ConsolePlugin` custom resource registers plugins with the console, and a cluster administrator enables plugins in the console Operator configuration.

# Key features

With dynamic plugins, you can make the following customizations to the OpenShift Container Platform experience:

- Add custom pages.

- Add perspectives beyond administrator and developer.

- Add navigation items.

- Add tabs and actions to resource pages.

# General guidelines

Follow these guidelines when you create a plugin:

- You must use [`Node.js`](https://nodejs.org/en/) to build and run your plugin. You can use any package manager, such as npm or yarn.

- Prefix your CSS class names with your plugin name to avoid collisions. For example, `my-plugin__heading` and `my-plugin_\_icon`.

- Maintain a consistent look, feel, and behavior with other console pages.

- Follow [react-i18next](https://www.i18next.com/) localization guidelines when creating your plugin. You can use the `useTranslation` hook like the one in the following example:

  ``` tsx
  const Header: React.FC = () => {
    const { t } = useTranslation('plugin__console-demo-plugin');
    return <h1>{t('Hello, World!')}</h1>;
  };
  ```

- Avoid selectors that could affect markup outside of your plugin components, such as element selectors. These are not APIs and are subject to change. Using them might break your plugin. To prevent this, do not use selectors that change HTML elements outside of your own plugin.

- Provide valid JavaScript Multipurpose Internet Mail Extension (MIME) type by using the `Content-Type` response header for all assets your plugin web server hosts. Each plugin deployment must include a web server that hosts the generated assets of the plugin.

- You must build your plugin with Webpack version 5 or later. Refer to the [console plugin template](https://github.com/openshift/console-plugin-template/) for the suggested setup.

- Prefix CSS class names with your plugin name to avoid collisions; for example, `my-plugin__heading` and `my-plugin_\_icon`.

# PatternFly guidelines

When creating your plugin, follow these guidelines for using PatternFly:

- Use [PatternFly](https://www.patternfly.org/components/all-components/) components and CSS variables directly. The SDK provides console-specific wrappers around certain PatternFly components; for example, the SDK’s `ListPageHeader` wraps PatternFly’s `PageHeader`. Using PatternFly components and variables helps your plugin look consistent in future console versions.

  - Use PatternFly 4.x with OpenShift Container Platform versions 4.14 and earlier.

  - Use PatternFly 5.x with OpenShift Container Platform versions 4.15 through 4.18.

  - Use PatternFly 6.x with OpenShift Container Platform versions 4.19 and later.

- Make your plugin accessible by following [PatternFly’s accessibility fundamentals](https://www.patternfly.org/accessibility/accessibility-fundamentals/).

- Avoid using other CSS libraries such as Bootstrap or Tailwind. They might conflict with PatternFly and not match the rest of the console. Include only styles specific to your plugin’s user interface. The console evaluates these styles on top of the base PatternFly styles. Do not import styles directly from `@patternfly/react-styles/*/.css` or `@patternfly/patternfly`. Instead, use components and CSS variables provided by the console SDK.

- The console application loads base styles for all supported PatternFly versions.

## Translating messages with react-i18next

The [plugin template](https://github.com/openshift/console-plugin-template) demonstrates how you can translate messages with [react-i18next](https://www.i18next.com/).

- You must have the plugin template cloned locally.

- Optional: To test your plugin locally, run the OpenShift Container Platform web console in a container. You can use either Docker or Podman 3.2.0 or later.

1.  Prefix the name with `plugin__` to avoid any naming conflicts. The plugin template uses the `plugin__console-plugin-template` namespace by default, and you must update when you rename your plugin for example, `plugin__my-plugin`. You can use the `useTranslation` hook, for example:

    ``` tsx
    conster Header: React.FC = () => {
      const { t } = useTranslation('plugin__console-demo-plugin');
      return <h1>{t('Hello, World!')}</h1>;
    };
    ```

    <div class="important">

    You must match the `i18n` namespace with the name of the `ConsolePlugin` resource.

    </div>

2.  Set the `spec.i18n.loadType` field based on needed behavior.

    `plugin__console-demo-plugin` **Example**

    ``` yaml
    spec:
      backend:
        service:
          basePath: /
          name: console-demo-plugin
          namespace: console-demo-plugin
          port: 9001
        type: Service
      displayName: OpenShift Console Demo Plugin
      i18n:
        loadType: Preload
    ```

    `loadType: Preload`
    Loads all the plugin’s localization resources from the `i18n` namespace after the dynamic plugin during loading.

3.  Use the format `%plugin__console-plugin-template~My Label%` for labels in `console-extensions.json`. The console replaces the value with the message for the current language from the `plugin__console-plugin-template` namespace. For example:

    ``` json
      {
        "type": "console.navigation/section",
        "properties": {
          "id": "admin-demo-section",
          "perspective": "admin",
          "name": "%plugin__console-plugin-template~Plugin Template%"
        }
      }
    ```

4.  Include a comment in a TypeScript file for [i18next-parser](https://github.com/i18next/i18next-parser) to add the message from `console-extensions.json` to your message catalog. For example:

    ``` tsx
    // t('plugin__console-demo-plugin~Demo Plugin')
    ```

5.  To update the JSON files in the `locales` folder of the plugin template when adding or changing a message, run the following command:

    ``` terminal
    $ yarn i18n
    ```
