# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

module "ubuntu_motd_server" {
  source      = "../terraform"
  app_name    = var.ubuntu_motd_server.app_name
  channel     = var.ubuntu_motd_server.channel
  config      = var.ubuntu_motd_server.config
  model_uuid  = var.model_uuid
  constraints = var.ubuntu_motd_server.constraints
  revision    = var.ubuntu_motd_server.revision
  base        = var.ubuntu_motd_server.base
  units       = var.ubuntu_motd_server.units
}

module "gateway_api" {
  source = "https://github.com/canonical/gateway-api-integrator-operator.git//terraform/product?depth=1&ref=gateway-route-rev3"

  model_uuid = var.model_uuid

  gateway_api_integrator = {
    app_name    = var.gateway_api.app_name
    channel     = var.gateway_api.channel
    config      = var.gateway_api.config
    constraints = var.gateway_api.constraints
    revision    = var.gateway_api.revision
    units       = var.gateway_api.units
  }

  gateway_route_configurator = {
    app_name    = var.gateway_route_configurator.app_name
    channel     = var.gateway_route_configurator.channel
    config      = var.gateway_route_configurator.config
    constraints = var.gateway_route_configurator.constraints
    revision    = var.gateway_route_configurator.revision
    units       = var.gateway_route_configurator.units
  }
}

resource "juju_integration" "motd_gateway_api" {
  model_uuid = var.model_uuid

  application {
    name     = module.ubuntu_motd_server.app_name
    endpoint = module.ubuntu_motd_server.endpoints.ingress
  }

  application {
    name     = module.gateway_api.gateway_route_configurator_app_name
    endpoint = module.gateway_api.gateway_route_configurator_provides.ingress
  }
}
