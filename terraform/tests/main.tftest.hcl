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
    channel    = "latest/edge"
    # renovate: depName="ubuntu-motd-server"
    revision = 1
  }

  assert {
    condition     = output.app_name == "ubuntu-motd-server"
    error_message = "ubuntu-motd-server app_name did not match expected"
  }
}
