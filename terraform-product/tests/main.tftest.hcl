# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

run "basic_deploy" {
  assert {
    condition     = module.ubuntu_motd_server.app_name == "motd-test"
    error_message = "MOTD app_name did not match expected"
  }
}
