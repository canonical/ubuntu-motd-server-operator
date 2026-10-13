# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

Each revision is versioned by the date of the revision.

## 2026-10-13

- Migrated the `terraform/` and `terraform-product/` modules to the CC008 Charm
  Terraform Standards: split the combined `endpoints` output into `provides`/`requires`,
  added the `application` output, added CI compliance/docs/release workflows, and pinned
  all module sources to tags or commit hashes.
- Breaking: `terraform/variables.tf` renamed the `storage` variable to `storage_directives`,
  and the `base`/`constraints` variables now default to `null` instead of
  `"ubuntu@22.04"`/`"arch=amd64"` (callers that relied on the implicit defaults must set
  them explicitly).
- Breaking: `terraform-product` dropped the deprecated `requires` output in favor of new
  `certificates`/`logging` input variables for wiring external integrations, and added the
  mandatory `risk`, `models` and `metadata` CC008 fields.

## 2025-12-17

- Moved architecture documentation from Explanation to Reference category.

## 2025-10-22

* Initial publication of the charm.
