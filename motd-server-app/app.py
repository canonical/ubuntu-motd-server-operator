# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

"""Flask application for serving Ubuntu MOTD content based on user agent."""

import re

import flask
import yaml

DEFAULT_MOTD = "Default motd"


app = flask.Flask(__name__)
app.config.from_prefixed_env()


def get_files_from_yaml(files_string: str) -> dict[str, str]:
    """Load files from a YAML string.

    Args:
        files_string: YAML string defining files.

    Returns:
        Dictionary mapping of filenames to their content.
    """
    files = {"index.txt": DEFAULT_MOTD}

    if not files_string:
        app.logger.warning("No files found in environment")
        return files

    try:
        raw_files = yaml.safe_load(files_string)
        files.update({target: "\n".join(content) for target, content in raw_files.items()})
    except yaml.YAMLError as e:
        app.logger.error("Could not parse MOTDs: %s", e)
        return files

    return files


app.config["FILES"] = get_files_from_yaml(app.config.get("FILES") or "")


def extract_user_agent_info(user_agent: str) -> tuple[str, str, str]:
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


def select_motd(files: dict, version: str, arch: str, cloud: str) -> str:
    """Select appropriate MOTD based on version, architecture, and cloud.

    Matches MOTDs in order of specificity from most to least specific.

    Args:
        files: Dictionary of available files.
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
        if candidate and candidate in files:
            return files[candidate]

    return ""


@app.route("/")
def index() -> str:
    """Serve MOTD content based on user agent information.

    Returns:
        MOTD content appropriate for the requesting system.
    """
    if not app.config["FILES"] or not flask.request.user_agent.string:
        return DEFAULT_MOTD

    version, arch, cloud = extract_user_agent_info(flask.request.user_agent.string)

    motd = select_motd(app.config["FILES"], version, arch, cloud)
    if motd:
        return motd

    return DEFAULT_MOTD


@app.route("/<path:filename>")
def serve_file(filename: str) -> tuple[str, int]:
    """Serve non-MOTD files directly if they exist.

    Args:
        filename: Name of the file to serve.

    Returns:
        File content if found, otherwise 404 error.
    """
    if filename in app.config["FILES"]:
        return app.config["FILES"][filename]

    return "Not found", 404
