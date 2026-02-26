#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2024-2026 NetBox Labs Inc
# Apache License 2.0 (see LICENSE)

"""Ansible module for ingesting entities into Diode."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: diode_ingest
short_description: Ingest entities into NetBox via Diode
version_added: "1.0.0"
description:
  - Ingest one or more entities into NetBox using the Diode ingestion service.
  - Supports all 70+ NetBox entity types including devices, sites, IP addresses,
    circuits, VLANs, and more.
  - Entities are sent via gRPC to a running Diode instance which processes them
    into NetBox.
  - Large entity lists are automatically chunked to stay within gRPC message
    size limits.
  - NetBox handles deduplication on the server side.
extends_documentation_fragment:
  - netboxlabs.diode.common.DIODE_CONNECTION
  - netboxlabs.diode.common.ENTITIES
author:
  - Matt York (@my0373)
  - NetBox Labs
"""

EXAMPLES = r"""
- name: Ingest a single device
  netboxlabs.diode.diode_ingest:
    target: "grpc://diode.example.com:8080/diode"
    app_name: "ansible-netbox"
    app_version: "1.0.0"
    entities:
      - type: device
        data:
          name: "switch-01"
          device_type: "Catalyst 9300"
          site: "NYC-DC1"
          role: "access-switch"
          status: "active"
          serial: "ABC123"
          tags:
            - managed
            - production

- name: Ingest multiple entity types in one call
  netboxlabs.diode.diode_ingest:
    target: "grpc://diode.example.com:8080/diode"
    app_name: "ansible-netbox"
    app_version: "1.0.0"
    client_id: "{{ diode_client_id }}"
    client_secret: "{{ diode_client_secret }}"
    entities:
      - type: site
        data:
          name: "NYC-DC1"
          status: "active"
      - type: device
        data:
          name: "switch-01"
          device_type: "Catalyst 9300"
          site: "NYC-DC1"
          role: "access-switch"
          status: "active"
      - type: ip_address
        data:
          address: "10.0.1.1/24"
          status: "active"
    metadata:
      source: "ansible"
      batch_id: "deploy-001"

- name: Ingest using string shorthand for simple entities
  netboxlabs.diode.diode_ingest:
    target: "grpc://diode.example.com:8080/diode"
    app_name: "ansible-netbox"
    entities:
      - type: site
        data: "NYC-DC1"
      - type: manufacturer
        data: "Cisco"
"""

RETURN = r"""
changed:
  description: Whether entities were sent to Diode.
  type: bool
  returned: always
  sample: true
ingested_count:
  description: Total number of entities sent to Diode.
  type: int
  returned: success
  sample: 5
chunk_count:
  description: Number of gRPC message chunks used.
  type: int
  returned: success
  sample: 1
errors:
  description: List of error messages from the Diode service, if any.
  type: list
  elements: str
  returned: always
  sample: []
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.netboxlabs.diode.plugins.module_utils.arg_specs import (
    diode_connection_arg_spec,
    diode_entities_arg_spec,
)
from ansible_collections.netboxlabs.diode.plugins.module_utils.diode_module import (
    DiodeModule,
)


def main():
    """Main entry point for module execution."""
    arg_spec = {}
    arg_spec.update(diode_connection_arg_spec())
    arg_spec.update(diode_entities_arg_spec())

    module = AnsibleModule(
        argument_spec=arg_spec,
        supports_check_mode=True,
    )

    diode = DiodeModule(module, "ingest")
    diode.run()


if __name__ == "__main__":
    main()
