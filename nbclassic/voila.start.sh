#!/bin/bash
mkdir -p ~/voila
voila --Voila.ip=0.0.0.0 --port=$VOILA_PORT --no-browser --classic-tree \
    --VoilaConfiguration.file_allowlist="['.*']" \
    ~/voila > /dev/null 2>&1 &
