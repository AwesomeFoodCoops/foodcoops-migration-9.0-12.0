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
MISSING_USER_ID=1

if [[ $(echo "$CHECKPOINT <= 10.0" | bc -l) -eq 1 ]]; then
  PREDB=$DB
  CURRDB="${DB}-mig-10"
  echo "Creating brackup.. $CURRDB"
  click-odoo-dropdb -c $CONFIG --if-exists $CURRDB
  click-odoo-copydb -c $CONFIG -f $PREDB $CURRDB

  echo 'Updating to 10.0..'
  /openupgrade/10.0/odoo-bin -c $CONFIG -d $CURRDB --addons-path=/openupgrade/10.0/odoo/addons,/openupgrade/10.0/addons --logfile=/proc/self/fd/1 --update all --stop-after-init
fi

if [[ $(echo "$CHECKPOINT <= 11.0" | bc -l) -eq 1 ]]; then
  PREDB="${DB}-mig-10"
  CURRDB="${DB}-mig-11"
  echo "Creating brackup.. $CURRDB"
  click-odoo-dropdb -c $CONFIG --if-exists $CURRDB
  click-odoo-copydb -c $CONFIG -f $PREDB $CURRDB

  echo 'Updating to 11.0..'
  /openupgrade/11.0/odoo-bin -c $CONFIG -d $CURRDB --addons-path=/openupgrade/11.0/odoo/addons,/openupgrade/11.0/addons --logfile=/proc/self/fd/1 --update all --stop-after-init
fi

if [[ $(echo "$CHECKPOINT <= 12.0" | bc -l) -eq 1 ]]; then
  PREDB="${DB}-mig-11"
  CURRDB="${DB}-mig-12"
  echo "Creating brackup.. $CURRDB"
  click-odoo-dropdb -c $CONFIG --if-exists $CURRDB
  click-odoo-copydb -c $CONFIG -f $PREDB $CURRDB

  echo 'Fixing weird issue'
  psql -d $CURRDB -c "DELETE FROM wizard_multi_charts_accounts;"

  # report id renamed from 'report_inventory_adjust' to 'report_inventory' in coop_inventory module.
  psql -d $CURRDB -c "delete from ir_ui_view where name = 'report_inventory_adjust';"
  #'report_inventory_louve' template not needed in coop_inventory module
  psql -d $CURRDB -c "delete from ir_ui_view where name = 'report_inventory_louve';"

  # Change in inherited form view of res.partner in purchase_discount module
  psql -d $CURRDB -c "delete from ir_ui_view where name = 'res.partner.form.inherit' and model='res.partner';"

  # report id renamed from 'report_inventory_package' to 'report_inventory' in purchase_package_qty module.
  psql -d $CURRDB -c "delete from ir_ui_view where name = 'report_inventory_package';"

  # res.groups xml IDs are changed in pos_access_right module
  psql -d $CURRDB -c "update ir_model_data set name = 'group_negative_qty' where model='res.groups' and module = 'pos_access_right' and name = 'group_pos_negative_qty';"
  psql -d $CURRDB -c "update ir_model_data set name = 'group_discount' where model='res.groups' and module = 'pos_access_right' and name = 'group_pos_discount';"
  psql -d $CURRDB -c "update ir_model_data set name = 'group_change_unit_price' where model='res.groups' and module = 'pos_access_right' and name = 'group_pos_change_unit_price';"
  psql -d $CURRDB -c "update ir_model_data set name = 'group_multi_order' where model='res.groups' and module = 'pos_access_right' and name = 'group_pos_multi_order';"
  psql -d $CURRDB -c "update ir_model_data set name = 'group_delete_order' where model='res.groups' and module = 'pos_access_right' and name = 'group_pos_delete_order';"

  # for account.jounal model: 'payment_mode' field is renamed to 'pos_terminal_payment_mode' in pos_payment_terminal module
  psql -d $CURRDB -c "delete from ir_ui_view where name = 'pos.payment.terminal.journal.form'"

  # pack_operation_product_ids removed from stock.picking models, coop_stock module
  psql -d $CURRDB -c "delete from ir_ui_view where arch_db ilike '%field[@name=''pack_operation_product_ids'']%'"

  echo 'Updating to 12.0..'
  /openupgrade/12.0/odoo-bin -c $CONFIG -d $CURRDB --addons-path=/openupgrade/12.0/odoo/addons,/openupgrade/12.0/addons --logfile=/proc/self/fd/1 --update all --stop-after-init

fi
