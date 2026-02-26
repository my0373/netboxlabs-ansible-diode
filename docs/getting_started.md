# Getting Started

This guide walks you through installing the collection, configuring credentials, and running your first playbook.

## Prerequisites

- **Ansible** >= 2.15.0
- **Python** >= 3.10
- A running **Diode** instance with connectivity to your NetBox deployment
- **OAuth2 credentials** (client ID and client secret) for your Diode instance

## Installation

### 1. Install the collection

```bash
ansible-galaxy collection install netboxlabs.diode
```

Or install from a local build:

```bash
git clone https://github.com/netboxlabs/netboxlabs-ansible-diode.git
cd netboxlabs-ansible-diode
ansible-galaxy collection build
ansible-galaxy collection install netboxlabs-diode-*.tar.gz
```

### 2. Install the Python SDK

```bash
pip install netboxlabs-diode-sdk
```

### 3. Verify the installation

```yaml
# verify_install.yml
- hosts: localhost
  connection: local
  gather_facts: false
  tasks:
    - name: Check Diode SDK
      netboxlabs.diode.diode_info:
      register: info

    - ansible.builtin.debug:
        msg: "SDK v{{ info.sdk_version }} — {{ info.entity_type_count }} entity types"
```

```bash
ansible-playbook verify_install.yml
```

## Configuring Credentials

You have three options for providing Diode credentials.

### Option A: Environment variables (recommended for CI)

```bash
export DIODE_TARGET="grpcs://your-instance.cloud.netboxapp.com/diode"
export DIODE_CLIENT_ID="your-client-id"
export DIODE_CLIENT_SECRET="your-client-secret"
```

Then reference them in your playbook:

```yaml
- netboxlabs.diode.diode_ingest:
    target: "{{ lookup('env', 'DIODE_TARGET') }}"
    app_name: "my-app"
    client_id: "{{ lookup('env', 'DIODE_CLIENT_ID') }}"
    client_secret: "{{ lookup('env', 'DIODE_CLIENT_SECRET') }}"
    entities: [...]
```

### Option B: Ansible Vault (recommended for version control)

```bash
ansible-vault create group_vars/all/vault.yml
```

Add your credentials:

```yaml
vault_diode_target: "grpcs://your-instance.cloud.netboxapp.com/diode"
vault_diode_client_id: "your-client-id"
vault_diode_client_secret: "your-client-secret"
```

Reference them in your playbook:

```yaml
- netboxlabs.diode.diode_ingest:
    target: "{{ vault_diode_target }}"
    app_name: "my-app"
    client_id: "{{ vault_diode_client_id }}"
    client_secret: "{{ vault_diode_client_secret }}"
    entities: [...]
```

### Option C: Inline variables (development only)

Pass credentials on the command line:

```bash
ansible-playbook site.yml \
  -e diode_target="grpcs://..." \
  -e diode_client_id="..." \
  -e diode_client_secret="..."
```

> **Never commit plaintext credentials to version control.**

## Your First Playbook

Create a file called `ingest_site.yml`:

```yaml
---
- name: Create a site in NetBox via Diode
  hosts: localhost
  connection: local
  gather_facts: false

  tasks:
    - name: Ingest a site and a device
      netboxlabs.diode.diode_ingest:
        target: "{{ lookup('env', 'DIODE_TARGET') }}"
        app_name: "getting-started"
        client_id: "{{ lookup('env', 'DIODE_CLIENT_ID') }}"
        client_secret: "{{ lookup('env', 'DIODE_CLIENT_SECRET') }}"
        entities:
          - type: site
            data:
              name: "NYC-DC1"
              status: "active"
              description: "New York data center"

          - type: device
            data:
              name: "switch-01"
              device_type: "Catalyst 9300"
              site: "NYC-DC1"
              role: "access-switch"
              status: "active"
      register: result

    - ansible.builtin.debug:
        msg: "Ingested {{ result.ingested_count }} entities in {{ result.chunk_count }} chunk(s)"
```

Run it:

```bash
ansible-playbook ingest_site.yml
```

## Next Steps

- Read the [User Guide](user_guide.md) for a complete reference on all modules, entity types, and workflows.
- See the `playbooks/examples/` directory for more playbook patterns.
- Check the [Testing Guide](testing.md) if you want to contribute.
