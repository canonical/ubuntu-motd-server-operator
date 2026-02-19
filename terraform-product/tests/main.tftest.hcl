# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

run "setup_tests" {
  module {
    source = "./tests/setup"
  }
}

run "basic_deploy" {
  variables {
    model_uuid = run.setup_tests.model_uuid
    ubuntu_motd_server = {
      app_name = "motd-test"
      channel  = "latest/edge"
      # renovate: depName="ubuntu-motd-server"
      revision = 1
      config   = {}
      base     = "ubuntu@22.04"
    }
    gateway_api_integrator = {
      app_name = "gateway-api"
      channel  = "latest/edge"
      # renovate: depName="gateway-api-integrator"
      revision = 136
      config   = {}
    }
    gateway_route_configurator = {
      app_name = "gateway-route-configurator"
      channel  = "latest/edge"
      # renovate: depName="gateway-api-configurator"
      revision = 4
      config   = {}
    }
  }

  assert {
    condition     = output.app_name == "motd-test"
    error_message = "MOTD app_name did not match expected"
  }
}
