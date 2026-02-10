# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.


variable "channel" {
  description = "The channel to use when deploying a charm."
  type        = string
  default     = "latest"
}

variable "revision" {
  description = "Revision number of the charm."
  type        = number
  default     = null
}

terraform {
  required_providers {
    juju = {
      version = ">= 1.0.0, <2"
      source  = "juju/juju"
    }
  }
}

provider "juju" {}

data "juju_model" "testing" {
  name  = "tf-testing-k8s"
  owner = "admin"
}

module "ubuntu_motd_server" {
  source     = "./.."
  model_uuid = data.juju_model.testing.uuid

  ubuntu_motd_server = {
    app_name = "motd-test"
    channel  = "latest/edge"
    config   = {}
    base     = "ubuntu@22.04"
  }

  gateway_api_integrator = {
    app_name = "gateway-api"
    channel  = "latest/edge"
    revision = 130
    config   = {}
  }

  gateway_route_configurator = {
    app_name = "gateway-route-configurator"
    channel  = "latest/edge"
    revision = 4
    config   = {}
  }
}
