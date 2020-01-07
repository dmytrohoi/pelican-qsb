#!/usr/bin/env python3
# -*- coding: utf-8 -*- #
"""
QUICK SITE BUILDER for Pelican (https://github.com/getpelican)

Script can build local server or push site to GitHub.
Have additional sub-arguments for allow drafts and backup on push.

ATTENTION: Use only in your virtual environment!

Author: Dmytro Hoi (https://github.com/dmytrohoi), 2019
"""
import sys

from subprocess import Popen
from os import path as os_path, getcwd
from json import dump as json_dump, load as json_load

from argparse import (ArgumentParser,
                      RawDescriptionHelpFormatter)

import logging

# Setup Logging
logger = logging.Logger(__name__, logging.INFO)
sh = logging.StreamHandler()
sh.setFormatter(logging.Formatter(" [ %(levelname)s ] %(message)s"))
logger.addHandler(sh)


def parse_commandline_arguments():
    """Parse commandline arguments passed to script."""
    parser = ArgumentParser(description=sys.modules[__name__].__doc__,
                            formatter_class=RawDescriptionHelpFormatter)

    parser.add_argument('function', choices=FUNCS,
                        help='choose a function, what you wanna start')

    parser.add_argument('-b', dest='make_backup', action='store_true',
                        help='make backup of current commit')
    parser.add_argument('-d', dest='allow_draft', action='store_true',
                        help='add drafts to repository')

    try:
        return parser.parse_args()
    except SystemExit:
        return None


def configure() -> dict:
    """Create a configuration file on first run by quiz.

    Args:
        None

    Returns:
        dict: dict contains script settings

    """
    available_settings = {
        'project_path': 'Please send full path to site project directory \n'
                        '\t or leave empty for current directory ["./"]:',
        'output': 'Set name of output folder ["output"]:',
        'gh-output': 'Set name of GitHub output folder ["gh-output"]:',
        'repo-url': 'Set repository URL:',
        'backup-url': 'Set backup URL:',
        'publishconf.py': 'Choose your publish config ["publishconf.py"]:',
    }

    logger.info('Please, configure project.\n'
                '(brackets contains default value)\n\n')

    _settings = {}
    for option, message in available_settings.items():
        answer = None
        default_check = None

        while not default_check and not answer:
            default_check = '[' in message
            answer = input(message)

        _chosen_value = answer.strip() if answer else option
        if option == 'project_path' and not answer:
            _option_value = CURRENT_DIR_PATH
        else:
            if 'url' in option:
                _option_value = _chosen_value
            else:
                _option_value = os_path.join(CURRENT_DIR_PATH, _chosen_value)

        _settings[option] = _option_value

    # Save config to file
    with open(CONFIG_FILE_PATH, mode='w') as config_file:
        json_dump(_settings, config_file)

    logger.info('Configuration file has been created!\n\n')
    return _settings


def shell_run(commands: list):
    """Run bash 'command' and return info - 'Successful/Unsuccessful'.

    Args:
        setup: bool - if after error need try install requirements.txt

    Return:
        bool - status of execution

    """
    _requirements_error_from = ['pelican', 'make']
    _ignore_returncode_from = ['fuser', 'rm', 'git']
    _project_path = SETTINGS['project_path']

    def _run(command: str):
        process = Popen(command, shell=True, stderr=sys.stdout,
                        stdout=sys.stdout, cwd=_project_path)
        process.communicate()
        return process.poll()

    for _command in commands:
        ignore_returncode_check = any(
            [_command.startswith(_from) for _from in _ignore_returncode_from]
        )
        requirements_error_check = any(
            [_command.startswith(_from) for _from in _requirements_error_from]
        )
        result = _run(_command)

        if result == 0 and _command.startswith('pip install'):
            logger.info('Requirements has been setup, please try again!')
            break
        elif result == 0 or ignore_returncode_check:
            logger.info(f'Run of bash command {_command} finished!')
        elif requirements_error_check:
            logger.info(f'Run of bash command {_command} failed!')
            logger.info(f'Try to install requirements from {_project_path}'
                        '/requirements.txt')
            shell_run(['pip install -r requirements.txt'])
        else:
            if _command.startswith('pip install'):
                logger.error('Requirements not installed from '
                             f'{_project_path}/requirements.txt !')
            logger.error(f'Run of bash command {_command} failed!')
            sys.exit(1)


def github_push(args):
    """Make gh-output and push it to github page.

    Args:
        -d: bool - add drafts to repository
        -b: bool - make backup

    """
    commands_list = [
        f'pelican content -o {SETTINGS["gh-output"]} '
        '-s {SETTINGS["publishconf.py"]}',
        f'ghp-import {SETTINGS["gh-output"]}',
        f'git push --force {SETTINGS["repo-url"]} gh-pages:master',
        f'rm -rf {SETTINGS["gh-output"]}'
    ]

    if args.make_backup:
        make_backup()
    else:
        logger.info('The project does not require backup.')

    if args.allow_draft:
        logger.info('Drafts will be loaded!')
    else:
        commands_list.insert(1, f'rm -rf {SETTINGS["gh-output"]}/drafts')
        logger.info('Drafts will not be loaded.')

    shell_run(commands_list)
    logger.info('Site successfully published!')


def start_local_server(*_):
    """Start local server using `pelicanconf.py` file.

    NOTE: Use Ctrl+C for stop server.

    """
    logger.info('Use Ctrl+C for stop server!')
    commands_list = [
        f'rm -rf {SETTINGS["output"]}',
        'fuser -k 8000/tcp',
        'make html && make serve'
    ]
    shell_run(commands_list)
    logger.info('Local server stopped!')


def make_backup(*_):
    """Backup all files and directories in project directory
    to backup repository."""
    commands_list = [
        'git add -A',
        'git commit -m "Backup site using make_site script"',
        f'git push --force {SETTINGS["backup-url"]}',
    ]

    shell_run(commands_list)
    logger.info('Backup completed')


def main():
    """Start main workflow."""
    cmd_args = parse_commandline_arguments()

    if not cmd_args:
        instruction = "\n\nFunctions:\n" + "\n".join(
            f"'{name}' - {func.__doc__}" for name, func in FUNCS.items()
        )
        print(instruction)
        return

    FUNCS.get(cmd_args.function)(cmd_args)


# Load Configuration
CURRENT_DIR_PATH = getcwd()
CONFIG_FILE_PATH = os_path.join(CURRENT_DIR_PATH, 'qsb-config.json')

if os_path.exists(CONFIG_FILE_PATH):
    with open(CONFIG_FILE_PATH, mode='r') as config:
        SETTINGS = json_load(config)
else:
    logger.warning(f'Configuration file "{CONFIG_FILE_PATH}" not found!\n\n')
    SETTINGS = configure()

FUNCS = {
        'github': github_push,
        'local': start_local_server,
        'backup': make_backup
}


if __name__ == "__main__":
    main()
