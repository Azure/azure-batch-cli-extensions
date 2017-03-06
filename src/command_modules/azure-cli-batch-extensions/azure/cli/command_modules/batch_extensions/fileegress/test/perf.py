import pytest
import os
import shutil

import time
import test_end_to_end

from test_end_to_end import fixture  # noqa: F401


@pytest.fixture(params=[(10, 50), (1, 500), (1000, 1), (10, 500), (5, 1000)])
def file_fixture(tmpdir, request):
    file_count = request.param[0]
    file_size_mb = request.param[1]
    print('creating {} files of size {} mb'.format(file_count, file_size_mb))
    file_size_bytes = 1024*1024*file_size_mb
    test_end_to_end.create_files(
        file_count,
        str(tmpdir / 'abc'),
        file_size_bytes)
    yield file_count, file_size_mb

    # clean up files afterwards
    dir_to_delete = os.path.join(str(tmpdir), 'abc')
    print('deleting directory {}'.format(dir_to_delete))
    shutil.rmtree(dir_to_delete)


def test_perf(fixture, file_fixture, tmpdir):  # noqa: F811
    config = test_end_to_end.create_specification(
        os.path.join(str(tmpdir), 'abc', '*.txt'),
        fixture.sas)

    file_count, file_size_mb = file_fixture

    start = time.clock()
    fixture.file_uploader.run(config, task_success=None)
    end = time.clock()
    runtime = end - start

    print('Took {}s to run, avg {} mbps'.format(
        runtime,
        (file_count * file_size_mb * 8) / runtime))
    assert file_count == len(list(
        fixture.blob_client.list_blobs(fixture.container)))
