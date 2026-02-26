# -*- coding: utf-8 -*-
# Copyright 2024-2026 NetBox Labs Inc
# Apache License 2.0 (see LICENSE)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ModuleDocFragment(object):
    DIODE_CONNECTION = r"""
---
options:
  target:
    description:
      - The Diode gRPC service URL.
      - "Use C(grpc://) or C(http://) for insecure connections."
      - "Use C(grpcs://) or C(https://) for TLS-secured connections."
    type: str
    required: true
  app_name:
    description:
      - Application name sent to Diode as the producer identifier.
    type: str
    required: true
  app_version:
    description:
      - Application version sent to Diode as the producer version.
    type: str
    default: "1.0.0"
  client_id:
    description:
      - OAuth2 client ID for authentication.
      - Can also be set via the E(DIODE_CLIENT_ID) environment variable.
    type: str
  client_secret:
    description:
      - OAuth2 client secret for authentication.
      - Can also be set via the E(DIODE_CLIENT_SECRET) environment variable.
    type: str
  cert_file:
    description:
      - Path to a custom TLS certificate file.
      - Can also be set via the E(DIODE_CERT_FILE) environment variable.
    type: path
  skip_tls_verify:
    description:
      - Whether to skip TLS certificate verification.
      - Can also be set via the E(DIODE_SKIP_TLS_VERIFY) environment variable.
    type: bool
    default: false
requirements:
  - netboxlabs-diode-sdk >= 1.10.0
"""

    ENTITIES = r"""
---
options:
  entities:
    description:
      - List of entities to process.
      - Each entity is a dict with a C(type) key identifying the NetBox object
        type and a C(data) key containing the object's attributes.
      - The C(type) value uses snake_case (e.g. C(device), C(ip_address),
        C(virtual_machine)).
      - The C(data) dict is passed directly to the corresponding SDK class
        constructor so all SDK-supported fields are available.
      - For simple entities that accept a single primary value, C(data) can
        be a string instead of a dict.
    type: list
    elements: dict
    required: true
  metadata:
    description:
      - Optional request-level metadata attached to the request.
      - Useful for tracking batch IDs, data sources, or audit information.
    type: dict
  stream:
    description:
      - Optional stream name for the request.
    type: str
  chunk_size_mb:
    description:
      - Maximum size in megabytes for each gRPC message chunk.
      - Entities are automatically split into chunks of this size.
    type: float
    default: 3.0
"""
