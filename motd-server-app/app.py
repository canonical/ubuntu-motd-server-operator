# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

"""Flask application for serving Ubuntu MOTD content based on user agent."""

import logging
import re

import flask
import yaml
from werkzeug.exceptions import HTTPException

DEFAULT_MOTD = "Default motd"

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

app = flask.Flask(__name__)
app.config.from_prefixed_env()


def get_motds_dict() -> dict[str, str]:
    """Load and parse MOTD configurations from environment.

    Returns:
        Dictionary mapping MOTD filenames to their content.
    """
    motds_env = app.config.get("MOTDS")
    if not motds_env:
        logger.warning("No motds found in environment")
        return {}

    try:
        raw_motds = yaml.safe_load(motds_env)
        motds = {target: "\n".join(content) for target, content in raw_motds.items()}
    except yaml.YAMLError as e:
        logger.error("Could not parse MOTDs: %s", e)
        return {}

    return motds


def extract_info(user_agent: str) -> tuple[str, str, str]:
    """Extract version, architecture, and cloud information from user agent.

    Args:
        user_agent: User agent string to parse.

    Returns:
        Tuple of (version, architecture, cloud_id).
    """
    version = re.search(r"Ubuntu/(\d{2}\.\d{2})", user_agent)
    arch = re.search(r"/(\w+) cloud_id", user_agent)
    cloud = re.search(r"cloud_id/(\w+)", user_agent)

    return (
        version.group(1) if version else "",
        arch.group(1) if arch else "",
        cloud.group(1) if cloud else "",
    )


def select_motd(motds: dict[str, str], version: str, arch: str, cloud: str) -> str:
    """Select appropriate MOTD based on version, architecture, and cloud.

    Matches MOTDs in order of specificity from most to least specific.

    Args:
        motds: Dictionary of available MOTDs.
        version: Ubuntu version (e.g., "24.04").
        arch: System architecture (e.g., "amd64").
        cloud: Cloud provider ID.

    Returns:
        Selected MOTD content or empty string if no match found.
    """
    # Try all combinations in order of specificity
    candidates = [
        f"index-{version}-{arch}-{cloud}.txt" if (version and arch and cloud) else None,
        f"index-{version}-{arch}.txt" if (version and arch) else None,
        f"index-{version}-{cloud}.txt" if (version and cloud) else None,
        f"index-{version}.txt" if version else None,
        f"index-{arch}.txt" if arch else None,
        f"index-{cloud}.txt" if cloud else None,
    ]

    for candidate in candidates:
        if candidate and candidate in motds:
            return motds[candidate]

    return ""


@app.route("/")
def index() -> str:
    """Serve MOTD content based on user agent information.

    Returns:
        MOTD content appropriate for the requesting system.
    """
    motds = get_motds_dict()
    logger.debug("Available MOTDs: %s", str(motds))

    if not motds or not flask.request.user_agent.string:
        return DEFAULT_MOTD

    user_agent_string = flask.request.user_agent.string
    version, arch, cloud = extract_info(user_agent_string)
    logger.debug("Extracted info - version: %s, arch: %s, cloud: %s", version, arch, cloud)

    motd = select_motd(motds, version, arch, cloud)

    if motd:
        logger.debug("Selected MOTD: %s characters", len(motd))
        return motd

    logger.debug("No matching MOTD found, returning default")
    return DEFAULT_MOTD


@app.errorhandler(404)
def page_not_found(exception: HTTPException) -> tuple[str, int]:  # pylint: disable=unused-argument
    """Handle 404 errors with a default MOTD response.

    Args:
        exception: The exception that was raised.

    Returns:
        Tuple of default MOTD and HTTP status code 200.
    """
    return index(), 200
