import click
import click_odoo


@click.command()
@click_odoo.env_options(default_log_level='error')
def main(env):
    print('Pre cleaning started...')
    modules_to_uninstall = [
        'account_payment_transfer_account', 'louve_custom_account',
        'account_cancel', 'account_deprecated',
        'account_budget',
        'pos_transfer_account',
        'account_finance_report_xlsx', 'smile_base', 'smile_upgrade',
        'louve_custom_product', 'louve_custom_email',
        'louve_welcome_email',
        'account_asset', 'web_sheet_full_width',

        'product_to_print',      # renamed to product_print_category
        'pos_return_order',      # renamed to pos_order_return
        'account_bank_statement_summary',  # renamed to
                                 # account_bank_statement_reconciliation_report
        'pos_product_barcodes',  # Merged with coop_point_of_sale

        # Modules to Migrate.
        'web_widget_image_webcam', 'coop_produce',
        'date_search_extended',
        'product_to_scale_bizerba', 'mass_editing',
        'pos_session_summary',
        'account_bank_statement_reconcile_option',
        'pos_automatic_cashdrawer', 'account_reconcile_pos_payments',
        'pos_payment_terminal_return', 'account_bank_reconciliation_rule',
        'account_bank_statement_import_caisse_epargne',
        'account_bank_statement_import_ofx', 'account_invoice_refund_option',
        'account_mass_reconcile', 'account_payment_confirm',
        'account_payment_select_account', 'account_payment_term_restricted',
        'account_reconcile_writeoff_improve', 'auto_backup',
        'base_import_security_group', 'base_technical_features',
        'email_attachment_custom', 'hw_cashlogy', 'pos_price_to_weight',
        'purchase_operation_adjust', 'scheduler_error_mailer',
        'stock_inventory_by_category', 'stock_inventory_xlsx',
        'web_readonly_bypass',

        # Moved to Enterprise in 12.0
        'marketing_campaign',

        # not needed in 12.0
        'stock_expense_transfer', 'pos_report_total_vat_excluded',
        'account_accountant', 'account_journal_inactive',
    ]
    for module in modules_to_uninstall:
        print('Uninstalling module: %s..' % module)
        module_id = env['ir.module.module'].search([('name', '=', module)])
        if module_id:
            module_id.button_immediate_uninstall()
        else:
            print('Module not found: %s' % module)

    print('Pre cleaning finished successfully!')


if __name__ == '__main__':
    main()
