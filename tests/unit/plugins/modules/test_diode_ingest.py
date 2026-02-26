# -*- coding: utf-8 -*-
# Copyright 2024-2026 NetBox Labs Inc
# Apache License 2.0 (see LICENSE)

"""Unit tests for the diode_ingest module."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
from unittest.mock import MagicMock, patch

import pytest

from ansible.module_utils import basic as ansible_basic


@pytest.fixture
def module_args():
    """Return default module arguments."""
    return {
        "target": "grpc://localhost:8080/diode",
        "app_name": "test-app",
        "app_version": "1.0.0",
        "client_id": None,
        "client_secret": None,
        "cert_file": None,
        "skip_tls_verify": False,
        "entities": [
            {"type": "device", "data": {"name": "switch-01", "status": "active"}},
        ],
        "metadata": None,
        "stream": None,
        "chunk_size_mb": 3.0,
    }


@pytest.fixture
def mock_module(module_args):
    """Patch AnsibleModule for testing."""
    args = json.dumps({"ANSIBLE_MODULE_ARGS": module_args})
    with patch.object(ansible_basic, "_ANSIBLE_ARGS", args.encode("utf-8")):
        yield module_args


DIODE_MOD = "ansible_collections.my0373.diode.plugins.module_utils.diode_module"


class TestDiodeIngestCheckMode:
    @patch("{0}.HAS_DIODE_SDK".format(DIODE_MOD), True)
    def test_check_mode_returns_changed(self, mock_module):
        with patch(
            "ansible_collections.my0373.diode.plugins.modules.diode_ingest.AnsibleModule"
        ) as MockAM:
            mock_instance = MagicMock()
            mock_instance.params = mock_module
            mock_instance.check_mode = True
            MockAM.return_value = mock_instance
            mock_instance.exit_json.side_effect = SystemExit(0)

            with pytest.raises(SystemExit):
                from ansible_collections.my0373.diode.plugins.modules import (
                    diode_ingest,
                )
                diode_ingest.main()

            call_kwargs = mock_instance.exit_json.call_args[1]
            assert call_kwargs["changed"] is True
            assert call_kwargs["ingested_count"] == 1


class TestDiodeIngestExecution:
    @patch("{0}.HAS_DIODE_SDK".format(DIODE_MOD), True)
    @patch("{0}.build_entities".format(DIODE_MOD))
    @patch("{0}.create_diode_client".format(DIODE_MOD))
    @patch("{0}.ingest_with_chunking".format(DIODE_MOD))
    def test_successful_ingestion(
        self, mock_ingest, mock_create_client, mock_build, mock_module
    ):
        mock_build.return_value = [MagicMock()]
        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_create_client.return_value = mock_client
        mock_ingest.return_value = {
            "ingested_count": 1,
            "chunk_count": 1,
            "errors": [],
        }

        with patch(
            "ansible_collections.my0373.diode.plugins.modules.diode_ingest.AnsibleModule"
        ) as MockAM:
            mock_instance = MagicMock()
            mock_instance.params = mock_module
            mock_instance.check_mode = False
            MockAM.return_value = mock_instance
            mock_instance.exit_json.side_effect = SystemExit(0)

            with pytest.raises(SystemExit):
                from ansible_collections.my0373.diode.plugins.modules import (
                    diode_ingest,
                )
                diode_ingest.main()

            mock_instance.exit_json.assert_called_once()
            call_kwargs = mock_instance.exit_json.call_args[1]
            assert call_kwargs["changed"] is True
            assert call_kwargs["ingested_count"] == 1
            assert call_kwargs["errors"] == []

    @patch("{0}.HAS_DIODE_SDK".format(DIODE_MOD), True)
    @patch("{0}.build_entities".format(DIODE_MOD))
    @patch("{0}.create_diode_client".format(DIODE_MOD))
    @patch("{0}.ingest_with_chunking".format(DIODE_MOD))
    def test_ingestion_with_errors(
        self, mock_ingest, mock_create_client, mock_build, mock_module
    ):
        mock_build.return_value = [MagicMock()]
        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_create_client.return_value = mock_client
        mock_ingest.return_value = {
            "ingested_count": 1,
            "chunk_count": 1,
            "errors": ["some error"],
        }

        with patch(
            "ansible_collections.my0373.diode.plugins.modules.diode_ingest.AnsibleModule"
        ) as MockAM:
            mock_instance = MagicMock()
            mock_instance.params = mock_module
            mock_instance.check_mode = False
            MockAM.return_value = mock_instance
            mock_instance.exit_json.side_effect = SystemExit(0)

            with pytest.raises(SystemExit):
                from ansible_collections.my0373.diode.plugins.modules import (
                    diode_ingest,
                )
                diode_ingest.main()

            call_kwargs = mock_instance.exit_json.call_args[1]
            assert call_kwargs["changed"] is True
            assert len(call_kwargs["errors"]) == 1

    @patch("{0}.HAS_DIODE_SDK".format(DIODE_MOD), True)
    @patch("{0}.build_entities".format(DIODE_MOD), side_effect=ValueError("Bad entity"))
    def test_entity_build_failure(self, mock_build, mock_module):
        with patch(
            "ansible_collections.my0373.diode.plugins.modules.diode_ingest.AnsibleModule"
        ) as MockAM:
            mock_instance = MagicMock()
            mock_instance.params = mock_module
            mock_instance.check_mode = False
            MockAM.return_value = mock_instance
            mock_instance.fail_json.side_effect = SystemExit(1)

            with pytest.raises(SystemExit):
                from ansible_collections.my0373.diode.plugins.modules import (
                    diode_ingest,
                )
                diode_ingest.main()

            mock_instance.fail_json.assert_called_once()
            assert "Bad entity" in mock_instance.fail_json.call_args[1]["msg"]

    @patch("{0}.HAS_DIODE_SDK".format(DIODE_MOD), False)
    def test_fails_when_sdk_missing(self, mock_module):
        with patch(
            "ansible_collections.my0373.diode.plugins.modules.diode_ingest.AnsibleModule"
        ) as MockAM:
            mock_instance = MagicMock()
            mock_instance.params = mock_module
            mock_instance.check_mode = False
            MockAM.return_value = mock_instance
            mock_instance.fail_json.side_effect = SystemExit(1)

            with pytest.raises(SystemExit):
                from ansible_collections.my0373.diode.plugins.modules import (
                    diode_ingest,
                )
                diode_ingest.main()

            mock_instance.fail_json.assert_called_once()
            assert "netboxlabs-diode-sdk" in mock_instance.fail_json.call_args[1]["msg"]
