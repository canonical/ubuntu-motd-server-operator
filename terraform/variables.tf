# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

variable "app_name" {
  description = "Name of the application in the Juju model."
  type        = string
  default     = "ubuntu-motd-server"
  nullable    = false
}

variable "base" {
  description = "The operating system on which to deploy. null lets the provider use the charm's default (previously defaulted to \"ubuntu@22.04\")."
  type        = string
  default     = null
}

variable "channel" {
  description = "The channel to use when deploying a charm."
  type        = string
  default     = "latest/stable"
  nullable    = false
}

variable "config" {
  description = "Application config. Details about available options can be found at https://charmhub.io/ubuntu-motd-server/configurations."
  type        = map(string)
  default     = {}
}

variable "constraints" {
  description = "Juju constraints to apply for this application. null applies no constraints (previously defaulted to \"arch=amd64\")."
  type        = string
  default     = null
}

variable "model_uuid" {
  description = "Reference to a `juju_model`."
  type        = string
  nullable    = false
}

variable "revision" {
  description = "Revision number of the charm"
  type        = number
  default     = null
}

variable "storage_directives" {
  description = "Map of storage used by the application."
  type        = map(string)
  default     = {}
}

variable "units" {
  description = "Number of units to deploy"
  type        = number
  default     = 1
}
