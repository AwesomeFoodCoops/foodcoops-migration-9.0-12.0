CURRDB=$1

  # pack_operation_product_ids removed from stock.picking models, coop_stock module
  psql -d $CURRDB -c "delete from ir_ui_view where arch_db ilike '%field[@name=''pack_operation_product_ids'']%'"
