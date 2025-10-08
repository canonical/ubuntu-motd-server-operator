#!/usr/bin/env python3

# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

"""Unit tests for motd-server-app/app.py."""

import pytest

from app import (
    DEFAULT_FILES,
    HEALTH_CONTENT,
    HEALTH_PATH,
    extract_user_agent_info,
    get_files_from_yaml,
    select_motd,
)


def test_get_files_from_yaml():
    """Test loading files from a valid YAML string."""

    yaml_content = """
index-24.04.txt:
  - Welcome to Ubuntu 24.04
  - System information

index-22.04.txt: 
  - Welcome to Ubuntu 22.04
"""
    result = get_files_from_yaml(yaml_content)
    expected = DEFAULT_FILES.copy()
    expected.update(
        {
            "index-24.04.txt": "Welcome to Ubuntu 24.04\nSystem information",
            "index-22.04.txt": "Welcome to Ubuntu 22.04",
        }
    )
    assert result == expected


def test_get_files_from_non_dict_yaml():
    """Test loading files from an invalid YAML string."""

    # If content is invalid, we silently fail and return healthcheck only
    result = get_files_from_yaml("not a dict")

    assert result == {HEALTH_PATH: HEALTH_CONTENT}


def test_get_files_from_invalid_yaml():
    """Test handling of invalid YAML string."""
    yaml_content = "::: invalid yaml :-::"
    result = get_files_from_yaml(yaml_content)
    assert result == DEFAULT_FILES


def test_get_files_from_enpty_yaml():
    """Test handling of empty YAML string."""
    result = get_files_from_yaml("")
    assert result == DEFAULT_FILES


@pytest.mark.parametrize(
    "user_agent,expected",
    [
        ("curl/7.68.0 Ubuntu/24.04/amd64 cloud_id/aws", ("24.04", "amd64", "aws")),
        ("curl/7.68.0 Ubuntu/22.04", ("22.04", "", "")),
        ("curl/7.68.0 /arm64 cloud_id/gce", ("", "arm64", "gce")),
        ("curl/7.68.0 cloud_id/gce", ("", "", "gce")),
        ("", ("", "", "")),
        ("random string without patterns", ("", "", "")),
    ],
)
def test_extract_user_agent_info(user_agent, expected):
    """Test extraction of version, architecture, and cloud from user agent."""
    assert extract_user_agent_info(user_agent) == expected


@pytest.fixture(name="motds")
def motds_fixture():
    """Fixture providing a sample MOTD files dictionary."""
    return {
        "index-24.04-amd64-aws.txt": "Specific MOTD",
        "index-24.04-amd64.txt": "Version and arch MOTD",
        "index-24.04-aws.txt": "Version and cloud MOTD",
        "index-24.04.txt": "Version only MOTD",
        "index-amd64.txt": "Arch only MOTD",
        "index-aws.txt": "Cloud only MOTD",
    }


@pytest.mark.parametrize(
    "version,arch,cloud,expected",
    [
        ("24.04", "amd64", "aws", "Specific MOTD"),
        ("24.04", "amd64", "gce", "Version and arch MOTD"),
        ("24.04", "arm64", "aws", "Version and cloud MOTD"),
        ("24.04", "arm64", "gce", "Version only MOTD"),
        ("22.04", "amd64", "gce", "Arch only MOTD"),
        ("22.04", "arm64", "aws", "Cloud only MOTD"),
        ("20.04", "s390x", "oracle", ""),
    ],
)
def test_select_motd_most_specific_match(motds, version, arch, cloud, expected):
    """Test selection of MOTD based on version, architecture, and cloud."""
    assert select_motd(motds, version, arch, cloud) == expected


def test_select_motd_empty_files_dict():
    """Test selection of MOTD when files dictionary is empty."""
    assert select_motd({}, "24.04", "amd64", "aws") == ""


def test_select_motd_empty_parameters(motds):
    """Test selection of MOTD when version, architecture, and cloud are empty."""
    assert select_motd(motds, "", "", "") == ""
