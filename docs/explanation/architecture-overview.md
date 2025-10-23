# Architecture overview

A typical deployment of the `ubuntu-motd-server` charm involves an `ingress` provider and a `certificate` provider to expose the service over HTTPS.

You can see an example in the following diagram:

```mermaid
C4Component
title Typical deployment for the Ubuntu MOTD server charm

Component(lego, "Lego", "", "Provides SSL certificates")

Component(traefik, "Traefik", "", "Handles incoming traffic and SSL termination")


Container_Boundary(imagebuildercharm), "MOTD charm") {
  Component(charm, "ubuntu-motd-server-app", "", "Serves HTTP requests")

}

Rel(lego, traefik, "'certificates' relation")
Rel(traefik, charm, "'ingress' relation")

UpdateLayoutConfig($c4ShapeInRow="1", $c4BoundaryInRow="1")

UpdateRelStyle(lego, traefik, $offsetX="15")
UpdateRelStyle(traefik, charm, $offsetX="15", $offsetY="-15")
```
