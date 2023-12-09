import unittest.mock as mock

import pytest

from src.utils.coordinator import Coordinator
from src.utils.grid_generator import GridGenerator


@pytest.fixture(scope='function')
def coordinator_with_mocked_grid_generator(mocked_grid_generator):
    """
    | Returns a coordinator object with a mocked grid generator.

    :param GridGenerator mocked_grid_generator: mocked grid generator fixture
    :returns: coordinator fixture
    :rtype: (Coordinator, GridGenerator)
    """
    coordinator = Coordinator(grid_generator=mocked_grid_generator,
                              bounding_box=(-128, -128, 128, 128),
                              tile_size=128,
                              epsg_code=25832)

    return coordinator, mocked_grid_generator


@pytest.fixture(scope='function')
def grid_generator():
    """
    | Returns a grid generator object.

    :returns: grid generator fixture
    :rtype: GridGenerator
    """
    return GridGenerator(bounding_box=(-128, -128, 128, 128),
                         epsg_code=25832)


@pytest.fixture(scope='function')
def mocked_grid_generator():
    """
    | Returns a mocked grid generator object.

    :returns: mocked grid generator fixture
    :rtype: GridGenerator
    """
    mocked_grid_generator = mock.Mock(spec=GridGenerator)
    mocked_grid_generator.x_min = -128
    mocked_grid_generator.y_min = -128
    mocked_grid_generator.x_max = 128
    mocked_grid_generator.y_max = 128
    mocked_grid_generator.epsg_code = 25832
    return mocked_grid_generator
