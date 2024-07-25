---
description: "List of profile commands for the Corda 5.3 CLI. You can use these commands to create profiles with default property values for use with other plugins."
date: '2024-07-25'
menu:
  corda53:
    identifier: corda53-cordacli-profile
    weight: 4030
    parent: corda53-cli-reference
title: "profile"
---

# profile

The `profile` command in the {{< tooltip >}}Corda CLI{{< /tooltip >}} allows you to create, list, update, and delete profiles. A profile is a collection of key-value properties that can be used with other CLI plugins to provide default values for various configuration options.
<style>
table th:first-of-type {
    width: 30%;
}
table th:nth-of-type(2) {
    width: 70%;
}
</style>
| Sub-Command | Description                                                  |
|-------------|--------------------------------------------------------------|
| `create`    | Create a new profile with the specified properties. See [create](#create). |
| `list`      | List all available profiles and their properties. See [list](#list).   |
| `update`    | Update an existing profile with new or modified properties. See [update](#update). |
| `delete`    | Delete an existing profile. See [delete](#delete).

## create
The `create` sub-command is used to create a new profile with the specified properties.
| Argument        | Description                                                                                                                          |
|-----------------|--------------------------------------------------------------------------------------------------------------------------------------|
| `-n, --name`    | The name of the profile to create. This is a required argument.                                                                    |
| `-p, --property`| A key-value pair representing a property for the profile. Valid keys are listed in the `ProfileKey` enum. This argument can be specified multiple times to set multiple properties. At least one property is required. |
Valid property keys are:
- `rest_username`: Username for the REST API
- `rest_password`: Password for the REST API
- `rest_endpoint`: Endpoint for the REST API
- `jdbc_username`: Username for the JDBC connection
- `jdbc_password`: Password for the JDBC connection
- `database_url`: URL for the database
  If a profile with the specified name already exists, you will be prompted to confirm if you want to overwrite it.
  For example, to create a new profile named `prod` with REST API and database properties:
  {{< tabs name="create-example">}}
  {{% tab name="Bash" %}}
   ```sh
   ./corda-cli.sh profile create -n prod -p rest_username=admin -p rest_password=securePassword -p rest_endpoint=https://example.com:8080 -p jdbc_username=dbuser -p jdbc_password=dbpassword -p database_url=jdbc:postgresql://localhost:5432/cordadb
   ```
  {{% /tab %}}
  {{% tab name="PowerShell" %}}
   ```powershell
   ./corda-cli.cmd profile create -n prod -p rest_username=admin -p rest_password=securePassword -p rest_endpoint=https://example.com:8080 -p jdbc_username=dbuser -p jdbc_password=dbpassword -p database_url=jdbc:postgresql://localhost:5432/cordadb
   ```
  {{% /tab %}}
  {{< /tabs >}}

## list
The `list` sub-command lists all available profiles and their properties.
| Argument             | Description                                                                |
|-----------------------|----------------------------------------------------------------------------|
| `-e, --encrypted`    | Show password properties in their encrypted form instead of decrypted.    |
The output will display the name of each profile and its properties. If the `-e` or `--encrypted` option is not provided, password properties will be decrypted and displayed in plain text.
For example, to list all available profiles and their properties:
{{< tabs name="list-example">}}
{{% tab name="Bash" %}}
   ```sh
   ./corda-cli.sh profile list
   ```
{{% /tab %}}
{{% tab name="PowerShell" %}}
   ```powershell
   ./corda-cli.cmd profile list
   ```
{{% /tab %}}
{{< /tabs >}}

## update
The `update` sub-command updates an existing profile with new or modified properties.
| Argument        | Description                                                                                                                          |
|-----------------|--------------------------------------------------------------------------------------------------------------------------------------|
| `-n, --name`    | The name of the profile to update. This is a required argument.                                                                    |
| `-p, --property`| A key-value pair representing a property to update or add to the profile. Valid keys are listed in the `ProfileKey` enum. This argument can be specified multiple times to update or add multiple properties. |
If the specified profile does not exist, a new profile will be created with the provided properties.
For example, to update the `prod` profile with a new REST API endpoint:
{{< tabs name="update-example">}}
{{% tab name="Bash" %}}
   ```sh
   ./corda-cli.sh profile update -n prod -p rest_endpoint=https://example.com:8443
   ```
{{% /tab %}}
{{% tab name="PowerShell" %}}
   ```powershell
   ./corda-cli.cmd profile update -n prod -p rest_endpoint=https://example.com:8443
   ```
{{% /tab %}}
{{< /tabs >}}

## delete
The `delete` sub-command deletes an existing profile.
| Argument     | Description                                           |
|--------------|-------------------------------------------------------|
| `-n, --name` | The name of the profile to delete. This is a required argument. |
You will be prompted to confirm the deletion before the profile is removed.
For example, to delete the `prod` profile:
{{< tabs name="delete-example">}}
{{% tab name="Bash" %}}
   ```sh
   ./corda-cli.sh profile delete -n prod
   ```
{{% /tab %}}
{{% tab name="PowerShell" %}}
   ```powershell
   ./corda-cli.cmd profile delete -n prod
   ```
{{% /tab %}}
{{< /tabs >}}

## Using Profiles with Other CLI Plugins
Once you have created a profile, you can use it with other CLI plugins by specifying the `--profile` option along with the profile name. The plugin will then use the properties defined in the specified profile as default values for its configuration options.
For example, if you have a profile named `prod` with REST API properties defined, you can use it with the `cpi` plugin like this:
```
./corda-cli.cmd cpi list --profile prod
```
In this case, the `cpi` plugin will use the `rest_username`, `rest_password`, and `rest_endpoint` properties from the `prod` profile as the default values for the corresponding options.
