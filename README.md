**Foodcoops Database Migration scripts from 9.0 to 12.0**

To migrate a database from 9.0 to 12.0, using openupgrade.


First step is downloading openupgrade and all the required repositories.

`./setup.py`

By executing this command, openupgrade versions 9.0, 10.0, 11.0 and 12.0 will be downloaded.
To know more about Openupgrade project, follow this link: https://github.com/OCA/OpenUpgrade

Please set the addons_path in odoo.conf and post_clean.conf files according to the local system.

Now, run the following command to start the migration of a database.

`/bin/bash migration.sh database_name_to_migrate`

This command will start the migration. It will go through the following stages:
* pre-clean the database
* update the database to 10.0
* update the database to 11.0
* run the pre-migrate scripts put in pre_migrate folder
* update the database to 12.0
* post-clean the database
* run the post-migrate scripts put in post_migrate folder


**TODO**

Make the addons_path set in odoo.conf and post_clean.conf files to system independent using git-aggregator.
