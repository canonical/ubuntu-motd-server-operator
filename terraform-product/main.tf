# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

module "ubuntu_motd_server" {
  source      = "../terraform"
  app_name    = var.ubuntu_motd_server.app_name
  channel     = local.ubuntu_motd_server_channel
  config      = var.ubuntu_motd_server.config
  model_uuid  = var.model_uuid
  constraints = var.ubuntu_motd_server.constraints
  revision    = var.ubuntu_motd_server.revision
  base        = var.ubuntu_motd_server.base
  units       = var.ubuntu_motd_server.units
}

module "gateway_api" {
  # renovate: depName="gateway-api-integrator-operator" currentRef="gateway-route-rev3"
  source = "git::https://github.com/canonical/gateway-api-integrator-operator.git//terraform/product?ref=433b3f39fda47693a77eec2c354e308dc875a6d4"

  model_uuid = var.model_uuid

  gateway_api_integrator = {
    app_name    = var.gateway_api_integrator.app_name
    channel     = local.gateway_api_integrator_channel
    config      = var.gateway_api_integrator.config
    constraints = var.gateway_api_integrator.constraints
    revision    = var.gateway_api_integrator.revision
    units       = var.gateway_api_integrator.units
  }

  gateway_route_configurator = {
    app_name    = var.gateway_route_configurator.app_name
    channel     = local.gateway_route_configurator_channel
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
    endpoint = module.ubuntu_motd_server.requires.ingress.endpoint
  }

  application {
    name     = module.gateway_api.gateway_route_configurator_app_name
    endpoint = module.gateway_api.gateway_route_configurator_provides.ingress
  }
}

# Integrate ubuntu-motd-server's "logging" requirement with an externally supplied
# endpoint or offer, when the deployer provides one via `var.logging`.
resource "juju_integration" "motd_logging" {
  count = var.logging != null ? 1 : 0

  model_uuid = var.model_uuid

  application {
    name      = var.logging.kind == "endpoint" ? var.logging.name : null
    endpoint  = var.logging.kind == "endpoint" ? var.logging.endpoint : null
    offer_url = var.logging.kind == "offer" ? var.logging.url : null
  }

  application {
    name     = module.ubuntu_motd_server.app_name
    endpoint = "logging"
  }
}

# Integrate gateway-api-integrator's "certificates" requirement with an externally
# supplied endpoint or offer, when the deployer provides one via `var.certificates`.
resource "juju_integration" "gateway_api_certificates" {
  count = var.certificates != null ? 1 : 0

  model_uuid = var.model_uuid

  application {
    name      = var.certificates.kind == "endpoint" ? var.certificates.name : null
    endpoint  = var.certificates.kind == "endpoint" ? var.certificates.endpoint : null
    offer_url = var.certificates.kind == "offer" ? var.certificates.url : null
  }

  application {
    name     = module.gateway_api.gateway_api_integrator_app_name
    endpoint = "certificates"
  }
}
