# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

locals {
  # The product owns each charm's channel risk; `risk` provides the fallback when a
  # per-charm `channel` is not explicitly set, preserving the historical "latest/stable"
  # default when `risk` is left at its default value.
  ubuntu_motd_server_channel         = coalesce(var.ubuntu_motd_server.channel, "latest/${var.risk}")
  gateway_api_integrator_channel     = coalesce(var.gateway_api_integrator.channel, "latest/${var.risk}")
  gateway_route_configurator_channel = coalesce(var.gateway_route_configurator.channel, "latest/${var.risk}")
}
