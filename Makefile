.PHONY: setup test molecule lint test-all build clean help version-check release-check

VENV := .venv
PYTHON := $(CURDIR)/$(VENV)/bin/python
PYTEST := PYTHONPATH=/tmp:$$PYTHONPATH $(VENV)/bin/pytest
COLLECTION_PATH := /tmp/ansible_collections/my0373/diode

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

setup: ## Create venv, install deps, create collection symlink
	uv venv
	$(VENV)/bin/pip install ansible-core netboxlabs-diode-sdk pytest pytest-mock molecule
	mkdir -p /tmp/ansible_collections/my0373
	ln -sf "$$(pwd)" $(COLLECTION_PATH)
	@echo "\nSetup complete. Run: source $(VENV)/bin/activate"

test: ## Run unit tests
	$(PYTEST) tests/unit/ -v

molecule: ## Run all Molecule scenarios
	MOLECULE_PYTHON_INTERPRETER=$(PYTHON) $(VENV)/bin/molecule test --all

molecule-s: ## Run a single Molecule scenario (usage: make molecule-s S=default)
	MOLECULE_PYTHON_INTERPRETER=$(PYTHON) $(VENV)/bin/molecule test -s $(S)

lint: ## Run yamllint on YAML files
	$(VENV)/bin/yamllint -d relaxed plugins/ meta/ extensions/molecule/

test-all: test molecule ## Run unit tests and Molecule scenarios

version-check: ## Verify galaxy.yml and requirements.txt versions are consistent
	@GALAXY_VER=$$(grep '^version:' galaxy.yml | sed 's/^version: *//;s/"//g'); \
	SDK_PIN=$$(grep 'netboxlabs-diode-sdk' requirements.txt | head -1); \
	echo "Collection version: $$GALAXY_VER"; \
	echo "SDK pin:            $$SDK_PIN"; \
	MINOR=$$(echo $$GALAXY_VER | cut -d. -f1,2); \
	echo $$SDK_PIN | grep -q "$$MINOR" && echo "✓ Versions consistent" || echo "✗ WARNING: SDK pin may not match collection version"

release-check: version-check test-all ## Run all checks required before a release
	@echo "\n✓ All release checks passed"

build: ## Build the collection tarball
	ansible-galaxy collection build --force

clean: ## Remove build artifacts and temp files
	rm -rf dist/ build/ *.egg-info *.tar.gz
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete 2>/dev/null || true
