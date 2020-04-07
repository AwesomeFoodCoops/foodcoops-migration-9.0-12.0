**Foodcoops Database Migration scripts from 9.0 to 12.0**

To migrate a database from 9.0 to 12.0, using openupgrade.

# Migrate

## 1. Load your database

Start the container:

`docker-compose -f docker-compose.load.yml up`

Then access https://localhost/8069 on your browser, and upload your database.

**IMPORTANT:** Database name has to be exactly: `migrate`.

Then `CTRL+C` to stop the container.

## 2. Migrate base modules to 12.0

`./migrate-all.sh`

## 3. Get your migrated database

It'll be located in `backups/final.zip`

## 4. Cleaning up

After you finished, you can remove all containers and volumes by running `clean.sh`
