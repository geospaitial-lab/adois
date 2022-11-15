# @author: Maryniak, Marius - Fachbereich Elektrotechnik, Westfälische Hochschule Gelsenkirchen

from pathlib import Path

import pytest

from src.preprocessing.preprocessor import Preprocessor


@pytest.fixture(scope='session')
def output_dir_path_empty_tiles_dir(tmp_path_factory):
    """
    | Returns the path to the temporary output directory.
    | The .tiles directory is empty.

    :param pytest.TempPathFactory tmp_path_factory: temporary path
    :returns: path to the output directory
    :rtype: Path
    """
    output_dir_path = tmp_path_factory.mktemp('output_dir')
    (output_dir_path / '.tiles').mkdir()
    return output_dir_path


@pytest.fixture(scope='session')
def output_dir_path_not_empty_tiles_dir(tmp_path_factory):
    """
    | Returns the path to the temporary output directory.
    | The .tiles directory is not empty.

    :param pytest.TempPathFactory tmp_path_factory: temporary path
    :returns: path to the output directory
    :rtype: Path
    """
    output_dir_path = tmp_path_factory.mktemp('output_dir')
    (output_dir_path / '.tiles').mkdir()
    (output_dir_path / '.tiles' / '512_1024').mkdir()
    (output_dir_path / '.tiles' / '768_1024').mkdir()
    (output_dir_path / '.tiles' / '512_-512').mkdir()
    (output_dir_path / '.tiles' / '768_-512').mkdir()
    (output_dir_path / '.tiles' / '-1024_-512').mkdir()
    (output_dir_path / '.tiles' / '-768_-512').mkdir()
    (output_dir_path / '.tiles' / '-1024_1024').mkdir()
    (output_dir_path / '.tiles' / '-768_1024').mkdir()
    (output_dir_path / '.tiles' / '-256_256').mkdir()
    (output_dir_path / '.tiles' / '0_256').mkdir()
    return output_dir_path


@pytest.fixture(scope='session')
def preprocessor():
    """
    | Returns a preprocessor instance.

    :returns: preprocessor
    :rtype: Preprocessor
    """
    preprocessor = Preprocessor()
    return preprocessor
