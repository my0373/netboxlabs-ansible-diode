# Contributing

Thank you for your interest in contributing to the NetBox Labs Diode Ansible Collection. This guide covers the architecture, how to extend the collection, and the pull request workflow.

## Architecture Overview

This collection follows the same structural patterns as the upstream [`netbox.netbox`](https://github.com/netbox-community/ansible_modules) collection:

| Layer | File(s) | Purpose |
|-------|---------|---------|
| **Doc fragments** | `plugins/doc_fragments/common.py` | Shared `DOCUMENTATION` blocks for connection params and entity format |
| **Arg specs** | `plugins/module_utils/arg_specs.py` | Reusable argument-spec dicts for `AnsibleModule` |
| **Entity builder** | `plugins/module_utils/entity_builder.py` | Maps user-facing `type` strings to SDK protobuf classes via `ENTITY_TYPE_MAP` |
| **Client helpers** | `plugins/module_utils/client.py` | Creates SDK clients and handles chunking |
| **Base class** | `plugins/module_utils/diode_module.py` | `DiodeModule` — handles SDK validation, entity building, client lifecycle, and error reporting |
| **Modules** | `plugins/modules/diode_*.py` | Thin wrappers: define `arg_spec`, create `DiodeModule`, call `run()` |

## Adding a New Entity Type

When the Diode SDK adds support for a new NetBox entity type, adding it to this collection requires a **single dictionary entry** — no new module files, no new tests.

### Step 1 — Update `ENTITY_TYPE_MAP`

Open `plugins/module_utils/entity_builder.py` and add the new type to the `ENTITY_TYPE_MAP` dictionary. The key is the user-facing `snake_case` name; the value is a tuple of `(sdk_kwarg_name, sdk_class)`:

```python
ENTITY_TYPE_MAP = {
    # ... existing entries ...
    "my_new_type": ("my_new_type", MyNewType if HAS_DIODE_SDK else None),
}
```

Also add the import at the top of the file inside the `try` / `except ImportError` block:

```python
try:
    from netboxlabs.diode.sdk.ingester import (
        # ... existing imports ...
        MyNewType,
    )
    HAS_DIODE_SDK = True
except ImportError:
    HAS_DIODE_SDK = False
```

### Step 2 — Verify

`SUPPORTED_ENTITY_TYPES` is auto-generated from `ENTITY_TYPE_MAP`, so it updates automatically. Run the tests to confirm:

```bash
make test
```

That's it. The existing modules (`diode_ingest`, `diode_dry_run`, `diode_replay`) and all tests automatically pick up the new type.

## Adding a New Module

If you need to add an entirely new module (not just a new entity type):

### Step 1 — Create the module file

Create `plugins/modules/diode_<name>.py` following the existing pattern:

```python
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.netboxlabs.diode.plugins.module_utils.arg_specs import (
    diode_connection_arg_spec,
    diode_entities_arg_spec,
)
from ansible_collections.netboxlabs.diode.plugins.module_utils.diode_module import (
    DiodeModule,
)


def main():
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
```

Use the doc fragments for shared documentation:

```yaml
extends_documentation_fragment:
  - netboxlabs.diode.common.DIODE_CONNECTION
  - netboxlabs.diode.common.ENTITIES
```

### Step 2 — Register in runtime.yml

Add the module to the action group in `meta/runtime.yml`:

```yaml
action_groups:
  diode:
    - diode_ingest
    - diode_dry_run
    - diode_replay
    - diode_info
    - diode_<name>    # add here
```

### Step 3 — Add tests

- Unit tests in `tests/unit/plugins/modules/test_diode_<name>.py`
- Molecule scenario in `extensions/molecule/<name>/` (optional but recommended)

See the [Testing Guide](docs/testing.md) for details.

## Development Setup

```bash
git clone https://github.com/my0373/netboxlabs-ansible-diode.git
cd netboxlabs-ansible-diode
make setup    # creates venv, installs deps, creates symlink
```

Or manually:

```bash
uv venv
source .venv/bin/activate
uv pip install ansible-core netboxlabs-diode-sdk pytest pytest-mock molecule
mkdir -p /tmp/ansible_collections/netboxlabs
ln -sf "$(pwd)" /tmp/ansible_collections/netboxlabs/diode
```

## Running Tests

```bash
make test          # unit tests
make molecule      # Molecule scenarios
make test-all      # everything
```

See the [Testing Guide](docs/testing.md) for full details.

## Branching Strategy

This project uses a two-branch model:

| Branch | Purpose |
|--------|---------|
| `main` | Stable, release-ready code. Tagged releases are cut from here. |
| `develop` | Integration branch. All feature/fix PRs target this branch. |

The typical flow is:

1. Create a feature branch from `develop`.
2. Open a PR against `develop`.
3. Once CI passes and the PR is approved, merge into `develop`.
4. When `develop` is ready for release, a maintainer opens a PR from
   `develop` into `main`.
5. After merging to `main`, tag the release (see [Releasing](docs/releasing.md)).

Both `main` and `develop` are protected branches — direct pushes are
blocked and all changes must go through a pull request with passing CI.

## Pull Request Workflow

1. **Fork** the repository and create a feature branch from `develop`.
2. **Make your changes** following the patterns described above.
3. **Add tests** for any new functionality.
4. **Run the full test suite** (`make test-all`) and ensure it passes.
5. **Open a pull request** against `develop` with a clear description of what changed and why.

### PR checklist

- [ ] Tests pass (`make test-all`)
- [ ] New functionality has test coverage
- [ ] Documentation updated if needed
- [ ] No secrets or credentials in the diff
- [ ] Commit messages are clear and descriptive

### Commit guidelines

- Use clear, descriptive commit messages.
- Follow [conventional commits](https://www.conventionalcommits.org/) where possible (e.g., `feat:`, `fix:`, `docs:`, `test:`).
- Each commit should represent a single logical change.

## Versioning and Releases

The collection version is pinned to the Diode SDK — collection `1.10.x`
requires SDK `>= 1.10.0`. See the [Release Guide](docs/releasing.md) for:

- The full versioning strategy
- Step-by-step release instructions
- How to set up the Galaxy API key
- Branch protection recommendations

Release PRs should update `galaxy.yml`, `requirements.txt`, and `CHANGELOG.rst`.
CI validates version consistency automatically.

## Reporting Issues

- Use [GitHub Issues](https://github.com/my0373/netboxlabs-ansible-diode/issues) for bug reports and feature requests.
- For security vulnerabilities, see [SECURITY.md](SECURITY.md).

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.
