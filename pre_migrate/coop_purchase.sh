CURRDB=$1

# modeule: coop_purchase. views removed in 12.0
psql -d $CURRDB -c "delete from ir_ui_view where name = 'report_purchaseorder_louve';"
psql -d $CURRDB -c "delete from ir_ui_view where arch_fs = 'coop_purchase/views/product_template_view.xml';"
psql -d $CURRDB -c "delete from ir_ui_view where name = 'report_purchasequotation_louve';"
psql -d $CURRDB -c "delete from ir_ui_view where name = 'invoice.supplier.form.inherit' and model = 'account.invoice' and arch_fs = 'coop_purchase/views/purchase_view.xml';"
psql -d $CURRDB -c "delete from ir_ui_view where arch_fs = 'coop_purchase/views/product_supplierinfo_view.xml';"
