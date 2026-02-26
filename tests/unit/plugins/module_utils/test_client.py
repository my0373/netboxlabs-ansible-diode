# -*- coding: utf-8 -*-
# Copyright 2024-2026 NetBox Labs Inc
# Apache License 2.0 (see LICENSE)

"""Unit tests for client module_utils."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os
from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def mock_sdk():
    """Provide mocked SDK classes for client tests."""
    mock_diode_client_cls = MagicMock()
    mock_dry_run_client_cls = MagicMock()
    mock_create_chunks = MagicMock()

    with patch.dict("sys.modules", {
        "netboxlabs": MagicMock(),
        "netboxlabs.diode": MagicMock(),
        "netboxlabs.diode.sdk": MagicMock(
            DiodeClient=mock_diode_client_cls,
            DiodeDryRunClient=mock_dry_run_client_cls,
            create_message_chunks=mock_create_chunks,
        ),
    }):
        import sys
        mod_name = "ansible_collections.my0373.diode.plugins.module_utils.client"
        if mod_name in sys.modules:
            del sys.modules[mod_name]

        from ansible_collections.my0373.diode.plugins.module_utils import client
        client.HAS_DIODE_SDK = True
        client.DiodeClient = mock_diode_client_cls
        client.DiodeDryRunClient = mock_dry_run_client_cls
        client.create_message_chunks = mock_create_chunks

        yield {
            "client_module": client,
            "DiodeClient": mock_diode_client_cls,
            "DiodeDryRunClient": mock_dry_run_client_cls,
            "create_message_chunks": mock_create_chunks,
        }


class TestCreateDiodeClient:
    def test_creates_client_with_required_params(self, mock_sdk):
        client_mod = mock_sdk["client_module"]
        params = {
            "target": "grpc://localhost:8080/diode",
            "app_name": "test-app",
            "app_version": "1.0.0",
            "client_id": None,
            "client_secret": None,
            "cert_file": None,
            "skip_tls_verify": False,
        }
        client_mod.create_diode_client(params)
        mock_sdk["DiodeClient"].assert_called_once_with(
            target="grpc://localhost:8080/diode",
            app_name="test-app",
            app_version="1.0.0",
        )

    def test_creates_client_with_auth(self, mock_sdk):
        client_mod = mock_sdk["client_module"]
        params = {
            "target": "grpc://localhost:8080/diode",
            "app_name": "test-app",
            "app_version": "1.0.0",
            "client_id": "my-id",
            "client_secret": "my-secret",
            "cert_file": None,
            "skip_tls_verify": False,
        }
        client_mod.create_diode_client(params)
        mock_sdk["DiodeClient"].assert_called_once_with(
            target="grpc://localhost:8080/diode",
            app_name="test-app",
            app_version="1.0.0",
            client_id="my-id",
            client_secret="my-secret",
        )

    def test_creates_client_with_cert(self, mock_sdk):
        client_mod = mock_sdk["client_module"]
        params = {
            "target": "grpcs://example.com",
            "app_name": "test-app",
            "app_version": "1.0.0",
            "client_id": None,
            "client_secret": None,
            "cert_file": "/path/to/cert.pem",
            "skip_tls_verify": False,
        }
        client_mod.create_diode_client(params)
        mock_sdk["DiodeClient"].assert_called_once_with(
            target="grpcs://example.com",
            app_name="test-app",
            app_version="1.0.0",
            cert_file="/path/to/cert.pem",
        )

    def test_skip_tls_verify_sets_env(self, mock_sdk):
        client_mod = mock_sdk["client_module"]
        params = {
            "target": "grpcs://example.com",
            "app_name": "test-app",
            "app_version": "1.0.0",
            "client_id": None,
            "client_secret": None,
            "cert_file": None,
            "skip_tls_verify": True,
        }
        with patch.dict(os.environ, {}, clear=False):
            client_mod.create_diode_client(params)
            assert os.environ.get("DIODE_SKIP_TLS_VERIFY") == "true"

    def test_raises_when_sdk_missing(self, mock_sdk):
        client_mod = mock_sdk["client_module"]
        client_mod.HAS_DIODE_SDK = False
        with pytest.raises(ImportError, match="netboxlabs-diode-sdk"):
            client_mod.create_diode_client({"target": "x", "app_name": "x"})
        client_mod.HAS_DIODE_SDK = True


class TestCreateDryRunClient:
    def test_creates_with_defaults(self, mock_sdk):
        client_mod = mock_sdk["client_module"]
        params = {"app_name": "dryrun", "output_dir": None}
        client_mod.create_dry_run_client(params)
        mock_sdk["DiodeDryRunClient"].assert_called_once_with(app_name="dryrun")

    def test_creates_with_output_dir(self, mock_sdk):
        client_mod = mock_sdk["client_module"]
        params = {"app_name": "my_import", "output_dir": "/tmp/output"}
        client_mod.create_dry_run_client(params)
        mock_sdk["DiodeDryRunClient"].assert_called_once_with(
            app_name="my_import",
            output_dir="/tmp/output",
        )

    def test_raises_when_sdk_missing(self, mock_sdk):
        client_mod = mock_sdk["client_module"]
        client_mod.HAS_DIODE_SDK = False
        with pytest.raises(ImportError, match="netboxlabs-diode-sdk"):
            client_mod.create_dry_run_client({"app_name": "x"})
        client_mod.HAS_DIODE_SDK = True


class TestIngestWithChunking:
    def test_single_chunk_ingest(self, mock_sdk):
        client_mod = mock_sdk["client_module"]
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.errors = []
        mock_client.ingest.return_value = mock_response

        entities = [MagicMock(), MagicMock()]
        mock_sdk["create_message_chunks"].return_value = [entities]

        result = client_mod.ingest_with_chunking(mock_client, entities)

        assert result["ingested_count"] == 2
        assert result["chunk_count"] == 1
        assert result["errors"] == []

    def test_multi_chunk_ingest(self, mock_sdk):
        client_mod = mock_sdk["client_module"]
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.errors = []
        mock_client.ingest.return_value = mock_response

        chunk1 = [MagicMock(), MagicMock()]
        chunk2 = [MagicMock()]
        mock_sdk["create_message_chunks"].return_value = [chunk1, chunk2]

        result = client_mod.ingest_with_chunking(
            mock_client, chunk1 + chunk2, chunk_size_mb=1.0
        )

        assert result["ingested_count"] == 3
        assert result["chunk_count"] == 2
        assert mock_client.ingest.call_count == 2

    def test_ingest_with_errors(self, mock_sdk):
        client_mod = mock_sdk["client_module"]
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.errors = ["error1", "error2"]
        mock_client.ingest.return_value = mock_response

        mock_sdk["create_message_chunks"].return_value = [[MagicMock()]]

        result = client_mod.ingest_with_chunking(mock_client, [MagicMock()])

        assert len(result["errors"]) == 2

    def test_ingest_with_metadata_and_stream(self, mock_sdk):
        client_mod = mock_sdk["client_module"]
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.errors = []
        mock_client.ingest.return_value = mock_response

        entities = [MagicMock()]
        mock_sdk["create_message_chunks"].return_value = [entities]

        result = client_mod.ingest_with_chunking(
            mock_client,
            entities,
            stream="my-stream",
            metadata={"key": "value"},
        )

        mock_client.ingest.assert_called_once_with(
            entities=entities,
            stream="my-stream",
            metadata={"key": "value"},
        )


class TestGetSdkVersion:
    def test_returns_version_string(self, mock_sdk):
        client_mod = mock_sdk["client_module"]
        with patch(
            "importlib.metadata.version",
            return_value="1.10.0",
        ):
            result = client_mod.get_sdk_version()
            assert result == "1.10.0"

    def test_returns_unknown_on_error(self, mock_sdk):
        client_mod = mock_sdk["client_module"]
        with patch(
            "importlib.metadata.version",
            side_effect=Exception("not found"),
        ):
            result = client_mod.get_sdk_version()
            assert result == "unknown"
