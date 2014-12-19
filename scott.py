from contextlib import contextmanager

import argparse
from functools import partial
import itertools
import os
import re
import shutil
from subprocess import Popen, PIPE
import sys
import tempfile

from pip.req import parse_requirements


HEADER = """# Generated file. Please do not edit manually
#
# `requirements.in` contains direct dependencies (and may be >version instead
# of ==version) This file is a list of dependencies and _their_ dependencies,
# completely frozen.  To generate this file, use scott-freeze
#
# Example
#     $ scott-freeze requirements.in > requirements.txt
#"""

SKIP = re.compile('^(argparse|distribute|wsgiref)==')


class FakeFinder(object):
    index_urls = None

    def output(self):
        lines = []
        # first one is main, subsequent are 'extra'
        param = '--index-url'
        for url in self.index_urls:
            lines.append('{}={}'.format(param, url))
            param = '--extra-index-url'

        return lines


def parse_cmdline():
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
    args = parser.parse_args()
    return args


@contextmanager
def tempdir():
    path = tempfile.mkdtemp(suffix='scott_freeze')
    try:
        yield path
    finally:
        shutil.rmtree(path)


def run_or_exit(cmd, verbose=False):
    proc = Popen(cmd, stdout=PIPE)
    proc.wait()
    if proc.returncode != 0:
        print proc.stdout.read()
        sys.exit(1)
    output = proc.stdout.read()

    if verbose:
        sys.stderr.write(output)

    return output


def find_index_url(req_file):
    finder = FakeFinder()
    for _ in parse_requirements(req_file, finder=finder):
        pass
    return finder.output()


def generate(req_file, python, verbose):
    # make temp virtualenv
    if python is not None:
        python = ['--python', python]
    else:
        python = []

    index_url_lines = find_index_url(req_file)

    with tempdir() as path:
        run = partial(run_or_exit, verbose=verbose)

        run(['virtualenv'] + python + [path])

        pip_path = os.path.join(path, 'bin', 'pip')
        run([pip_path, 'install', '-r', req_file])
        pinned = run([pip_path, 'freeze']).splitlines()
        pinned = itertools.ifilterfalse(SKIP.match, pinned)
        pinned = sorted(pinned, key=lambda req: req.lower())
        print HEADER
        for line in index_url_lines:
            print line
        print

        for req in pinned:
            print req


def main():
    args = parse_cmdline()

    if not os.path.exists(args.requirements):
        print 'No such file: {}'.format(args.requirements)
        sys.exit(1)

    generate(args.requirements, args.python, args.verbose)


if __name__ == '__main__':
    main()
