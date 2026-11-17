# How to upgrade

The charm and the application are stateless. Upgrades within the same Ubuntu base can safely be
done through the `juju refresh` command.

## Upgrade to the Ubuntu 26.04 LTS charm (`paas-charm` 2.0)

The charm now runs on Ubuntu 26.04 LTS and uses `paas-charm` 2.0. This upgrade has these
consequences:

- The workload container is renamed from `flask-app` to `app`, and the OCI resource from
  `flask-app-image` to `app-image`.
- The application secret key is regenerated, which signs out existing users and invalidates
  their sessions. To keep sessions, provide the existing key as a Juju user secret before or
  right after deploying, as described below.

### Remove and redeploy the charm

Because the container is renamed, `juju refresh` doesn't work on Juju 3.x and 4.0. A Juju bug
([LP#1991955](https://bugs.launchpad.net/juju/+bug/1991955)) keeps the old container alive and
makes the refresh fail. You must remove the charm and deploy the new version instead:

```shell
juju remove-application ubuntu-motd-server
juju deploy ubuntu-motd-server --base ubuntu@26.04 \
  --resource app-image=<registry>/motd-server-app:<version>
```

Then recreate the integrations, for example with `juju integrate`, and reapply the
configuration of the previous deployment.

### Reapply the application secret key

```shell
juju add-secret motd-secret-key value=<secret-string>
juju grant-secret motd-secret-key ubuntu-motd-server
juju config ubuntu-motd-server app-secret-key=secret:<secret id>
```
