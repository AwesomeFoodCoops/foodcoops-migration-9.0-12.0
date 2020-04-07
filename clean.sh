#!/bin/bash
set -e

docker-compose -f docker-compose.load.yml down -v
docker-compose -f docker-compose.9.0.yml down -v
docker-compose -f docker-compose.10.0.yml down -v
docker-compose -f docker-compose.11.0.yml down -v
docker-compose -f docker-compose.12.0.yml down -v
docker-compose -f docker-compose.final.yml down -v
docker-compose -f docker-compose.test.yml down -v
