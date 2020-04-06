#!/usr/bin/env python
from __future__ import print_function
import click
import click_odoo
from config import *

import logging
_logger = logging.getLogger(__name__)


def _report_modules_states(env):
    # Modules to install
    modules = env['ir.module.module'].search([
        ('state', '=', 'to install')])
    if modules:
        _logger.warning(
            '\n\nModules to install:\n%s' % '\n'.join(modules.mapped('name')))
    # Modules to update
    modules = env['ir.module.module'].search([
        ('state', '=', 'to upgrade')])
    if modules:
        _logger.warning(
            '\n\nModules to update:\n%s' % '\n'.join(modules.mapped('name')))
    # Modules to remove
    modules = env['ir.module.module'].search([
        ('state', '=', 'to remove')])
    if modules:
        _logger.warning(
            '\n\nModules to remove:\n%s' % '\n'.join(modules.mapped('name')))


def _deactivate_custom_views(env):
    '''
    Gets views that are not linked to any
    installed module (no ir.model.data)
    '''

    ir_model_data = env['ir.model.data'].search([
        ('model', '=', 'ir.ui.view')])
    view_ids = env['ir.ui.view'].search([
        ('id', 'not in', ir_model_data.mapped('res_id'))])
    for view in view_ids:
        _logger.info('Deactivating custom view (%s): %s' % (
            view.type, view.name))
        view.write({
            'active': False,
            'name': '%s | Deactivated because of migration' % view.name,
        })


def _deactivate_orphan_views(env):
    '''
    Orphan views are views of uninstalled modules
    For some reason OpenUpgrade keept them.
    '''
    uninstalled_modules = env['ir.module.module'].search([
        ('state', 'not in', ['installed', 'to upgrade'])])
    ir_model_data = env['ir.model.data'].search([
        ('module', 'in', uninstalled_modules.mapped('name')),
        ('model', '=', 'ir.ui.view')])
    view_ids = env['ir.ui.view'].search([
        ('id', 'in', ir_model_data.mapped('res_id'))])
    for view in view_ids:
        _logger.info('Deactivating orphan view (%s): %s' % (
            view.type, view.name))
        view.write({
            'active': False,
            'name': '%s | Deactivated orphan view' % view.name,
        })


def _fix_deprecated_ir_values(env):
    '''
    ir.values does not exist anymore in 12.0
    But for some reason, ir_model_data still points to that
    model for some old act_window actions.

    This function will remove the related act_window, and its
    ir_model_data.

    https://github.com/OCA/OpenUpgrade/issues/2270
    '''
    ir_model_data = env̈́['ir.model.data'].search([
        ('model', '=', 'ir.values')])
    ir_model_data.unlink()


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
        ('state', 'in', ['to upgrade']),
        ('name', 'not in', modules_to_uninstall)])
    if modules:
        _logger.info('Upgrading modules: %s', modules.mapped('name'))
        modules.button_immediate_upgrade()


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

    module_ids = ir_module.search([
        ('name', 'in', modules_to_uninstall),
        ('state', 'in', ['installed', 'to upgrade', 'to remove']),
    ])

    # Force installed state
    # Because odoo won't uninstall modules in 'to upgrade' state
    module_ids.write({'state': 'installed'})
    _logger.info('Uninstalling modules: %s' % module_ids.mapped('name'))
    module_ids.button_immediate_uninstall()


def _install_modules(env):
    '''
    Install all planned to install modules
    '''
    ir_module = env['ir.module.module']
    modules_to_install = (
        MODULES_TO_INSTALL
        + [i[1] for i in MODULES_TO_REPLACE]
    )

    module_ids = env['ir.module.module'].search([
        ('name', 'in', modules_to_install)])

    missing_modules = set(modules_to_install) - set(module_ids.mapped('name'))
    if missing_modules:
        _logger.error(
            'Trying to install modules that are missing: '
            '%s' % missing_modules)

    _logger.info('Installing modules: %s' % module_ids.mapped('name'))
    module_ids.button_immediate_install()


def _apply_post_fixes(env):
    '''
    Post migration required by some modules
    TODO: Move this to a separate file
    '''

    # Fix modules left in inconsistent states
    module_ids = ir_module.search([
        ('state', 'in', ['to upgrade', 'to remove'])])
    module_ids.write({'state': 'installed'})

    # pos_payment_terminal: field renamed
    env.cr.execute("""
        UPDATE account_journal SET pos_terminal_payment_mode = payment_mode;
    """)


def _apply_configs(env):
    '''
    Applies configurations needed in 12.0
    '''

    # Pos configurations
    pos_configs = env['pos.config'].search([])
    for config in pos_configs:
        if config.pricelist_id:
            config.write(
                {
                    'use_pricelist': True,
                    'available_pricelist_ids': [(4, config.pricelist_id.id)],
                 }
            )

    # web_m2x_options config
    param = env['ir.config_parameter'].sudo().set_param(
        'web_m2x_options.create', 'False')


@click.command()
@click_odoo.env_options(default_log_level='error')
def main(env):
    _logger.info('Starting post clean..')
    ir_module = env['ir.module.module']
    ir_module.update_list()
    _logger.info('Module list updated...')

    # Already done in pre-9.0 so probably not needed here
    # anyways, it doesn't hurt
    _deactivate_custom_views(env)
    _deactivate_orphan_views(env)

    # This should probably be fixed in openupgrade
    _fix_deprecated_ir_values(env)

    _upgrade_modules(env)
    _uninstall_modules(env)
    _install_modules(env)

    # Almost ready, time for last minute fixes and config setup
    _apply_post_fixes(env)
    _apply_configs(env)


if __name__ == '__main__':
    main()
