# Release Process

This document describes how to release a new version of the `netboxlabs.diode`
Ansible collection.

## Versioning Strategy

The collection version tracks the minimum Diode SDK version it supports:

| Collection Version | Minimum SDK Version | SDK Upper Bound |
|--------------------|---------------------|-----------------|
| 1.10.x             | 1.10.0              | < 2.0.0         |

- **Major.Minor** matches the SDK minor version (e.g., collection `1.10.x`
  requires SDK `>= 1.10.0`).
- **Patch** is the collection's own release counter within that minor
  (e.g., `1.10.0`, `1.10.1`, `1.10.2` are all collection releases for
  SDK 1.10.x).
- When the SDK releases a new minor (e.g., 1.11.0), bump the collection
  to `1.11.0` and update `requirements.txt` accordingly.

The SDK version pin lives in two places that must stay in sync:

- `requirements.txt` — the pip constraint
- `galaxy.yml` — the collection version

CI validates this on every PR and at release time.

## Prerequisites

- Push access to the repository (or a maintainer to merge your release PR)
- The `GALAXY_API_KEY` repository secret must be configured
  (see [Galaxy API Key Setup](#galaxy-api-key-setup))

## Step-by-Step Release

### 1. Create a Release Branch

```bash
git checkout main && git pull
git checkout -b release/v1.10.1
```

### 2. Update the Version

Edit `galaxy.yml`:

```yaml
version: "1.10.1"
```

If the SDK minimum version changed, also update `requirements.txt`:

```
netboxlabs-diode-sdk>=1.11.0,<2.0.0
```

### 3. Update the Changelog

Add a fragment in `changelogs/fragments/`:

```bash
cat > changelogs/fragments/v1.10.1.yml << 'EOF'
---
release_summary: |
  Patch release with bug fixes and new entity type support.
bugfixes:
  - "Fixed handling of null fields in device entities."
minor_changes:
  - "Added support for FooBar entity type."
EOF
```

Update `CHANGELOG.rst` with the new version entry.

### 4. Run the Full Test Suite

```bash
make test-all
```

All unit tests and Molecule scenarios must pass.

### 5. Commit, Push, and Open a PR

```bash
git add galaxy.yml requirements.txt CHANGELOG.rst changelogs/
git commit -m "Release v1.10.1"
git push -u origin release/v1.10.1
gh pr create --title "Release v1.10.1" --body "Release PR for v1.10.1"
```

Wait for CI to pass and get an approval from a maintainer.

### 6. Merge and Tag

After the PR is merged:

```bash
git checkout main && git pull
git tag -a v1.10.1 -m "Release v1.10.1"
git push origin v1.10.1
```

### 7. Automated Release Pipeline

Pushing the tag triggers the release workflow which:

1. **Validates** that `galaxy.yml` version matches the tag.
2. **Runs** the full test suite across Python 3.10, 3.11, and 3.12.
3. **Builds** the collection tarball (`netboxlabs-diode-1.10.1.tar.gz`).
4. **Creates a GitHub Release** with the tarball attached and
   auto-generated release notes.
5. **Publishes to Ansible Galaxy** using the `GALAXY_API_KEY` secret.

### 8. Verify

```bash
# Check Galaxy
ansible-galaxy collection install netboxlabs.diode:==1.10.1 --force

# Check GitHub release
gh release view v1.10.1
```

## Galaxy API Key Setup

1. Log in to [Ansible Galaxy](https://galaxy.ansible.com/).
2. Navigate to **Collections** > **API Token** and generate a new token.
3. In the GitHub repository, go to **Settings** > **Secrets and variables** >
   **Actions**.
4. Add a new repository secret named `GALAXY_API_KEY` with the token value.

## SDK Version Bump Workflow

When a new Diode SDK minor version is released:

1. Update `requirements.txt` to the new pin
   (e.g., `netboxlabs-diode-sdk>=1.11.0,<2.0.0`).
2. Bump `galaxy.yml` version to `1.11.0`.
3. Test against the new SDK version to verify compatibility.
4. Update the compatibility matrix in this document.
5. Follow the standard release process above.

## Hotfix Releases

For critical fixes that need to ship immediately:

```bash
git checkout main && git pull
git checkout -b hotfix/v1.10.2
# Make the fix, update version to 1.10.2
git commit -m "Hotfix: fix critical issue in diode_ingest"
git push -u origin hotfix/v1.10.2
gh pr create --title "Hotfix v1.10.2" --body "Critical fix for ..."
```

After merge, tag as normal. The release pipeline handles the rest.

## Branch Protection (Recommended)

Configure these branch protection rules on `main`:

| Setting                          | Value  |
|----------------------------------|--------|
| Require pull request reviews     | 1+     |
| Require status checks to pass    | Yes    |
| Required checks                  | `Unit Tests`, `Molecule`, `Lint`, `Sanity` |
| Require branches to be up to date| Yes    |
| Require signed commits           | Optional |
| Include administrators           | Yes    |
| Allow force pushes               | No     |
| Allow deletions                  | No     |

These can be configured in **Settings** > **Branches** > **Branch protection
rules** > **Add rule** for `main`.
