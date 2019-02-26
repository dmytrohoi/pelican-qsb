#!/usr/bin/env python3
# -*- coding: utf-8 -*- #

"""=============================================================================
                        SITE BUILDER using Pelican

Script can build local server or push site to GitHub. Have additional 
sub-arguments.

            Attention! Use only in your virtual enviroment!

                    Created by Dmytro Hoi - 2019 (c)
============================================================================="""

from os import system
from sys import argv

OUTPUT_FOLDER = 'output'
GH_OUTPUT_FOLDER = 'gh-output'
GH_REPO_URL = 'git@github.com:dmytrohoi/dmytrohoi.github.io.git'
GH_BACKUP_REPO_URL = 'git@github.com:dmytrohoi/site_backup.git'
PUBLISH_CONFIG_FILE = 'publishconf.py'


def shell_run(command, setup=False):
    """ run bash 'command' and return info - 'Successful/Unsuccessful'
    setup: Bool - if after error need try install requirements.txt"""
    result_code = system(command)

    if result_code == 0:
        return print(f'[INFO] Succesful run bash command {command!r}')
    print(f'[INFO] Unsuccesful run bash command {command!r}')

    if setup:
        print('\n\t[!!!]\tRequirements installing request..\t[!!!]\t\n')
        return system('pip3 install -r requirements.txt')


def backup():
    """ backup all in dir to backup repo """
    shell_run('git add . && git commit -m "Site backup" && git push --force '
              + f'{GH_BACKUP_REPO_URL}')


def github(*params):
    """ make gh-output and push it to github page
             -d          add drafts to repository;
             -b          make backup; """

    params = {
        'publish_drafts': '-d' in params,
        'make_backup': '-b' in params,
    }

    shell_run(
            f'pelican content -o {GH_OUTPUT_FOLDER} -s {PUBLISH_CONFIG_FILE}',
            setup=True
        )

    print('[INFO] Drafts will be load!') if params['publish_drafts'] else \
        shell_run(f'rm -rf {GH_OUTPUT_FOLDER}/drafts')

    backup() if params['make_backup'] else \
        print('[INFO] Directory not backuped!')

    shell_run(f'ghp-import {GH_OUTPUT_FOLDER}')
    shell_run(f'git push --force {GH_REPO_URL} gh-pages:master')
    shell_run(f'rm -rf {GH_OUTPUT_FOLDER}')
    return


def local_host(*args):
    """ make local server using pelicanconf file """
    shell_run(f'rm -rf {OUTPUT_FOLDER}')
    shell_run('fuser -k 8000/tcp')
    shell_run('make html && make serve', setup=True)
    return


def help_doc(*args):
    """ print functions annotations """
    help_info = f'{__doc__}\n\tFunctions:\n\n'
    for name, func in FUNCTIONS.items():
        help_info += f'  {name:22.16}{func.__doc__}\n'
    return print(help_info)


unknow_command = lambda *a: print('\n[ERROR] Unknow command! For help use ' \
                                  f'"python {__file__} help"..\n')


FUNCTIONS = {
        'github': github,
        'local': local_host,
        'backup': backup,
        'help': help_doc,
    }


def main():
    try:
        FUNCTIONS.get(argv[1], unknow_command)(*argv[2:])
    except IndexError:
        help_doc()

    return print('='*77)


if __name__ == "__main__":
    main()
