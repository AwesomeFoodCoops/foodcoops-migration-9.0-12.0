CURRDB=$1

  # report id renamed from 'report_inventory_adjust' to 'report_inventory' in coop_inventory module.
  psql -d $CURRDB -c "delete from ir_ui_view where name = 'report_inventory_adjust';"
  #'report_inventory_louve' template not needed in coop_inventory module
  psql -d $CURRDB -c "delete from ir_ui_view where name = 'report_inventory_louve';"
