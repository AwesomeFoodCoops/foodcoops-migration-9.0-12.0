#!/bin/bash
set -e

# Download repositories
./setup.py

# Openupgrade
sudo docker-compose -f docker-compose.9.0.yml up --abort-on-container-exit
sudo docker-compose -f docker-compose.10.0.yml up --abort-on-container-exit
sudo docker-compose -f docker-compose.11.0.yml up --abort-on-container-exit
sudo docker-compose -f docker-compose.12.0.yml up --abort-on-container-exit
sudo docker-compose -f docker-compose.final.yml up --abort-on-container-exit
