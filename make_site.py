#!/usr/bin/env python3
# -*- coding: utf-8 -*- #

"""=============================================================================
                        SITE BUILDER using Pelican

Script can build local server or push site to GitHub. Have additional 
sub-arguments.

            Attention! Use only in your virtual enviroment!

                    Created by Dmytro Hoi - 2019 (c)
============================================================================="""

# from os import system
import subprocess
from sys import path as sys_path, modules, stdout
from os import path as os_path
from json import load as json_load, dump as json_dump, JSONDecodeError
import argparse

def parse_arguments():
    functions = ['github', 'local', 'backup']

    functions_description = "".join(
        name + " - " + getattr(modules[__name__], name).__doc__
             for name in functions)

    parser = argparse.ArgumentParser(
                        description=modules[__name__].__doc__,
                        epilog=f'Functions:\n    {functions_description}',
                        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('function', \
                        choices=functions, \
                        help='choose function, what you wanna start')

    parser.add_argument('-b', dest='make_backup', action='store_true',
                        help='make backup')
    parser.add_argument('-d', dest='allow_draft', action='store_true',
                        help='add drafts to repository')
    return parser.parse_args()


def parse_config():
    try:
        with open('config.json', mode='r') as config:
            return json_load(config)

    except (FileNotFoundError, JSONDecodeError):
        settings = {}
        settings_request = {
        'output': 'Set path to output folder ["output"]:',
        'gh-output': 'Set path to GitHub output folder ["gh-output"]:',
        'repo-url': 'Set repository URL:',
        'backup-url': 'Set backup URL:',
        'publishconf.py': 'Choose your publish config ["publishconf.py"]:',
        'project_path': 'Please send relative path to site project directory ("./" for current directory):'
        }
    
        print('Please, configure project!\n(inside brackets - default value)\n')
        for key, value in settings_request.items():
            answer = None

            # If it's not first time and message don't have default value - retry
            # else - after first input use default value
            while not answer and \
              ('[' not in value if answer is not None else True):
                answer = input(value)
            settings[key] = answer.strip() if answer else key
        with open('config.json', mode='w') as config:
            json_dump(settings, config)
        return settings


def shell_run(command:str, setup=False):
    """ Run bash 'command' and return info - 'Successful/Unsuccessful'

    Args:
        setup: bool - if after error need try install requirements.txt

    Return:
        bool - status of execution
    """
    def _run(command):
        proc = subprocess.Popen(command, \
                cwd=os_path.join(sys_path[0], settings['project_path']), \
                shell=True, stderr=stdout, stdout=stdout)
        proc.communicate()
        return proc.poll()

    ignore_returncode_from = ['fuser', 'rm', 'git']
    ignore_check = any([ command.startswith(_from) for _from in ignore_returncode_from ])
    returncode = _run(command)

    pass_capture = f'[INFO] Successful run bash command {command}'
    fail_capture = f'[{"INFO" if setup else "ERROR"}] Unsuccessful run bash command {command}'

    if returncode == 0 or ignore_check:
        return print(pass_capture)
    elif setup:
        return shell_run('pip3 install -r requirements.txt')
    elif command.startswith('pip3 install'):
        raise ValueError('[ERROR] Requirements not installed! '\
            'Please put requirements to requirements.txt in project directory')
    raise ValueError(fail_capture)


def backup(*_):
    """ Backup all in dir to backup repository

    Args:
        None

    Return:
        None
    """
    _commands_workflow = [
        'git add -A',
        'git commit -m "Site backuped using make_site script"',
        'git push --force ' + settings['backup-url'],
    ]

    for _command in _commands_workflow:
        shell_run(_command)
    
    return print('[INFO] Successful backuped your site')


def github(shell_args):
    """ Make gh-output and push it to github page

    Args:
        -d: bool - add drafts to repository
        -b: bool - make backup

    Return:
        None
    """

    if shell_args.make_backup:
        backup()
    else:
        print('[INFO] Directory not backuped.')

    if shell_args.allow_draft:
        print('[INFO] Drafts will be load!')
    else:
        print('[INFO] Drafts can\'t loaded.')

    _commands_workflow = [
        f'pelican content -o {settings["gh-output"]} '\
            + f' -s {settings["publishconf.py"]}',
        '' if shell_args.allow_draft else \
            f'rm -rf {settings["gh-output"]}/drafts'
        f'ghp-import {settings["gh-output"]}',
        f'git push --force {settings["repo-url"]} gh-pages:master',
        f'rm -rf {settings["gh-output"]}'
    ]

    for _command in _commands_workflow:
        if not _command: continue
        setup = _command.startswith('pelican')
        shell_run(_command, setup)

    return print('[INFO] Site successful published')


def local(*_):
    """ Make local server using `pelicanconf.py` file
    Use Ctrl+C for stop server!

    Args:
        None

    Return:
        None
    """
    _commands_workflow = [
        f'rm -rf {settings["output"]}',
        'fuser -k 8000/tcp',
        'make html && make serve'
    ]
    for _command in _commands_workflow:
        setup = _command.startswith('make')
        shell_run(_command)
    return print('[INFO] Local server stopped!')

settings = parse_config()

def main():
    shell_args = parse_arguments()

    try:
        globals()[shell_args.function](shell_args)
    except ValueError as error_message:
        print(error_message)
    return


if __name__ == "__main__":
    main()
