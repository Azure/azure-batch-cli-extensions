import os
import util
import uploader
try:
    import pathlib
except:
    import pathlib2 as pathlib


def setup_module(module):
    os.environ['AZ_BATCH_TASK_WORKING_DIR'] = os.getcwd()


def get_expected_path(partial_path):
    return os.path.join(os.environ['AZ_BATCH_TASK_WORKING_DIR'], partial_path)


def test_exact_relative_path():
    path = os.path.join('foo', 'bar', 'test.txt')
    base_path, pattern, fullpath, recursive = uploader._extract_pathinfo(path)
    assert get_expected_path(os.path.join('foo', 'bar')) == base_path
    assert get_expected_path(path) == pattern
    assert fullpath
    assert not recursive


def test_exact_absolute_path(tmpdir):
    path = os.path.join(str(tmpdir), 'foo', 'bar', 'test.txt')
    base_path, pattern, fullpath, recursive = uploader._extract_pathinfo(path)
    assert os.path.join(str(tmpdir), 'foo', 'bar') == base_path
    assert path == pattern
    assert fullpath
    assert not recursive


def test_nonrecursive_relative_pattern():
    path = os.path.join('foo', 'bar', '*.txt')
    base_path, pattern, fullpath, recursive = uploader._extract_pathinfo(path)
    assert get_expected_path(os.path.join('foo', 'bar')) == base_path
    assert get_expected_path(path) == pattern
    assert not fullpath
    assert not recursive


def test_nonrecursive_absolute_pattern(tmpdir):
    path = os.path.join(str(tmpdir), 'foo', 'bar', '*.txt')
    base_path, pattern, fullpath, recursive = uploader._extract_pathinfo(path)
    assert os.path.join(str(tmpdir), 'foo', 'bar') == base_path
    assert path == pattern
    assert not fullpath
    assert not recursive


def test_nonrecursive_relative_pattern_trailing_star():
    path = os.path.join('foo', 'bar', 'file*')
    base_path, pattern, fullpath, recursive = uploader._extract_pathinfo(path)
    assert get_expected_path(os.path.join('foo', 'bar')) == base_path
    assert get_expected_path(path) == pattern
    assert not fullpath
    assert not recursive


def test_nonrecursive_absolute_pattern_trailing_star(tmpdir):
    path = os.path.join(str(tmpdir), 'foo', 'bar', 'file*')
    base_path, pattern, fullpath, recursive = uploader._extract_pathinfo(path)
    assert os.path.join(str(tmpdir), 'foo', 'bar') == base_path
    assert path == pattern
    assert not fullpath
    assert not recursive


def test_nonrecursive_relative_pattern_multi_star():
    path = os.path.join('foo', 'bar', '*', '*.txt')
    base_path, pattern, fullpath, recursive = uploader._extract_pathinfo(path)
    assert get_expected_path(os.path.join('foo', 'bar')) == base_path
    assert get_expected_path(path) == pattern
    assert not fullpath
    assert not recursive


def test_nonrecursive_absolute_pattern_multi_star(tmpdir):
    path = os.path.join(str(tmpdir), 'foo', 'bar', '*', '*.txt')
    base_path, pattern, fullpath, recursive = uploader._extract_pathinfo(path)
    assert os.path.join(str(tmpdir), 'foo', 'bar') == base_path
    assert path == pattern
    assert not fullpath
    assert not recursive


def test_recursive_relative_pattern():
    path = os.path.join('foo', 'bar', '**', '*.txt')
    base_path, pattern, fullpath, recursive = uploader._extract_pathinfo(path)
    assert get_expected_path(os.path.join('foo', 'bar')) == base_path
    assert get_expected_path(path) == pattern
    assert not fullpath
    assert recursive


def test_recursive_absolute_pattern(tmpdir):
    path = os.path.join(str(tmpdir), 'foo', 'bar', '**', '*.txt')
    base_path, pattern, fullpath, recursive = uploader._extract_pathinfo(path)
    assert os.path.join(str(tmpdir), 'foo', 'bar') == base_path
    assert path == pattern
    assert not fullpath
    assert recursive


def test_path_with_environment_variable():
    os.environ['TEST'] = 'foo'
    if util.on_windows():
        env_var = '%TEST%'
    else:
        env_var = '$TEST'
    path = os.path.join(env_var, 'myfile.txt')
    base_path, pattern, fullpath, recursive = uploader._extract_pathinfo(path)
    assert get_expected_path('foo') == base_path
    assert get_expected_path(os.path.join('foo', 'myfile.txt')) == pattern
    assert fullpath
    assert not recursive


def test_relative_path_with_dots():
    path = os.path.join('..', 'myfile.txt')
    expected_base_path = os.path.join(os.getcwd(), '..')
    expected_base_path = pathlib.Path(expected_base_path).resolve()
    base_path, pattern, fullpath, recursive = uploader._extract_pathinfo(path)
    assert str(expected_base_path) == base_path
    assert get_expected_path(path) == pattern
    assert fullpath
    assert not recursive


def test_absolute_path_with_dots(tmpdir):
    folder = os.path.join(str(tmpdir), 'foo', 'bar', '..', '..')
    if not os.path.exists(folder):
        os.makedirs(folder)
    path = os.path.join(folder, 'myfile.txt')
    base_path, pattern, fullpath, recursive = uploader._extract_pathinfo(path)
    assert tmpdir == base_path
    assert path == pattern
    assert fullpath
    assert not recursive
