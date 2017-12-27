#!/bin/bash
docker run -d -p '53:53/udp' -p '53:53/tcp' -v /etc/host.aliases:/etc/host.aliases --restart=unless-stopped --name dns dns
