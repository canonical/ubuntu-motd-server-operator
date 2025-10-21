# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

output "app_name" {
  description = "Name of the deployed application."
  value       = module.ubuntu_motd_server.app_name
}

output "certificates_requirer" {
  description = "Name of the application requiring certificates."
  value       = module.traefik_k8s.app_name
}

output "requires" {
  value = {
    logging      = "logging"
    certificates = "certificates"
  }
}

output "provides" {
  value = {
    grafana_dashboard = "grafana-dashboard"
    metrics_endpoint  = "metrics-endpoint"
  }
}
