# Getting started

## What you’ll do

- Deploy the `ubuntu-motd-server` charm.
- Configure the `ubuntu-motd-server` charm.

## Requirements

- Juju 3.x installed.
- Juju controller that can create a model of type Kubernetes.
- Configuration compatible with the traefik-k8s charms. In the case of MicroK8s this can be achieved with the `metallb` add-on.

For more information about how to install Juju, see [Get started with Juju](https://documentation.ubuntu.com/juju/3.6/tutorial/).

## Setting up a tutorial model

To manage resources effectively and to separate this tutorial's workload from
your usual work, we recommend creating a new model using the following command.

```shell
juju add-model motd-tutorial
```

## Deploy

Deploy the `ubuntu-motd-server` charm.

```shell
juju deploy ubuntu-motd-server --channel latest/stable
```

Once the deployment is completed, you shoud see something like:

```shell
App                 Version  Status  Scale  Charm               Channel      Rev  Address         Exposed  Message
ubuntu-motd-server           active      1  ubuntu-motd-server  latest/stable    5  10.152.183.193  no  
```

You should be able to reach the service on port 8000 of the previous address. As no `files` are configured yet, it will return a 404 error.

```shell
curl http://10.152.183.193:8000 -D -
HTTP/1.1 404 NOT FOUND
```

### Configure

The easiest way to define the content of the MOTD server is to populate a file with the configuration. Create the following `content.yaml` file:

```yaml
index.txt: |
  default motd

index-22.04.txt: |
  aws motd
```

Apply this configuration with the following command:

```shell
juju config ubuntu-motd-server files="$(cat content.yaml)"
```

You can now retrieve the default MOTD:

```shell
curl 10.152.183.193:8000 
default index
```

And you can test that it serves a cloud specific MOTD when requests:

```shell
curl 10.152.183.193:8000 -D - -H "User-Agent: Ubuntu/22.04"
22.04 index
```

Congratulations, you configured and test the MOTD server.
