import os

import uploader


def test_normalize_blob_name_relative_path():
    base_path = 'C:/users/tasks/task1'
    path = 'foo/bar/test.txt'
    full_path = os.path.join(base_path, path)
    assert uploader.normalize_blob_name(base_path, full_path) == path
