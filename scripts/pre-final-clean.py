#!/usr/bin/python3
from __future__ import print_function
import click
import click_odoo
from config import *


def _upgrade_modules(env):
    '''
    Upgrade all installed modules, with exception
    of those that we plan to uninstall, because we
    may not have them in the sources.

    Idea is we upgrade modules first, so that our
    dependency tree no longer depends on modules
    that are planned to be uninstalled.
    '''
    ir_module = env['ir.module.module']
    modules_to_uninstall = (
        MODULES_TO_UNINSTALL
        + MODULES_PENDING_MIGRATION
        + [i[0] for i in MODULES_TO_REPLACE]
    )
    modules = ir_module.search([
        ('state', 'in', ['installed', 'to upgrade']),
        ('name', 'not in', modules_to_uninstall)])
    if modules:
        print('Updating modules: %s', modules.mapped('name'))
        modules.button_upgrade()


def _uninstall_modules(env):
    '''
    Uninstall all planned to uninstall modules.
    Some modules on this list might already have
    been uninstalled by pre-clean.

    But it's ok, we check again and if they're
    present we remove them.
    '''
    ir_module = env['ir.module.module']

    modules_to_uninstall = (
        MODULES_TO_UNINSTALL
        + MODULES_PENDING_MIGRATION
        + [i[0] for i in MODULES_TO_REPLACE]
    )

    for module in modules_to_uninstall:
        module_id = ir_module.search([('name', '=', module)])
        if not module_id:
            print('Module not found: %s' % module)
            continue
        # Skip modules that are not installed
        if module_id.state not in ['installed', 'to upgrade', 'to remove']:
            print('Skipping module uninstall: %s. Not installed.' % module)
            continue
        # Uninstall module
        print('Uninstalling module: %s..' % module)
        module_id.button_immediate_uninstall()


def _install_modules(env):
    '''
    Install all planned to install modules
    '''
    ir_module = env['ir.module.module']
    modules_to_install = (
        MODULES_TO_INSTALL
        + [i[1] for i in MODULES_TO_REPLACE]
    )

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
    env.cr.execute(
        "update ir_model_data set module='coop_account_check_deposit' where "
        "module='account_check_deposit' and model='account.journal'"
    )

    # model name changed from product.category.print to product.print.category
    env.cr.execute(
        "alter table product_template "
        "add column category_print_id_bkp integer;")
    env.cr.execute(
        "update product_template "
        "set category_print_id_bkp=category_print_id;")
    env.cr.execute(
        "alter table product_category_print "
        "rename to product_print_category;")
    env.cr.execute(
        "alter sequence product_category_print_id_seq rename to "
        "product_print_category_id_seq;")
    env.cr.execute(
        "update ir_model_data set model='product.print.category' where "
        "model='product.category.print';")
    env.cr.execute(
        "update ir_model_data set name='ppc_demo_category' where "
        "name='demo_category' and model='product.print.category';")

    ir_module.update_list()


@click.command()
@click_odoo.env_options(default_log_level='error')
def main(env):
    print('Starting post clean...')
    ir_module = env['ir.module.module']
    ir_module.update_list()
    print('modules list updated...')

    _upgrade_modules(env)
    _install_modules(env)
    _uninstall_modules(env)

    #  Weird problem: odoo.tools.convert.ParseError: "Invalid model name
    #  'create.shifts.wizard' in action definition. module: coop_shift
    env.cr.execute("delete from ir_act_window where name = 'Create Shifts';")

    # Apply configurations
    pos_configs = env['pos.config'].search([])
    for config in pos_configs:
        if config.pricelist_id:
            config.write(
                {
                    'use_pricelist': True,
                    'available_pricelist_ids': [(4, config.pricelist_id.id)],
                 }
            )

    print('Post cleaning finished successfully!')


if __name__ == '__main__':
    main()
