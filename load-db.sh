#!/bin/bash
set -e

# Load dump.gz database automatically
echo "Starting load container.."
sudo docker-compose -f docker-compose.load.yml up -d

# Wait for it
./wait-for-it.sh --timeout=0 localhost:8069

# Try to drop database
curl -F name=migrate -F master_pwd=admin http://localhost:8069/web/database/drop

# Upload new database
if [[ -f backups/migrate.dump.gz ]]; then
	echo "Loading backup from migrate.dump.gz.."
	curl -F backup_file=@backups/migrate.dump.gz -F name=migrate -F master_pwd=admin -F copy=true http://localhost:8069/web/database/restore
elif [[ -f backups/migrate.zip ]]; then
	echo "Loading backup from migrate.zip.."
	curl -F backup_file=@backups/migrate.zip -F name=migrate -F master_pwd=admin -F copy=true http://localhost:8069/web/database/restore
fi

echo "Shutting down load container.."
sudo docker-compose -f docker-compose.load.yml down
