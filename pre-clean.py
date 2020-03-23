import click
import click_odoo
from config import *


@click.command()
@click_odoo.env_options(default_log_level='error')
def main(env):
    print('Pre cleaning started...')

    modules_to_uninstall = (
        + MODULES_TO_UNINSTALL
        + MODULES_PENDING_MIGRATION
        + [i[0] for i in MODULES_TO_REPLACE]
    )

    for module in modules_to_uninstall:
        # Skip modules that are depended by others,
        # because that might trigger a chain uninstall,
        # removing modules we don't want to remove.
        # These will be uninstalled by post-clean.
        depended_by = env['ir.module.module'].search([
            ('state', 'in', ['installed', 'to upgrade']),
            ('dependencies_id', 'in', module)])
        if depended_by:
            print((
                'Skipping module uninstall: %s, '
                'because it\'s dependend by: %s'
                ) % (module, depended_by.mapped('name')))
            continue

        module_id = env['ir.module.module'].search([('name', '=', module)])
        if not module_id:
            print('Module not found: %s' % module)
            continue

        # Skip modules that are not installed
        if module_id.state not in ['installed', 'to upgrade']:
            print('Skipping module uninstall: %s. Not installed.' % module)
            continue

        # Uninstall module
        print('Uninstalling module: %s..' % module)
        module_id.button_immediate_uninstall()

    print('Pre cleaning finished successfully!')


if __name__ == '__main__':
    main()
