#!/usr/bin/env python3
# -*- coding: utf-8 -*- #

"""
SITE BUILDER using Pelican

Script can build local server or push site to GitHub.
Have additional sub-arguments for allow drafts and backup on push.

ATTENTION: Use only in your virtual environment!

Created by Dmytro Hoi - 2019 (c)
"""

# from os import system
from subprocess import Popen
from sys import path as sys_path, modules, stdout
from os import path as os_path
from json import load as json_load, \
                 dump as json_dump, \
                 JSONDecodeError
from argparse import ArgumentParser, RawDescriptionHelpFormatter

settings: dict


def parse_commandline_arguments():
    """Parse commandline arguments passed to script."""
    global commandline_args
    global epilog

    func_descriptions = "\n".join(
        f"\t'{name}' - {func.__doc__}" for name, func in FUNCS.items()
    )

    parser = ArgumentParser(
                        description=modules[__name__].__doc__,
                        epilog=f'Functions:\n{func_descriptions}',
                        formatter_class=RawDescriptionHelpFormatter)

    parser.add_argument('function', choices=FUNCS,
                        help='choose a function, what you wanna start')

    parser.add_argument('-b', dest='make_backup', action='store_true',
                        help='make backup of current commit')
    parser.add_argument('-d', dest='allow_draft', action='store_true',
                        help='add drafts to repository')

    epilog = parser.epilog
    commandline_args = parser.parse_args()
    return


def load_configuration():
    """Load a configuration file.

    If config.json not exists in current folder it will be created
    using configure function.

    Args:
        None

    Returns:
        dict: dict contains script settings

    """
    global settings

    try:
        with open('config.json', mode='r') as config:
            settings = json_load(config)

    except (FileNotFoundError, JSONDecodeError):
        print('Configuration file "config.json not found!"')
        settings = configure()


def configure() -> dict:
    """Create a configuration file on first run by quiz.

    Args:
        None

    Returns:
        dict: dict contains script settings

    """
    setting_messages = {
        'output': 'Set path to output folder ["output"]:',
        'gh-output': 'Set path to GitHub output folder ["gh-output"]:',
        'repo-url': 'Set repository URL:',
        'backup-url': 'Set backup URL:',
        'publishconf.py': 'Choose your publish config ["publishconf.py"]:',
        'project_path': 'Please send relative path to site project directory \n'\
            '\t("./" for current directory) ["./"]:'
    }

    print('Please, configure project.\n'
          '(brackets contains default value)\n\n')

    settings = {}
    for setting, message in setting_messages.items():
        answer = None
        default_check = None

        while not default_check and not answer:
            default_check = '[' in message
            answer = input(message)

        settings[setting] = answer.strip() if answer else setting

    # Save config to file
    with open('config.json', mode='w') as config:
        json_dump(settings, config)

    return settings


def shell_run(commands: list):
    """Run bash 'command' and return info - 'Successful/Unsuccessful'.

    Args:
        setup: bool - if after error need try install requirements.txt

    Return:
        bool - status of execution

    """
    _REQUIREMENTS_ERROR = ['pelican', 'make']
    _IGNORE_RETURNCODE = ['fuser', 'rm', 'git']
    _project_path = os_path.join(sys_path[0], settings['project_path'])

    def _run(command: str):
        process = Popen(command, shell=True, stderr=stdout,
                        stdout=stdout, cwd=_project_path)
        process.communicate()
        return process.poll()

    for _command in commands:
        ignore_returncode_check = any(
            [_command.startswith(_from) for _from in _IGNORE_RETURNCODE]
        )
        requirements_error_check = any(
            [_command.startswith(_from) for _from in _REQUIREMENTS_ERROR]
        )
        result = _run(_command)

        if result == 0 or ignore_returncode_check:
            print(f'[INFO] Successfully run bash command {_command}')
            if _command.startswith('pip3 install'):
                print('["INFO"] Requirements was setup, please try again!')
                return
            continue
        elif requirements_error_check:
            print(f'["INFO"] Unsuccessfully run bash command {_command}')
            print(f'["INFO"] Try to install requirements from {_project_path}'\
                '/requirements.txt')
            return shell_run(['pip3 install -r requirements.txt'])
        elif _command.startswith('pip3 install'):
            print('[ERROR] Requirements not installed! '\
                f'Please show error message above of add requirements '\
                'to {_project_path}/requirements.txt')
            break
        print(f'["ERROR"] Unsuccessfully run bash command {_command}')
        break


def github_push(args):
    """Make gh-output and push it to github page.

    Args:
        -d: bool - add drafts to repository
        -b: bool - make backup

    """
    _COMMANDS = [
        f'pelican content -o {settings["gh-output"]} -s {settings["publishconf.py"]}',
        f'ghp-import {settings["gh-output"]}',
        f'git push --force {settings["repo-url"]} gh-pages:master',
        f'rm -rf {settings["gh-output"]}'
    ]

    if args.make_backup:
        make_backup()
    else:
        print('[INFO] The project does not require backup.')

    if args.allow_draft:
        print('[INFO] Drafts will be loaded!')
    else:
        _COMMANDS.insert(1, f'rm -rf {settings["gh-output"]}/drafts')
        print('[INFO] Drafts will not be loaded.')

    shell_run(_COMMANDS)
    return print('[INFO] Site successfully published!')


def start_local_server(*args):
    """Start local server using `pelicanconf.py` file.

    NOTE: Use Ctrl+C for stop server.

    """
    _COMMANDS = [
        f'rm -rf {settings["output"]}',
        'fuser -k 8000/tcp',
        'make html && make serve'
    ]
    shell_run(_COMMANDS)
    return print('[INFO] Local server stopped!')


def make_backup(*args):
    """Backup all files and directories in project directory
    to backup repository."""
    _COMMANDS = [
        'git add -A',
        'git commit -m "Backup site using make_site script"',
        f'git push --force {settings["backup-url"]}',
    ]

    shell_run(_COMMANDS)
    return print('[INFO] Backup completed')



FUNCS = {
        'github': github_push,
        'local': start_local_server,
        'backup': make_backup
}


def main():
    """Start main workflow."""
    load_configuration()
    try:
        parse_commandline_arguments()
    except:
        return print(epilog)

    chosen_function = FUNCS.get(commandline_args.function)
    if chosen_function is not None:
        chosen_function(commandline_args)
    return


if __name__ == "__main__":
    main()
