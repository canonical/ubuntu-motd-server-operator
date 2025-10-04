#!/usr/bin/env python3

# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

"""Unit tests for motd-server-app/app.py."""

import unittest
from unittest.mock import patch

import pytest

from app import DEFAULT_MOTD, app, extract_info, get_motds_dict, select_motd


class TestGetMotdsDict(unittest.TestCase):
    """Tests for get_motds_dict function."""

    @patch("app.app.config")
    def test_no_motds_in_environment(self, mock_config):
        """Test when no MOTDs are configured."""
        mock_config.get.return_value = None
        result = get_motds_dict()
        assert result == {}

    @patch("app.app.config")
    def test_valid_yaml_motds(self, mock_config):
        """Test parsing valid YAML MOTDs."""
        yaml_content = """
index-24.04.txt:
  - "Welcome to Ubuntu 24.04"
  - "System information"
index-22.04.txt:
  - "Welcome to Ubuntu 22.04"
"""
        mock_config.get.return_value = yaml_content
        result = get_motds_dict()
        assert result == {
            "index-24.04.txt": "Welcome to Ubuntu 24.04\nSystem information",
            "index-22.04.txt": "Welcome to Ubuntu 22.04",
        }

    @patch("app.app.config")
    def test_invalid_yaml_motds(self, mock_config):
        """Test handling of invalid YAML."""
        mock_config.get.return_value = "invalid: yaml: content: ["
        result = get_motds_dict()
        assert result == {}

    @patch("app.app.config")
    def test_empty_yaml_motds(self, mock_config):
        """Test handling of empty YAML."""
        mock_config.get.return_value = ""
        result = get_motds_dict()
        assert result == {}


class TestExtractInfo(unittest.TestCase):
    """Tests for extract_info function."""

    def test_full_user_agent(self):
        """Test extracting all information from a complete user agent."""
        user_agent = "curl/7.68.0 Ubuntu/24.04/amd64 cloud_id/aws"
        version, arch, cloud = extract_info(user_agent)
        assert version == "24.04"
        assert arch == "amd64"
        assert cloud == "aws"

    def test_partial_user_agent_version_only(self):
        """Test user agent with only version information."""
        user_agent = "curl/7.68.0 Ubuntu/22.04"
        version, arch, cloud = extract_info(user_agent)
        assert version == "22.04"
        assert arch == ""
        assert cloud == ""

    def test_partial_user_agent_no_version(self):
        """Test user agent without version information."""
        user_agent = "curl/7.68.0 /arm64 cloud_id/gce"
        version, arch, cloud = extract_info(user_agent)
        assert version == ""
        assert arch == "arm64"
        assert cloud == "gce"

    def test_empty_user_agent(self):
        """Test empty user agent string."""
        user_agent = ""
        version, arch, cloud = extract_info(user_agent)
        assert version == ""
        assert arch == ""
        assert cloud == ""

    def test_malformed_user_agent(self):
        """Test malformed user agent string."""
        user_agent = "random string without patterns"
        version, arch, cloud = extract_info(user_agent)
        assert version == ""
        assert arch == ""
        assert cloud == ""

    def test_different_cloud_providers(self):
        """Test different cloud provider IDs."""
        test_cases = [
            ("Ubuntu/24.04/amd64 cloud_id/aws", "aws"),
            ("Ubuntu/24.04/amd64 cloud_id/gce", "gce"),
            ("Ubuntu/24.04/amd64 cloud_id/azure", "azure"),
        ]
        for user_agent, expected_cloud in test_cases:
            _, _, cloud = extract_info(user_agent)
            assert cloud == expected_cloud


class TestSelectMotd(unittest.TestCase):
    """Tests for select_motd function."""

    def setUp(self):
        """Set up test MOTDs dictionary."""
        self.motds = {
            "index-24.04-amd64-aws.txt": "Specific MOTD",
            "index-24.04-amd64.txt": "Version and arch MOTD",
            "index-24.04-aws.txt": "Version and cloud MOTD",
            "index-24.04.txt": "Version only MOTD",
            "index-amd64.txt": "Arch only MOTD",
            "index-aws.txt": "Cloud only MOTD",
        }

    def test_most_specific_match(self):
        """Test selecting most specific MOTD when all parameters match."""
        result = select_motd(self.motds, "24.04", "amd64", "aws")
        assert result == "Specific MOTD"

    def test_version_arch_match(self):
        """Test selecting version-arch MOTD."""
        result = select_motd(self.motds, "24.04", "amd64", "gce")
        assert result == "Version and arch MOTD"

    def test_version_cloud_match(self):
        """Test selecting version-cloud MOTD."""
        result = select_motd(self.motds, "24.04", "arm64", "aws")
        assert result == "Version and cloud MOTD"

    def test_version_only_match(self):
        """Test selecting version-only MOTD."""
        result = select_motd(self.motds, "24.04", "arm64", "gce")
        assert result == "Version only MOTD"

    def test_arch_only_match(self):
        """Test selecting arch-only MOTD."""
        result = select_motd(self.motds, "22.04", "amd64", "gce")
        assert result == "Arch only MOTD"

    def test_cloud_only_match(self):
        """Test selecting cloud-only MOTD."""
        result = select_motd(self.motds, "22.04", "arm64", "aws")
        assert result == "Cloud only MOTD"

    def test_no_match(self):
        """Test when no MOTD matches."""
        result = select_motd(self.motds, "20.04", "s390x", "oracle")
        assert result == ""

    def test_empty_motds_dict(self):
        """Test with empty MOTDs dictionary."""
        result = select_motd({}, "24.04", "amd64", "aws")
        assert result == ""

    def test_empty_parameters(self):
        """Test with empty parameters."""
        result = select_motd(self.motds, "", "", "")
        assert result == ""


class TestIndexRoute(unittest.TestCase):
    """Tests for the Flask index route."""

    def setUp(self):
        """Set up Flask test client."""
        app.config["TESTING"] = True
        self.client = app.test_client()

    @patch("app.get_motds_dict")
    def test_default_motd_when_no_motds(self, mock_get_motds):
        """Test returning default MOTD when no MOTDs are available."""
        mock_get_motds.return_value = {}
        response = self.client.get("/")
        assert response.status_code == 200
        assert response.data.decode() == DEFAULT_MOTD

    @patch("app.get_motds_dict")
    def test_default_motd_when_no_match(self, mock_get_motds):
        """Test returning default MOTD when no matching MOTD is found."""
        mock_get_motds.return_value = {"index-24.04.txt": "Ubuntu 24.04 MOTD"}
        response = self.client.get(
            "/",
            headers={"User-Agent": "curl/7.68.0 Ubuntu/22.04/amd64 cloud_id/aws"},
        )
        assert response.status_code == 200
        assert response.data.decode() == DEFAULT_MOTD

    @patch("app.get_motds_dict")
    def test_specific_motd_match(self, mock_get_motds):
        """Test returning specific MOTD when a match is found."""
        expected_motd = "Welcome to Ubuntu 24.04 on AWS"
        mock_get_motds.return_value = {"index-24.04.txt": expected_motd}
        response = self.client.get(
            "/",
            headers={"User-Agent": "curl/7.68.0 Ubuntu/24.04/amd64 cloud_id/aws"},
        )
        assert response.status_code == 200
        assert response.data.decode() == expected_motd

    @patch("app.get_motds_dict")
    def test_empty_user_agent(self, mock_get_motds):
        """Test handling empty user agent."""
        mock_get_motds.return_value = {"index-24.04.txt": "Ubuntu MOTD"}
        response = self.client.get("/", headers={"User-Agent": ""})
        assert response.status_code == 200
        assert response.data.decode() == DEFAULT_MOTD

    @patch("app.get_motds_dict")
    def test_hierarchical_motd_selection(self, mock_get_motds):
        """Test that MOTDs are selected hierarchically by specificity."""
        mock_get_motds.return_value = {
            "index-24.04-amd64-aws.txt": "Most specific",
            "index-24.04-amd64.txt": "Medium specific",
            "index-24.04.txt": "Least specific",
        }

        # Should match most specific
        response = self.client.get(
            "/",
            headers={"User-Agent": "curl/7.68.0 Ubuntu/24.04/amd64 cloud_id/aws"},
        )
        assert response.data.decode() == "Most specific"

        # Should match medium specific
        response = self.client.get(
            "/",
            headers={"User-Agent": "curl/7.68.0 Ubuntu/24.04/amd64 cloud_id/gce"},
        )
        assert response.data.decode() == "Medium specific"

        # Should match least specific
        response = self.client.get(
            "/",
            headers={"User-Agent": "curl/7.68.0 Ubuntu/24.04/arm64 cloud_id/gce"},
        )
        assert response.data.decode() == "Least specific"


if __name__ == "__main__":
    pytest.main([__file__])
