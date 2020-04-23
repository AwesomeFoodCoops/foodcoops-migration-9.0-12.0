#!/bin/bash
set -e

# Load db
docker-compose -f docker-compose.load.yml down -v

# Openupgrade
docker-compose -f docker-compose.9.0.yml down -v
docker-compose -f docker-compose.10.0.yml down -v
docker-compose -f docker-compose.11.0.yml down -v
docker-compose -f docker-compose.12.0.yml down -v

# Tests
docker-compose -f docker-compose.9.0-test.yml down -v
docker-compose -f docker-compose.10.0-test.yml down -v
docker-compose -f docker-compose.11.0-test.yml down -v
docker-compose -f docker-compose.12.0-test.yml down -v
