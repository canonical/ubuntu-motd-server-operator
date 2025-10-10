#!/usr/bin/env python3

# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

"""Integration tests."""

import logging
from pathlib import Path

import requests
import yaml

logger = logging.getLogger(__name__)

CHARMCRAFT_DATA = yaml.safe_load(Path("./charmcraft.yaml").read_text(encoding="utf-8"))
APP_NAME = CHARMCRAFT_DATA["name"]

MOTD_HEALTH_CONTENT = "OK"
NOT_FOUND_CONTENT = "Not found"


def test_health(motd_url: str):
    """
    arrange: Deploy the motd-server-app charm.
    act: Get the _health endpoint.
    assert: The _health endpoint returns 200 OK.
    """
    res = requests.get(motd_url + "/_health", timeout=5)
    assert res.status_code == 200
    assert res.text == MOTD_HEALTH_CONTENT


def test_404(motd_url: str):
    """
    arrange: Deploy the motd-server-app charm.
    act: Get a non existing page.
    assert: The _health endpoint returns 404
    """
    res = requests.get(motd_url + "/does_not_exist", timeout=5)
    assert res.status_code == 404
    assert res.text == NOT_FOUND_CONTENT


def test_specific_motds(motd_url: str, expected_motd_contents: dict[str, str]):
    """
    arrange: Deploy the motd-server-app charm.
    act: Get / with a specific user agent
    assert: The server returns the expected MOTD content.
    """
    for user_agent, expected_content in expected_motd_contents.items():
        res = requests.get(motd_url, timeout=5, headers={"User-Agent": user_agent})
        assert res.status_code == 200, f"Bad status for UA: {user_agent}"
        assert res.text == expected_content, f"Bad content for UA: {user_agent}"
