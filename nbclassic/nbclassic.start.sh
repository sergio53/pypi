#!/bin/bash
mkdir -p ~/.jupyter/nbconfig
cp -n /etc/jupyter/notebook.json ~/.jupyter/nbconfig
cp -n /etc/jupyter/edit.json ~/.jupyter/nbconfig

jupyter nbclassic --ip=0.0.0.0 --no-browser > /dev/null 2>&1 &
