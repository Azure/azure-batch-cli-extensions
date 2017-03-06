import os
import io
import json
import mock
import pytest
import enum
import sys

import batchfileuploader
import configuration


class ConfigurationMode(enum.Enum):
    File = 'File'
    Env = 'Env'
    Stdin = 'Stdin'


_SPEC_ENV = 'specification_env'
_TEST_MODE_ARGS = [
    ConfigurationMode.File,
    ConfigurationMode.Env,
    ConfigurationMode.Stdin]


@mock.patch('sys.stdin', io.BytesIO())
@pytest.mark.parametrize('mode', _TEST_MODE_ARGS)
def test_load_specification_basic_valid(tmpdir, mode):
    dict = {
        'outputFiles': [
            {
                'filePattern': '*.txt',
                'destination': {'container': {
                    'containerSas': 'sas', 'path': 'a/b/c'}},
                'uploadDetails': {'taskStatus': 'TaskFailure'}
            }
        ]
    }
    if mode == ConfigurationMode.File:
        file_path = _create_specification_file(dict, str(tmpdir))
        spec = batchfileuploader.load_specification_from_file(file_path)
    elif mode == ConfigurationMode.Env:
        _create_specification_env(dict, _SPEC_ENV)
        spec = batchfileuploader.load_specification_from_env(_SPEC_ENV)
    else:
        _write_specification(dict, sys.stdin)
        spec = batchfileuploader.load_specification_from_stdin()
    assert len(spec.output_files) == 1
    assert spec.output_files[0].file_pattern == '*.txt'
    assert spec.output_files[0].destination.container.container_sas == 'sas'
    assert spec.output_files[0].destination.container.path == 'a/b/c'
    assert spec.output_files[0].upload_details.task_status == \
        configuration.TaskStatus.TaskFailure


@mock.patch('sys.stdin', io.BytesIO())
@pytest.mark.parametrize('mode', _TEST_MODE_ARGS)
def test_load_specification_multiple_specifications(tmpdir, mode):
    dict = {
        'outputFiles': [
            {
                'filePattern': 'a.txt',
                'destination': {'container': {'containerSas': 'sas'}},
                'uploadDetails': {'taskStatus': 'TaskFailure'}
            },
            {
                'filePattern': 'b.txt',
                'destination': {'container': {'containerSas': 'sas'}},
                'uploadDetails': {'taskStatus': 'TaskSuccess'}
            },
            {
                'filePattern': 'c.txt',
                'destination': {'container': {'containerSas': 'sas'}},
                'uploadDetails': {'taskStatus': 'TaskCompletion'}
            },
        ]
    }

    if mode == ConfigurationMode.File:
        file_path = _create_specification_file(dict, str(tmpdir))
        spec = batchfileuploader.load_specification_from_file(file_path)
    elif mode == ConfigurationMode.Env:
        _create_specification_env(dict, _SPEC_ENV)
        spec = batchfileuploader.load_specification_from_env(_SPEC_ENV)
    else:
        _write_specification(dict, sys.stdin)
        spec = batchfileuploader.load_specification_from_stdin()

    assert len(spec.output_files) == 3
    assert spec.output_files[0].file_pattern == 'a.txt'
    assert spec.output_files[0].destination.container.container_sas == 'sas'
    assert spec.output_files[0].upload_details.task_status == \
        configuration.TaskStatus.TaskFailure

    assert spec.output_files[1].file_pattern == 'b.txt'
    assert spec.output_files[1].destination.container.container_sas == 'sas'
    assert spec.output_files[1].upload_details.task_status == \
        configuration.TaskStatus.TaskSuccess

    assert spec.output_files[2].file_pattern == 'c.txt'
    assert spec.output_files[2].destination.container.container_sas == 'sas'
    assert spec.output_files[2].upload_details.task_status == \
        configuration.TaskStatus.TaskCompletion


@mock.patch('sys.stdin', io.BytesIO())
@pytest.mark.parametrize('mode', _TEST_MODE_ARGS)
def test_load_specification_missing_required(tmpdir, mode):
    dict = {
        'outputFiles': [
            {
                'destination': {'container': {'containerSas': 'sas'}},
                'uploadDetails': {'taskStatus': 'TaskFailure'}
            }
        ]
    }
    if mode == ConfigurationMode.File:
        file_path = _create_specification_file(dict, str(tmpdir))
        with pytest.raises(ValueError) as e:
            batchfileuploader.load_specification_from_file(file_path)
    elif mode == ConfigurationMode.Env:
        _create_specification_env(dict, _SPEC_ENV)
        with pytest.raises(ValueError) as e:
            batchfileuploader.load_specification_from_env(_SPEC_ENV)
    else:
        _write_specification(dict, sys.stdin)
        with pytest.raises(ValueError) as e:
            batchfileuploader.load_specification_from_stdin()

    assert e.value.args[0] == 'Missing required filePattern'


@mock.patch('sys.stdin', io.BytesIO())
@pytest.mark.parametrize('mode', _TEST_MODE_ARGS)
def test_load_specification_invalid_taskstatus(tmpdir, mode):
    dict = {
        'outputFiles': [
            {
                'filePattern': '*.txt',
                'destination': {'container': {'containerSas': 'sas'}},
                'uploadDetails': {'taskStatus': 'Foo'}
            }
        ]
    }

    if mode == ConfigurationMode.File:
        file_path = _create_specification_file(dict, str(tmpdir))
        with pytest.raises(ValueError) as e:
            batchfileuploader.load_specification_from_file(file_path)
    elif mode == ConfigurationMode.Env:
        _create_specification_env(dict, _SPEC_ENV)
        with pytest.raises(ValueError) as e:
            batchfileuploader.load_specification_from_env(_SPEC_ENV)
    else:
        _write_specification(dict, sys.stdin)
        with pytest.raises(ValueError) as e:
            batchfileuploader.load_specification_from_stdin()

    assert e.value.args[0] == "Foo is not a valid TaskStatus"


@mock.patch('sys.stdin', io.BytesIO())
@pytest.mark.parametrize('mode', _TEST_MODE_ARGS)
def test_load_specification_invalid_child_type(tmpdir, mode):
    dict = {
        'outputFiles': [
            {
                'filePattern': '*.txt',
                'destination': {'container': {
                    'containerSas': 'sas'}, 'bar': 'test'},
                'uploadDetails': {'taskStatus': 'TaskFailure'}
            }
        ]
    }
    if mode == ConfigurationMode.File:
        file_path = _create_specification_file(dict, str(tmpdir))
        with pytest.raises(ValueError) as e:
            batchfileuploader.load_specification_from_file(file_path)
    elif mode == ConfigurationMode.Env:
        _create_specification_env(dict, _SPEC_ENV)
        with pytest.raises(ValueError) as e:
            batchfileuploader.load_specification_from_env(_SPEC_ENV)
    else:
        _write_specification(dict, sys.stdin)
        with pytest.raises(ValueError) as e:
            batchfileuploader.load_specification_from_stdin()

    assert e.value.args[0] == 'unexpected keys {}'.format([u'bar'])


def _write_specification(specification, file):
    print(json.dumps(specification, indent=4))
    json.dump(specification, file, indent=4)
    file.seek(0)


def _create_specification_file(specification, directory):
    file_path = os.path.join(directory, 'spec.json')
    with io.open(file_path, mode='wb') as f:
        _write_specification(specification, f)
    return file_path


def _create_specification_env(specification, env):
    print(json.dumps(specification, indent=4))
    os.environ[env] = json.dumps(specification)
