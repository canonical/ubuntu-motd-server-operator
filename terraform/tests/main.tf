# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

variable "model_uuid" {
  description = "The juju model uuid"
  type        = string
  default     = "fake_uuid"
}

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
  model_uuid = var.model_uuid
  revision   = var.revision
}
