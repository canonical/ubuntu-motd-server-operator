# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

output "app_name" {
  description = "Name of the deployed application."
  value       = module.ubuntu_motd_server.app_name
}

output "certificates_requirer" {
  description = "Name of the application requiring certificates."
  value       = module.gateway_api.gateway_api_integrator_app_name
}

output "metadata" {
  description = "Metadata of the product deployment."
  value = {
    version     = var.metadata_version
    deployed_at = null
    updated_at  = null
  }
}

output "models" {
  description = "Map of the model key to its model_uuid and the components deployed in it."
  value = {
    ubuntu_motd_server = {
      model_uuid = var.model_uuid
      components = {
        ubuntu_motd_server         = module.ubuntu_motd_server.application
        gateway_api_integrator     = module.gateway_api.gateway_api_integrator_app_name
        gateway_route_configurator = module.gateway_api.gateway_route_configurator_app_name
      }
    }
  }
}

output "provides" {
  description = "Map of provided integration endpoints."
  value       = module.ubuntu_motd_server.provides
}
