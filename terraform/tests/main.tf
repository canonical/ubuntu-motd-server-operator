# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

variable "channel" {
  description = "The channel to use when deploying a charm."
  type        = string
  default     = "latest/edge"
}

variable "revision" {
  description = "Revision number of the charm."
  type        = number
  default     = null
}

data "juju_model" "testing" {
  name  = "tf-testing"
  owner = "admin"
}

terraform {
  required_providers {
    juju = {
      version = ">= 1.1.0, <2"
      source  = "juju/juju"
    }
  }
}

provider "juju" {}

module "charm_name" {
  source     = "./.."
  app_name   = "mymotd"
  channel    = var.channel
  model_uuid = data.juju_model.testing.uuid
  revision   = var.revision
}
