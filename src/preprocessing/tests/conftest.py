# @author: Maryniak, Marius - Fachbereich Elektrotechnik, Westfälische Hochschule Gelsenkirchen

from pathlib import Path

import pytest

from src.preprocessing.preprocessor import Preprocessor


@pytest.fixture(scope='session')
def output_dir_path_empty_features_dir(tmp_path_factory):
    """Returns the path to the temporary output directory.
    The .features directory is empty.

    :param pytest.TempPathFactory tmp_path_factory: temporary path
    :returns: path to the output directory
    :rtype: Path
    """
    output_dir_path = tmp_path_factory.mktemp('output_dir')
    (output_dir_path / '.features').mkdir()
    return output_dir_path


@pytest.fixture(scope='session')
def output_dir_path_not_empty_features_dir(tmp_path_factory):
    """Returns the path to the temporary output directory.
    The .features directory is not empty.

    :param pytest.TempPathFactory tmp_path_factory: temporary path
    :returns: path to the output directory
    :rtype: Path
    """
    output_dir_path = tmp_path_factory.mktemp('output_dir')
    (output_dir_path / '.features').mkdir()
    (output_dir_path / '.features' / '512_1024.json').touch()
    (output_dir_path / '.features' / '768_1024.json').touch()
    (output_dir_path / '.features' / '512_-512.json').touch()
    (output_dir_path / '.features' / '768_-512.json').touch()
    (output_dir_path / '.features' / '-1024_-512.json').touch()
    (output_dir_path / '.features' / '-768_-512.json').touch()
    (output_dir_path / '.features' / '-1024_1024.json').touch()
    (output_dir_path / '.features' / '-768_1024.json').touch()
    (output_dir_path / '.features' / '-256_256.json').touch()
    (output_dir_path / '.features' / '0_256.json').touch()
    return output_dir_path


@pytest.fixture(scope='session')
def color_codes():
    """Returns color codes.

    :returns: color codes
    :rtype: dict[tuple[int, int, int], int]
    """
    color_codes = {(0, 0, 0): 0,
                   (0, 128, 255): 51,
                   (255, 128, 0): 102,
                   (255, 128, 255): 153,
                   (255, 255, 255): 255}
    return color_codes


@pytest.fixture(scope='session')
def preprocessor(color_codes):
    """Returns a preprocessor instance.

    :param dict[tuple[int, int, int], int] color_codes: color codes
    :returns: preprocessor
    :rtype: Preprocessor
    """
    preprocessor = Preprocessor(color_codes=color_codes)
    return preprocessor
