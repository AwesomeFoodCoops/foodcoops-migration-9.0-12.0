#!/usr/bin/env python

import os
import sys
from multiprocessing import cpu_count
from subprocess import check_call


SOURCES = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'sources',
)

RESOURCES = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'resources',
)


if not os.path.exists(SOURCES):
    print('Creating %s..' % SOURCES)
    os.makedirs(SOURCES)


for version in ['9.0', '10.0', '11.0', '12.0']:
    print('Cloning repositories: %s..' % version)
    REPOSITORIES = os.path.join(SOURCES, version)
    if not os.path.exists(REPOSITORIES):
        os.makedirs(REPOSITORIES)
    check_call(
        [
            'gitaggregate',
            '--expand-env',
            '--config',
            os.path.join(RESOURCES, 'repos.%s.yml' % version),
            '--jobs',
            str(cpu_count() or 1),
        ],
        cwd=REPOSITORIES,
        env=dict(os.environ, ODOO_VERSION=version),
        stderr=sys.stderr,
        stdout=sys.stdout,
    )
