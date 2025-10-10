# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

"""Tests for the Flask application serving Ubuntu MOTD content."""

from motd_server.motd import HEALTH_CONTENT, HEALTH_PATH

MOTD_CONFIG = "../tests/integration/charm-files.yaml"
DEFAULT_MOTD = """index
This is a great MOTD
With a lot of interesting content
"""


def test_health(client):
    """
    arrange: given a motd server with a valid config
    act: when we call the health endpoint
    assert: then we get a 200 OK with the health content
    """
    response = client.get(f"/{HEALTH_PATH}")
    assert response.status_code == 200
    assert response.data.decode() == HEALTH_CONTENT
    assert response.content_type == "text/plain; charset=utf-8"


def test_no_user_agent(client):
    """
    arrange: given a motd server with a valid config
    act: when we call the root of the website with an empty user agent
    assert: then we get a 200 OK with the index.txt content
    """
    response = client.get("/", headers={"User-Agent": ""})
    assert response.status_code == 200
    assert response.data.decode() == DEFAULT_MOTD
    assert response.content_type == "text/plain; charset=utf-8"


def test_default_index(client):
    """
    arrange: given a motd server with a valid config
    act: when we call the root of the website with no user agent
    assert: then we get a 200 OK with the index.txt content
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.data.decode() == DEFAULT_MOTD
    assert response.content_type == "text/plain; charset=utf-8"


def test_non_motd(client):
    """
    arrange: given a motd server with a valid config
    act: when we call a non-motd file
    assert: then we get a 200 OK with the file content
    """
    response = client.get("/aptnews.json")
    assert response.status_code == 200
    assert response.data.decode() == '{ "key": "value" }'
    assert response.content_type == "application/json"


def test_motd(client, expected_motd_contents):
    """
    arrange: given a motd server with a valid config
    act: when we call a the root of the website with a user agent that matches a specific motd
    assert: then we get a 200 OK with the specific motd content
    """
    for user_agent, expected_content in expected_motd_contents.items():
        response = client.get("/", headers={"User-Agent": user_agent})
        assert response.status_code == 200
        assert response.data.decode() == expected_content
        assert response.content_type == "text/plain; charset=utf-8"


def test_404(client):
    """
    arrange: given a motd server with a valid config
    act: when we call a non existing file
    assert: then we get a 404 with "Not found" content
    """
    response = client.get("/does_not_exist", headers={"User-Agent": ""})
    assert response.status_code == 404
    assert response.data.decode() == "Not found"
    assert response.content_type == "text/plain; charset=utf-8"


def test_no_index(test_app, client):
    """
    arrange: given a motd server with no index.txt in the config
    act: when we call the root of the website
    assert: then we get a 404 with "Not found" content
    """
    test_app.config["PROCESSED_FILES"] = ""
    response = client.get("/", headers={"User-Agent": ""})
    assert response.data.decode() == "Not found"
    assert response.status_code == 404
    assert response.content_type == "text/plain; charset=utf-8"
