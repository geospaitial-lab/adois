from collections import OrderedDict

import geopandas as gpd
from shapely.geometry import Polygon


class Aggregator:
    DECIMAL_PLACES = 2

    def __init__(self,
                 gdf,
                 bounding_box):
        """
        | Constructor method

        :param gpd.GeoDataFrame gdf: geodataframe
        :param (int, int, int, int) bounding_box: bounding box (x_1, y_1, x_2, y_2)
        :returns: None
        :rtype: None
        """
        self.gdf = gdf
        self.bounding_box = bounding_box

    @staticmethod
    def evaluate_stats(aggregation_gdf, aggregated_gdf):
        """
        | Returns an geodataframe with statistical values of the aggregated geodataframe and its shape file schema.
        | Each polygon has the following attributes:
        | - area, imp_area, imp_dens
        | - bui_area, bui_dens
        | - sur_area, sur_dens
        | - bui_imp_r, sur_imp_r

        :param gpd.GeoDataFrame aggregation_gdf: geodataframe for aggregation
        :param gpd.GeoDataFrame aggregated_gdf: aggregated geodataframe
        :returns: geodataframe with statistical values of the aggregated geodataframe and its shape file schema
        :rtype: (gpd.GeoDataFrame, dict[str, OrderedDict[str, str] or str])
        """
        for index in aggregation_gdf['aggregation_id']:
            area = float(aggregation_gdf.loc[aggregation_gdf['aggregation_id'] == index].area)
            imp_area = float(aggregated_gdf.loc[aggregated_gdf['aggregation_id'] == index].area.sum())
            imp_density = imp_area / area
            bui_area = float(aggregated_gdf.loc[(aggregated_gdf['aggregation_id'] == index) &
                                                (aggregated_gdf['class'] == 1)].area.sum())
            bui_density = bui_area / area
            sur_area = float(aggregated_gdf.loc[(aggregated_gdf['aggregation_id'] == index) &
                                                (aggregated_gdf['class'] == 2)].area.sum())
            sur_density = sur_area / area

            try:
                bui_imp_ratio = min(bui_area / imp_area, 1.)
                sur_imp_ratio = min(sur_area / imp_area, 1.)
            except ZeroDivisionError:
                bui_imp_ratio = 0.
                sur_imp_ratio = 0.

            aggregation_gdf.at[index, 'area'] = area
            aggregation_gdf.at[index, 'imp_area'] = imp_area
            aggregation_gdf.at[index, 'imp_dens'] = imp_density
            aggregation_gdf.at[index, 'bui_area'] = bui_area
            aggregation_gdf.at[index, 'bui_dens'] = bui_density
            aggregation_gdf.at[index, 'sur_area'] = sur_area
            aggregation_gdf.at[index, 'sur_dens'] = sur_density
            aggregation_gdf.at[index, 'bui_imp_r'] = bui_imp_ratio
            aggregation_gdf.at[index, 'sur_imp_r'] = sur_imp_ratio

        aggregation_gdf = aggregation_gdf.drop(columns='aggregation_id')

        attributes = OrderedDict()
        attributes['area'] = f'float:13.{Aggregator.DECIMAL_PLACES}'
        attributes['imp_area'] = f'float:13.{Aggregator.DECIMAL_PLACES}'
        attributes['imp_dens'] = f'float:13.{Aggregator.DECIMAL_PLACES}'
        attributes['bui_area'] = f'float:13.{Aggregator.DECIMAL_PLACES}'
        attributes['bui_dens'] = f'float:13.{Aggregator.DECIMAL_PLACES}'
        attributes['sur_area'] = f'float:13.{Aggregator.DECIMAL_PLACES}'
        attributes['sur_dens'] = f'float:13.{Aggregator.DECIMAL_PLACES}'
        attributes['bui_imp_r'] = f'float:13.{Aggregator.DECIMAL_PLACES}'
        attributes['sur_imp_r'] = f'float:13.{Aggregator.DECIMAL_PLACES}'
        schema = {'properties': attributes,
                  'geometry': 'Polygon'}

        return aggregation_gdf, schema

    def mask_gdf(self, gdf):
        """
        | Returns a masked geodataframe.

        :param gpd.GeoDataFrame gdf: geodataframe
        :returns: masked geodataframe
        :rtype: gpd.GeoDataFrame
        """
        polygon_bounding_box = Polygon([[self.bounding_box[0], self.bounding_box[1]],
                                        [self.bounding_box[0], self.bounding_box[3]],
                                        [self.bounding_box[2], self.bounding_box[3]],
                                        [self.bounding_box[2], self.bounding_box[1]]])
        masked_gdf = gpd.clip(gdf,
                              mask=polygon_bounding_box,
                              keep_geom_type=True)
        return masked_gdf

    def aggregate_gdf(self,
                      aggregation_gdf,
                      boundary_gdf):
        """
        | Returns an geodataframe with statistical values of the aggregated geodataframe and its shape file schema.
        | Each polygon has the following attributes:
        | - area, imp_area, imp_dens
        | - bui_area, bui_dens
        | - sur_area, sur_dens
        | - bui_imp_r, sur_imp_r

        :param gpd.GeoDataFrame aggregation_gdf: geodataframe for aggregation
        :param gpd.GeoDataFrame or None boundary_gdf: boundary geodataframe
        :returns: geodataframe with statistical values of the aggregated geodataframe and its shape file schema
        :rtype: (gpd.GeoDataFrame, dict[str, OrderedDict[str, str] or str])
        """
        aggregation_gdf = aggregation_gdf[['geometry']]
        aggregation_gdf['aggregation_id'] = aggregation_gdf.index
        aggregation_gdf = self.mask_gdf(aggregation_gdf)

        if boundary_gdf is not None:
            aggregation_gdf = gpd.clip(aggregation_gdf,
                                       mask=boundary_gdf,
                                       keep_geom_type=True)

        aggregated_gdf = gpd.overlay(df1=self.gdf,
                                     df2=aggregation_gdf,
                                     how='intersection',
                                     keep_geom_type=False)

        aggregation_gdf, schema = self.evaluate_stats(aggregation_gdf=aggregation_gdf,
                                                      aggregated_gdf=aggregated_gdf)

        return aggregation_gdf, schema
