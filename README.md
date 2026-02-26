# NetBox Labs Diode Ansible Collection

[![CI](https://github.com/my0373/netboxlabs-ansible-diode/actions/workflows/ci.yml/badge.svg)](https://github.com/my0373/netboxlabs-ansible-diode/actions/workflows/ci.yml)
[![Security](https://github.com/my0373/netboxlabs-ansible-diode/actions/workflows/security.yml/badge.svg)](https://github.com/my0373/netboxlabs-ansible-diode/actions/workflows/security.yml)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

An Ansible collection for ingesting network data into [NetBox](https://netbox.dev) via the [Diode](https://netboxlabs.com/blog/introducing-diode-streamlining-data-ingestion-in-netbox/) ingestion service. It wraps the [Diode SDK for Python](https://github.com/netboxlabs/diode-sdk-python) and supports all 70+ NetBox entity types.

## Modules

| Module | Description |
|--------|-------------|
| `netboxlabs.diode.diode_ingest` | Ingest entities into NetBox via Diode |
| `netboxlabs.diode.diode_dry_run` | Write entities to JSON files for review |
| `netboxlabs.diode.diode_replay` | Replay dry-run JSON files into a live Diode instance |
| `netboxlabs.diode.diode_info` | Retrieve SDK version and supported entity types |

## Quick Start

```bash
# Install the collection and its Python dependency
ansible-galaxy collection install netboxlabs.diode
pip install netboxlabs-diode-sdk
```

```yaml
- name: Ingest a device into NetBox
  netboxlabs.diode.diode_ingest:
    target: "grpcs://diode.example.com/diode"
    app_name: "ansible-netbox"
    client_id: "{{ diode_client_id }}"
    client_secret: "{{ diode_client_secret }}"
    entities:
      - type: device
        data:
          name: "switch-01"
          device_type: "Catalyst 9300"
          site: "NYC-DC1"
          role: "access-switch"
          status: "active"
```

See the [Getting Started](docs/getting_started.md) guide for a full walkthrough.

## Documentation

| Document | Description |
|----------|-------------|
| [Getting Started](docs/getting_started.md) | Installation, first playbook, credentials setup |
| [User Guide](docs/user_guide.md) | Complete reference: all modules, entity types, authentication, TLS, chunking, workflows |
| [Testing Guide](docs/testing.md) | How to run unit tests, Molecule scenarios, and sanity tests |
| [Contributing](CONTRIBUTING.md) | Architecture overview, how to add entity types and modules, PR workflow |
| [Releasing](docs/releasing.md) | Version strategy, release process, Galaxy publishing |
| [Security Policy](SECURITY.md) | How to report vulnerabilities |
| [Code of Conduct](CODE_OF_CONDUCT.md) | Community standards |
| [Changelog](CHANGELOG.rst) | Release history |

## Compatibility

The collection version tracks the Diode SDK: collection `1.10.x` requires
SDK `>= 1.10.0, < 2.0.0`. See the [Release Guide](docs/releasing.md) for
details on the versioning strategy.

| Requirement | Minimum |
|-------------|---------|
| Ansible     | >= 2.15.0 |
| Python      | >= 3.10   |
| Diode SDK   | >= 1.10.0 |

## License

Apache License 2.0. See [LICENSE](LICENSE) for details.

## Links

- [Diode SDK for Python](https://github.com/netboxlabs/diode-sdk-python)
- [NetBox](https://netbox.dev)
- [NetBox Labs](https://netboxlabs.com)
