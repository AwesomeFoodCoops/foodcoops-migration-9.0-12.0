#!/usr/bin/python3
from __future__ import print_function
import click
import click_odoo


@click.command()
@click_odoo.env_options(default_log_level='error')
def main(env):
    print('Starting post clean...')
    ir_module = env['ir.module.module']
    print('modules list updated...')
    ir_module.update_list()
    modules_to_install = [
        'queue_job', 'web_responsive', 'product_print_category',
        'barcodes_generator_abstract', 'barcodes_generator_partner',
        'barcodes_generator_product', 'pos_order_return',
        'pos_ticket_send_by_mail',
        'account_bank_statement_reconciliation_report',
        'coop_default_pricetag',
    ]
    for m in modules_to_install:
        print('Installing module: %s..' % m)
        module_id = ir_module.search([('name', '=', m)])
        if module_id:
            module_id.button_install()
        else:
            print('Module not found: %s' % m)

    # for account.jounal model: 'payment_mode' field is renamed to
    # 'pos_terminal_payment_mode' in pos_payment_terminal module
    env.cr.execute(
        'update account_journal set pos_terminal_payment_mode=payment_mode;')

    ir_module.update_list()

    modules_to_uninstall = [
        'marketing_campaign', 'hw_proxy',
        'create_users_partners', 'connector',
        'hr_equipment',  # Not found in 12.0, exist in 9.0 core modules
        'barcodes_generate',
        # barcodes_generate splitted into barcodes_generator_abstract
        #                                 barcodes_generator_partner
        #                                 barcodes_generator_product
        'email_pos_receipt',    # renamed to pos_ticket_send_by_mail

        # Not Migrated yet.
        'l10n_fr_pos_cert_base',
        'account_product_fiscal_classification',
        'server_mode', 'saas_client', 'server_mode_fetchmail',
        'server_mode_mail',
        ]
    for m in modules_to_uninstall:
        print('Uninstalling module: %s..' % m)
        module_id = ir_module.search([('name', '=', m)])
        if module_id:
            module_id.module_uninstall()
        else:
            print('Module not found: %s' % m)

    modules = ir_module.search(
        [('state', 'in', ('installed', 'to upgrade'))])
    if modules:
        print('Updating All modules...', len(modules))
        modules.button_upgrade()

    #  Weird problem: odoo.tools.convert.ParseError: "Invalid model name
    #  'create.shifts.wizard' in action definition. module: coop_shift
    env.cr.execute("delete from ir_act_window where name = 'Create Shifts';")

    print('Post cleaning finished successfully!')


if __name__ == '__main__':
    main()
