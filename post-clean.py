#!/usr/bin/python
from __future__ import print_function
import click
import click_odoo


@click.command()
@click_odoo.env_options(default_log_level='error')
def main(env):
    MODULES_TO_UNINSTALL = [
        'create_users_partners', 'connector',
        'hr_equipment',  # Not found in 12.0, exist in 9.0 core modules
        'barcodes_generate',
        # barcodes_generate splitted into barcodes_generator_abstract
        #                                 barcodes_generator_partner
        #                                 barcodes_generator_product
        'email_pos_receipt',    # renamed to pos_ticket_send_by_mail

        # Not Migrated yet.
        'l10n_fr_pos_cert_base',

        ]
    for m in MODULES_TO_UNINSTALL:
        print('Installing module: %s..' % m)
        module_id = env['ir.module.module'].search([('name', '=', m)])
        if module_id:
            module_id.button_immediate_uninstall()
        else:
            print('Module not found: %s' % m)

    MODULES_TO_INSTALL = [
        'queue_job', 'web_responsive', 'product_print_category',
        'barcodes_generator_abstract', 'barcodes_generator_partner',
        'barcodes_generator_product', 'pos_order_return',
        'pos_ticket_send_by_mail',
        'account_bank_statement_reconciliation_report',

    ]
    for m in MODULES_TO_INSTALL:
        print('Installing module: %s..' % m)
        module_id = env['ir.module.module'].search([('name', '=', m)])
        if module_id:
            module_id.button_immediate_install()
        else:
            print('Module not found: %s' % m)


if __name__ == '__main__':
    main()
