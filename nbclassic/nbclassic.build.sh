#!/bin/bash
chmod +x *.start.sh
podman build -t nbclassic:latest .
echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
podman images