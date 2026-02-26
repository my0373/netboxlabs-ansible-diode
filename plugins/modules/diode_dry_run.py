#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2024-2026 NetBox Labs Inc
# Apache License 2.0 (see LICENSE)

"""Ansible module for writing Diode entities to JSON files (dry run)."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: diode_dry_run
short_description: Write Diode entities to JSON files without ingesting
version_added: "1.0.0"
description:
  - Generate JSON files representing Diode ingestion requests without actually
    sending them to a Diode service.
  - Useful for previewing, auditing, or archiving what would be ingested.
  - The generated files can later be replayed using M(netboxlabs.diode.diode_replay).
  - File names follow the pattern C(<app_name>_<timestamp_ns>.json).
extends_documentation_fragment:
  - netboxlabs.diode.common.ENTITIES
options:
  app_name:
    description:
      - Application name used as the filename prefix for generated JSON files.
    type: str
    default: "dryrun"
  output_dir:
    description:
      - Directory where JSON files will be written.
      - Can also be set via the E(DIODE_DRY_RUN_OUTPUT_DIR) environment variable.
      - "If not set, output is printed to stdout."
    type: path
requirements:
  - netboxlabs-diode-sdk >= 1.10.0
author:
  - Matt York (@my0373)
  - NetBox Labs
"""

EXAMPLES = r"""
- name: Dry run - write devices to JSON file
  netboxlabs.diode.diode_dry_run:
    app_name: "my_import"
    output_dir: "/tmp/diode-dryrun"
    entities:
      - type: device
        data:
          name: "switch-01"
          device_type: "Catalyst 9300"
          site: "NYC-DC1"
          role: "access-switch"
          status: "active"
"""

RETURN = r"""
changed:
  description: Whether files were written.
  type: bool
  returned: always
  sample: true
entity_count:
  description: Number of entities written to the dry-run output.
  type: int
  returned: success
  sample: 3
output_dir:
  description: Directory where files were written, if set.
  type: str
  returned: success
  sample: "/tmp/diode-dryrun"
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.netboxlabs.diode.plugins.module_utils.arg_specs import (
    diode_dry_run_arg_spec,
    diode_entities_arg_spec,
)
from ansible_collections.netboxlabs.diode.plugins.module_utils.client import (
    HAS_DIODE_SDK,
    SDK_IMPORT_ERROR,
    create_dry_run_client,
    ingest_with_chunking,
)
from ansible_collections.netboxlabs.diode.plugins.module_utils.entity_builder import (
    build_entities,
)


def main():
    """Main entry point for module execution."""
    arg_spec = {}
    arg_spec.update(diode_dry_run_arg_spec())
    arg_spec.update(diode_entities_arg_spec())

    module = AnsibleModule(
        argument_spec=arg_spec,
        supports_check_mode=True,
    )

    if not HAS_DIODE_SDK:
        module.fail_json(msg=SDK_IMPORT_ERROR)

    if module.check_mode:
        module.exit_json(
            changed=True,
            entity_count=len(module.params["entities"]),
            output_dir=module.params.get("output_dir", ""),
        )

    try:
        entities = build_entities(module.params["entities"])
    except (ValueError, TypeError) as exc:
        module.fail_json(msg="Failed to build entities: {0}".format(str(exc)))

    try:
        client = create_dry_run_client(module.params)
    except Exception as exc:
        module.fail_json(
            msg="Failed to create dry-run client: {0}".format(str(exc))
        )

    try:
        with client:
            result = ingest_with_chunking(
                client=client,
                entities=entities,
                stream=module.params.get("stream"),
                metadata=module.params.get("metadata"),
                chunk_size_mb=module.params.get("chunk_size_mb", 3.0),
            )
    except Exception as exc:
        module.fail_json(msg="Dry run failed: {0}".format(str(exc)))

    module.exit_json(
        changed=True,
        entity_count=result["ingested_count"],
        output_dir=module.params.get("output_dir", ""),
    )


if __name__ == "__main__":
    main()
