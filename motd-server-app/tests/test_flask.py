# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

"""Tests for the Flask application serving Ubuntu MOTD content."""

import pytest

from app import app
from motd_server.motd import HEALTH_CONTENT, HEALTH_PATH, process_config


@pytest.fixture(name="client")
def client_fixture():
    """Flask test client fixture.

    Yields:
        Flask test client.
    """
    app.config["TESTING"] = True
    app.config[
        "FILES"
    ] = f"""index.txt: index
index-22.04-amd64-aws.txt:
- 22.04-amd64-aws
- additional line
aptnews.json: apt news
{HEALTH_PATH}: {HEALTH_CONTENT}
    """
    process_config(app)

    with app.test_client() as client:
        yield client


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
    assert response.data.decode() == "index"
    assert response.content_type == "text/plain; charset=utf-8"


def test_default_index(client):
    """
    arrange: given a motd server with a valid config
    act: when we call the root of the website with no user agent
    assert: then we get a 200 OK with the index.txt content
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.data.decode() == "index"
    assert response.content_type == "text/plain; charset=utf-8"


def test_non_motd(client):
    """
    arrange: given a motd server with a valid config
    act: when we call a non-motd file
    assert: then we get a 200 OK with the file content
    """
    response = client.get("/aptnews.json")
    assert response.status_code == 200
    assert response.data.decode() == "apt news"
    assert response.content_type == "application/json"


def test_motd(client):
    """
    arrange: given a motd server with a valid config
    act: when we call a the root of the website with a user agent that matches a specific motd
    assert: then we get a 200 OK with the specific motd content
    """
    response = client.get(
        "/", headers={"User-Agent": "curl/7.68.0 Ubuntu/22.04/amd64 cloud_id/aws"}
    )
    assert response.status_code == 200
    assert response.data.decode() == "22.04-amd64-aws\nadditional line"
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


def test_no_index(client):
    """
    arrange: given a motd server with no index.txt in the config
    act: when we call the root of the website
    assert: then we get a 404 with "Not found" content
    """
    app.config["PROCESSED_FILES"] = ""
    response = client.get("/", headers={"User-Agent": ""})
    assert response.data.decode() == "Not found"
    assert response.status_code == 404
    assert response.content_type == "text/plain; charset=utf-8"
