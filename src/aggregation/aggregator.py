# @author: Maryniak, Marius - Fachbereich Elektrotechnik, Westfälische Hochschule Gelsenkirchen

from collections import OrderedDict

import geopandas as gpd


class Aggregator:
    DECIMAL_PLACES = 4

    def __init__(self, gdf):
        """Constructor method

        :param gpd.GeoDataFrame gdf: geodataframe
        :returns: None
        :rtype: None
        """
        self.gdf = gdf

    @staticmethod
    def evaluate_stats(gdf_aggregation, gdf_aggregated):
        """Returns an geodataframe with statistical values of the aggregated geodataframe and its shape file schema.
        Each polygon has the following attributes:
        area, imp_area, imp_dens, bui_area, bui_dens, sur_area, sur_dens, bui_imp_r, sur_imp_r

        :param gpd.GeoDataFrame gdf_aggregation: geodataframe for aggregation
        :param gpd.GeoDataFrame gdf_aggregated: aggregated geodataframe
        :returns: geodataframe with statistical values of the aggregated geodataframe and its shape file schema
        :rtype: (gpd.GeoDataFrame, dict[str, OrderedDict[str, str] or str])
        """
        for index in gdf_aggregation['FID']:
            area = float(gdf_aggregation.loc[gdf_aggregation['FID'] == index].area)
            imp_area = float(gdf_aggregated.loc[gdf_aggregated['FID'] == index].area.sum())
            imp_density = imp_area / area
            bui_area = float(gdf_aggregated.loc[(gdf_aggregated['FID'] == index) &
                                                (gdf_aggregated['class'] == 1)].area.sum())
            bui_density = bui_area / area
            sur_area = float(gdf_aggregated.loc[(gdf_aggregated['FID'] == index) &
                                                (gdf_aggregated['class'] == 2)].area.sum())
            sur_density = sur_area / area

            if round(imp_area, 4) != 0:
                bui_imp_ratio = bui_area / imp_area
                sur_imp_ratio = sur_area / imp_area
            else:
                bui_imp_ratio = 1.
                sur_imp_ratio = 1.

            gdf_aggregation.at[index, 'area'] = area
            gdf_aggregation.at[index, 'imp_area'] = imp_area
            gdf_aggregation.at[index, 'imp_dens'] = imp_density
            gdf_aggregation.at[index, 'bui_area'] = bui_area
            gdf_aggregation.at[index, 'bui_dens'] = bui_density
            gdf_aggregation.at[index, 'sur_area'] = sur_area
            gdf_aggregation.at[index, 'sur_dens'] = sur_density
            gdf_aggregation.at[index, 'bui_imp_r'] = bui_imp_ratio
            gdf_aggregation.at[index, 'sur_imp_r'] = sur_imp_ratio

        attributes = OrderedDict()
        attributes['FID'] = 'int:10'
        attributes['area'] = f'float:10.{Aggregator.DECIMAL_PLACES}'
        attributes['imp_area'] = f'float:10.{Aggregator.DECIMAL_PLACES}'
        attributes['imp_dens'] = f'float:10.{Aggregator.DECIMAL_PLACES}'
        attributes['bui_area'] = f'float:10.{Aggregator.DECIMAL_PLACES}'
        attributes['bui_dens'] = f'float:10.{Aggregator.DECIMAL_PLACES}'
        attributes['sur_area'] = f'float:10.{Aggregator.DECIMAL_PLACES}'
        attributes['sur_dens'] = f'float:10.{Aggregator.DECIMAL_PLACES}'
        attributes['bui_imp_r'] = f'float:10.{Aggregator.DECIMAL_PLACES}'
        attributes['sur_imp_r'] = f'float:10.{Aggregator.DECIMAL_PLACES}'
        schema = {'properties': attributes,
                  'geometry': 'Polygon'}

        return gdf_aggregation, schema

    def aggregate_gdf(self, gdf_aggregation):
        """Returns an geodataframe with statistical values of the aggregated geodataframe and its shape file schema.
        Each polygon has the following attributes:
        area, imp_area, imp_dens, bui_area, bui_dens, sur_area, sur_dens, bui_imp_r, sur_imp_r

        :param gpd.GeoDataFrame gdf_aggregation: geodataframe for aggregation
        :returns: geodataframe with statistical values of the aggregated geodataframe and its shape file schema
        :rtype: (gpd.GeoDataFrame, dict[str, OrderedDict[str, str] or str])
        """
        gdf_aggregated = gpd.overlay(df1=self.gdf,
                                     df2=gdf_aggregation,
                                     how='intersection',
                                     keep_geom_type=False)

        gdf_aggregation, schema = self.evaluate_stats(gdf_aggregation=gdf_aggregation,
                                                      gdf_aggregated=gdf_aggregated)

        return gdf_aggregation, schema
