# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

Each revision is versioned by the date of the revision.

## 2026-11-17

- Upgraded the charm to `paas-charm` 2.0 on Ubuntu 26.04 LTS.
- Renamed the workload container to `app` and the OCI resource to `app-image`.
- Because of the container rename, `juju refresh` fails on Juju earlier than 4.1
  ([LP#1991955](https://bugs.launchpad.net/juju/+bug/1991955)). Remove the charm and redeploy
  it. See [How to upgrade](how-to/upgrade.md).
- The application secret key is regenerated on upgrade, which signs out existing users unless
  a Juju secret is provided through the `app-secret-key` option.

## 2025-12-17

- Moved architecture documentation from Explanation to Reference category.

## 2025-10-22

* Initial publication of the charm.
