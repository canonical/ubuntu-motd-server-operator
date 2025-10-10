# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

"""Fixtures for charm tests."""


def pytest_addoption(parser):
    """Parse additional pytest options.

    Args:
        parser: Pytest parser.
    """
    parser.addoption("--model", action="store")
    parser.addoption("--keep-models", action="store_true", default=False)
    parser.addoption("--charm-file", action="store")
    parser.addoption("--motd-server-app-image", action="store")
    parser.addoption("--use-existing", action="store_true", default=False)
