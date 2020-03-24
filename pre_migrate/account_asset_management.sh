CURRDB=$1

psql -d $CURRDB -c "delete from ir_ui_view where name = 'account.invoice.supplier.form' and arch_fs='account_asset/views/account_invoice_views.xml';"
psql -d $CURRDB -c "delete from ir_ui_view where name = 'Product Template (form)' and arch_fs='account_asset/views/product_views.xml';"
