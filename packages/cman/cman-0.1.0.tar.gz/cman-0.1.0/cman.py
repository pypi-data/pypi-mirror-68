#!/usr/bin/env python3

import shutil
import urllib.request
from argparse import ArgumentParser
from hashlib import md5
from os import chdir, makedirs
from os.path import dirname, expanduser, isdir, isfile, join
from subprocess import check_call
from tempfile import NamedTemporaryFile

import yaml
import os


def call(*args):
    if len(args) == 1 and ' ' in args[0]:
        return check_call(args[0].split())
    return check_call(args)


class BaseFolder:
    def __init__(self, root):
        self.root = root

    def folder(self, *path):
        p = join(self.root, *path)
        makedirs(p, exist_ok=True)
        return p


def main():
    parser = ArgumentParser(description='Container manager')
    parser.add_argument('conf_file', help='YAML configuration file of container')
    args = parser.parse_args()
    
    if not os.geteuid() == 0:
        parser.error('Script must be run as root')

    with open(args.conf_file) as f:
        conf = yaml.safe_load(f)

    base_url = conf['base_url']
    image_root = conf['base_root']
    container_name = conf['name']
    command = conf['command']

    base_hash = md5(base_url.encode()).hexdigest()[:8]
    base = BaseFolder(join(expanduser('~'), '.local', 'share', 'cman'))
    download_file = join(base.folder('images'), '{}.tar.gz'.format(base_hash))
    if not isfile(download_file):
        with NamedTemporaryFile() as nf:
            call('wget', base_url, '-O', nf.name)
            shutil.move(nf.name, download_file)
            nf.delete = False

    rootfs = join(base.folder('containers'), container_name)
    rootfs_proc = join(rootfs, 'proc')
    if not isdir(rootfs):
        chdir(dirname(download_file))
        call('tar', '-xzvf', download_file)
        call('mv', image_root, rootfs)

    chdir(rootfs)
    call('sudo', 'mount', '--bind', '/proc', rootfs_proc)
    try:
        call('sudo', 'unshare', '-p', '-f', '--mount-proc={}'.format(rootfs_proc), 'chroot', rootfs, '/bin/bash', '-c', command)
    finally:
        call('sudo', 'umount', rootfs_proc)


if __name__ == '__main__':
    main()
