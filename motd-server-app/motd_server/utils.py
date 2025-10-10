# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

"""Utility functions for the MOTD server application."""


def get_mime_type(filename: str) -> str:
    """Get the MIME type based on the file extension.
    In MOTD server, we only handle .json and plain text files.

    Args:
        filename: Name of the file.

    Returns:
        Corresponding MIME type as a string.
    """
    if filename.endswith(".json"):
        return "application/json"
    else:
        return "text/plain"
