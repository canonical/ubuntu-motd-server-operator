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
  source      = "./modules/traefik-k8s"
  app_name    = var.traefik_k8s.app_name
  channel     = var.traefik_k8s.channel
  config      = var.traefik_k8s.config
  constraints = var.traefik_k8s.constraints
  model       = data.juju_model.ubuntu_motd_server.name
  revision    = var.traefik_k8s.revision
  base        = var.traefik_k8s.base
  units       = var.traefik_k8s.units
}

module "httprequest_lego_k8s" {
  source      = "./modules/httprequest-lego-k8s"
  app_name    = var.httprequest_lego_k8s.app_name
  channel     = var.httprequest_lego_k8s.channel
  config      = var.httprequest_lego_k8s.config
  constraints = var.httprequest_lego_k8s.constraints
  model       = data.juju_model.ubuntu_motd_server.name
  revision    = var.httprequest_lego_k8s.revision
  base        = var.httprequest_lego_k8s.base
  units       = var.httprequest_lego_k8s.units
}

resource "juju_integration" "motd_traefik" {
  model = data.juju_model.ubuntu_motd_server.name

  application {
    name     = module.ubuntu_motd_server.app_name
    endpoint = module.ubuntu_motd_server.requires.ingress
  }

  application {
    name     = module.traefik_k8s.app_name
    endpoint = module.traefik_k8s.provides.ingress
  }
}

resource "juju_integration" "traefik_certs" {
  model = data.juju_model.ubuntu_motd_server.name

  application {
    name     = module.traefik_k8s.app_name
    endpoint = module.traefik_k8s.requires.certificates
  }

  application {
    name     = module.httprequest_lego_k8s.app_name
    endpoint = module.httprequest_lego_k8s.provides.certificates
  }
}
