"""Documentations build script.

Command example:
$ python build_docs.py
"""

import hashlib
import os
import re
import shutil
import subprocess as sp
from logging import Logger
from typing import Any
from typing import Dict
from typing import List
from typing import Match
from typing import Optional
from typing import Tuple

from typing_extensions import Final

from apysc._console import loggers
from apysc._jslib import jslib_util

logger: Logger = loggers.get_info_logger()

_jslib_file_names: List[str] = jslib_util.get_jslib_file_names()
_jslib_file_name_keys_dict: Dict[str, Any] = {
    jslib_file_name: None for jslib_file_name in _jslib_file_names}


def _main() -> None:
    """Entry point of this command.
    """
    shutil.rmtree('./docs_src/build/', ignore_errors=True)
    os.makedirs('./docs_src/build/', exist_ok=True)

    logger.info(msg='Document\'s scripts execution started...')
    _exec_document_script()

    logger.info(msg='Sphinx build command started...')
    os.chdir('./docs_src/')
    complete_process: sp.CompletedProcess = sp.run(
        'make html', shell=True,
        stdout=sp.PIPE, stderr=sp.STDOUT)
    stdout: str = complete_process.stdout.decode('utf-8')
    print(stdout)

    logger.info(msg='Moving documentation to docs directory...')
    os.chdir('../')
    shutil.rmtree('./docs/', ignore_errors=True)
    shutil.copytree(src='./docs_src/build/html/', dst='./docs/')

    logger.info(msg='Replacing `_static` and `_images` paths by `static`...')
    _replace_static_path()

    logger.info(
        msg='Removing `# runnable` inline comment from code blocks...')
    _remove_runnable_inline_comment_from_code_blocks()

    logger.info(msg='Build completed!')


def _remove_runnable_inline_comment_from_code_blocks(
        dir_path: str = './docs/') -> None:
    """
    Remove `# runnable` inline comment from each exported documents'
    code blocks recursively.

    Parameters
    ----------
    dir_path : str, default './docs/'
        Target directory path.
    """
    from apysc._string import string_util
    RUNNABLE_COMMENT_CODE: Final[str] = (
        r'<span></span><span class="c1"># runnable</span>'
    )
    file_or_dir_names: List[str] = os.listdir(dir_path)
    for file_or_dir_name in file_or_dir_names:
        file_or_dir_path: str = os.path.join(dir_path, file_or_dir_name)
        if os.path.isdir(file_or_dir_path):
            _remove_runnable_inline_comment_from_code_blocks(
                dir_path=file_or_dir_path)
            continue
        if not file_or_dir_path.endswith('.html'):
            continue
        string_util.substitute_file_by_pattern(
            file_path=file_or_dir_path,
            pattern=RUNNABLE_COMMENT_CODE,
            repl='',
            flags=re.MULTILINE)


def _exec_document_script(
        limit_count: Optional[int] = None) -> List[str]:
    """
    Execute each runnable scripts in the documents.

    Parameters
    ----------
    limit_count : int or None, optional
        Limitation of script execution count.

    Returns
    -------
    executed_scripts : list of str
        List of executed Python scripts.
    """
    from apysc._file import file_util
    from apysc._file import module_util
    md_file_paths: List[str] = \
        file_util.get_specified_ext_file_paths_recursively(
            extension='.md', dir_path='./docs_src/')
    hashed_vals: List[str]
    md_file_paths, hashed_vals = _slice_md_file_by_hashed_val(
        md_file_paths=md_file_paths)
    count: int = 0
    is_limit: bool = False
    executed_scripts: List[str] = []
    for md_file_path, hashed_val in zip(md_file_paths, hashed_vals):
        runnable_scripts: List[str] = _get_runnable_scripts_in_md_code_blocks(
            md_file_path=md_file_path)
        for runnable_script in runnable_scripts:
            print()
            print('-' * 20)
            logger.info(
                msg=(f'Executing document script: \n{runnable_script}'))
            print('-' * 20)
            stdout: str = module_util.save_tmp_module_and_run_script(
                script=runnable_script)
            if 'Traceback' in stdout:
                raise Exception(
                    f'Error occurred while executing script:\n{stdout}')
            executed_scripts.append(runnable_script)
            _save_md_hashed_val(
                md_file_path=md_file_path, hashed_val=hashed_val)
            count += 1
            if limit_count is not None and count == limit_count:
                is_limit = True
                break
        if is_limit:
            break
    return executed_scripts


def _save_md_hashed_val(md_file_path: str, hashed_val: str) -> None:
    """
    Save markdown hashed string value to file.

    Parameters
    ----------
    md_file_path : str
        Original markdown file path.
    hashed_val : str
        Hashed markdown text value.
    """
    from apysc._file import file_util
    under_source_file_path: str = _get_md_under_source_file_path(
        md_file_path=md_file_path)
    dest_path: str = os.path.join(
        HASHED_VALS_DIR_PATH, under_source_file_path,
    )
    file_util.save_plain_txt(txt=hashed_val, file_path=dest_path)


HASHED_VALS_DIR_PATH: Final[str] = './docs_src/hashed_vals/'


def _slice_md_file_by_hashed_val(
        md_file_paths: List[str]) -> Tuple[List[str], List[str]]:
    """
    Slice markdown file paths by hashed values (remove unchanged
    documents from list).

    Parameters
    ----------
    md_file_paths : list of str
        Target markdown file paths.

    Returns
    -------
    sliced_md_file_paths : list of str
        Sliced markdown file paths.
    hashed_vals : list of str
        Hashed values.
    """
    sliced_md_file_paths: List[str] = []
    hashed_vals: List[str] = []
    for md_file_path in md_file_paths:
        if '/hashed_vals/' in md_file_path:
            continue
        under_source_file_path: str = _get_md_under_source_file_path(
            md_file_path=md_file_path)
        hash_file_path: str = os.path.join(
            HASHED_VALS_DIR_PATH,
            under_source_file_path,
        )
        hash_file_dir_path: str = os.path.dirname(hash_file_path)
        os.makedirs(hash_file_dir_path, exist_ok=True)
        saved_hashed_val: str = _read_md_file_hashed_val_from_file(
            hash_file_path=hash_file_path)
        md_hashed_val: str = _read_md_file_and_hash_txt(
            md_file_path=md_file_path)
        if saved_hashed_val == md_hashed_val:
            print(
                'Skipped markdown file since it is not changed: '
                f'{md_file_path}')
            continue
        sliced_md_file_paths.append(md_file_path)
        hashed_vals.append(md_hashed_val)
    return sliced_md_file_paths, hashed_vals


def _get_md_under_source_file_path(md_file_path: str) -> str:
    """
    Get a markdown file path under the source directory.

    Parameters
    ----------
    md_file_path : str
        Target markdown file path.

    Returns
    -------
    under_source_file_path : str
        File path that under the document source directory,
        e.g., './doc_src/source/any/path.md' will be 'any/path.md'.
    """
    under_source_file_path: str = md_file_path.split('/source/', 1)[1]
    return under_source_file_path


def _read_md_file_and_hash_txt(md_file_path: str) -> str:
    """
    Read markdown file and hash that text.

    Parameters
    ----------
    md_file_path : str
        Target markdown file path.

    Returns
    -------
    hashed_val : str
        Hashed string value.
    """
    from apysc._file import file_util
    md_txt: str = file_util.read_txt(file_path=md_file_path)
    hashed_val: str = hashlib.sha1(md_txt.encode()).hexdigest()
    return hashed_val


def _read_md_file_hashed_val_from_file(hash_file_path: str) -> str:
    """
    Read the markdown file hashed value from the saved file.

    Parameters
    ----------
    hash_file_path : str
        Target hash file path.

    Returns
    -------
    hashed_val : str
        Hashed string value. If file does not exist, then blank string
        will be returned.
    """
    from apysc._file import file_util
    if not os.path.exists(hash_file_path):
        return ''
    hashed_val: str = file_util.read_txt(file_path=hash_file_path)
    hashed_val = hashed_val.strip()
    return hashed_val


class _CodeBlock:

    code_type: str
    code: str
    runnable: bool

    def __init__(self, code_type: str, code: str, runnable: bool) -> None:
        """
        Code block data class.

        Parameters
        ----------
        code_type : str
            Code type (e.g., 'py', 'sql', '', or something else).
        code : str
            Code in the target code block.
        runnable : bool
            If runnable code block, this will be True.
        """
        self.code_type = code_type
        self.code = code
        self.runnable = runnable


def _get_runnable_scripts_in_md_code_blocks(md_file_path: str) -> List[str]:
    """
    Get runnable Python scripts in the markdown code blocks.

    Parameters
    ----------
    md_file_path : str
        Target markdown file path.

    Returns
    -------
    runnable_scripts : list of str
        Runnable Python scripts in code blocks.
        Code blocks with the `# runnable` inline comment
        at the begining of the block will be targeted.
    """
    from apysc._file.file_util import read_txt
    md_txt: str = read_txt(file_path=md_file_path)
    code_blocks: List[_CodeBlock] = _get_code_blocks_from_txt(md_txt=md_txt)
    runnable_scripts: List[str] = []
    for code_block in code_blocks:
        if code_block.code_type != 'py':
            continue
        if not code_block.runnable:
            continue
        code: str = code_block.code
        code = _replace_html_saving_export_path_by_doc_path(code=code)
        code = _append_js_lib_path_and_skip_settings(code=code)
        runnable_scripts.append(code)
    return runnable_scripts


def _append_js_lib_path_and_skip_settings(code: str) -> str:
    """
    Append JavaScript libraries exporting directory path
    setting (js_lib_dir_path) and skipping setting
    (skip_js_lib_exporting) arguments in the code.

    Parameters
    ----------
    code : str
        Target Python code.

    Returns
    -------
    code : str
        Settings appended code.
    """
    code = re.sub(
        pattern=(
            r'(save_overall_html\(.+?)\)'
        ),
        repl=r"\1,\n    js_lib_dir_path='../', skip_js_lib_exporting=True)",
        string=code,
        count=1,
        flags=re.MULTILINE | re.DOTALL)
    return code


def _replace_html_saving_export_path_by_doc_path(code: str) -> str:
    """
    Replace html saving interace's export path argument value
    in the code by document path.

    Parameters
    ----------
    code : str
        Target Python code.

    Returns
    -------
    code : str
        Replaced code. html saving interface argument,
        for example, `save_overall_html` `dest_dir_path`
        will be replaced by './docs_src/_static/<original_path>/'.
    """
    match: Optional[Match] = re.search(
        pattern=(
            r"save_overall_html\(.*?dest_dir_path='(.+?)'\)"
        ),
        string=code,
        flags=re.MULTILINE | re.DOTALL)
    if match is None:
        return code
    original_path: str = match.group(1)
    while original_path.startswith('.'):
        original_path = original_path.replace('.', '', 1)
    if original_path.startswith('/'):
        original_path = original_path.replace('/', '', 1)
    if not original_path.endswith('/'):
        original_path += '/'

    code = re.sub(
        pattern=(
            r"(save_overall_html\(.*?dest_dir_path=).+?\)"
        ),
        repl=rf"\1'./docs_src/source/_static/{original_path}')",
        string=code, count=1,
        flags=re.MULTILINE | re.DOTALL)
    return code


def _get_code_blocks_from_txt(md_txt: str) -> List[_CodeBlock]:
    """
    Get code blocks from a markdown text.

    Parameters
    ----------
    md_txt : str
        Target markdown text.

    Returns
    -------
    code_blocks : list of _CodeBlock
        Code blocks in a markdown text.
    """
    is_code_block: bool = False
    code_block_line_num: int = 0
    lines: List[str] = md_txt.splitlines()
    code_type: str = ''
    code: str = ''
    runnable: bool = False
    code_blocks: List[_CodeBlock] = []
    for line in lines:
        if not is_code_block and line.startswith('```'):
            code_type = line.replace('```', '')
            code_type = code_type.split(':')[0]
            is_code_block = True
            continue
        if not is_code_block:
            continue
        if line.startswith('```'):
            code_blocks.append(_CodeBlock(
                code_type=code_type, code=code, runnable=runnable))
            is_code_block = False
            code_block_line_num = 0
            code = ''
            runnable = False
            continue
        code_block_line_num += 1
        if code_block_line_num == 1 and line == '# runnable':
            runnable = True
            continue
        if code != '':
            code += '\n'
        code += line
    return code_blocks


def _replace_static_path() -> None:
    """
    Replace document `_static` paths by `static`.
    """
    shutil.move(src='./docs/_static/', dst='./docs/static/')
    shutil.move(src='./docs/_images/', dst='./docs/images/')
    _replace_static_path_recursively(dir_path='./docs/')


def _replace_static_path_recursively(dir_path: str) -> None:
    """
    Replace each files' `_static` paths by `static`.

    Parameters
    ----------
    dir_path : str
        Target directory path.
    """
    file_or_dir_names: List[str] = os.listdir(dir_path)
    file_extensions: List[str] = ['.html', '.js']
    for file_or_dir_name in file_or_dir_names:
        if file_or_dir_name in _jslib_file_name_keys_dict:
            continue
        file_or_dir_path: str = os.path.join(dir_path, file_or_dir_name)
        if os.path.isdir(file_or_dir_path):
            _replace_static_path_recursively(dir_path=file_or_dir_path)
            continue
        extension: str = os.path.splitext(file_or_dir_path)[1]
        if extension not in file_extensions:
            continue
        with open(file_or_dir_path) as f:
            file_txt: str = f.read()
        file_txt = file_txt.replace('_static', 'static')
        file_txt = file_txt.replace('_images', 'images')
        with open(file_or_dir_path, 'w') as f:
            f.write(file_txt)


if __name__ == '__main__':
    _main()
