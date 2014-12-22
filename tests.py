from mock import patch, DEFAULT
import pytest

import scott_freeze
from scott_freeze import (
    find_index_urls, install_and_freeze, generate, setup_argparse, Abort)


@pytest.fixture
def req_in(tmpdir):
    req_in = tmpdir.join('req.in')
    req_in.write("""
--index-url=https://pypi.python.org/simple/
flask<1.0
""")
    return str(req_in)


def test_find_index_url(req_in):
    assert find_index_urls(req_in) == [
        '--index-url=https://pypi.python.org/simple/']


def test_install_and_freeze(req_in):
    pinned = install_and_freeze(req_in)
    stripped_reqs = [req.split('=')[0] for req in pinned]
    assert stripped_reqs == [
        'Flask',
        'itsdangerous',
        'Jinja2',
        'MarkupSafe',
        'Werkzeug',
    ]


def test_generate(req_in, capsys):
    parser = setup_argparse()
    args = parser.parse_args([req_in])
    with patch.multiple(
        scott_freeze,
        find_index_urls=DEFAULT,
        install_and_freeze=DEFAULT,
    ) as patches:
        patches['find_index_urls'].return_value = ['url1', 'url2']
        patches['install_and_freeze'].return_value = ['req1==1', 'req2==2']
        generate(args)
        out, err = capsys.readouterr()
        lines = out.splitlines()
        assert lines[-9:] == [
            '# Example',
            '#     $ scott-freeze requirements.in > requirements.txt',
            '#',
            '',
            'url1',
            'url2',
            '',
            'req1==1',
            'req2==2',
        ]


def test_file_error(capsys):
    parser = setup_argparse()
    args = parser.parse_args(['foo'])
    with pytest.raises(Abort):
        generate(args)
    out, err = capsys.readouterr()
    assert 'No such file: foo' in err


def test_pip_error(tmpdir, capsys):
    req_in = tmpdir.join('req.in')
    req_in.write("non-existent")
    with pytest.raises(Abort):
        install_and_freeze(str(req_in))
    out, err = capsys.readouterr()
    assert 'No distributions at all found for non-existent' in err
