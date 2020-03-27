**Foodcoops Database Migration scripts from 9.0 to 12.0**

To migrate a database from 9.0 to 12.0, using openupgrade.

# Setup

## 1. Download openupgrade and all repositories required

First step is downloading openupgrade and all the required repositories.

`./setup.py`

By executing this command, openupgrade versions 9.0, 10.0, 11.0 and 12.0 will be downloaded.
To know more about Openupgrade project, follow this link: https://github.com/OCA/OpenUpgrade

Also all the required repositories for 12.0 will also be downloaded.

## 2. Log in to docker.hub

Your user needs access to druidoo's repositories and have access to odoo-saas.
This step is only necessary if you're not logged in already.


`docker login -u YOU_USERNAME -p YOUR_PASSWORD`

# Migrate

## 1. Load your database

Start the container:

`docker-compose -f docker-compose.pre.yml up`

Then access https://localhost/8069 on your browser, and upload your database.
**IMPORTANT:** Database name has to be exactly: `migrate`.


Then `CTRL+C` to stop the container.

## 2. Migrate base modules to 12.0

`./migrate-all.sh`

## 3. Get your migrated database

It'll be located in `backups/final.zip`

