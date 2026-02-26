# User Guide

Complete reference for the `my0373.diode` Ansible collection.

## Table of Contents

- [Module Reference](#module-reference)
  - [diode_ingest](#diode_ingest)
  - [diode_dry_run](#diode_dry_run)
  - [diode_replay](#diode_replay)
  - [diode_info](#diode_info)
- [Entity Format](#entity-format)
- [Supported Entity Types](#supported-entity-types)
- [Connection Parameters](#connection-parameters)
- [Authentication](#authentication)
- [TLS Configuration](#tls-configuration)
- [Message Chunking](#message-chunking)
- [Check Mode](#check-mode)
- [Workflows](#workflows)

---

## Module Reference

### diode_ingest

Ingest one or more entities into NetBox via the Diode gRPC service. This is the primary module in the collection.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `target` | str | yes | — | Diode gRPC URL |
| `app_name` | str | yes | — | Producer application name |
| `app_version` | str | no | `1.0.0` | Producer version |
| `client_id` | str | no | — | OAuth2 client ID |
| `client_secret` | str | no | — | OAuth2 client secret |
| `cert_file` | path | no | — | Custom TLS certificate path |
| `skip_tls_verify` | bool | no | `false` | Skip TLS verification |
| `entities` | list | yes | — | Entities to ingest (see [Entity Format](#entity-format)) |
| `metadata` | dict | no | — | Request-level metadata |
| `stream` | str | no | — | Stream name |
| `chunk_size_mb` | float | no | `3.0` | Max gRPC message chunk size |

**Return values:**

| Key | Type | Description |
|-----|------|-------------|
| `changed` | bool | Whether entities were sent |
| `ingested_count` | int | Total entities sent |
| `chunk_count` | int | Number of gRPC chunks used |
| `errors` | list | Error messages from Diode, if any |

**Example:**

```yaml
- name: Ingest network infrastructure
  my0373.diode.diode_ingest:
    target: "grpcs://diode.example.com/diode"
    app_name: "ansible-netbox"
    client_id: "{{ vault_client_id }}"
    client_secret: "{{ vault_client_secret }}"
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
    metadata:
      source: "ansible"
      batch_id: "deploy-001"
```

### diode_dry_run

Generate JSON files representing what *would* be ingested without connecting to Diode. Files can later be reviewed and replayed using `diode_replay`.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `app_name` | str | no | `dryrun` | Filename prefix for generated files |
| `output_dir` | path | no | — | Directory for JSON output |
| `entities` | list | yes | — | Entities to write |
| `metadata` | dict | no | — | Request-level metadata |
| `stream` | str | no | — | Stream name |
| `chunk_size_mb` | float | no | `3.0` | Max chunk size |

**Return values:**

| Key | Type | Description |
|-----|------|-------------|
| `changed` | bool | Whether files were written |
| `entity_count` | int | Number of entities written |
| `output_dir` | str | Directory where files were written |

**Example:**

```yaml
- name: Preview entities before ingesting
  my0373.diode.diode_dry_run:
    app_name: "audit"
    output_dir: "/tmp/diode-preview"
    entities:
      - type: device
        data:
          name: "new-switch"
          device_type: "EX4300"
          site: "ORD-DC1"
          role: "access-switch"
          status: "active"
```

### diode_replay

Replay one or more dry-run JSON files into a live Diode instance. This enables a review-then-apply workflow.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `target` | str | yes | — | Diode gRPC URL |
| `app_name` | str | yes | — | Producer application name |
| `app_version` | str | no | `1.0.0` | Producer version |
| `client_id` | str | no | — | OAuth2 client ID |
| `client_secret` | str | no | — | OAuth2 client secret |
| `cert_file` | path | no | — | Custom TLS certificate path |
| `skip_tls_verify` | bool | no | `false` | Skip TLS verification |
| `files` | list | yes | — | Paths to dry-run JSON files |
| `chunk_size_mb` | float | no | `3.0` | Max chunk size |

**Return values:**

| Key | Type | Description |
|-----|------|-------------|
| `changed` | bool | Whether entities were ingested |
| `total_ingested` | int | Total entities ingested across all files |
| `files_processed` | int | Number of files processed |
| `errors` | list | Error messages, if any |

**Example:**

```yaml
- name: Apply approved dry-run files
  my0373.diode.diode_replay:
    target: "grpcs://diode.example.com/diode"
    app_name: "ansible-replay"
    files:
      - "/tmp/diode-preview/audit_1706123456.json"
```

### diode_info

Return information about the installed Diode SDK. Takes no parameters and makes no changes.

**Return values:**

| Key | Type | Description |
|-----|------|-------------|
| `sdk_installed` | bool | Whether the SDK is installed |
| `sdk_version` | str | Installed SDK version |
| `supported_entity_types` | list | All supported entity type names |
| `entity_type_count` | int | Number of supported types |

**Example:**

```yaml
- my0373.diode.diode_info:
  register: info

- ansible.builtin.debug:
    msg: "SDK v{{ info.sdk_version }} — {{ info.entity_type_count }} types"
```

---

## Entity Format

Each entity in the `entities` list is a dictionary with two keys:

- **`type`** — The entity type in `snake_case` (e.g., `device`, `ip_address`, `virtual_machine`)
- **`data`** — Either a dictionary of attributes or a string shorthand

### Full form

```yaml
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
```

### String shorthand

For entities that accept a single primary value (usually `name`), `data` can be a string:

```yaml
- type: site
  data: "NYC-DC1"

- type: manufacturer
  data: "Cisco"
```

### Entity-level metadata

Individual entities can carry metadata in their `data` dictionary:

```yaml
- type: device
  data:
    name: "switch-01"
    device_type: "Catalyst 9300"
    site: "NYC-DC1"
    metadata:
      discovered_by: "network_scan"
      scan_date: "2026-01-15"
```

### Nested references

Entities can reference related objects by name:

```yaml
- type: device
  data:
    name: "switch-01"
    device_type: "Catalyst 9300"   # references a DeviceType
    site: "NYC-DC1"                 # references a Site
    manufacturer: "Cisco"           # references a Manufacturer
    role: "access-switch"           # references a DeviceRole
    platform: "IOS-XE"             # references a Platform
```

Diode resolves these references server-side, creating objects as needed.

---

## Supported Entity Types

The collection supports all entity types available in the Diode SDK (90+). Use `diode_info` to get the complete list for your installed SDK version.

**Devices & Hardware:** `device`, `device_type`, `device_role`, `device_bay`, `device_config`, `manufacturer`, `platform`, `module`, `module_bay`, `module_type`, `module_type_profile`, `console_port`, `console_server_port`, `power_port`, `power_outlet`, `power_feed`, `power_panel`, `front_port`, `rear_port`, `inventory_item`, `inventory_item_role`

**Sites & Locations:** `site`, `site_group`, `location`, `region`, `rack`, `rack_role`, `rack_type`, `rack_reservation`

**Networking:** `interface`, `ip_address`, `ip_range`, `prefix`, `vlan`, `vlan_group`, `vlan_translation_policy`, `vlan_translation_rule`, `vrf`, `route_target`, `asn`, `asn_range`, `aggregate`, `mac_address`, `fhrp_group`, `fhrp_group_assignment`, `vm_interface`

**Circuits:** `circuit`, `circuit_type`, `circuit_group`, `circuit_group_assignment`, `circuit_termination`, `provider`, `provider_account`, `provider_network`, `rir`

**Virtualization:** `virtual_machine`, `virtual_disk`, `virtual_chassis`, `virtual_circuit`, `virtual_circuit_type`, `virtual_circuit_termination`, `virtual_device_context`, `cluster`, `cluster_group`, `cluster_type`

**VPN:** `tunnel`, `tunnel_group`, `tunnel_termination`, `ike_policy`, `ike_proposal`, `ip_sec_policy`, `ip_sec_profile`, `ip_sec_proposal`, `l2vpn`, `l2vpn_termination`

**Wireless:** `wireless_lan`, `wireless_lan_group`, `wireless_link`

**Contacts & Tenants:** `contact`, `contact_group`, `contact_role`, `contact_assignment`, `tenant`, `tenant_group`

**Other:** `tag`, `role`, `service`, `cable`, `cable_path`, `cable_termination`, `custom_field`, `custom_field_choice_set`, `custom_link`, `journal_entry`, `owner`, `owner_group`

---

## Connection Parameters

All modules that connect to Diode (`diode_ingest`, `diode_replay`) accept these parameters:

| Parameter | Type | Required | Default | Env Variable |
|-----------|------|----------|---------|--------------|
| `target` | str | yes | — | — |
| `app_name` | str | yes | — | — |
| `app_version` | str | no | `1.0.0` | — |
| `client_id` | str | no | — | `DIODE_CLIENT_ID` |
| `client_secret` | str | no | — | `DIODE_CLIENT_SECRET` |
| `cert_file` | path | no | — | `DIODE_CERT_FILE` |
| `skip_tls_verify` | bool | no | `false` | `DIODE_SKIP_TLS_VERIFY` |

---

## Authentication

Diode uses OAuth2 for authentication. Provide credentials either as module parameters or environment variables.

### Module parameters

```yaml
- my0373.diode.diode_ingest:
    target: "grpcs://diode.example.com/diode"
    app_name: "my-app"
    client_id: "{{ vault_diode_client_id }}"
    client_secret: "{{ vault_diode_client_secret }}"
    entities: [...]
```

### Environment variables

```bash
export DIODE_CLIENT_ID="your-client-id"
export DIODE_CLIENT_SECRET="your-client-secret"
```

The `client_secret` parameter is marked `no_log: true`, so Ansible will never print it in output or logs.

---

## TLS Configuration

TLS is controlled by the target URL scheme:

| Scheme | TLS |
|--------|-----|
| `grpcs://` or `https://` | Enabled |
| `grpc://` or `http://` | Disabled |

### Custom CA certificate

```yaml
- my0373.diode.diode_ingest:
    target: "grpcs://diode.internal.com/diode"
    cert_file: "/etc/ssl/certs/diode-ca.pem"
    ...
```

### Skip verification (not recommended for production)

```yaml
- my0373.diode.diode_ingest:
    target: "grpcs://diode.internal.com/diode"
    skip_tls_verify: true
    ...
```

---

## Message Chunking

When ingesting large numbers of entities, the collection automatically splits them into chunks to stay within gRPC message size limits. The default chunk size is 3 MB.

```yaml
- my0373.diode.diode_ingest:
    target: "grpcs://diode.example.com/diode"
    app_name: "bulk-import"
    chunk_size_mb: 2.0    # adjust if needed
    entities: [...]       # thousands of entities
```

---

## Check Mode

All modules support Ansible's `--check` flag. In check mode:

- `diode_ingest` reports what would be ingested without sending anything
- `diode_dry_run` reports what would be written without creating files
- `diode_replay` reports what would be replayed without sending anything
- `diode_info` behaves identically (it's always read-only)

```bash
ansible-playbook site.yml --check
```

---

## Workflows

### Direct ingestion

The simplest pattern: ingest entities directly.

```yaml
- my0373.diode.diode_ingest:
    target: "{{ diode_target }}"
    app_name: "direct-import"
    entities:
      - type: site
        data:
          name: "NYC-DC1"
          status: "active"
```

### Dry-run and replay

A two-phase workflow for reviewing changes before applying them.

```yaml
# Phase 1: Generate preview
- my0373.diode.diode_dry_run:
    app_name: "audit"
    output_dir: "/tmp/diode-audit"
    entities:
      - type: device
        data:
          name: "new-switch"
          device_type: "EX4300"
          site: "ORD-DC1"

# Phase 2: Review /tmp/diode-audit/*.json manually

# Phase 3: Apply
- my0373.diode.diode_replay:
    target: "{{ diode_target }}"
    app_name: "audit-apply"
    files:
      - "/tmp/diode-audit/audit_1706123456.json"
```

### Bulk import from variables

Build entity lists dynamically from Ansible variables:

```yaml
vars:
  sites:
    - { name: "NYC-DC1", status: "active" }
    - { name: "LAX-DC1", status: "active" }
    - { name: "ORD-DC1", status: "planned" }

tasks:
  - my0373.diode.diode_ingest:
      target: "{{ diode_target }}"
      app_name: "bulk-import"
      entities: "{{ sites | map('combine', {}) | map('dict2items') | map('items2dict') | zip(sites | map('extract', {}, default='site')) | list }}"
```

See `playbooks/examples/bulk_ingest.yml` for a full working example.

### Request metadata

Attach audit metadata to any ingestion request:

```yaml
- my0373.diode.diode_ingest:
    target: "{{ diode_target }}"
    app_name: "audit-import"
    entities: [...]
    metadata:
      source: "ansible"
      batch_id: "DEPLOY-2026-001"
      operator: "{{ ansible_user_id }}"
      timestamp: "{{ ansible_date_time.iso8601 }}"
```
