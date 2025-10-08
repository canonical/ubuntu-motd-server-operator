# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

"""Tests for the Flask application serving Ubuntu MOTD content."""

import pytest

from app import HEALTH_CONTENT, HEALTH_PATH, app, process_config


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
    process_config()

    with app.test_client() as client:
        yield client


def test_health(client):
    """Test default behavior when no configuration is provided."""
    response = client.get(f"/{HEALTH_PATH}")
    assert response.status_code == 200
    assert response.data.decode() == HEALTH_CONTENT


def test_no_user_agent(client):
    """Test default behavior when no configuration is provided."""
    response = client.get("/", headers={"User-Agent": ""})
    assert response.status_code == 200
    assert response.data.decode() == "index"


def test_default_index(client):
    """Test default index route without specific user agent."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.data.decode() == "index"


def test_non_motd(client):
    """Test serving a non-MOTD file."""
    response = client.get("/aptnews.json")
    assert response.status_code == 200
    assert response.data.decode() == "apt news"


def test_motd(client):
    """Test serving a specific MOTD based on user agent."""
    response = client.get(
        "/", headers={"User-Agent": "curl/7.68.0 Ubuntu/22.04/amd64 cloud_id/aws"}
    )
    assert response.status_code == 200
    assert response.data.decode() == "22.04-amd64-aws\nadditional line"


def test_404(client):
    """Test 404 response for non-existing file."""
    response = client.get("/does_not_exist", headers={"User-Agent": ""})
    assert response.status_code == 404
    assert response.data.decode() == "Not found"
