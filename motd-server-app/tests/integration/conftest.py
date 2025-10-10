# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

"""Generated expected results for integration tests."""

from pathlib import Path

import pytest

from app import app
from motd_server.motd import process_config

MOTD_CONFIG = "../tests/integration/charm-files.yaml"


@pytest.fixture(name="test_app")
def app_fixture():
    """Flask app fixture.

    Yields:
        Flask app.
    """
    yield app


@pytest.fixture(name="client")
def client_fixture(test_app):
    """Flask test client fixture.

    Yields:
        Flask test client.
    """
    test_app.config["TESTING"] = True
    test_app.config["FILES"] = Path(MOTD_CONFIG).read_text(encoding="utf-8")
    process_config(test_app.config)

    with test_app.test_client() as client:
        yield client


@pytest.fixture(name="expected_motd_contents")
def generate_expected_contents() -> dict[str, str]:
    """Generate expected content for all combinations of version, arch, cloud."""
    expected_contents = {}
    # Example UA:
    # wget/1.21.4-1ubuntu4.1 Ubuntu/24.04.1/LTS GNU/Linux/6.8.0-1021-aws/aarch64 cloud_id/aws
    for version in ["", "22.04", "24.04"]:
        for arch in ["", "amd64", "arm64", "s390x"]:
            for cloud in ["", "aws", "azure", "gcp"]:
                if arch and not cloud:
                    continue

                expected_content = "index"
                user_agent = "wget/1.21.4-1ubuntu4.1"

                if version:
                    expected_content += f"-{version}"
                    user_agent += f" Ubuntu/{version}"
                if arch:
                    expected_content += f"-{arch}"
                    user_agent += f" GNU/Linux/6.8.0/{arch}"
                if cloud:
                    expected_content += f"-{cloud}"
                    user_agent += f" cloud_id/{cloud}"

                expected_content += (
                    "\n" + "This is a great MOTD\nWith a lot of interesting content\n"
                )
                expected_contents[user_agent] = expected_content

    return expected_contents
