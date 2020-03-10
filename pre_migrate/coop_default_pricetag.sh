CURRDB=$1

  # module: coop_default_pricetag. Added records in ir_model_data which are deleted due to uninstalling of louve_custom_product module
  psql -d $CURRDB -c "insert into ir_model_data (id, create_uid, create_date, write_uid, write_date, noupdate, name, date_init, date_update, module, model, res_id) VALUES (nextval('ir_model_data_id_seq'), 1, (now() at time zone 'UTC'), 1, (now() at time zone 'UTC'), 't', 'decimal_product_attribute_volume', (now() at time zone 'UTC'), (now() at time zone 'UTC'), 'coop_default_pricetag', 'decimal.precision', 7);"
#  psql -d $CURRDB -c "insert into ir_model_data (id, create_uid, create_date, write_uid, write_date, noupdate, name, date_init, date_update, module, model, res_id) VALUES (nextval('ir_model_data_id_seq'), 1, (now() at time zone 'UTC'), 1, (now() at time zone 'UTC'), 't', 'vegetable_category', (now() at time zone 'UTC'), (now() at time zone 'UTC'), 'coop_default_pricetag', 'product.print.category', 2);"
