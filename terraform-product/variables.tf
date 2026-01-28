# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

variable "model_uuid" {
  description = "Reference to the k8s Juju model to deploy application to."
  type        = string
}

variable "ubuntu_motd_server" {
  type = object({
    app_name    = optional(string, "motd-server")
    channel     = optional(string, "latest/stable")
    config      = optional(map(string), {})
    constraints = optional(string, "arch=amd64")
    revision    = optional(number)
    base        = optional(string, "ubuntu@24.04")
    units       = optional(number, 1)
  })
}

variable "gateway_api" {
  type = object({
    app_name    = optional(string, "gateway_api")
    channel     = optional(string, "latest/stable")
    config      = optional(map(string), {})
    constraints = optional(string, "arch=amd64")
    revision    = optional(number)
    base        = optional(string, "ubuntu@24.04")
    units       = optional(number, 1)
    storage     = optional(map(string), {})
  })
}

variable "gateway_route_configurator" {
  type = object({
    app_name    = optional(string, "gateway_route_configurator")
    channel     = optional(string, "latest/stable")
    config      = optional(map(string), {})
    constraints = optional(string, "arch=amd64")
    revision    = optional(number)
    base        = optional(string, "ubuntu@24.04")
    units       = optional(number, 1)
    storage     = optional(map(string), {})
  })
}
