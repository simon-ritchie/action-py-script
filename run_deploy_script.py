"""Deploying script (GitHub Actions) that handle linting, tests, and
PyPI uploading.

Command example:
$ python apply_lints.py
"""

import re
import subprocess as sp
from logging import Logger
from typing import List
from typing import Match
from typing import Optional

from apply_lints_and_build_docs import FLAKE8_COMMAND
from apply_lints_and_build_docs import MYPY_COMMAND
from apply_lints_and_build_docs import NUMDOCLINT_COMMAND
from apysc import __version__
from apysc._console import loggers

logger: Logger = loggers.get_info_logger()


def _main() -> None:
    """Entry point of this command.
    """
    logger.info('Lint script started.')
    _run_flake8()
    _run_numdoclint()
    _run_mypy()
    _run_tests()
    _build()
    _save_version_env_var()


def _save_version_env_var() -> None:
    """
    Save version number to .env file.
    """
    logger.info('Saving version number file.')
    with open('.env', 'a') as f:
        f.write(f'VERSION="{__version__}"\n')


def _build() -> None:
    """
    Run build command.

    Raises
    ------
    Exception
        If there is any Traceback.
    """
    logger.info('Build command started.')
    stdout: str = _run_command(command='python build.py')
    if 'Traceback' in stdout:
        raise Exception('There is build command error.')


def _run_tests() -> None:
    """
    Run testing command.

    Raises
    ------
    Exception
        If there are any failed tests.
    """
    logger.info('testing command started.')
    stdout: str = _run_command(
        command=(
            'pytest --cov=./apysc tests/ -v -s --workers auto '
            '--cov-report term-missing'
        ))
    if ' failed, ' in stdout:
        raise Exception('There are failed tests.')
    _save_coverage(stdout=stdout)


def _save_coverage(stdout: str) -> None:
    """
    Svae test coverage to .env file.

    Parameters
    ----------
    stdout : str
        Test command stdout.
    """
    lines: List[str] = stdout.splitlines()
    coverage: str = ''
    for line in lines:
        if not line.startswith('TOTAL '):
            continue
        match: Optional[Match] = re.search(
            pattern=r'(\d+?\%)', string=line)
        if match is None:
            raise Exception('Test coverage value is missing.')
        coverage = match.group(1)
    logger.info('Saving version number file.')
    with open('.env', 'a') as f:
        f.write(f'COVERAGE="{coverage}"\n')


def _run_mypy() -> None:
    """
    Run mypy command.

    Raises
    ------
    Exception
        If there are any mypy errors.
    """
    logger.info('mypy command started.')
    stdout: str = _run_command(command=MYPY_COMMAND)
    if 'Success' not in stdout:
        raise Exception('There are mypy errors.')


def _run_numdoclint() -> None:
    """
    Run numdoclint command.

    Raises
    ------
    Exception
        If command standard out is not blank.
    """
    logger.info('numdoclint command started.')
    stdout: str = _run_command(command=NUMDOCLINT_COMMAND)
    if stdout != '':
        raise Exception('There are numdoclint errors.')


def _run_flake8() -> None:
    """
    Run flake8 command.

    Raises
    ------
    Exception
        If command standard out is not blank.
    """
    logger.info('flake8 command started.')
    stdout: str = _run_command(command=FLAKE8_COMMAND)
    if stdout != '':
        raise Exception('There are flake8 errors or warning.')


def _run_command(command: str) -> str:
    """
    Run lint command and return its stdout.

    Parameters
    ----------
    command : str
        Target lint command.

    Returns
    -------
    stdout : str
        Command result stdout.
    """
    logger.info(f'Target command: {command}')
    complete_process: sp.CompletedProcess = sp.run(
        command, shell=True, stdout=sp.PIPE, stderr=sp.STDOUT)
    stdout: str = complete_process.stdout.decode('utf-8')
    stdout = stdout.strip()
    if stdout == '[]':
        stdout = ''
    print(stdout)
    return stdout


if __name__ == '__main__':
    _main()
