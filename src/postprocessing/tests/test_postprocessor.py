# @author: Maryniak, Marius - Fachbereich Elektrotechnik, Westfälische Hochschule Gelsenkirchen

import geopandas as gpd
import geopandas.testing
import pytest

from src.postprocessing.postprocessor import Postprocessor
from src.postprocessing.tests.data import tests_data


@pytest.mark.parametrize('test_input, expected', tests_data.parameters_sieve_gdf)
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
