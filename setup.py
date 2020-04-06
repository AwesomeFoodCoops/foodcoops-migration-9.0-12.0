#!/usr/bin/env python

import os
import sys
from multiprocessing import cpu_count
from subprocess import check_call


SOURCES = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'sources',
)


if not os.path.exists(SOURCES):
    print('Creating %s..' % SOURCES)
    os.makedirs(SOURCES)


print('Adding final project repositories')
REPOSITORIES = os.path.join(SOURCES, 'repositories')
if not os.path.exists(REPOSITORIES):
    os.makedirs(REPOSITORIES)

check_call(
    [
        'gitaggregate',
        '--config',
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'repos.yml'),
        '--jobs',
        str(cpu_count() or 1),
    ],
    cwd=REPOSITORIES,
    stderr=sys.stderr,
    stdout=sys.stdout,
)
