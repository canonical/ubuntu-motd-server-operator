# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

output "app_name" {
  description = "Name of the deployed application."
  value       = juju_application.ubuntu_motd_server.name
}

output "application" {
  description = "The deployed application object."
  value       = juju_application.ubuntu_motd_server
}

output "provides" {
  description = "Map of the provided integration endpoints."
  value = {
    grafana_dashboard = {
      kind     = "endpoint"
      name     = juju_application.ubuntu_motd_server.name
      endpoint = "grafana-dashboard"
    }
    metrics_endpoint = {
      kind     = "endpoint"
      name     = juju_application.ubuntu_motd_server.name
      endpoint = "metrics-endpoint"
    }
  }
}

output "requires" {
  description = "Map of the required integration endpoints."
  value = {
    ingress = {
      kind     = "endpoint"
      name     = juju_application.ubuntu_motd_server.name
      endpoint = "ingress"
    }
    logging = {
      kind     = "endpoint"
      name     = juju_application.ubuntu_motd_server.name
      endpoint = "logging"
    }
  }
}
