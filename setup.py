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


print('Generating openupgrade repos.yml..')

versions = ['9.0', '10.0', '11.0', '12.0']
content = '\n'.join(['''
openupgrade-{branch}:
  defaults:
    depth: 1
  remotes:
    origin: https://github.com/OCA/openupgrade.git
  merges:
    - origin {branch}
  target: origin {branch}
'''.format(branch=version) for version in versions])

repos_file = os.path.join(SOURCES, 'openupgrade.yml')
with open(repos_file, 'w+') as file:
    file.write(content)


print('Aggregatting openugprade requirements..')
check_call(
    [
        'gitaggregate',
        '--config',
        repos_file,
    ],
    cwd=SOURCES,
    stderr=sys.stderr,
    stdout=sys.stdout,
)
os.remove(repos_file)


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
