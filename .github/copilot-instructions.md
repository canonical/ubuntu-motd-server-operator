# Ubuntu MOTD Server Operator - Copilot Instructions

## Repository Overview

This repository contains a Juju charm operator for deploying and managing the Ubuntu Message Of The Day (MOTD) server on Kubernetes. The charm is built using the [paas-charm](https://github.com/canonical/paas-charm/) Flask framework extension.

**Project Type**: Juju Charm Operator for Kubernetes  
**Primary Language**: Python 3.12  
**Framework**: Juju Ops framework with Flask (via paas-charm)  
**Target Runtime**: Kubernetes (tested on Canonical Kubernetes)

## Project Structure

### Key Directories
- **`src/`** - Charm code (main entry point: [src/charm.py](src/charm.py))
- **`tests/`** - Unit and integration tests for the charm
- **`motd-server-app/`** - Flask application serving MOTD content
  - **`motd_server/`** - Application logic (Flask routes, MOTD selection, utilities)
  - **`tests/`** - Application-specific tests
- **`terraform/`** and **`terraform-product/`** - Terraform modules for deployment
- **`docs/`** - Documentation (tutorial, how-to, reference, explanation)
- **`lib/`** - Charm libraries (currently empty, would contain charm libs)

### Configuration Files
- **`charmcraft.yaml`** - Charm metadata and build configuration (uses flask-framework extension)
- **`tox.ini`** - Test environment configuration
- **`pyproject.toml`** - Python tooling configuration (black, isort, mypy, pylint, ruff, bandit)
- **`requirements.txt`** - Minimal runtime dependencies: `ops >= 2.2.0`, `paas-charm>=1.0,<2`
- **`Makefile`** and **`Makefile.docs`** - Build and documentation targets

## Build and Development Tools

**Required Tools**:
- Python 3.12 (tested with 3.12.3)
- tox 4.13+ (`/usr/bin/tox`)
- charmcraft 4.0.1+ (`/snap/bin/charmcraft`)
- vale (for documentation linting, optional)
- lychee (for link checking, optional)

## Testing and Validation

### Running Tests

**ALWAYS run tests in this order:**

1. **Lint/Format Code** (apply formatting before linting):
   ```bash
   tox -e fmt       # Apply black and isort formatting
   tox -e lint      # Run all linters (pydocstyle, codespell, pflake8, isort, black, mypy, pylint)
   ```

2. **Unit Tests**:
   ```bash
   tox -e unit      # Currently placeholder (empty tests)
   ```

3. **Static Analysis**:
   ```bash
   tox -e static    # Run bandit security checks
   ```

4. **Integration Tests** (requires Juju setup):
   ```bash
   tox -e integration -- --model <model-name>
   ```

5. **Application Tests** (for motd-server-app):
   ```bash
   cd motd-server-app && tox -e lint
   ```

### Linting Configuration

- **Line length**: 99 characters (configured in pyproject.toml)
- **Ignored flake8 rules**: W503, E501 (black handles these), D107 (missing __init__ docstrings)
- **Test files exempt from**: D100, D101, D102, D103, D104, D205, D212, D415 (docstring requirements)
- **Docstring convention**: Google style

### Documentation Checks

```bash
make docs-check      # Run both vale and lychee
make vale            # Run Vale style checks (requires vale sync first)
make vale-sync       # Download Vale style configurations
make lychee          # Run link checker
```

**Important**: Vale and lychee must be installed separately. The Makefile will error if they're missing.

## Continuous Integration

The repository uses GitHub Actions workflows in `.github/workflows/`:

- **`test.yaml`** - Runs `tox -e lint unit static` on PRs (uses canonical/operator-workflows)
- **`test_app.yaml`** - Runs tests for motd-server-app (working-directory: ./motd-server-app/)
- **`integration_test.yaml`** - Runs integration tests on PRs and Saturday schedule, includes Trivy security scanning
- **`publish_charm.yaml`** - Publishes to Charmhub latest/edge on push to main
- **`docs.yaml`** - Documentation build/publish
- **`test_terraform_files.yaml`** and **`test_terraform_module.yaml`** - Terraform validation

**All workflows run on self-hosted runners with label "edge".**

## Building the Charm

**To build the charm:**
```bash
charmcraft pack
```

This creates a `.charm` file (e.g., `ubuntu-motd-server_ubuntu-22.04-amd64.charm`).

**Requirements**:
- charmcraft.yaml must be present
- Dependencies in requirements.txt will be bundled
- The flask-framework extension handles most boilerplate

## Charm Architecture

The charm is extremely minimal due to using the flask-framework extension from charmcraft:

```python
# src/charm.py
class UbuntuMotdServerCharm(paas_charm.flask.Charm):
    """Flask Charm service."""
```

The extension handles:
- Pebble configuration
- Flask app lifecycle
- Service management
- Ingress integration

**Configuration**: Single option `files` (string) - YAML mapping of file paths to content.

## Application Logic

The Flask app ([motd-server-app/app.py](motd-server-app/app.py)) serves MOTD content based on User-Agent:

- **`/`** - Returns MOTD based on User-Agent parsing (version, architecture, cloud)
- **`/<filename>`** - Serves static files from config
- **`/_health`** - Health check endpoint (returns "OK")

User-Agent parsing logic in `motd_server/motd.py` extracts Ubuntu version, architecture, and cloud provider.

## Common Pitfalls and Workarounds

### Import Organization
**ALWAYS** run `tox -e fmt` before `tox -e lint`. The fmt environment applies isort and black formatting which must be done before linting checks them.

### Unit Tests
The unit tests are currently placeholders (empty `python -c ""`). Integration tests in `tests/integration/` are the primary test coverage.

### Terraform Module Testing
Terraform tests are in separate directories and have their own CI workflows. They're independent of charm tests.

### Documentation
The documentation uses Vale for style checking and expects specific style guides. Run `make vale-sync` once before running `make vale` for the first time.

### Charm Libraries
The `lib/charms/` directory is currently empty. If adding charm libraries, update the codespell command in tox.ini to check them (currently commented out).

## Key Dependencies

**Runtime**:
- `ops >= 2.2.0` - Juju Ops framework
- `paas-charm>=1.0,<2` - Flask PaaS charm framework

**Development** (from tox.ini lint environment):
- black, isort (formatting)
- flake8, pylint, mypy (linting)
- pydocstyle (docstring linting)
- bandit (security)
- codespell (spell checking)
- pytest, pytest-operator (testing)

## Making Changes

**Standard workflow**:
1. Make your code changes
2. Run `tox -e fmt` to format code
3. Run `tox -e lint` to check for issues
4. Run `tox -e static` for security checks
5. If touching docs, run `make docs-check`
6. Commit with signed commits (CLA required)
7. Update docs/changelog.md if applicable

**PR Requirements** (from CONTRIBUTING.md):
- Follow charm style guide
- Follow ISD054 complexity management
- Update documentation
- Update changelog
- Sign commits (Canonical CLA)
- Tag PR appropriately (trivial, senior-review-required)

## Trust These Instructions

The commands and configurations documented here have been validated against the actual codebase. Only perform additional searches if:
- The instructions are incomplete for your specific task
- You encounter errors contradicting these instructions
- You need to understand implementation details not covered here
