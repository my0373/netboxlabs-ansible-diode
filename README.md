# NetBox Labs Diode Ansible Collection

[![CI](https://github.com/my0373/netboxlabs-ansible-diode/actions/workflows/ci.yml/badge.svg)](https://github.com/my0373/netboxlabs-ansible-diode/actions/workflows/ci.yml)
[![Security](https://github.com/my0373/netboxlabs-ansible-diode/actions/workflows/security.yml/badge.svg)](https://github.com/my0373/netboxlabs-ansible-diode/actions/workflows/security.yml)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Diode SDK](https://img.shields.io/badge/Diode_SDK->=1.10.0,_<2.0.0-green.svg)](https://github.com/netboxlabs/diode-sdk-python)

An Ansible collection for ingesting network data into [NetBox](https://netbox.dev) via the [Diode](https://netboxlabs.com/blog/introducing-diode-streamlining-data-ingestion-in-netbox/) ingestion service. It wraps the [Diode SDK for Python](https://github.com/netboxlabs/diode-sdk-python) (`netboxlabs-diode-sdk`) and supports all 70+ NetBox entity types.

## Modules

| Module | Description |
|--------|-------------|
| `my0373.diode.diode_ingest` | Ingest entities into NetBox via Diode |
| `my0373.diode.diode_dry_run` | Write entities to JSON files for review |
| `my0373.diode.diode_replay` | Replay dry-run JSON files into a live Diode instance |
| `my0373.diode.diode_info` | Retrieve SDK version and supported entity types |

## Quick Start

```bash
# Install the collection and its Python dependency
ansible-galaxy collection install my0373.diode
pip install netboxlabs-diode-sdk
```

```yaml
- name: Ingest a device into NetBox
  my0373.diode.diode_ingest:
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

This collection is built and tested against
[Diode SDK for Python](https://github.com/netboxlabs/diode-sdk-python)
**>= 1.10.0, < 2.0.0**. The collection version tracks the SDK: collection
`1.10.x` requires SDK `>= 1.10.0`. See the
[Release Guide](docs/releasing.md) for details on the versioning strategy.

| Requirement | Version |
|-------------|---------|
| [Diode SDK for Python](https://github.com/netboxlabs/diode-sdk-python) | >= 1.10.0, < 2.0.0 |
| Ansible     | >= 2.15.0 |
| Python      | >= 3.10   |

## License

Apache License 2.0. See [LICENSE](LICENSE) for details.

## Links

- [Diode SDK for Python](https://github.com/netboxlabs/diode-sdk-python)
- [NetBox](https://netbox.dev)
- [NetBox Labs](https://netboxlabs.com)
