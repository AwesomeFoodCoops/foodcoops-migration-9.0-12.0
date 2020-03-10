CURRDB=$1

  # inherited view(event_sale_product_template_form_inherit) of product.template removed from 12.0, module: coop_shift
  psql -d $CURRDB -c "delete from ir_ui_view where model = 'product.template' and arch_db ilike '%<label for=%event_ok%position=%attributes%';"
  psql -d $CURRDB -c "delete from ir_ui_view where model = 'res.partner' and arch_db ilike '%expr=%field[@name=''notify_email'']%';"
