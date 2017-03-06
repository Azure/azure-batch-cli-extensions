import pytest

import batchfileuploader


def test_env_argparse():
    args = ['--env', 'Test']
    args = batchfileuploader.parseargs(args)

    assert args.env == 'Test'
    assert args.success is None
    assert args.failure is None


def test_file_argparse():
    args = ['--file', 'Test']
    args = batchfileuploader.parseargs(args)

    assert args.file == 'Test'
    assert args.success is None
    assert args.failure is None


def test_env_file_mutually_exclusive_argparse():
    args = ['--env', 'Test', '--file', 'Bar']

    with pytest.raises(SystemExit):
        args = batchfileuploader.parseargs(args)


def test_env_file_required_argparse():
    args = []

    with pytest.raises(SystemExit):
        args = batchfileuploader.parseargs(args)


def test_success_argparse():
    args = ['--file', 'Foo', '-s']

    args = batchfileuploader.parseargs(args)
    assert args.success


def test_failure_argparse():
    args = ['--file', 'Foo', '-f']

    args = batchfileuploader.parseargs(args)
    assert args.failure


def test_success_failure_exclusive_argparse():
    args = ['--file', 'Foo', '-f', '-s']

    with pytest.raises(SystemExit):
        args = batchfileuploader.parseargs(args)
