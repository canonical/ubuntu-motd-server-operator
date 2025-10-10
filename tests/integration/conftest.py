# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

"""Fixtures for charm integration tests."""
import typing
from collections.abc import Generator

import jubilant
import pytest

MOTD_APP_NAME = "ubuntu-motd-server"
MOTD_HEALTH_PATH = "/_health"
MOTD_PORT = 8000


@pytest.fixture(scope="session", name="juju")
def juju_fixture(request: pytest.FixtureRequest) -> Generator[jubilant.Juju, None, None]:
    """Juju controller interface fixture.

    Yields:
        Juju controller interface.
    """

    def show_debug_log(juju: jubilant.Juju):
        """Show the Juju debug log if any test failed.

        Args:
            juju: Juju controller interface.
        """
        if request.session.testsfailed:
            log = juju.debug_log(limit=1000)
            print(log, end="")

    use_existing = request.config.getoption("--use-existing", default=False)
    if use_existing:
        juju = jubilant.Juju()
        yield juju
        show_debug_log(juju)
        return

    model = request.config.getoption("--model")
    if model:
        juju = jubilant.Juju(model=model)
        yield juju
        show_debug_log(juju)
        return

    keep_models = typing.cast(bool, request.config.getoption("--keep-models"))
    with jubilant.temp_model(keep=keep_models) as juju:
        juju.wait_timeout = 10 * 60
        yield juju
        show_debug_log(juju)
        return


@pytest.fixture(scope="module", name="motd_charm")
def motd_charm_fixture(pytestconfig: pytest.Config) -> str:
    """Path to the MOTD charm to be deployed.

    Args:
        pytestconfig: Pytest configuration object.

    Returns:
        Path to the MOTD charm.
    """
    return pytestconfig.getoption("--charm-file")


@pytest.fixture(scope="module", name="motd_image")
def motd_image_fixture(pytestconfig: pytest.Config) -> str:
    """Container image for the MOTD server application.

    Args:
        pytestconfig: Pytest configuration object.

    Returns:
        Container image for the MOTD server application.
    """
    return pytestconfig.getoption("--motd-server-app-image")


@pytest.fixture(scope="module", name="motd_app")
def motd_app_fixture(
    request: pytest.FixtureRequest, motd_charm: str, motd_image: str, juju: jubilant.Juju
) -> str:
    """Deployed MOTD application fixture.

    Args:
        motd_charm: Path to the MOTD charm to be deployed.
        motd_image: Container image for the MOTD server application.
        juju: Juju controller interface.

    Returns:
        Deployed MOTD application.
    """
    resources = {"flask-app-image": motd_image}

    if request.config.getoption("--use-existing"):
        return MOTD_APP_NAME

    juju.deploy(
        motd_charm, resources=resources, config={"files": "@tests/integration/charm-files.yaml"}
    )
    juju.wait(
        lambda status: status.apps[MOTD_APP_NAME].app_status.current == "active",
        error=jubilant.any_blocked,
        timeout=1000,
    )

    return MOTD_APP_NAME


@pytest.fixture(scope="module", name="motd_url")
def motd_url_fixture(juju: jubilant.Juju, motd_app: str) -> str:
    """URL of the MOTD application."""
    status = juju.status()
    address = status.apps[motd_app].address
    return f"http://{address}:{MOTD_PORT}"


# This fixture should remain aligned with the one from the app
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
