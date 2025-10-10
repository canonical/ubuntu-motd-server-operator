# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

import flask


class TextResponse(flask.Response):
    """Custom Flask response class to set default mimetype to text/plain.

    Attributes:
        default_mimetype: Default MIME type for responses.
    """

    default_mimetype = "text/plain"
