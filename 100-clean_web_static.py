#!/usr/bin/python3
# Fabric Script that deletes out-of-date archives

from fabric.api import *
import os

env.hosts = ["100.25.118.136", "54.160.105.221"]
env.user = 'ubuntu'


def do_clean(number=0):
    """Deletes out-of-date archives"""
    number = int(number)
    if number == 0 or number == 1:
        number = 1
    number += 1
    with lcd('versions'):
        archives = sorted(os.listdir('.'))
        [archives.pop() for i in range(number)]
        [local('rm -f {}'.format(archive)) for archive in archives]
    with cd('/data/web_static/releases'):
        archives = run('ls -tr').split()
        [archives.pop() for i in range(number)]
        [run('rm -f {}'.format(archive)) for archive in archives]
