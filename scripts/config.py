
MODULES_TO_UNINSTALL = [
    # Not needed modules:
    'account_cancel',
    'account_deprecated',
    'account_budget',
    'account_payment_transfer_account',
    'account_finance_report_xlsx',
    'pos_transfer_account',
    'stock_inventory_by_category',
    'create_users_partners',
    'hr_equipment',  # Not found in 12.0, exist in 9.0 core modules
    'marketing_campaign',   # Moved to Enterprise in 12.0
    # Not needed in 12.0:
    'account_accountant',
    'account_journal_inactive',
    'stock_expense_transfer',
    'pos_report_total_vat_excluded',
    # Technical modules we no longer need:
    'web_readonly_bypass',
    'smile_base',
    'smile_upgrade',
    'server_mode_mail',
    'server_mode_fetchmail',
    'l10n_pos_cert_base',  # Deprecated
    # Modules that have been merged into other modules:
    'louve_custom_account',
    'louve_custom_product',
    'louve_custom_email',
    'louve_welcome_email',
    'louve_custom_purchase',
    'pos_product_barcodes',  # Merged with coop_point_of_sale
    'date_search_extended',  # Merged in coop_account and coop_point_of_sale
    'account_reconcile_writeoff_improve',  # Merged into coop_account
    'account_bank_reconciliation_rule',  # Merged into account_bank_statement_reconcile_option
    'purchase_operation_adjust',  # Merged in product_package_qty
    # Posbox modules that where installed by mistake:
    'hw_cashlogy',
    # Deprecated modules
    # https://github.com/OCA/account-financial-reporting/issues/466#issuecomment-445182691
    'account_financial_report_date_range',
]

MODULES_TO_INSTALL = [
    'account_bank_statement_reconciliation_report',
    'coop_default_pricetag',
    'coop_account_check_deposit',
    'coop_account_product_fiscal_classification',
    # We want these extra modules:
    'web_m2x_options',
    # Only if l10n_fr - TODO?
    'l10n_fr_fec_background',
    'l10n_fr_coop_default_pricetag',
    'l10n_fr_fec_group_sale_purchase',
    'l10n_fr_certification',
    'l10n_fr_pos_cert',
    # Somehow uninstalled by openupgrade
    'account_cancel',
]

MODULES_TO_REPLACE = [
    ('connector', 'queue_job'),
    ('barcodes_generate', 'barcodes_generator_abstract'),
    ('web_sheet_full_width', 'web_responsive'),
    ('product_to_print', 'product_print_category'),
    ('pos_return_order', 'pos_order_return'),
    ('email_pos_receipt', 'pos_ticket_send_by_mail'),
    ('account_bank_statement_summary', 'account_bank_statement_reconciliation_report'),
    ('pos_session_summary', 'pos_report_session_summary'),
    ('l10n_fr_fec_custom', 'l10n_fr_fec_background'),
    # Modules that will be replaced, but are awaiting improvement PR:
    ('stock_inventory_xlsx', 'stock_inventory_valuation_report'),
    # Modules that need data migration
    ('account_asset', 'account_asset_management'),
    ('email_attachment_custom', 'mail_template_conditional_attachment'),
]

MODULES_PENDING_MIGRATION = [
    'base_import_security_group',
    'web_widget_image_webcam',
]
