# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

"""Unit tests for motd-server-app/utils.py."""

from motd_server.utils import get_mime_type


def test_json_mime_type():
    """
    arrange: a filename with a .json extension
    act: when we get its mime type
    assert: we get application/json
    """
    assert get_mime_type("file.json") == "application/json"


def test_default_mime_type():
    """
    arrange: a filename with a .non json extension
    act: when we get its mime type
    assert: we get text/plain
    """
    assert get_mime_type("file.xml") == "text/plain"
