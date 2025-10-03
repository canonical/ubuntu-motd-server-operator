#!/usr/bin/env python3
# Copyright 2025 Ubuntu
# See LICENSE file for licensing details.

"""Flask Charm entrypoint."""

import logging

import ops
import paas_charm.flask

logger = logging.getLogger(__name__)


class UbuntuMotdServerCharm(paas_charm.flask.Charm):
    """Flask Charm service."""


if __name__ == "__main__":
    ops.main(UbuntuMotdServerCharm)
