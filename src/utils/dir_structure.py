# @author: Maryniak, Marius - Fachbereich Elektrotechnik, Westfälische Hochschule Gelsenkirchen

from pathlib import Path


def create_features_dir(output_dir_path):
    """Creates a hidden .features directory in the output directory.

    :param str or Path output_dir_path: path to the output directory
    :returns: None
    :rtype: None
    """
    output_dir_path = Path(output_dir_path)
    (output_dir_path / '.features').mkdir(exist_ok=True)
