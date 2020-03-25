CURRDB=$1

val=$(psql -d $CURRDB -c "select max(id) from product_print_category;")
seq="${val:15:1}"
psql -d $CURRDB -c "ALTER SEQUENCE product_print_category_id_seq RESTART WITH $seq"

psql -d $CURRDB -c "alter table ir_model_fields_product_print_category_rel drop constraint ir_model_fields_product_print_category_rel_category_id_fkey;"
psql -d $CURRDB -c "alter table ir_model_fields_product_print_category_rel add CONSTRAINT ir_model_fields_product_print_category_rel_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.product_print_category (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE CASCADE;"
psql -d $CURRDB -c "update product_template set print_category_id=category_print_id_bkp;"