
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
    # Modules that have been merged into other modules:
    'louve_custom_account',
    'louve_custom_product',
    'louve_custom_email',
    'louve_welcome_email',
    'pos_product_barcodes',  # Merged with coop_point_of_sale
    'date_search_extended',  # Merged in coop_account and coop_point_of_sale
    'account_reconcile_writeoff_improve',  # Merged into coop_account
    # Posbox modules that where installed by mistake:
    'hw_cashlogy',

    # Other technical modules
    # TODO: add them to the repositories, we need them
    'saas_client',
    'server_mode',
    'server_mode_fetchmail',
    'server_mode_mail',
]

MODULES_TO_INSTALL = [
    'account_bank_statement_reconciliation_report',
    'coop_default_pricetag',
    'coop_account_check_deposit',
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
    # Modules that will be replaced, but are awaiting improvement PR:
    ('stock_inventory_xlsx', 'stock_inventory_valuation_report'),
    # Modules that need data migration
    ('account_asset', 'account_asset_management'),
    ('email_attachment_custom', 'mail_template_conditional_attachment'),
]

MODULES_PENDING_MIGRATION = [
    'account_bank_statement_import_caisse_epargne',
    'account_bank_statement_reconcile_option',
    'account_bank_reconciliation_rule',
    'account_payment_select_account',
    'account_product_fiscal_classification',
    'base_import_security_group',
    'pos_automatic_cashdrawer',
    'pos_payment_terminal_return',
    'product_to_scale_bizerba',
    'purchase_operation_adjust',
    'l10n_fr_pos_cert_base',
    'web_widget_image_webcam',
]
