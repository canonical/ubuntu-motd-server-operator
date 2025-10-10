# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

"""Unit tests for motd-server-app/app.py."""

import pytest

from motd_server.motd import (
    DEFAULT_FILES,
    extract_user_agent_info,
    get_files_from_yaml,
    process_config,
    select_motd,
)


def test_get_files_from_yaml():
    """Test loading files from a valid YAML string."""

    yaml_content = """
index-24.04.txt: |
  Welcome to Ubuntu 24.04
  System information

index-22.04.txt: 
  Welcome to Ubuntu 22.04
"""
    result = get_files_from_yaml(yaml_content)
    expected = DEFAULT_FILES.copy()
    expected.update(
        {
            "index-24.04.txt": "Welcome to Ubuntu 24.04\nSystem information\n",
            "index-22.04.txt": "Welcome to Ubuntu 22.04",
        }
    )
    assert result == expected


def test_get_files_from_non_dict_yaml():
    """
    arrange: an invalid YAML content (not a dict)
    act: when we try to get the files from it
    assert: we get only the default files
    """

    # If content is invalid, we silently fail and return healthcheck only
    result = get_files_from_yaml("not a dict")

    assert result == DEFAULT_FILES


def test_get_files_from_invalid_yaml():
    """
    arrange: an invalid YAML content (bad syntax)
    act: when we try to get the files from it
    assert: we get only the default files
    """
    yaml_content = "::: invalid yaml :-::"
    result = get_files_from_yaml(yaml_content)
    assert result == DEFAULT_FILES


def test_get_files_from_enpty_yaml():
    """
    arrange: an empty YAML content
    act: when we try to get the files from it
    assert: we get only the default files
    """
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
    """
    arrange: a user agent string following the expected patterns
    act: when we try to retrieve the version, arch, and cloud from it
    assert: we get the expected values
    """
    assert extract_user_agent_info(user_agent) == expected


@pytest.fixture(name="motds")
def motds_fixture():
    """Fixture providing a sample MOTD files dictionary."""
    return {
        "index-24.04-amd64-aws.txt": "version arch cloud",
        "index-24.04-amd64.txt": "version arch",
        "index-24.04-aws.txt": "version cloud",
        "index-24.04.txt": "version",
        "index-amd64-aws.txt": "arch cloud",
        "index-amd64.txt": "arch",
        "index-aws.txt": "cloud",
    }


@pytest.mark.parametrize(
    "version,arch,cloud,expected",
    [
        ("24.04", "amd64", "aws", "version arch cloud"),
        ("24.04", "amd64", "gce", "version arch"),
        ("24.04", "arm64", "aws", "version cloud"),
        ("24.04", "arm64", "gce", "version"),
        ("22.04", "amd64", "gce", "arch"),
        ("22.04", "arm64", "aws", "cloud"),
        ("22.04", "amd64", "aws", "arch cloud"),
        ("20.04", "s390x", "oracle", ""),
    ],
)
def test_select_motd_most_specific_match(motds, version, arch, cloud, expected):
    """
    arrange: a set of MOTD files and various version, architecture, and cloud combinations
    act: when we try to retrieve the motd for a give combination
    assert: we get the expected values
    """
    assert select_motd(motds, version, arch, cloud) == expected


def test_select_motd_empty_files_dict():
    """
    arrange: an empty set of motd files
    act: when we try to retrieve the motd for a given version, arch, and cloud combination
    assert: we get an empty string
    """
    assert select_motd({}, "24.04", "amd64", "aws") == ""


def test_select_motd_empty_parameters(motds):
    """
    arrange: a valid set of motd files
    act: when we try to retrieve the motd for empty version, arch, and cloud
    assert: we get an empty string
    """
    assert select_motd(motds, "", "", "") == ""


def test_process_config_missing_files():
    """
    arrange: a config with no FILES environment variable
    act: when we process the config
    assert: we get only the default files in PROCESSED_FILES
    """
    config: dict = {}
    process_config(config)

    assert config["PROCESSED_FILES"] == DEFAULT_FILES


def test_process_config_with_files():
    """
    arrange: a config with a valid FILES variable
    act: when we process the config
    assert: files are available in PROCESSED_FILES
    """
    config = {"FILES": "index.txt: index"}
    process_config(config)

    expected = DEFAULT_FILES.copy()
    expected.update({"index.txt": "index"})
    assert config["PROCESSED_FILES"] == expected
