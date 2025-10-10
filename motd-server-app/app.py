# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

"""Flask application for serving Ubuntu MOTD content based on user agent."""

import flask

from motd_server.flask import TextResponse
from motd_server.motd import extract_user_agent_info, process_config, select_motd
from motd_server.utils import get_mime_type

app = flask.Flask(__name__)
app.response_class = TextResponse
app.config.from_prefixed_env()
process_config(app.config)


@app.route("/")
def index() -> tuple[str | flask.Response, int]:
    """Serve MOTD content based on user agent information.

    Returns:
        MOTD content appropriate for the requesting system.
    """
    version, arch, cloud = extract_user_agent_info(flask.request.user_agent.string)

    motd = select_motd(app.config["PROCESSED_FILES"], version, arch, cloud)
    if motd:
        return motd, 200

    return "Not found", 404


@app.route("/<path:filename>")
def serve_file(filename: str) -> tuple[str | flask.Response, int]:
    """Serve non-MOTD files directly if they exist.

    Args:
        filename: Name of the file to serve.

    Returns:
        File content if found, otherwise 404 error.
    """
    if filename in app.config["PROCESSED_FILES"]:
        return (
            flask.Response(
                app.config["PROCESSED_FILES"][filename], mimetype=get_mime_type(filename)
            ),
            200,
        )

    return "Not found", 404
