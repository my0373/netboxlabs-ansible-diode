# -*- coding: utf-8 -*-
# Copyright 2024-2026 NetBox Labs Inc
# Apache License 2.0 (see LICENSE)

"""Base module class for Diode Ansible modules.

This follows the same pattern as ``netbox.netbox.NetboxModule`` -- a base
class that encapsulates common logic (SDK check, client creation, entity
building, error handling) so that individual module files stay thin and
easy to extend.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.my0373.diode.plugins.module_utils.client import (
    HAS_DIODE_SDK,
    SDK_IMPORT_ERROR,
    create_diode_client,
    create_dry_run_client,
    ingest_with_chunking,
)
from ansible_collections.my0373.diode.plugins.module_utils.entity_builder import (
    build_entities,
)


class DiodeModule(object):
    """Base helper for all Diode modules.

    Subclasses only need to call ``super().__init__()`` and then
    ``self.run()`` inside ``main()``.  The base class handles SDK
    validation, entity building, client lifecycle, and error reporting.

    Args:
        module: An ``AnsibleModule`` instance.
        mode:   One of ``"ingest"``, ``"dry_run"``, or ``"replay"``.
    """

    def __init__(self, module, mode):
        self.module = module
        self.mode = mode
        self.result = {"changed": False}

        if not HAS_DIODE_SDK:
            self.module.fail_json(msg=SDK_IMPORT_ERROR)

    def _create_client(self):
        """Create the appropriate SDK client for this mode."""
        try:
            if self.mode == "dry_run":
                return create_dry_run_client(self.module.params)
            return create_diode_client(self.module.params)
        except Exception as exc:
            self.module.fail_json(
                msg="Failed to create {0} client: {1}".format(self.mode, str(exc))
            )

    def _build_entities(self):
        """Convert raw entity dicts to SDK Entity objects."""
        try:
            return build_entities(self.module.params["entities"])
        except (ValueError, TypeError) as exc:
            self.module.fail_json(
                msg="Failed to build entities: {0}".format(str(exc))
            )

    def run(self):
        """Execute the module action.

        Concrete modules can override this if they need custom flow
        (e.g. ``diode_replay``), but most will just call ``super().run()``.
        """
        params = self.module.params

        if self.module.check_mode:
            self.module.exit_json(
                changed=True,
                ingested_count=len(params["entities"]),
                chunk_count=0,
                errors=[],
            )

        entities = self._build_entities()
        client = self._create_client()

        try:
            with client:
                result = ingest_with_chunking(
                    client=client,
                    entities=entities,
                    stream=params.get("stream"),
                    metadata=params.get("metadata"),
                    chunk_size_mb=params.get("chunk_size_mb", 3.0),
                )
        except Exception as exc:
            self.module.fail_json(
                msg="{0} failed: {1}".format(self.mode.replace("_", " ").title(), str(exc))
            )

        self.module.exit_json(
            changed=True,
            ingested_count=result["ingested_count"],
            chunk_count=result["chunk_count"],
            errors=result["errors"],
        )
