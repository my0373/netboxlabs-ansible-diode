# -*- coding: utf-8 -*-
# Copyright 2024-2026 NetBox Labs Inc
# Apache License 2.0 (see LICENSE)

"""Unit tests for the diode_info module."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from unittest.mock import MagicMock, patch

import pytest


class TestDiodeInfoWithSdk:
    @patch(
        "ansible_collections.netboxlabs.diode.plugins.modules.diode_info.HAS_DIODE_SDK",
        True,
    )
    @patch(
        "ansible_collections.netboxlabs.diode.plugins.modules.diode_info.get_sdk_version",
        return_value="1.10.0",
    )
    @patch(
        "ansible_collections.netboxlabs.diode.plugins.modules.diode_info.SUPPORTED_ENTITY_TYPES",
        ["device", "ip_address", "site"],
    )
    def test_returns_sdk_info(self, mock_version):
        with patch(
            "ansible_collections.netboxlabs.diode.plugins.modules.diode_info.AnsibleModule"
        ) as MockAM:
            mock_instance = MagicMock()
            mock_instance.params = {}
            mock_instance.check_mode = False
            MockAM.return_value = mock_instance
            mock_instance.exit_json.side_effect = SystemExit(0)

            with pytest.raises(SystemExit):
                from ansible_collections.netboxlabs.diode.plugins.modules import (
                    diode_info,
                )
                diode_info.main()

            call_kwargs = mock_instance.exit_json.call_args[1]
            assert call_kwargs["changed"] is False
            assert call_kwargs["sdk_installed"] is True
            assert call_kwargs["sdk_version"] == "1.10.0"
            assert call_kwargs["supported_entity_types"] == [
                "device", "ip_address", "site"
            ]
            assert call_kwargs["entity_type_count"] == 3


class TestDiodeInfoWithoutSdk:
    @patch(
        "ansible_collections.netboxlabs.diode.plugins.modules.diode_info.HAS_DIODE_SDK",
        False,
    )
    def test_reports_sdk_not_installed(self):
        with patch(
            "ansible_collections.netboxlabs.diode.plugins.modules.diode_info.AnsibleModule"
        ) as MockAM:
            mock_instance = MagicMock()
            mock_instance.params = {}
            mock_instance.check_mode = False
            MockAM.return_value = mock_instance
            mock_instance.exit_json.side_effect = SystemExit(0)

            with pytest.raises(SystemExit):
                from ansible_collections.netboxlabs.diode.plugins.modules import (
                    diode_info,
                )
                diode_info.main()

            call_kwargs = mock_instance.exit_json.call_args[1]
            assert call_kwargs["changed"] is False
            assert call_kwargs["sdk_installed"] is False
            assert "not installed" in call_kwargs["msg"]


class TestDiodeInfoCheckMode:
    @patch(
        "ansible_collections.netboxlabs.diode.plugins.modules.diode_info.HAS_DIODE_SDK",
        True,
    )
    @patch(
        "ansible_collections.netboxlabs.diode.plugins.modules.diode_info.get_sdk_version",
        return_value="1.10.0",
    )
    @patch(
        "ansible_collections.netboxlabs.diode.plugins.modules.diode_info.SUPPORTED_ENTITY_TYPES",
        ["device"],
    )
    def test_check_mode_is_safe(self, mock_version):
        with patch(
            "ansible_collections.netboxlabs.diode.plugins.modules.diode_info.AnsibleModule"
        ) as MockAM:
            mock_instance = MagicMock()
            mock_instance.params = {}
            mock_instance.check_mode = True
            MockAM.return_value = mock_instance
            mock_instance.exit_json.side_effect = SystemExit(0)

            with pytest.raises(SystemExit):
                from ansible_collections.netboxlabs.diode.plugins.modules import (
                    diode_info,
                )
                diode_info.main()

            call_kwargs = mock_instance.exit_json.call_args[1]
            assert call_kwargs["changed"] is False
