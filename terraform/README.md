<!-- Remember to update this file for your charm -- replace <charm_name> with the appropriate name. -->
# <charm_name> Terraform module

This folder contains a base [Terraform][Terraform] module for the `ubuntu-motd-server` charm.

The module uses the [Terraform Juju provider][Terraform Juju provider] to model the charm
deployment onto any Kubernetes environment managed by [Juju][Juju].

## Module structure

- **main.tf** - Defines the Juju application to be deployed.
- **variables.tf** - Allows customization of the deployment. Also models the charm configuration,
  except for exposing the deployment options (Juju model name, channel or application name).
- **output.tf** - Integrates the module with other Terraform modules, primarily
  by defining potential integration endpoints (charm integrations), but also by exposing
  the Juju application name.
- **versions.tf** - Defines the Terraform provider version.

## Using `ubuntu-motd-server` base module in higher level modules

If you want to use `ubuntu-motd-server` base module as part of your Terraform module, import it
like shown below:

```text
data "juju_model" "my_model" {
  name = var.model
}

module "<charm_name>" {
  source = "git::https://github.com/canonical/ubuntu-motd-server-operator//terraform"
  
  model = juju_model.my_model.name
  # (Customize configuration variables here if needed)
}
```

Create integrations, for instance:

```text
resource "juju_integration" "ubuntu-motd-server-loki" {
  model = juju_model.my_model.name
  application {
    name     = module.ubuntu-motd-server.app_name
    endpoint = module.ubuntu-motd-server.endpoints.logging
  }
  application {
    name     = "loki-k8s"
    endpoint = "logging"
  }
}
```

The complete list of available integrations can be found [in the Integrations tab][ubuntu-motd-server-integrations].

[Terraform]: https://developer.hashicorp.com/terraform
[Terraform Juju provider]: https://registry.terraform.io/providers/juju/juju/latest
[Juju]: https://juju.is
[ubuntu-motd-server-integrations]: https://charmhub.io/ubuntu-motd-server/integrations
