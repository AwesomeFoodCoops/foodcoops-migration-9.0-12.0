CURRDB=$1

# report id renamed from 'report_inventory_package' to 'report_inventory' in purchase_package_qty module.
psql -d $CURRDB -c "delete from ir_ui_view where name = 'report_inventory_package';"
