#!/bin/bash
set -e

# Load db
sudo docker-compose -f docker-compose.load.yml down -v

# Openupgrade
sudo docker-compose -f docker-compose.9.0.yml down -v
sudo docker-compose -f docker-compose.10.0.yml down -v
sudo docker-compose -f docker-compose.11.0.yml down -v
sudo docker-compose -f docker-compose.12.0.yml down -v

# Tests
sudo docker-compose -f docker-compose.9.0-test.yml down -v
sudo docker-compose -f docker-compose.10.0-test.yml down -v
sudo docker-compose -f docker-compose.11.0-test.yml down -v
sudo docker-compose -f docker-compose.12.0-test.yml down -v
