import inspect

import numpy as np
import pytest

from src.utils.coordinator import Coordinator
from src.utils.grid_generator import GridGenerator


def test_init(mocked_grid_generator: GridGenerator) -> None:
    """
    | Tests __init__().

    :param mocked_grid_generator: mocked grid generator fixture
    :returns: None
    """
    bounding_box = (-128, -128, 128, 128)
    tile_size = 128
    epsg_code = 25832

    coordinator = Coordinator(grid_generator=mocked_grid_generator,
                              bounding_box=bounding_box,
                              tile_size=tile_size,
                              epsg_code=epsg_code)

    assert isinstance(coordinator, Coordinator)
    attributes = ['grid_generator', 'tile_size', 'epsg_code']
    assert list(vars(coordinator).keys()) == attributes

    assert isinstance(coordinator.grid_generator, GridGenerator)
    assert coordinator.grid_generator.x_min == bounding_box[0]
    assert coordinator.grid_generator.y_min == bounding_box[1]
    assert coordinator.grid_generator.x_max == bounding_box[2]
    assert coordinator.grid_generator.y_max == bounding_box[3]
    assert coordinator.grid_generator.epsg_code == epsg_code
    assert isinstance(coordinator.tile_size, int)
    assert coordinator.tile_size == tile_size
    assert isinstance(coordinator.epsg_code, int)
    assert coordinator.epsg_code == epsg_code


def test_compute_coordinates(coordinator_with_mocked_grid_generator: tuple[Coordinator, GridGenerator]) -> None:
    """
    | Tests compute_coordinates().

    :param coordinator_with_mocked_grid_generator: coordinator fixture
    :returns: None
    """
    coordinator, mocked_grid_generator = coordinator_with_mocked_grid_generator

    coordinates = np.array([[-128, -128], [0, -128], [-128, 0], [0, 0]], dtype=np.int32)
    mocked_grid_generator.compute_coordinates.return_value = coordinates

    coordinates = coordinator.compute_coordinates()

    expected = np.array([[-128, 0], [0, 0], [-128, 128], [0, 128]], dtype=np.int32)

    # noinspection PyUnresolvedReferences
    mocked_grid_generator.compute_coordinates.assert_called_once_with(tile_size=coordinator.tile_size,
                                                                      quantize=True)

    assert isinstance(coordinates, np.ndarray)
    assert coordinates.dtype == np.int32
    assert coordinates.ndim == 2
    assert coordinates.shape[-1] == 2
    np.testing.assert_array_equal(coordinates, expected)


@pytest.mark.skip(reason='Test not implemented yet.')
def test_filter_coordinates_outside_boundary():
    pass


@pytest.mark.skip(reason='Test not implemented yet.')
def test_extract_coordinates_processed():
    pass


@pytest.mark.skip(reason='Test not implemented yet.')
def test_filter_coordinates_processed():
    pass


def test_filter_coordinates_default(coordinator_with_mocked_grid_generator: tuple[Coordinator, GridGenerator]) -> None:
    """
    | Tests the default values of the parameters of filter_coordinates().

    :param coordinator_with_mocked_grid_generator: coordinator fixture
    :returns: None
    """
    coordinator, _ = coordinator_with_mocked_grid_generator

    signature = inspect.signature(coordinator.filter_coordinates)
    boundary_default = signature.parameters['boundary'].default
    path_tiles_processed_dir_default = signature.parameters['path_tiles_processed_dir'].default

    assert boundary_default is None
    assert path_tiles_processed_dir_default is None


@pytest.mark.skip(reason='Test not implemented yet.')
def test_filter_coordinates():
    pass
