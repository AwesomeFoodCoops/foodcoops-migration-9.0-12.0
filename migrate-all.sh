#!/bin/bash
set -e

# Download repositories
./setup.py

# Openupgrade
docker-compose -f docker-compose.9.0.yml up --abort-on-container-exit
docker-compose -f docker-compose.10.0.yml up --abort-on-container-exit
docker-compose -f docker-compose.11.0.yml up --abort-on-container-exit
docker-compose -f docker-compose.12.0.yml up --abort-on-container-exit
