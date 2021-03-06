import os
import shutil
from random import randint
from typing import List

from retrying import retry

from apysc._file import file_util
from tests import testing_helper


def test_empty_directory() -> None:
    tmp_dir_path: str = '../.tmp_apysc/'
    os.makedirs(tmp_dir_path, exist_ok=True)
    test_file_path: str = os.path.join(tmp_dir_path, 'test.txt')
    testing_helper.make_blank_file(file_path=test_file_path)
    file_util.empty_directory(directory_path=tmp_dir_path)
    assert os.path.isdir(tmp_dir_path)
    assert len(os.listdir(tmp_dir_path)) == 0

    shutil.rmtree(tmp_dir_path, ignore_errors=True)
    file_util.empty_directory(directory_path=tmp_dir_path)
    assert os.path.isdir(tmp_dir_path)

    shutil.rmtree(tmp_dir_path, ignore_errors=True)


@retry(stop_max_attempt_number=15, wait_fixed=randint(10, 3000))
def test_read_txt() -> None:
    tmp_file_path: str = '../tmp_apysc_test_file_util.txt'
    with open(tmp_file_path, 'w') as f:
        f.write('To be, or not to be, that is the question.')
    txt: str = file_util.read_txt(file_path=tmp_file_path)
    assert txt == 'To be, or not to be, that is the question.'
    os.remove(tmp_file_path)

    with open(tmp_file_path, 'w', encoding='cp932') as f:
        f.write('猫')
    testing_helper.assert_raises(
        expected_error_class=Exception,
        func_or_method=file_util.read_txt,
        kwargs={'file_path': tmp_file_path})
    os.remove(tmp_file_path)


@retry(stop_max_attempt_number=15, wait_fixed=randint(10, 3000))
def test_save_plain_txt() -> None:
    tmp_file_path: str = '../tmp_apysc_test_file_util.txt'
    file_util.save_plain_txt(
        txt='To be, or not to be, that is the question.',
        file_path=tmp_file_path)
    txt: str = file_util.read_txt(file_path=tmp_file_path)
    assert txt == 'To be, or not to be, that is the question.'
    os.remove(tmp_file_path)

    tmp_dir_path: str = '../tmp_apysc_test_file_util/'
    tmp_file_path = os.path.join(tmp_dir_path, 'test.txt')
    shutil.rmtree(tmp_dir_path, ignore_errors=True)
    file_util.save_plain_txt(
        txt='To be, or not to be, that is the question.',
        file_path=tmp_file_path)
    assert os.path.isfile(tmp_file_path)
    shutil.rmtree(tmp_dir_path, ignore_errors=True)


@retry(stop_max_attempt_number=15, wait_fixed=randint(10, 3000))
def test_remove_file_if_exists() -> None:
    tmp_file_path: str = '../tmp_apysc_test_file_util.txt'
    file_util.save_plain_txt(
        txt='To be, or not to be, that is the question.',
        file_path=tmp_file_path)
    file_util.remove_file_if_exists(file_path=tmp_file_path)
    assert not os.path.exists(tmp_file_path)

    file_util.remove_file_if_exists(file_path=tmp_file_path)


@retry(stop_max_attempt_number=15, wait_fixed=randint(10, 3000))
def test_get_abs_module_dir_path() -> None:
    abs_module_dir_path: str = file_util.get_abs_module_dir_path(
        module=file_util)
    assert abs_module_dir_path.endswith('/apysc/_file/')


@retry(stop_max_attempt_number=15, wait_fixed=randint(10, 3000))
def test_get_abs_directory_path_from_file_path() -> None:
    dir_path: str = file_util.get_abs_directory_path_from_file_path(
        file_path='any/dir/path.txt')
    assert dir_path == 'any/dir/'


@retry(stop_max_attempt_number=15, wait_fixed=randint(10, 3000))
def test_append_plain_txt() -> None:
    tmp_file_path: str = '../tmp_test_file_util.txt'
    file_util.remove_file_if_exists(file_path=tmp_file_path)
    file_util.append_plain_txt(txt='Hello ', file_path=tmp_file_path)
    file_util.append_plain_txt(txt='World!', file_path=tmp_file_path)
    txt: str = file_util.read_txt(file_path=tmp_file_path)
    assert txt == 'Hello World!'


@retry(stop_max_attempt_number=15, wait_fixed=randint(10, 3000))
def test_get_specified_ext_file_paths_recursively() -> None:
    file_paths: List[str] = file_util.get_specified_ext_file_paths_recursively(
        extension='md', dir_path='./docs_src/')
    assert './docs_src/source/index.md' in file_paths
    assert './docs_src/source/quick_start.md' in file_paths
    assert './docs_src/source/conf.py' not in file_paths
