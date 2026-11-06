# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

variable "certificates" {
  description = <<-EOT
    External TLS endpoint or offer to integrate gateway-api-integrator's "certificates"
    relation with. Set to null to leave the relation unfulfilled. Set kind to "endpoint"
    for an in-model relation (name/endpoint) or "offer" to consume a cross-model offer (url).
  EOT
  type = object({
    kind       = string
    name       = optional(string, null)
    endpoint   = optional(string, null)
    url        = optional(string, null)
    controller = optional(string, null)
  })
  default = null
}

variable "gateway_api_integrator" {
  type = object({
    app_name    = optional(string, "gateway_api")
    channel     = optional(string, null)
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
    channel     = optional(string, null)
    config      = optional(map(string), {})
    constraints = optional(string, "arch=amd64")
    revision    = optional(number)
    base        = optional(string, "ubuntu@24.04")
    units       = optional(number, 1)
    storage     = optional(map(string), {})
  })
}

variable "logging" {
  description = <<-EOT
    External logging endpoint or offer to integrate ubuntu-motd-server's "logging"
    relation with. Set to null to leave the relation unfulfilled. Set kind to "endpoint"
    for an in-model relation (name/endpoint) or "offer" to consume a cross-model offer (url).
  EOT
  type = object({
    kind       = string
    name       = optional(string, null)
    endpoint   = optional(string, null)
    url        = optional(string, null)
    controller = optional(string, null)
  })
  default = null
}

variable "metadata_version" {
  description = "Version string reported in the product module's `metadata` output."
  type        = string
  default     = "1.0.0"
}

variable "model_uuid" {
  description = "Reference to the k8s Juju model to deploy application to."
  type        = string
  nullable    = false
}

variable "risk" {
  description = <<-EOT
    Risk level controlling the channel risk of the charms in the solution. Used as the
    fallback channel risk (e.g. "latest/<risk>") for any bundled charm whose per-charm
    `channel` field is left unset.
  EOT
  type        = string
  default     = "stable"

  validation {
    condition     = contains(["stable", "edge"], var.risk)
    error_message = "risk must be one of: stable, edge."
  }
}

variable "ubuntu_motd_server" {
  type = object({
    app_name    = optional(string, "motd-server")
    channel     = optional(string, null)
    config      = optional(map(string), {})
    constraints = optional(string, "arch=amd64")
    revision    = optional(number)
    base        = optional(string, "ubuntu@24.04")
    units       = optional(number, 1)
  })
}
