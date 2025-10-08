# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

variables {
  channel = "latest/edge"
  # renovate: depName="charm_name"
  revision = 1
  model = "tf-testing"
}

run "basic_deploy" {
  assert {
    condition     = module.charm_name.app_name == "mymotd"
    error_message = "charm_name app_name did not match expected"
  }
}
