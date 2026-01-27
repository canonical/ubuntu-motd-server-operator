# Contributing

This document explains the processes and practices recommended for contributing enhancements to the `ubuntu-motd-server` charm.

## Overview

- Generally, before developing enhancements to this charm, you should consider [opening an issue
  ](link to issues page) explaining your use case.
- If you would like to chat with us about your use-cases or proposed implementation, you can reach
  us at [Canonical Matrix public channel](https://matrix.to/#/#charmhub-charmdev:ubuntu.com)
  or [Discourse](https://discourse.charmhub.io/).
- Familiarizing yourself with the [Juju documentation](https://documentation.ubuntu.com/juju/3.6/howto/manage-charms/)
  will help you a lot when working on new features or bug fixes.
- All enhancements require review before being merged. Code review typically examines
  - code quality
  - test coverage
  - user experience for Juju operators of this charm.
- Once your pull request is approved, we squash and merge your pull request branch onto
  the `main` branch. This creates a linear Git commit history.
- For further information on contributing, please refer to our
  [Contributing Guide](https://github.com/canonical/is-charms-contributing-guide).

## Code of conduct

When contributing, you must abide by the
[Ubuntu Code of Conduct](https://ubuntu.com/community/ethos/code-of-conduct).

## Changelog

Please ensure that any new feature, fix, or significant change is documented by
adding an entry to the [CHANGELOG.md](link to changelog) file. Use the date of the
contribution as the header for new entries.

To learn more about changelog best practices, visit [Keep a Changelog](https://keepachangelog.com/).

## Submissions

If you want to address an issue or a bug in this project,
notify in advance the people involved to avoid confusion;
also, reference the issue or bug number when you submit the changes.

- [Fork](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/about-forks)
  our [GitHub repository](link to GitHub repository)
  and add the changes to your fork, properly structuring your commits,
  providing detailed commit messages and signing your commits.
- Make sure the updated project builds and runs without warnings or errors;
  this includes linting, documentation, code and tests.
- Submit the changes as a
  [pull request (PR)](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork).

Your changes will be reviewed in due time; if approved, they will be eventually merged.

### Describing pull requests

To be properly considered, reviewed and merged,
your pull request must provide the following details:

- **Title**: Summarize the change in a short, descriptive title.

- **Overview**: Describe the problem that your pull request solves.
  Mention any new features, bug fixes or refactoring.

- **Rationale**: Explain why the change is needed.

- **Juju Events Changes**: Describe any changes made to Juju events, or
  "None" if the pull request does not change any Juju events.

- **Module Changes**: Describe any changes made to the module, or "None"
  if your pull request does not change the module.

- **Library Changes**: Describe any changes made to the library,
  or "None" is the library is not affected.

- **Checklist**: Complete the following items:

  - The [charm style guide](https://documentation.ubuntu.com/juju/3.6/reference/charm/charm-development-best-practices/) was applied
  - The [contributing guide](https://github.com/canonical/is-charms-contributing-guide) was applied
  - The changes are compliant with [ISD054 - Managing Charm Complexity](https://discourse.charmhub.io/t/specification-isd014-managing-charm-complexity/11619)
  - The documentation is updated
  - The PR is tagged with appropriate label (trivial, senior-review-required)
  - The changelog has been updated

### Signing commits

To improve contribution tracking,
we use the [Canonical contributor license agreement](https://assets.ubuntu.com/v1/ff2478d1-Canonical-HA-CLA-ANY-I_v1.2.pdf)
(CLA) as a legal sign-off, and we require all commits to have verified signatures.

#### Canonical contributor agreement

Canonical welcomes contributions to the `ubuntu-motd-server` charm. Please check out our
[contributor agreement](https://ubuntu.com/legal/contributors) if you're interested in contributing to the solution.

The CLA sign-off is simple line at the
end of the commit message certifying that you wrote it
or have the right to commit it as an open-source contribution.

#### Verified signatures on commits

All commits in a pull request must have cryptographic (verified) signatures.
To add signatures on your commits, follow the
[GitHub documentation](https://docs.github.com/en/authentication/managing-commit-signature-verification/signing-commits).

## Develop

### Development setup

To make contributions to this charm, you'll need a working development setup.
We recommend using `multipass` to have a dedicated and isolated environment.

Create your virtual machine with:

```shell
multipass launch 22.04 \
  --name motd-vm \
  --cpus 4 \
  --memory 8G \
  --disk 50G \
  --timeout 1800
```

Connect to your virtual machine, and install [`concierge`](https://github.com/canonical/concierge) to ease the deployment of the required components:

```shell
multipass shell motd-vm
sudo snap install --classic concierge
```

Install the development requirements:

```shell
sudo concierge prepare -p k8s
```

Once completed, you should be able to run `juju status` and see something like:

```text
Model    Controller     Cloud/Region  Version  SLA          Timestamp
testing  concierge-k8s  k8s           3.6.13   unsupported  14:48:06+01:00

Model "admin/testing" is empty.
```

As we will need a container registry, we need to deploy one using the following command:

```shell
cat << EOF | kubectl apply -f -
> ---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: private-registry
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      app: private-registry
  template:
    metadata:
      labels:
        app: private-registry
    spec:
      containers:
        - name: registry
          image: registry:2
          ports:
            - containerPort: 5000
          volumeMounts:
            - name: registry-storage
              mountPath: /var/lib/registry
      volumes:
        - name: registry-storage
          emptyDir: {}

---
apiVersion: v1
kind: Service
metadata:
  name: private-registry
  namespace: default
spec:
  selector:
    app: private-registry
  ports:
    - protocol: TCP
      port: 5000
      targetPort: 5000
EOF
```

And we need to allow plain HTTP access to it with the following:

```shell
REGISTRY_IP=$(kubectl get svc private-registry -o jsonpath='{.spec.clusterIP}')
sudo mkdir -p /etc/containerd/hosts.d/${REGISTRY_IP}$:5000
sudo cat << EOF | sudo tee /etc/containerd/hosts.d/${REGISTRY_IP}:5000/hosts.toml
server = "http://${REGISTRY_IP}:5000"

[host."http://${REGISTRY_IP}:5000"]
  capabilities = ["pull", "resolve"]
  skip_verify = true
EOF
```

The final steps is to install `tox` with:

```shell
sudo apt install python3-venv
python3 -m venv venv
source venv/bin/activate
pip install tox
``````

### Retrieve the sources

The code for this charm can be downloaded as follows:

```shell
git clone https://github.com/canonical/ubuntu-motd-server-operator
```

### Test

This project uses `tox` for managing test environments. There are some pre-configured environments
that can be used for linting and formatting code when you're preparing contributions to the charm:

- ``tox``: Executes all of the basic checks and tests (``lint``, ``unit``, ``static``, and ``coverage-report``).
- ``tox -e fmt``: Runs formatting using ``black`` and ``isort``.
- ``tox -e lint``: Runs a range of static code analysis to check the code.
- ``tox -e static``: Runs other checks such as ``bandit`` for security issues.
- ``tox -e unit``: Runs the unit tests.
- ``tox -e integration``: Runs the integration tests. Note: these tests require the rock and charm to be built first, see next sections.

### Build the rock and charm

Use [Rockcraft](https://documentation.ubuntu.com/rockcraft/stable/) to create an
OCI image for the `motd-server` app.

```shell
cd motd-server-app
rockcraft pack
```

Build the charm in this git repository using:

```shell
charmcraft pack
```

### Deploy

Push the rock to the registry:

```bash
REGISTRY_IP=$(kubectl get svc private-registry -o jsonpath='{.spec.clusterIP}')
APP_VERSION=0.15
skopeo --insecure-policy copy --dest-tls-verify=false oci-archive:motd-server-app/motd-server-app_${APP_VERSION}_amd64.rock docker://${REGISTRY_IP}:5000/motd-server-app:latest
```

```bash
# Create a model
juju add-model charm-dev
# Enable DEBUG logging
juju model-config logging-config="<root>=INFO;unit=DEBUG"
# Deploy the charm
juju deploy ./ubuntu-motd-server_ubuntu-22.04-amd64.charm --resource flask-app-image=${REGISTRY_IP}:5000/motd-server-app:latest
```
