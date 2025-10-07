#!/usr/bin/env python3

# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

"""Integration tests."""

import logging
from pathlib import Path

import pytest
import requests
import yaml

logger = logging.getLogger(__name__)

CHARMCRAFT_DATA = yaml.safe_load(Path("./charmcraft.yaml").read_text(encoding="utf-8"))
APP_NAME = CHARMCRAFT_DATA["name"]

MOTD_HEALTH_CONTENT = "OK"


@pytest.mark.abort_on_fail
def test_health(motd_url: str):
    """
    arrange: Deploy the motd-server-app charm.
    act: Get the _health endpoint.
    assert: The _health endpoint returns 200 OK.
    """
    res = requests.get(motd_url, timeout=5)
    assert res.status_code == 200
    assert res.text == MOTD_HEALTH_CONTENT
