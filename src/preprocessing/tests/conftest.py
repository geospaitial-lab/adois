# @author: Maryniak, Marius - Fachbereich Elektrotechnik, Westfälische Hochschule Gelsenkirchen

from pathlib import Path

import pytest


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
