# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

module "ubuntu_motd_server" {
  source      = "../terraform"
  app_name    = var.ubuntu_motd_server.app_name
  channel     = var.ubuntu_motd_server.channel
  config      = var.ubuntu_motd_server.config
  model       = var.model
  constraints = var.ubuntu_motd_server.constraints
  revision    = var.ubuntu_motd_server.revision
  base        = var.ubuntu_motd_server.base
  units       = var.ubuntu_motd_server.units
}

module "traefik_k8s" {
  source      = "git::ssh://git@github.com/canonical/traefik-k8s-operator//terraform?depth=1"
  app_name    = var.traefik_k8s.app_name
  channel     = var.traefik_k8s.channel
  config      = var.traefik_k8s.config
  constraints = var.traefik_k8s.constraints
  model       = var.model
  revision    = var.traefik_k8s.revision
  units       = var.traefik_k8s.units
}

/*
module "lego" {
  model    = var.model
  source   = "git::ssh://git@github.com/canonical/platform-engineering-staging-deployments//modules/lego?depth=1&ref=feat/1st_iteration"
  app_name = var.lego.app_name
  channel  = var.lego.channel
  revision = var.lego.revision
  config   = var.lego.config
}
*/

resource "juju_integration" "motd_traefik" {
  model = var.model

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
  model = var.model

  application {
    name     = module.traefik_k8s.app_name
    endpoint = module.traefik_k8s.endpoints.certificates
  }

  application {
    name     = var.certificate_provider_name
    endpoint = "certificates"
  }
}
