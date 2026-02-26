# Testing Guide

This guide covers how to run the test suite and how to add tests when contributing new functionality.

## Prerequisites

```bash
# Create and activate a virtual environment
uv venv
source .venv/bin/activate

# Install all development dependencies
uv pip install ansible-core netboxlabs-diode-sdk pytest pytest-mock molecule

# Create the collection symlink so Ansible can find the collection
mkdir -p /tmp/ansible_collections/netboxlabs
ln -sf "$(pwd)" /tmp/ansible_collections/netboxlabs/diode
```

Or use the Makefile shortcut:

```bash
make setup
```

## Running Tests

### Quick reference

```bash
make test          # Run unit tests
make molecule      # Run all Molecule scenarios
make lint          # Run sanity checks
make test-all      # Run everything
```

### Unit Tests

Unit tests live in `tests/unit/` and use `pytest` with mocked SDK classes. They run without any network or Diode instance.

```bash
PYTHONPATH=/tmp:$PYTHONPATH pytest tests/unit/ -v
```

To run a specific test file or class:

```bash
PYTHONPATH=/tmp:$PYTHONPATH pytest tests/unit/plugins/modules/test_diode_ingest.py -v
PYTHONPATH=/tmp:$PYTHONPATH pytest tests/unit/plugins/module_utils/test_entity_builder.py::TestBuildEntity -v
```

**What's tested:**

| Test File | Coverage |
|-----------|----------|
| `test_client.py` | Client creation, TLS config, chunking, SDK version detection |
| `test_entity_builder.py` | Entity type mapping, all 90+ types, error handling |
| `test_diode_ingest.py` | Check mode, successful ingestion, error propagation, SDK-missing |
| `test_diode_dry_run.py` | Check mode, file generation, entity build failure, SDK-missing |
| `test_diode_replay.py` | Check mode, replay execution, missing files, corrupt files, SDK-missing |
| `test_diode_info.py` | SDK-installed and SDK-missing paths, check mode |

### Molecule Tests

Molecule tests are integration-style tests that run actual Ansible playbooks against the collection. They live in `extensions/molecule/`.

```bash
# Run all scenarios
molecule test --all

# Run a specific scenario
molecule test -s default
molecule test -s dry_run
molecule test -s ingest
```

**Scenarios:**

| Scenario | What It Tests |
|----------|---------------|
| `default` | SDK availability, entity type discovery, check mode for single/multi/shorthand entities |
| `dry_run` | File creation, JSON structure validation, check mode no-write guarantee, metadata support |
| `ingest` | All entity categories (DCIM, IPAM, virtualization, circuits, VPN, wireless), error handling |

> **Note:** Molecule tests run locally against `localhost`. They test entity building and validation but do not require a live Diode instance. The `ingest` scenario uses `check_mode` for ingestion tests.

### Sanity Tests

If you have `ansible-test` available:

```bash
ansible-test sanity --docker default
```

### Integration Tests

Integration tests in `tests/integration/` require a live Diode instance:

```bash
ansible-test integration --docker default
```

## Test Architecture

### How unit tests work

Unit tests mock the Diode SDK entirely. The `mock_sdk` fixture in `test_client.py` patches `sys.modules` to inject mock classes for `DiodeClient`, `DiodeDryRunClient`, and `create_message_chunks`. This lets tests run without installing the SDK.

Module tests patch `AnsibleModule` to capture `exit_json` and `fail_json` calls, then assert on the keyword arguments.

### How Molecule tests work

Each Molecule scenario has:

- `molecule.yml` — scenario config (driver, provisioner, test sequence)
- `converge.yml` — setup tasks (must be idempotent for the idempotence step)
- `verify.yml` — assertion tasks that validate the converge results

The provisioner sets `ANSIBLE_COLLECTIONS_PATH=/tmp` and points `ansible_python_interpreter` at the project's `.venv` to ensure the SDK is available.

## Adding Tests

### For a new entity type

No new tests needed. The existing `test_all_entity_types_buildable` test in `test_entity_builder.py` automatically covers all entries in `ENTITY_TYPE_MAP`.

### For a new module

1. Create `tests/unit/plugins/modules/test_diode_<name>.py`
2. Follow the patterns in `test_diode_ingest.py`:
   - Test check mode behavior
   - Test successful execution
   - Test error handling (entity build failure, SDK missing)
3. Optionally create a Molecule scenario in `extensions/molecule/<name>/`

### Test conventions

- Use `pytest` fixtures for shared setup
- Mock the SDK — never import it directly in tests
- Use `SystemExit` as the boundary for `exit_json`/`fail_json` assertions
- Keep test names descriptive: `test_<what>_<condition>` (e.g., `test_check_mode_returns_changed`)
