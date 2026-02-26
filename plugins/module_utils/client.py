# -*- coding: utf-8 -*-
# Copyright 2024-2026 NetBox Labs Inc
# Apache License 2.0 (see LICENSE)

"""Wrapper helpers for creating Diode SDK clients from Ansible module params."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os

try:
    from netboxlabs.diode.sdk import (
        DiodeClient,
        DiodeDryRunClient,
        create_message_chunks,
    )

    HAS_DIODE_SDK = True
except ImportError:
    HAS_DIODE_SDK = False

SDK_IMPORT_ERROR = (
    "netboxlabs-diode-sdk is required but not installed. "
    "Install it with: pip install netboxlabs-diode-sdk"
)


def get_sdk_version():
    """Return the installed Diode SDK version string."""
    try:
        from importlib.metadata import version

        return version("netboxlabs-diode-sdk")
    except Exception:
        return "unknown"


def create_diode_client(params):
    """Create a DiodeClient from Ansible module params.

    Args:
        params: The ``module.params`` dict.

    Returns:
        A configured DiodeClient instance.

    Raises:
        ImportError: If the SDK is not installed.
    """
    if not HAS_DIODE_SDK:
        raise ImportError(SDK_IMPORT_ERROR)

    if params.get("skip_tls_verify"):
        os.environ["DIODE_SKIP_TLS_VERIFY"] = "true"

    kwargs = dict(
        target=params["target"],
        app_name=params["app_name"],
        app_version=params.get("app_version", "1.0.0"),
    )

    if params.get("client_id"):
        kwargs["client_id"] = params["client_id"]
    if params.get("client_secret"):
        kwargs["client_secret"] = params["client_secret"]
    if params.get("cert_file"):
        kwargs["cert_file"] = params["cert_file"]

    return DiodeClient(**kwargs)


def create_dry_run_client(params):
    """Create a DiodeDryRunClient from Ansible module params.

    Args:
        params: The ``module.params`` dict.

    Returns:
        A configured DiodeDryRunClient instance.

    Raises:
        ImportError: If the SDK is not installed.
    """
    if not HAS_DIODE_SDK:
        raise ImportError(SDK_IMPORT_ERROR)

    kwargs = dict(
        app_name=params.get("app_name", "dryrun"),
    )

    if params.get("output_dir"):
        kwargs["output_dir"] = params["output_dir"]

    return DiodeDryRunClient(**kwargs)


def ingest_with_chunking(client, entities, stream=None, metadata=None, chunk_size_mb=3.0):
    """Ingest entities, automatically chunking if needed.

    Args:
        client: A DiodeClient or DiodeDryRunClient instance.
        entities: List of Entity protobuf messages.
        stream: Optional stream name.
        metadata: Optional request-level metadata dict.
        chunk_size_mb: Max chunk size in MB.

    Returns:
        dict with ``ingested_count`` and ``errors`` keys.
    """
    errors = []
    ingested = 0

    if chunk_size_mb and chunk_size_mb > 0 and HAS_DIODE_SDK:
        chunks = list(create_message_chunks(entities, max_chunk_size_mb=chunk_size_mb))
    else:
        chunks = [entities]

    for chunk in chunks:
        kwargs = {}
        if stream is not None:
            kwargs["stream"] = stream
        if metadata is not None:
            kwargs["metadata"] = metadata

        response = client.ingest(entities=chunk, **kwargs)
        ingested += len(chunk)

        if hasattr(response, "errors") and response.errors:
            for err in response.errors:
                errors.append(str(err))

    return {
        "ingested_count": ingested,
        "chunk_count": len(chunks),
        "errors": errors,
    }
