# @author: Maryniak, Marius - Fachbereich Elektrotechnik, Westfälische Hochschule Gelsenkirchen

import geopandas as gpd
import geopandas.testing
import pytest
from shapely.geometry import Polygon

from src.postprocessing.postprocessor import Postprocessor
from src.postprocessing.tests.data import *


@pytest.mark.parametrize('test_input, expected', parameters_sieve_gdf)
def test_sieve_gdf(test_input, expected):
    """
    | Tests sieve_gdf() with different geodataframes and sieve sizes.

    :param (gpd.GeoDataFrame, int) test_input: geodataframe and sieve size
    :param gpd.GeoDataFrame: sieved geodataframe
    :returns: None
    :rtype: None
    """
    sieved_gdf = Postprocessor.sieve_gdf(gdf=test_input[0],
                                         sieve_size=test_input[1])

    gpd.testing.assert_geodataframe_equal(sieved_gdf,
                                          expected,
                                          check_index_type=False)


@pytest.mark.parametrize('test_input, expected', parameters_fill_polygon)
def test_fill_polygon(test_input, expected):
    """
    | Tests fill_polygon() with different polygons and hole sizes.

    :param (Polygon, int) test_input: polygon and hole size
    :param Polygon expected: filled polygon
    :returns: None
    :rtype: None
    """
    filled_polygon = Postprocessor.fill_polygon(polygon=test_input[0],
                                                hole_size=test_input[1])

    assert filled_polygon == expected


@pytest.mark.parametrize('test_input, expected', parameters_fill_gdf)
def test_fill_gdf(test_input, expected):
    """
    | Tests fill_gdf() with different geodataframes and hole sizes.

    :param (gpd.GeoDataFrame, int) test_input: geodataframe and hole size
    :param gpd.GeoDataFrame: filled geodataframe
    :returns: None
    :rtype: None
    """
    filled_gdf = Postprocessor.fill_gdf(gdf=test_input[0],
                                        hole_size=test_input[1])

    gpd.testing.assert_geodataframe_equal(filled_gdf,
                                          expected,
                                          check_index_type=False)
