#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2024-2026 NetBox Labs Inc
# Apache License 2.0 (see LICENSE)

"""Ansible module for retrieving Diode SDK information."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: diode_info
short_description: Retrieve Diode SDK and connection information
version_added: "1.0.0"
description:
  - Returns information about the installed Diode SDK, including the version
    and all supported entity types.
  - Useful for validating that the SDK is installed and discovering available
    entity types for use with M(my0373.diode.diode_ingest).
  - This module makes no changes and requires no connection parameters.
options: {}
requirements:
  - netboxlabs-diode-sdk >= 1.10.0
author:
  - Matt York (@my0373)
  - NetBox Labs
"""

EXAMPLES = r"""
- name: Get Diode SDK information
  my0373.diode.diode_info:
  register: diode_sdk_info

- name: Display SDK version
  ansible.builtin.debug:
    msg: "Diode SDK version: {{ diode_sdk_info.sdk_version }}"

- name: Display supported entity types
  ansible.builtin.debug:
    msg: "Supported types: {{ diode_sdk_info.supported_entity_types }}"
"""

RETURN = r"""
sdk_installed:
  description: Whether the Diode SDK is installed.
  type: bool
  returned: always
  sample: true
sdk_version:
  description: The installed Diode SDK version.
  type: str
  returned: when SDK is installed
  sample: "1.10.0"
supported_entity_types:
  description: List of entity type names accepted by the ingest modules.
  type: list
  elements: str
  returned: when SDK is installed
  sample:
    - device
    - ip_address
    - site
entity_type_count:
  description: Number of supported entity types.
  type: int
  returned: when SDK is installed
  sample: 73
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.my0373.diode.plugins.module_utils.client import (
    HAS_DIODE_SDK,
    get_sdk_version,
)
from ansible_collections.my0373.diode.plugins.module_utils.entity_builder import (
    SUPPORTED_ENTITY_TYPES,
)


def main():
    module = AnsibleModule(
        argument_spec={},
        supports_check_mode=True,
    )

    result = dict(
        changed=False,
        sdk_installed=HAS_DIODE_SDK,
    )

    if HAS_DIODE_SDK:
        result["sdk_version"] = get_sdk_version()
        result["supported_entity_types"] = SUPPORTED_ENTITY_TYPES
        result["entity_type_count"] = len(SUPPORTED_ENTITY_TYPES)
    else:
        result["msg"] = (
            "netboxlabs-diode-sdk is not installed. "
            "Install it with: pip install netboxlabs-diode-sdk"
        )

    module.exit_json(**result)


if __name__ == "__main__":
    main()
