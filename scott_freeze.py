from __future__ import print_function

from contextlib import contextmanager

import argparse
from functools import partial
import os
import shutil
from subprocess import Popen, PIPE
import sys
import tempfile


HEADER = """# Generated file. Please do not edit manually
#
# `requirements.in` contains direct dependencies (and may be >version instead
# of ==version) This file is a list of dependencies and _their_ dependencies,
# completely frozen.  To generate this file, use scott-freeze
#
# Example
#     $ scott-freeze requirements.in > requirements.txt
#"""


class Abort(Exception):
    pass


def setup_argparse():
    parser = argparse.ArgumentParser(
        description='Generate a complete requirements file with all '
        'dependencies pinned')
    parser.add_argument(
        'requirements', metavar='requirements.in',
        help='direct requirements; may be unpinned')
    parser.add_argument(
        '--python', help='python interpreter for virtualenv to use')
    parser.add_argument(
        '--verbose', action='store_true', help='verbose output')
    return parser


def parse_cmdline():
    parser = setup_argparse()
    args = parser.parse_args()
    return args


@contextmanager
def tempdir():
    path = tempfile.mkdtemp(suffix='scott_freeze')
    try:
        yield path
    finally:
        shutil.rmtree(path)


def write_err(text):
    sys.stderr.write(text)
    sys.stderr.write('\n')


def run_or_abort(cmd, verbose=False):
    proc = Popen(cmd, stdout=PIPE)
    output = []
    for line in iter(proc.stdout.readline, b''):
        output.append(line.decode('utf-8'))
        if verbose:
            sys.stderr.write(line)

    output = ''.join(output)

    proc.communicate()  # close stdout. wait for proc to exit
    if proc.returncode != 0 and not verbose:
        write_err(output)
        raise Abort()

    return output


def find_index_urls(req_file):
    found = []
    with open(req_file) as handle:
        for line in handle:
            line = line.strip()
            if line.startswith('-i') or line.startswith('--index-url'):
                found.append(line)
            elif line.startswith('--extra-index-url'):
                found.append(line)

    return found


def install_and_freeze(req_file, python=None, verbose=False):
    # make temp virtualenv
    if python is not None:
        python = ['--python', python]
    else:
        python = []

    with tempdir() as path:
        run = partial(run_or_abort, verbose=verbose)

        run(['virtualenv'] + python + [path])

        pip_path = os.path.join(path, 'bin', 'pip')
        run([pip_path, 'install', '-r', req_file])
        pinned = run([pip_path, 'freeze', '-l']).splitlines()
        pinned = sorted(pinned, key=lambda req: req.lower())

        return pinned


def generate(args):
    if not os.path.exists(args.requirements):
        write_err('No such file: {}'.format(args.requirements))
        raise Abort()

    index_url_lines = find_index_urls(args.requirements)
    pinned = install_and_freeze(args.requirements, args.python, args.verbose)

    print(HEADER)
    print()
    print('\n'.join(index_url_lines))
    print()
    print('\n'.join(pinned))


def main():
    args = parse_cmdline()
    try:
        generate(args)
    except Abort:
        sys.exit(1)
