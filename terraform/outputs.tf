# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

output "app_name" {
  description = "Name of the deployed application."
  value       = juju_application.ubuntu_motd_server.name
}

output "endpoints" {
  value = {
    ingress = "ingress"
  }
}

output "requires" {
  value = {
    ingress = "ingress"
    logging = "logging"
  }
}
