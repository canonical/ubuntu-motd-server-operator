# Ubuntu `MOTD` server operator

A [Juju](https://juju.is/) [charm](https://documentation.ubuntu.com/juju/3.6/reference/charm/) deploying and managing Ubuntu MOTD server on Kubernetes.

This charm simplifies the deployment and operations of the `ubuntu-motd-server` application that serves the Ubuntu Message Of The Day (MOTD).

It's currently tested on [Canonical Kubernetes](https://ubuntu.com/kubernetes).

For information about how to deploy, integrate, and manage this charm, see the Official [Ubuntu MOTD server operator Documentation](https://charmhub.io/ubuntu-motd-server).

## Get started

To begin, refer to the [Getting started](docs/tutorial/getting-start.md) tutorial.

## Integrations

Deployment of `ubuntu-motd-server` requires a certificate provider, common options are [`self-signed-certificates`](https://charmhub.io/self-signed-certificates) and [`lego`](https://charmhub.io/lego).

Refer to the [tutorial](docs/tutorial.md) to see how to integrate with `self-signed-certificates`.

## Learn more

* [Read more](https://charmhub.io/ubuntu-motd-server)
* [Official webpage](https://motd.ubuntu.com/)

## Project and community

* [Issues](https://github.com/canonical/ubuntu-motd-server-operator/issues)
* [Matrix](https://matrix.to/#/#charmhub-charmdev:ubuntu.com)
