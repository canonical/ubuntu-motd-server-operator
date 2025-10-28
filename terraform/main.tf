# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.
# Trigger test 1

resource "juju_application" "ubuntu_motd_server" {
  name  = var.app_name
  model = var.model

  charm {
    name     = "ubuntu-motd-server"
    channel  = var.channel
    revision = var.revision
    base     = var.base
  }

  config             = var.config
  constraints        = var.constraints
  units              = var.units
  storage_directives = var.storage
}
