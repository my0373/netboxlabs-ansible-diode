# -*- coding: utf-8 -*-
# Copyright 2024-2026 NetBox Labs Inc
# Apache License 2.0 (see LICENSE)

"""Unit tests for the diode_dry_run module."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def module_args():
    return {
        "app_name": "test_dryrun",
        "output_dir": "/tmp/diode-test",
        "entities": [
            {"type": "site", "data": {"name": "Site-A", "status": "active"}},
        ],
        "metadata": None,
        "stream": None,
        "chunk_size_mb": 3.0,
    }


class TestDiodeDryRunCheckMode:
    @patch(
        "ansible_collections.netboxlabs.diode.plugins.module_utils.client.HAS_DIODE_SDK",
        True,
    )
    def test_check_mode_reports_entity_count(self, module_args):
        with patch(
            "ansible_collections.netboxlabs.diode.plugins.modules.diode_dry_run.AnsibleModule"
        ) as MockAM:
            mock_instance = MagicMock()
            mock_instance.params = module_args
            mock_instance.check_mode = True
            MockAM.return_value = mock_instance
            mock_instance.exit_json.side_effect = SystemExit(0)

            with pytest.raises(SystemExit):
                from ansible_collections.netboxlabs.diode.plugins.modules import (
                    diode_dry_run,
                )
                diode_dry_run.main()

            call_kwargs = mock_instance.exit_json.call_args[1]
            assert call_kwargs["changed"] is True
            assert call_kwargs["entity_count"] == 1
            assert call_kwargs["output_dir"] == "/tmp/diode-test"


class TestDiodeDryRunExecution:
    @patch(
        "ansible_collections.netboxlabs.diode.plugins.module_utils.client.HAS_DIODE_SDK",
        True,
    )
    @patch(
        "ansible_collections.netboxlabs.diode.plugins.modules.diode_dry_run.build_entities"
    )
    @patch(
        "ansible_collections.netboxlabs.diode.plugins.modules.diode_dry_run.create_dry_run_client"
    )
    @patch(
        "ansible_collections.netboxlabs.diode.plugins.modules.diode_dry_run.ingest_with_chunking"
    )
    def test_successful_dry_run(
        self, mock_ingest, mock_create_client, mock_build, module_args
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
            "ansible_collections.netboxlabs.diode.plugins.modules.diode_dry_run.AnsibleModule"
        ) as MockAM:
            mock_instance = MagicMock()
            mock_instance.params = module_args
            mock_instance.check_mode = False
            MockAM.return_value = mock_instance
            mock_instance.exit_json.side_effect = SystemExit(0)

            with pytest.raises(SystemExit):
                from ansible_collections.netboxlabs.diode.plugins.modules import (
                    diode_dry_run,
                )
                diode_dry_run.main()

            call_kwargs = mock_instance.exit_json.call_args[1]
            assert call_kwargs["changed"] is True
            assert call_kwargs["entity_count"] == 1

    @patch(
        "ansible_collections.netboxlabs.diode.plugins.module_utils.client.HAS_DIODE_SDK",
        True,
    )
    @patch(
        "ansible_collections.netboxlabs.diode.plugins.modules.diode_dry_run.build_entities",
        side_effect=ValueError("Bad type"),
    )
    def test_entity_build_failure(self, mock_build, module_args):
        with patch(
            "ansible_collections.netboxlabs.diode.plugins.modules.diode_dry_run.AnsibleModule"
        ) as MockAM:
            mock_instance = MagicMock()
            mock_instance.params = module_args
            mock_instance.check_mode = False
            MockAM.return_value = mock_instance
            mock_instance.fail_json.side_effect = SystemExit(1)

            with pytest.raises(SystemExit):
                from ansible_collections.netboxlabs.diode.plugins.modules import (
                    diode_dry_run,
                )
                diode_dry_run.main()

            assert "Bad type" in mock_instance.fail_json.call_args[1]["msg"]

    def test_fails_when_sdk_missing(self, module_args):
        with patch(
            "ansible_collections.netboxlabs.diode.plugins.modules.diode_dry_run.HAS_DIODE_SDK",
            False,
        ):
            with patch(
                "ansible_collections.netboxlabs.diode.plugins.modules.diode_dry_run.AnsibleModule"
            ) as MockAM:
                mock_instance = MagicMock()
                mock_instance.params = module_args
                mock_instance.check_mode = False
                MockAM.return_value = mock_instance
                mock_instance.fail_json.side_effect = SystemExit(1)

                with pytest.raises(SystemExit):
                    from ansible_collections.netboxlabs.diode.plugins.modules import (
                        diode_dry_run,
                    )
                    diode_dry_run.main()

                assert "netboxlabs-diode-sdk" in mock_instance.fail_json.call_args[1]["msg"]
