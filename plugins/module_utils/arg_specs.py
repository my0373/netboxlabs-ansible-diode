# -*- coding: utf-8 -*-
# Copyright 2024-2026 NetBox Labs Inc
# Apache License 2.0 (see LICENSE)

"""Shared argument specifications for Diode connection parameters."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type


def diode_connection_arg_spec():
    """Return argument spec for Diode connection parameters."""
    return dict(
        target=dict(
            type="str",
            required=True,
        ),
        app_name=dict(
            type="str",
            required=True,
        ),
        app_version=dict(
            type="str",
            default="1.0.0",
        ),
        client_id=dict(
            type="str",
        ),
        client_secret=dict(
            type="str",
            no_log=True,
        ),
        cert_file=dict(
            type="path",
        ),
        skip_tls_verify=dict(
            type="bool",
            default=False,
        ),
    )


def diode_dry_run_arg_spec():
    """Return argument spec for DiodeDryRunClient parameters."""
    return dict(
        app_name=dict(
            type="str",
            default="dryrun",
        ),
        output_dir=dict(
            type="path",
        ),
    )


def diode_entities_arg_spec():
    """Return argument spec for entity ingestion parameters."""
    return dict(
        entities=dict(
            type="list",
            required=True,
            elements="dict",
        ),
        metadata=dict(
            type="dict",
        ),
        stream=dict(
            type="str",
        ),
        chunk_size_mb=dict(
            type="float",
            default=3.0,
        ),
    )
