from datetime import datetime
from pathlib import Path

import geopandas as gpd


class Exporter:

    def __init__(self,
                 path_output_dir: Path) -> None:
        """
        :param path_output_dir: path to the output directory
        """
        assert isinstance(path_output_dir, Path)

        self.path_output_dir = path_output_dir / str(datetime.now().isoformat(sep='_', timespec='seconds'))

    def create_output_dir(self) -> None:
        """
        | Creates the output directory.
        """
        self.path_output_dir.mkdir()

    def export_gdf(self,
                   gdf: gpd.GeoDataFrame,
                   relative_path: Path) -> None:
        """
        | Exports the geodataframe as a geopackage.

        :param gdf: geodataframe
        :param relative_path: relative path
        """
        assert isinstance(gdf, gpd.GeoDataFrame)

        assert isinstance(relative_path, Path)

        path = self.path_output_dir / relative_path

        if len(relative_path.parts) > 1:
            path.parents[0].mkdir(parents=True,
                                  exist_ok=True)

        gdf.to_file(str(path), driver='GPKG')
