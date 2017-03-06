import json
import uploader
import azure.common

import batchfileuploader
import configuration


def test_bad_sas():
    # Note: This error was confirmed from observations of actual requests
    err = azure.common.AzureHttpError(
        u'Server failed to authenticate the request. Make sure the '
        u'value of Authorization header is formed correctly '
        u'including the signature.\n<?xml version="1.0" encoding="utf-8"?>'
        u'<Error><Code>AuthenticationFailed</Code>'
        u'<Message>Server failed to authenticate the request. '
        u'Make sure the value of Authorization header is formed '
        u'correctly including the signature.\n'
        u'RequestId:be9953a6-0001-010c-07ab-2f1267000000\n'
        u'Time:2016-10-26T17:10:28.5908484Z</Message>'
        u'<AuthenticationErrorDetail>Signature fields not well formed.'
        u'</AuthenticationErrorDetail></Error>',
        403)
    agg = uploader.AggregateException([('file', 'pattern', err)])
    error_specification = batchfileuploader.generate_error_specification(agg)
    assert error_specification.code == \
        configuration.ErrorCode.AuthenticationFailed
    assert error_specification.file == 'file'
    assert error_specification.pattern == 'pattern'
    assert error_specification.user_error is True


def test_missing_container():
    # Note: This error was confirmed from observations of actual requests
    err = azure.common.AzureMissingResourceHttpError(
        u'The specified container does not exist.\n'
        u'<?xml version="1.0" encoding="utf-8"?>'
        u'<Error><Code>ContainerNotFound</Code>'
        u'<Message>The specified container does not exist.\n'
        u'RequestId:ab7b93e5-0001-007b-58b2-2fd173000000\n'
        u'Time:2016-10-26T17:56:41.7813237Z</Message></Error>',
        404)
    agg = uploader.AggregateException([('file', 'pattern', err)])
    error_specification = batchfileuploader.generate_error_specification(agg)
    assert error_specification.code == \
        configuration.ErrorCode.ContainerNotFound
    assert error_specification.file == 'file'
    assert error_specification.pattern == 'pattern'
    assert error_specification.user_error is True


def test_internal_server_error():
    err = azure.common.AzureHttpError(u'Some text here', 500)
    agg = uploader.AggregateException([('file', 'pattern', err)])
    error_specification = batchfileuploader.generate_error_specification(agg)
    assert error_specification.code == configuration.ErrorCode.InternalError
    assert error_specification.file == 'file'
    assert error_specification.pattern == 'pattern'
    assert error_specification.user_error is False


def test_server_busy():
    err = azure.common.AzureHttpError(u'Some text here', 503)
    agg = uploader.AggregateException([('file', 'pattern', err)])
    error_specification = batchfileuploader.generate_error_specification(agg)
    assert error_specification.code == configuration.ErrorCode.InternalError
    assert error_specification.file == 'file'
    assert error_specification.pattern == 'pattern'
    assert error_specification.user_error is False


def test_unknown_azure_error():
    err = azure.common.AzureHttpError(u'Some text here', 411)
    agg = uploader.AggregateException([('file', 'pattern', err)])
    error_specification = batchfileuploader.generate_error_specification(agg)
    assert error_specification.code == configuration.ErrorCode.UnknownError
    assert error_specification.file == 'file'
    assert error_specification.pattern == 'pattern'
    assert error_specification.user_error is False


def test_unknown_error():
    err = ValueError('test')
    agg = uploader.AggregateException([('file', 'pattern', err)])
    error_specification = batchfileuploader.generate_error_specification(agg)
    assert error_specification.code == configuration.ErrorCode.UnknownError
    assert error_specification.file == 'file'
    assert error_specification.pattern == 'pattern'
    assert error_specification.user_error is False


def test_non_aggregate_exception():
    err = ValueError('test')
    error_specification = batchfileuploader.generate_error_specification(err)
    assert error_specification.code == configuration.ErrorCode.UnknownError
    assert error_specification.file is None
    assert error_specification.pattern is None
    assert error_specification.user_error is False


def test_serialize_error():
    err = azure.common.AzureHttpError(u'Some text here', 411)
    agg = uploader.AggregateException([('file', 'pattern', err)])
    error_specification = batchfileuploader.generate_error_specification(agg)
    text = json.dumps(
        error_specification,
        cls=configuration.SpecificationEncoder,
        sort_keys=True)

    assert text == '{"code": "UnknownError", "file": "file", ' \
                   '"pattern": "pattern", "user_error": false}'
