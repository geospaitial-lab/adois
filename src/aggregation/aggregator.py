from collections import OrderedDict

import geopandas as gpd
from shapely.geometry import Polygon


class Aggregator:
    ATTRIBUTES = OrderedDict()
    ATTRIBUTES['area'] = 'float:13.2'
    ATTRIBUTES['imp_area'] = 'float:13.2'
    ATTRIBUTES['imp_dens'] = 'float:4.2'
    ATTRIBUTES['bui_area'] = 'float:13.2'
    ATTRIBUTES['bui_dens'] = 'float:4.2'
    ATTRIBUTES['pav_area'] = 'float:13.2'
    ATTRIBUTES['pav_dens'] = 'float:4.2'
    ATTRIBUTES['bui_imp_r'] = 'float:4.2'
    ATTRIBUTES['pav_imp_r'] = 'float:4.2'
    SCHEMA = {'properties': ATTRIBUTES,
              'geometry': 'Polygon'}

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
        | Returns a geodataframe with statistical values of the aggregated geodataframe.
        | Each polygon has the following attributes:
        | - area, imp_area, imp_dens
        | - bui_area, bui_dens
        | - pav_area, pav_dens
        | - bui_imp_r, pav_imp_r

        :param gpd.GeoDataFrame aggregation_gdf: geodataframe for aggregation
        :param gpd.GeoDataFrame aggregated_gdf: aggregated geodataframe
        :returns: geodataframe with statistical values of the aggregated geodataframe
        :rtype: gpd.GeoDataFrame
        """
        for index in aggregation_gdf['aggregation_id']:
            area = float(aggregation_gdf.loc[aggregation_gdf['aggregation_id'] == index].area)
            imp_area = float(aggregated_gdf.loc[aggregated_gdf['aggregation_id'] == index].area.sum())
            imp_density = min(imp_area / area, 1.)
            bui_area = float(aggregated_gdf.loc[(aggregated_gdf['aggregation_id'] == index) &
                                                (aggregated_gdf['class'] == 'Hochbau')].area.sum())
            bui_density = min(bui_area / area, 1.)
            pav_area = float(aggregated_gdf.loc[(aggregated_gdf['aggregation_id'] == index) &
                                                (aggregated_gdf['class'] == 'Tiefbau')].area.sum())
            pav_density = min(pav_area / area, 1.)

            try:
                bui_imp_ratio = min(bui_area / imp_area, 1.)
                pav_imp_ratio = min(pav_area / imp_area, 1.)
            except ZeroDivisionError:
                bui_imp_ratio = 0.
                pav_imp_ratio = 0.

            aggregation_gdf.at[index, 'area'] = area
            aggregation_gdf.at[index, 'imp_area'] = imp_area
            aggregation_gdf.at[index, 'imp_dens'] = imp_density
            aggregation_gdf.at[index, 'bui_area'] = bui_area
            aggregation_gdf.at[index, 'bui_dens'] = bui_density
            aggregation_gdf.at[index, 'pav_area'] = pav_area
            aggregation_gdf.at[index, 'pav_dens'] = pav_density
            aggregation_gdf.at[index, 'bui_imp_r'] = bui_imp_ratio
            aggregation_gdf.at[index, 'pav_imp_r'] = pav_imp_ratio

        aggregation_gdf = aggregation_gdf.drop(columns='aggregation_id')
        return aggregation_gdf

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
        | Returns a geodataframe with statistical values of the aggregated geodataframe.
        | Each polygon has the following attributes:
        | - area, imp_area, imp_dens
        | - bui_area, bui_dens
        | - pav_area, pav_dens
        | - bui_imp_r, pav_imp_r

        :param gpd.GeoDataFrame aggregation_gdf: geodataframe for aggregation
        :param gpd.GeoDataFrame or None boundary_gdf: boundary geodataframe
        :returns: geodataframe with statistical values of the aggregated geodataframe
        :rtype: gpd.GeoDataFrame
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

        aggregation_gdf = self.evaluate_stats(aggregation_gdf=aggregation_gdf,
                                              aggregated_gdf=aggregated_gdf)

        return aggregation_gdf
