===================================
NetBox Labs Diode Collection Release Notes
===================================

.. contents:: Topics

v1.10.0
=======

Release Summary
---------------

Initial public release of the ``netboxlabs.diode`` Ansible collection,
pinned to Diode SDK >= 1.10.0.

Major Changes
-------------

- Added ``diode_ingest`` module for ingesting entities into Diode.
- Added ``diode_dry_run`` module for writing entities to JSON files.
- Added ``diode_replay`` module for replaying dry-run JSON files.
- Added ``diode_info`` module for retrieving SDK and connection info.
- Support for all 70+ NetBox entity types via the Diode SDK.
- Collection versioning strategy tracks the minimum SDK version.

Minor Changes
-------------

- Automated release pipeline with GitHub Actions and Ansible Galaxy publishing.
- CI pipeline with unit tests, Molecule scenarios, sanity checks, and linting.
- Security scanning via CodeQL, TruffleHog, and Dependabot.
- Comprehensive documentation: getting started, user guide, testing, releasing.
