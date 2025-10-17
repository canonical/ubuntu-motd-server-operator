# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

data "juju_model" "ubuntu_motd_server" {
  name = var.model
}

module "ubuntu_motd_server" {
  source      = "../terraform"
  app_name    = var.ubuntu_motd_server.app_name
  channel     = var.ubuntu_motd_server.channel
  config      = var.ubuntu_motd_server.config
  model       = data.juju_model.ubuntu_motd_server.name
  constraints = var.ubuntu_motd_server.constraints
  revision    = var.ubuntu_motd_server.revision
  base        = var.ubuntu_motd_server.base
  units       = var.ubuntu_motd_server.units
}

module "traefik_k8s" {
  source      = "git::https://github.com/canonical/traefik-k8s-operator//terraform?depth=1"
  app_name    = var.traefik_k8s.app_name
  channel     = var.traefik_k8s.channel
  config      = var.traefik_k8s.config
  constraints = var.traefik_k8s.constraints
  model       = data.juju_model.ubuntu_motd_server.name
  revision    = var.traefik_k8s.revision
  units       = var.traefik_k8s.units
}

module "httprequest_lego" {
  count    = length(local.offers.certificate_provider) > 0 ? 0 : 1
  model    = data.juju_model.ubuntu_motd_server.name
  source   = "git::https://github.com/canonical/httprequest-lego-provider//terraform?depth=1&ref=feat/terraform_module"
  channel  = local.channels.lego
  revision = local.revisions.lego
  config   = local.config_lego
}

resource "juju_integration" "motd_traefik" {
  model = data.juju_model.ubuntu_motd_server.name

  application {
    name     = module.ubuntu_motd_server.app_name
    endpoint = module.ubuntu_motd_server.endpoints.ingress
  }

  application {
    name     = module.traefik_k8s.app_name
    endpoint = module.traefik_k8s.endpoints.ingress
  }
}

resource "juju_integration" "traefik_certs" {
  count = length(local.offers.certificate_provider) > 0 ? 0 : 1

  model = data.juju_model.ubuntu_motd_server.name

  application {
    name     = module.traefik_k8s.app_name
    endpoint = module.traefik_k8s.requires.certificates
  }

  application {
    name     = module.httprequest_lego.app_name
    endpoint = module.httprequest_lego.provides.certificates
  }
}
