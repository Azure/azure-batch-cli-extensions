import io
import pytest
import os
import datetime

try:
    import urllib.parse as urlparse
except:
    import urlparse
try:
    import pathlib
except:
    import pathlib2 as pathlib
import azure.storage.blob
import uploader
import configuration
import util


class Fixture:
    dummy_sas = 'https://acct.blob.core.windows.net/' \
                'aaatestcontainer?sr=c&sp=rw&sig=abc' \
                '&sv=2015-07-08&se=2016-11-01T18%3A21%3A23Z'

    def __init__(
            self,
            container,  # type: str
            blob_client,  # type: azure.storage.blob.BlockBlobService
            file_uploader,  # type: uploader.FileUploader
            sas,  # type: str,
            mock_details  # type: List[Tuple[]]
    ):
        self.container = container
        self.blob_client = blob_client
        self.file_uploader = file_uploader
        self.sas = sas
        self.mock_details = mock_details


def generate_sas(blob_client, container, account, permissions):
    sas_expiry = util.datetime_utcnow() + datetime.timedelta(days=1)

    if account:
        sas = blob_client.generate_account_shared_access_signature(
            resource_types='o',
            permission=permissions,
            expiry=sas_expiry)
    else:
        sas = blob_client.generate_container_shared_access_signature(
            container,
            permission=permissions,
            expiry=sas_expiry)

    print("Generated SAS: {}".format(sas))

    url_segments = [
        'https',
        '{}.blob.core.windows.net'.format(blob_client.account_name),
        container,
        sas,
        '']
    full_sas = urlparse.urlunsplit(url_segments)

    print("full sas: {}".format(full_sas))
    return full_sas


@pytest.fixture(params=[
    'container_write',
    'container_create',
    'account_write',
    'account_create'])
def fixture(tmpdir, monkeypatch, request):
    container = 'aaatestcontainer'
    storage_account = os.environ.get('MABOM_StorageAccount', None)
    storage_key = os.environ.get('MABOM_StorageKey', None)

    # Dummy sas value
    full_sas = Fixture.dummy_sas
    blob_client = None
    mock_details = []
    if storage_account is not None and storage_key is not None:
        blob_client = azure.storage.blob.BlockBlobService(
            storage_account,
            storage_key)
        cleanup_container(blob_client, container)
        if request.param == 'container_write':
            full_sas = generate_sas(blob_client, container, False, 'w')
        elif request.param == 'container_create':
            full_sas = generate_sas(blob_client, container, False, 'c')
        elif request.param == 'account_write':
            full_sas = generate_sas(blob_client, container, True, 'w')
        elif request.param == 'account_create':
            full_sas = generate_sas(blob_client, container, True, 'c')
    else:
        def create_blob_from_path(
                self, container_name, blob_name, file_path, max_connections=2):
            mock_details.append((container_name, blob_name, file_path))

        monkeypatch.setattr(
            azure.storage.blob.BlockBlobService,
            'create_blob_from_path',
            create_blob_from_path)

    os.environ['AZ_BATCH_TASK_DIR'] = os.getcwd()
    os.environ['AZ_BATCH_TASK_WORKING_DIR'] = os.getcwd()

    file_uploader = uploader.FileUploader(
        'job-id',
        'task-id')

    return Fixture(
        container,
        blob_client,
        file_uploader,
        full_sas,
        mock_details)


def cleanup_container(blob_client, container):
    blobs = blob_client.list_blobs(container)
    for blob in blobs:
        blob_client.delete_blob(container, blob.name)


def create_files(count, directory, file_size=None):
    if file_size is None:
        file_size = 7
    files_to_create = ['{}.txt'.format(x) for x in range(0, count)]
    files_to_create = \
        [os.path.join(directory, file_path)
         for file_path in files_to_create]
    if not os.path.exists(directory):
        os.makedirs(directory)

    for file_path in files_to_create:
        with io.open(file_path, mode='wb') as file:
            file.seek(file_size)
            file.write('\0')


def create_specification(
        file_pattern, sas, destination_path=None, task_status=None):
    if task_status is None:
        task_status = configuration.TaskStatus.TaskCompletion
    file_mapping = configuration.Specification()
    file_mapping.output_files.append(configuration.OutputFile(
        file_pattern=file_pattern,
        destination=configuration.OutputFileDestination(
            container=configuration.BlobContainerDestination(
                container_sas=sas,
                path=destination_path)),
        upload_details=configuration.OutputFileUploadDetails(
            task_status=task_status)))
    return file_mapping


def test_upload_single_file_after_process_exit(
        fixture, tmpdir):
    file_path = os.path.join(str(tmpdir), 'test1.txt')

    spec = create_specification(
        file_path,
        fixture.sas,
        task_status=configuration.TaskStatus.TaskSuccess)
    with io.open(file_path, mode='wb') as file:
        file.write('test')

    fixture.file_uploader.run(spec, task_success=True)

    if fixture.blob_client is not None:
        blob_properties = fixture.blob_client.get_blob_properties(
            fixture.container, 'test1.txt')
        assert os.path.getsize(file_path) == \
            blob_properties.properties.content_length
    else:
        assert len(fixture.mock_details) == 1
        container, blob, fp = fixture.mock_details[0]
        assert container == fixture.container
        assert blob == 'test1.txt'
        assert fp == file_path


def test_upload_dotdot_pattern(
        fixture, tmpdir):
    file_path = os.path.join(str(tmpdir), 'abc', '..', 'test1.txt')

    # make a dummy directory
    os.makedirs(str(tmpdir / 'abc'))
    pattern = os.path.join(str(tmpdir), 'abc', '..', '*.txt')

    spec = create_specification(
        pattern,
        fixture.sas,
        task_status=configuration.TaskStatus.TaskSuccess)
    with io.open(file_path, mode='wb') as file:
        file.write('test')

    fixture.file_uploader.run(spec, task_success=True)

    if fixture.blob_client is not None:
        blob_properties = fixture.blob_client.get_blob_properties(
            fixture.container, 'test1.txt')
        assert os.path.getsize(file_path) == \
            blob_properties.properties.content_length
    else:
        assert len(fixture.mock_details) == 1
        container, blob, fp = fixture.mock_details[0]
        assert container == fixture.container
        assert blob == 'test1.txt'
        assert fp == file_path


def test_upload_multi_star_dotdot_pattern(
        fixture, tmpdir):
    file_path = os.path.join(str(tmpdir), 'abc', '..', 'test1.txt')

    # make a dummy directory
    os.makedirs(str(tmpdir / 'abc'))
    pattern = os.path.join(str(tmpdir), '*', '..', '*.txt')

    spec = create_specification(
        pattern,
        fixture.sas,
        task_status=configuration.TaskStatus.TaskSuccess)
    with io.open(file_path, mode='wb') as file:
        file.write('test')

    fixture.file_uploader.run(spec, task_success=True)

    if fixture.blob_client is not None:
        blob_properties = fixture.blob_client.get_blob_properties(
            fixture.container, 'test1.txt')
        assert os.path.getsize(file_path) == \
            blob_properties.properties.content_length
    else:
        assert len(fixture.mock_details) == 1
        container, blob, fp = fixture.mock_details[0]
        assert container == fixture.container
        assert blob == 'test1.txt'
        assert fp == file_path


def test_upload_directory_after_process_exit(
        fixture, tmpdir):
    file_count = 10
    create_files(file_count, os.path.join(str(tmpdir), 'abc'))

    spec = create_specification(
        os.path.join(
            str(tmpdir),
            'abc',
            '*.txt'),
        fixture.sas,
        task_status=configuration.TaskStatus.TaskSuccess)

    fixture.file_uploader.run(spec, task_success=True)

    if fixture.blob_client is not None:
        assert file_count == len(list(
            fixture.blob_client.list_blobs(fixture.container)))
    else:
        assert len(fixture.mock_details) == file_count


def test_upload_missing_file_after_process_exit(
        fixture, tmpdir):
    file_path = os.path.join(str(tmpdir), 'missing_file.txt')
    spec = create_specification(
        file_path,
        fixture.sas,
        task_status=configuration.TaskStatus.TaskSuccess)

    fixture.file_uploader.run(spec, task_success=True)

    if fixture.blob_client is not None:
        blobs = fixture.blob_client.list_blobs(fixture.container)
        assert 0 == len(list(blobs))
    else:
        assert len(fixture.mock_details) == 0


def test_upload_and_reroot_directory_after_process_exit(
        fixture, tmpdir):
    file_count = 10
    create_files(file_count, os.path.join(str(tmpdir), 'abc'))

    sub_directory = 'abc/def'

    spec = create_specification(
        os.path.join(str(tmpdir), 'abc', '*.txt'),
        fixture.sas,
        destination_path=sub_directory,
        task_status=configuration.TaskStatus.TaskSuccess)

    fixture.file_uploader.run(spec, task_success=True)

    if fixture.blob_client is not None:
        blobs = list(fixture.blob_client.list_blobs(fixture.container))
        assert file_count == len(blobs)
        for blob in blobs:
            assert blob.name.startswith(sub_directory)
    else:
        assert len(fixture.mock_details) == file_count
        for container, blob, fp in fixture.mock_details:
            assert container == fixture.container
            assert blob.startswith(sub_directory)
            assert fp.startswith(os.path.join(str(tmpdir), 'abc'))


def test_upload_and_rename_single_file_after_process_exit(
        fixture, tmpdir):
    file_path = os.path.join(str(tmpdir), 'test1.txt')
    destination_blob_name = 'foo.txt'
    spec = create_specification(
        file_path,
        fixture.sas,
        destination_blob_name,
        task_status=configuration.TaskStatus.TaskSuccess)
    with io.open(file_path, mode='wb') as file:
        file.write('test')

    fixture.file_uploader.run(spec, task_success=True)

    if fixture.blob_client is not None:
        blob_properties = fixture.blob_client.get_blob_properties(
            fixture.container,
            destination_blob_name)
        assert os.path.getsize(file_path) == \
            blob_properties.properties.content_length
    else:
        assert len(fixture.mock_details) == 1
        container, blob, fp = fixture.mock_details[0]
        assert container == fixture.container
        assert blob == destination_blob_name
        assert fp == file_path


def test_upload_one_file_of_many(
        fixture, tmpdir):
    file_count = 100
    create_files(file_count, os.path.join(str(tmpdir), 'abc'))

    # create some extra directories and files too
    create_files(file_count, os.path.join(str(tmpdir), 'def'))
    create_files(file_count, os.path.join(str(tmpdir), 'abc', '123'))
    create_files(file_count, os.path.join(str(tmpdir), 'abc', '456'))
    create_files(file_count, os.path.join(str(tmpdir), 'abc', '789'))
    create_files(0, os.path.join(str(tmpdir), 'abc', 'zzz'))
    create_files(0, os.path.join(str(tmpdir), 'zzz'))

    spec = create_specification(
        os.path.join(str(tmpdir), 'abc', '*'),
        fixture.sas,
        task_status=configuration.TaskStatus.TaskSuccess)

    fixture.file_uploader.run(spec, task_success=True)

    if fixture.blob_client is not None:
        blobs = list(fixture.blob_client.list_blobs(fixture.container))
        assert file_count == len(blobs)
    else:
        assert len(fixture.mock_details) == file_count
        for container, blob, fp in fixture.mock_details:
            assert container == fixture.container
            assert fp.startswith(os.path.join(str(tmpdir), 'abc'))


@pytest.mark.parametrize(
    ('task_success', 'upload_task_status'),
    [(True, configuration.TaskStatus.TaskSuccess),
     (False, configuration.TaskStatus.TaskFailure),
     (None, configuration.TaskStatus.TaskCompletion),
     (True, configuration.TaskStatus.TaskCompletion),
     (False, configuration.TaskStatus.TaskCompletion)])
def test_task_success_and_task_status_pairings(
        tmpdir, monkeypatch, task_success, upload_task_status):
    file_path = os.path.join(str(tmpdir), 'test1.txt')
    spec = create_specification(
        file_path,
        Fixture.dummy_sas,
        task_status=upload_task_status)
    with io.open(file_path, mode='wb') as file:
        file.write('test')

    mock_details = []

    def create_blob_from_path(
            self, container_name, blob_name, file_path, max_connections=2):
        mock_details.append((container_name, blob_name, file_path))

    monkeypatch.setattr(
        azure.storage.blob.BlockBlobService,
        'create_blob_from_path',
        create_blob_from_path)

    file_uploader = uploader.FileUploader(
        'job-id',
        'task-id')
    file_uploader.run(spec, task_success=task_success)

    assert len(mock_details) == 1
    container, blob, fp = mock_details[0]
    assert blob == 'test1.txt'
    assert fp == file_path


@pytest.mark.parametrize(('task_success', 'upload_task_status'),
                         [(False, configuration.TaskStatus.TaskSuccess),
                          (True, configuration.TaskStatus.TaskFailure)])
def test_upload_files_skipped_on_unmatching_task_status(
        fixture, tmpdir, task_success, upload_task_status):
    file_path = os.path.join(str(tmpdir), 'test1.txt')
    destination_blob_name = 'foo.txt'
    spec = create_specification(
        file_path,
        fixture.sas,
        destination_blob_name,
        task_status=upload_task_status)

    with io.open(file_path, mode='wb') as file:
        file.write('test')

    fixture.file_uploader.run(spec, task_success=task_success)

    if fixture.blob_client is not None:
        blobs = fixture.blob_client.list_blobs(fixture.container)
        assert 0 == len(list(blobs))
    else:
        assert len(fixture.mock_details) == 0


def test_upload_with_bad_sas_fails(
        fixture, tmpdir, monkeypatch):
    if fixture.blob_client is None:

        def create_blob_from_path(
                self, container_name, blob_name, file_path, max_connections=2):
            raise azure.common.AzureHttpError(u'Some text here', 403)

        monkeypatch.setattr(
            azure.storage.blob.BlockBlobService,
            'create_blob_from_path',
            create_blob_from_path)

    file_path = os.path.join(str(tmpdir), 'test1.txt')
    destination_blob_name = 'foo.txt'
    bad_sas = fixture.sas[:-6]
    spec = create_specification(
        file_path,
        bad_sas,
        destination_blob_name,
        task_status=configuration.TaskStatus.TaskSuccess)
    with io.open(file_path, mode='wb') as file:
        file.write('test')

    with pytest.raises(uploader.AggregateException) as agg:
        fixture.file_uploader.run(spec, task_success=True)

    assert len(agg.value.errors) == 1
    file, pattern, error = agg.value.errors[0]
    assert file == file_path
    assert pattern == file_path
    assert error.status_code == 403
    print(repr(agg.value))


def test_upload_to_nonexistant_container(
        fixture, tmpdir, monkeypatch):
    if fixture.blob_client is None:

        def create_blob_from_path(
                self, container_name, blob_name, file_path, max_connections=2):
            raise azure.common.AzureHttpError(u'Some text here', 404)

        monkeypatch.setattr(
            azure.storage.blob.BlockBlobService,
            'create_blob_from_path',
            create_blob_from_path)
        bad_sas = fixture.sas
    else:
        bad_sas = generate_sas(
            fixture.blob_client,
            'nonexistcontainer',
            True,
            'w')

    file_path = os.path.join(str(tmpdir), 'test1.txt')
    destination_blob_name = 'foo.txt'

    spec = create_specification(
        file_path,
        bad_sas,
        destination_blob_name,
        task_status=configuration.TaskStatus.TaskSuccess)
    with io.open(file_path, mode='wb') as file:
        file.write('test')

    with pytest.raises(uploader.AggregateException) as agg:
        fixture.file_uploader.run(spec, task_success=True)

    assert len(agg.value.errors) == 1
    file, pattern, error = agg.value.errors[0]
    assert file == file_path
    assert pattern == file_path
    assert error.status_code == 404
    print(repr(agg.value))


def test_upload_files_with_no_read_access(fixture, tmpdir, monkeypatch):
    file_path = os.path.join(str(tmpdir), 'test1.txt')

    spec = create_specification(
        file_path,
        fixture.sas,
        task_status=configuration.TaskStatus.TaskSuccess)

    with io.open(file_path, mode='wb') as file:
        file.write('test')

    def _select_from(self, parent_path, is_dir, exists, listdir):
        raise OSError(13, 'Permission denied')

    # We would remove read and execute from this directory except that tests
    # run as root, so we have to fake it. Here we monkeypatch the pathlib
    # behavior to throw a PermissionError
    monkeypatch.setattr(
        pathlib._PreciseSelector,
        '_select_from',
        _select_from)
    # os.chmod(str(tmpdir), 0o000)

    with pytest.raises(uploader.AggregateException) as agg:
        fixture.file_uploader.run(spec, task_success=True)
    assert len(agg.value.errors) == 1
    file, pattern, error = agg.value.errors[0]
    assert file is None
    assert pattern == file_path
    assert error.errno == 13

    if fixture.blob_client is not None:
        blobs = fixture.blob_client.list_blobs(fixture.container)
        assert 0 == len(list(blobs))
    else:
        assert len(fixture.mock_details) == 0
