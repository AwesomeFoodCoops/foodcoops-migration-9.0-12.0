#!/bin/bash

set -e

# Database name to migrate
DB=$1

# Checkpoint. Continue from a saved checkpoint
CHECKPOINT=$2
if [ -z $CHECKPOINT ]; then
  CHECKPOINT=9.0
fi

CONFIG=./odoo.conf
POST_CONFIG=./post_clean.conf

python pre-clean.py -d $DB -c $CONFIG

if [[ $(echo "$CHECKPOINT <= 10.0" | bc -l) -eq 1 ]]; then
  PREDB=$DB
  CURRDB="${DB}-mig-10"
  echo "Creating new database.. $CURRDB"
  click-odoo-dropdb -c $CONFIG --if-exists $CURRDB
  click-odoo-copydb -c $CONFIG -f $PREDB $CURRDB

  echo 'Updating to 10.0..'
  /openupgrade/10.0/odoo-bin -c $CONFIG -d $CURRDB --addons-path=/openupgrade/10.0/odoo/addons,/openupgrade/10.0/addons --logfile=/proc/self/fd/1 --update all --stop-after-init
fi

if [[ $(echo "$CHECKPOINT <= 11.0" | bc -l) -eq 1 ]]; then
  PREDB="${DB}-mig-10"
  CURRDB="${DB}-mig-11"
  echo "Creating new database.. $CURRDB"
  click-odoo-dropdb -c $CONFIG --if-exists $CURRDB
  click-odoo-copydb -c $CONFIG -f $PREDB $CURRDB

  echo 'Updating to 11.0..'
  /openupgrade/11.0/odoo-bin -c $CONFIG -d $CURRDB --addons-path=/openupgrade/11.0/odoo/addons,/openupgrade/11.0/addons --logfile=/proc/self/fd/1 --update all --stop-after-init
fi

if [[ $(echo "$CHECKPOINT <= 12.0" | bc -l) -eq 1 ]]; then
  PREDB="${DB}-mig-11"
  CURRDB="${DB}-mig-12"
  echo "Creating new database.. $CURRDB"
  click-odoo-dropdb -c $CONFIG --if-exists $CURRDB
  click-odoo-copydb -c $CONFIG -f $PREDB $CURRDB

  for script in ./pre_migrate/*.sh;
  do
    if [ -e "$script" ]
    then
      echo 'Pre-migrate script::: '$script
      /bin/bash $script $CURRDB
    fi
  done

  # Change in inherited form view of res.partner in purchase_discount module
  psql -d $CURRDB -c "delete from ir_ui_view where name = 'res.partner.form.inherit' and model='res.partner';"

  # res.groups xml IDs are changed in pos_access_right module
  psql -d $CURRDB -c "update ir_model_data set name = 'group_negative_qty' where model='res.groups' and module = 'pos_access_right' and name = 'group_pos_negative_qty';"
  psql -d $CURRDB -c "update ir_model_data set name = 'group_discount' where model='res.groups' and module = 'pos_access_right' and name = 'group_pos_discount';"
  psql -d $CURRDB -c "update ir_model_data set name = 'group_change_unit_price' where model='res.groups' and module = 'pos_access_right' and name = 'group_pos_change_unit_price';"
  psql -d $CURRDB -c "update ir_model_data set name = 'group_multi_order' where model='res.groups' and module = 'pos_access_right' and name = 'group_pos_multi_order';"
  psql -d $CURRDB -c "update ir_model_data set name = 'group_delete_order' where model='res.groups' and module = 'pos_access_right' and name = 'group_pos_delete_order';"

  # for account.jounal model: 'payment_mode' field is renamed to 'pos_terminal_payment_mode' in pos_payment_terminal module
  psql -d $CURRDB -c "delete from ir_ui_view where name = 'pos.payment.terminal.journal.form'"

  # field name changed in queue.job model from channel to channel_method_name;
  psql -d $CURRDB -c "ALTER TABLE queue_job ADD COLUMN channel_bkp character varying COLLATE pg_catalog."default";"
  psql -d $CURRDB -c "update queue_job set channel_bkp=channel;"
  psql -d $CURRDB -c "ALTER TABLE queue_job RENAME COLUMN channel TO channel_method_name;"

  echo 'Updating to 12.0..'
  /openupgrade/12.0/odoo-bin -c $CONFIG -d $CURRDB --addons-path=/openupgrade/12.0/odoo/addons,/openupgrade/12.0/addons --logfile=/proc/self/fd/1 --update all --stop-after-init

  python3 post-clean.py -d $CURRDB -c $POST_CONFIG

  echo 'Post Migration scripts started...'
  for script in ./post_migrate/*.sh;
  do
    if [ -e "$script" ]
    then
      echo 'Post-migrate script::: '$script
      /bin/bash $script $CURRDB
    fi
  done

  psql -d $CURRDB -c "delete from ir_act_window where name = 'Create Shifts';"
echo 'Updating to 12.0 all modules..'
/home/krunal/workspace/12.0/odoo-bin -c $POST_CONFIG -d $CURRDB --logfile=/proc/self/fd/1 --update all --stop-after-init

fi
