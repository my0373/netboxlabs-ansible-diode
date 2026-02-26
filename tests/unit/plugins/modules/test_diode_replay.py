# -*- coding: utf-8 -*-
# Copyright 2024-2026 NetBox Labs Inc
# Apache License 2.0 (see LICENSE)

"""Unit tests for the diode_replay module."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os
from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def module_args(tmp_path):
    test_file = tmp_path / "test_dryrun.json"
    test_file.write_text('{"entities": []}')
    return {
        "target": "grpc://localhost:8080/diode",
        "app_name": "replay-test",
        "app_version": "1.0.0",
        "client_id": None,
        "client_secret": None,
        "cert_file": None,
        "skip_tls_verify": False,
        "files": [str(test_file)],
        "chunk_size_mb": 3.0,
    }


class TestDiodeReplayCheckMode:
    @patch(
        "ansible_collections.netboxlabs.diode.plugins.module_utils.client.HAS_DIODE_SDK",
        True,
    )
    @patch(
        "ansible_collections.netboxlabs.diode.plugins.modules.diode_replay.HAS_LOAD_DRYRUN",
        True,
    )
    def test_check_mode_reports_file_count(self, module_args):
        with patch(
            "ansible_collections.netboxlabs.diode.plugins.modules.diode_replay.AnsibleModule"
        ) as MockAM:
            mock_instance = MagicMock()
            mock_instance.params = module_args
            mock_instance.check_mode = True
            MockAM.return_value = mock_instance
            mock_instance.exit_json.side_effect = SystemExit(0)

            with pytest.raises(SystemExit):
                from ansible_collections.netboxlabs.diode.plugins.modules import (
                    diode_replay,
                )
                diode_replay.main()

            call_kwargs = mock_instance.exit_json.call_args[1]
            assert call_kwargs["changed"] is True
            assert call_kwargs["files_processed"] == 1


class TestDiodeReplayExecution:
    @patch(
        "ansible_collections.netboxlabs.diode.plugins.module_utils.client.HAS_DIODE_SDK",
        True,
    )
    @patch(
        "ansible_collections.netboxlabs.diode.plugins.modules.diode_replay.HAS_LOAD_DRYRUN",
        True,
    )
    @patch(
        "ansible_collections.netboxlabs.diode.plugins.modules.diode_replay.load_dryrun_entities"
    )
    @patch(
        "ansible_collections.netboxlabs.diode.plugins.modules.diode_replay.create_diode_client"
    )
    @patch(
        "ansible_collections.netboxlabs.diode.plugins.modules.diode_replay.ingest_with_chunking"
    )
    def test_successful_replay(
        self, mock_ingest, mock_create_client, mock_load, module_args
    ):
        mock_load.return_value = [MagicMock(), MagicMock()]
        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_create_client.return_value = mock_client
        mock_ingest.return_value = {
            "ingested_count": 2,
            "chunk_count": 1,
            "errors": [],
        }

        with patch(
            "ansible_collections.netboxlabs.diode.plugins.modules.diode_replay.AnsibleModule"
        ) as MockAM:
            mock_instance = MagicMock()
            mock_instance.params = module_args
            mock_instance.check_mode = False
            MockAM.return_value = mock_instance
            mock_instance.exit_json.side_effect = SystemExit(0)

            with pytest.raises(SystemExit):
                from ansible_collections.netboxlabs.diode.plugins.modules import (
                    diode_replay,
                )
                diode_replay.main()

            call_kwargs = mock_instance.exit_json.call_args[1]
            assert call_kwargs["changed"] is True
            assert call_kwargs["total_ingested"] == 2
            assert call_kwargs["files_processed"] == 1
            assert call_kwargs["errors"] == []

    @patch(
        "ansible_collections.netboxlabs.diode.plugins.module_utils.client.HAS_DIODE_SDK",
        True,
    )
    @patch(
        "ansible_collections.netboxlabs.diode.plugins.modules.diode_replay.HAS_LOAD_DRYRUN",
        True,
    )
    def test_fails_on_missing_file(self):
        args = {
            "target": "grpc://localhost:8080/diode",
            "app_name": "replay-test",
            "app_version": "1.0.0",
            "client_id": None,
            "client_secret": None,
            "cert_file": None,
            "skip_tls_verify": False,
            "files": ["/nonexistent/file.json"],
            "chunk_size_mb": 3.0,
        }

        with patch(
            "ansible_collections.netboxlabs.diode.plugins.modules.diode_replay.AnsibleModule"
        ) as MockAM:
            mock_instance = MagicMock()
            mock_instance.params = args
            mock_instance.check_mode = False
            MockAM.return_value = mock_instance
            mock_instance.fail_json.side_effect = SystemExit(1)

            with pytest.raises(SystemExit):
                from ansible_collections.netboxlabs.diode.plugins.modules import (
                    diode_replay,
                )
                diode_replay.main()

            assert "File not found" in mock_instance.fail_json.call_args[1]["msg"]

    @patch(
        "ansible_collections.netboxlabs.diode.plugins.module_utils.client.HAS_DIODE_SDK",
        True,
    )
    @patch(
        "ansible_collections.netboxlabs.diode.plugins.modules.diode_replay.HAS_LOAD_DRYRUN",
        True,
    )
    @patch(
        "ansible_collections.netboxlabs.diode.plugins.modules.diode_replay.load_dryrun_entities",
        side_effect=Exception("Corrupt JSON"),
    )
    @patch(
        "ansible_collections.netboxlabs.diode.plugins.modules.diode_replay.create_diode_client"
    )
    def test_handles_corrupt_file(
        self, mock_create_client, mock_load, module_args
    ):
        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_create_client.return_value = mock_client

        with patch(
            "ansible_collections.netboxlabs.diode.plugins.modules.diode_replay.AnsibleModule"
        ) as MockAM:
            mock_instance = MagicMock()
            mock_instance.params = module_args
            mock_instance.check_mode = False
            MockAM.return_value = mock_instance
            mock_instance.exit_json.side_effect = SystemExit(0)

            with pytest.raises(SystemExit):
                from ansible_collections.netboxlabs.diode.plugins.modules import (
                    diode_replay,
                )
                diode_replay.main()

            call_kwargs = mock_instance.exit_json.call_args[1]
            assert call_kwargs["files_processed"] == 0
            assert len(call_kwargs["errors"]) == 1
            assert "Corrupt JSON" in call_kwargs["errors"][0]

    def test_fails_when_sdk_missing(self, module_args):
        with patch(
            "ansible_collections.netboxlabs.diode.plugins.modules.diode_replay.HAS_DIODE_SDK",
            False,
        ):
            with patch(
                "ansible_collections.netboxlabs.diode.plugins.modules.diode_replay.AnsibleModule"
            ) as MockAM:
                mock_instance = MagicMock()
                mock_instance.params = module_args
                mock_instance.check_mode = False
                MockAM.return_value = mock_instance
                mock_instance.fail_json.side_effect = SystemExit(1)

                with pytest.raises(SystemExit):
                    from ansible_collections.netboxlabs.diode.plugins.modules import (
                        diode_replay,
                    )
                    diode_replay.main()

                assert "netboxlabs-diode-sdk" in mock_instance.fail_json.call_args[1]["msg"]
