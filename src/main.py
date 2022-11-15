# @author: Maryniak, Marius - Fachbereich Elektrotechnik, Westfälische Hochschule Gelsenkirchen

import logging
from datetime import datetime as DateTime  # PEP8 compliant
from pathlib import Path

import enlighten
import geopandas as gpd

import src.utils as utils
from src.aggregation import Aggregator, GridGenerator
from src.data import RemoteSensingDataDownloader
from src.inference import Inference
from src.postprocessing import Postprocessor
from src.preprocessing import filter_downloaded_coordinates, get_coordinates, Preprocessor, get_internal_coordinates
from src.utils import ConfigParser, create_dir_structure, create_tiles_dir, export, get_argument_parser, get_metadata


def main():
    # region Argument parsing
    manager = enlighten.get_manager()
    status_bar = manager.status_bar(status_format=u'adois{fill}Stage: {stage}{fill}{elapsed}',
                                    justify=enlighten.Justify.CENTER,
                                    autorefresh=True,
                                    stage='Initializing')

    start_time = DateTime.now()

    argument_parser = get_argument_parser()
    args = argument_parser.parse_args()
    # endregion

    # region Config parsing
    config_parser = ConfigParser(args.config_file_path)
    config_parser.update_config_dict(args=args)
    config = config_parser.parse_config()
    # endregion

    # region Logging
    utils.DEBUG = args.debug

    logger_formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s: %(message)s',
                                         datefmt="%Y-%m-%d %H:%M:%S")
    logger = logging.getLogger('main_logger')

    console_handler = logging.StreamHandler()
    if utils.DEBUG:
        console_handler.setLevel(logging.DEBUG)
    else:
        console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logger_formatter)
    logger.addHandler(console_handler)

    if utils.DEBUG:
        date_time = str(DateTime.now().isoformat(sep='_', timespec='seconds')).replace(':', '-')
        file_handler = logging.FileHandler(Path(config.export_settings.output_dir_path) / f"{date_time}.log", mode='w')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logger_formatter)
        logger.addHandler(file_handler)

    logger.setLevel(logging.DEBUG)

    utils.set_exception_hook()
    # endregion

    # region Initializing
    create_tiles_dir(output_dir_path=config.export_settings.output_dir_path)
    logger.debug('.features directory created')

    if config.data.boundary_shape_file_path:
        boundary_gdf = gpd.read_file(config.data.boundary_shape_file_path)
        if boundary_gdf.crs is None:
            boundary_gdf = boundary_gdf.set_crs(f'EPSG:{config.data.epsg_code}')
        else:
            boundary_gdf = boundary_gdf.to_crs(f'EPSG:{config.data.epsg_code}')
        boundary_gdf = boundary_gdf[['geometry']]
        # noinspection PyTypeChecker
        coordinates = get_internal_coordinates(bounding_box=config.data.bounding_box,
                                               epsg_code=config.data.epsg_code,
                                               boundary_gdf=boundary_gdf)
    else:
        boundary_gdf = None
        # noinspection PyTypeChecker
        coordinates = get_coordinates(bounding_box=config.data.bounding_box)
    logger.debug('Coordinates calculated')

    if not args.ignore_cached_tiles:
        filtered_coordinates = filter_downloaded_coordinates(coordinates=coordinates,
                                                             output_dir_path=config.export_settings.output_dir_path)
        logger.debug('Coordinates filtered')
    else:
        filtered_coordinates = coordinates

    # noinspection PyTypeChecker
    preprocessor = Preprocessor()
    logger.debug('Preprocessor initialized')

    rsdd_rgb = RemoteSensingDataDownloader(wms_url=config.data.rgb.wms_url,
                                           wms_layer=config.data.rgb.wms_layer,
                                           epsg_code=config.data.epsg_code)
    logger.debug('RemoteSensingDataDownloader (rgb) initialized')

    rsdd_nir = RemoteSensingDataDownloader(wms_url=config.data.nir.wms_url,
                                           wms_layer=config.data.nir.wms_layer,
                                           epsg_code=config.data.epsg_code)
    logger.debug('RemoteSensingDataDownloader (nir) initialized')

    inference = Inference('data/model/model.onnx')
    logger.debug('Inference initialized')

    # noinspection PyTypeChecker
    postprocessor = Postprocessor(output_dir_path=config.export_settings.output_dir_path,
                                  bounding_box=config.data.bounding_box,
                                  epsg_code=config.data.epsg_code,
                                  boundary_gdf=boundary_gdf)
    logger.debug('Postprocessor initialized')

    # noinspection PyTypeChecker
    grid_generator = GridGenerator(bounding_box=config.data.bounding_box,
                                   epsg_code=config.data.epsg_code)
    logger.debug('GridGenerator initialized')

    iterations = len(filtered_coordinates)
    if iterations:
        logger.info(f'Iterations: {iterations}')
    else:
        logger.info('Iterations: 0 (area is already being processed)')
    # endregion

    # region Download
    # noinspection PyTypeChecker
    status_bar.update(stage='Download, Inference, Caching',
                      force=True)
    progress_bar = manager.counter(total=iterations,
                                   desc='Download, Inference, Caching',
                                   unit='tiles',
                                   count=0,
                                   min_delta=0)
    progress_bar.refresh()

    for index, coordinates_element in enumerate(filtered_coordinates):
        rgb_image = rsdd_rgb.get_image(coordinates_element)
        logger.debug(f'Iteration {index + 1} / {iterations} ->  rgb image downloaded')
        nir_image = rsdd_nir.get_image(coordinates_element)
        logger.debug(f'Iteration {index + 1} / {iterations} ->  nir image downloaded')

        image = preprocessor.get_image(rgb_image=rgb_image,
                                       nir_image=nir_image)

        mask = inference.get_mask(image)
        logger.debug(f'Iteration {index + 1} / {iterations} -> mask created')

        postprocessor.vectorize_mask(mask=mask,
                                     coordinates=coordinates_element)
        logger.debug(f'Iteration {index + 1} / {iterations} -> mask vectorized and cached')
        logger.info(f'Iteration {index + 1} / {iterations} -> tile cached')
        progress_bar.update()
    # endregion

    # region Postprocessing
    # noinspection PyTypeChecker
    status_bar.update(stage='Postprocessing',
                      force=True)
    raw_gdf = postprocessor.concatenate_gdfs(coordinates=coordinates)
    logger.info('Cached geodataframes concatenated')

    if config.postprocessing.sieve_size:
        postprocessed_gdf = postprocessor.sieve_gdf(raw_gdf,
                                                    sieve_size=config.postprocessing.sieve_size)
        postprocessed_gdf = postprocessor.fill_gdf(postprocessed_gdf,
                                                   hole_size=config.postprocessing.sieve_size)
        logger.info('Geodataframe postprocessed (sieved and filled)')
    else:
        postprocessed_gdf = None

    if config.postprocessing.simplify:
        if postprocessed_gdf is not None:
            postprocessed_gdf = postprocessor.simplify_gdf(postprocessed_gdf)
        else:
            postprocessed_gdf = postprocessor.simplify_gdf(raw_gdf)
        logger.info('Geodataframe postprocessed (simplified)')
    # endregion

    # region Create grids
    if config.aggregation.tile_size or config.aggregation.shape_file_path:
        # noinspection PyTypeChecker
        status_bar.update(stage='Aggregation',
                          force=True)

    gdfs_grid = []
    grid_iterations = len(config.aggregation.tile_size)

    for index, tile_size_meters in enumerate(config.aggregation.tile_size):
        gdfs_grid.append(grid_generator.get_grid(tile_size_meters=tile_size_meters))
        logger.info(f'Grid {index + 1} / {grid_iterations} created')
    # endregion

    # region Create Shape files
    gdfs_shape_file = []
    shape_file_iterations = len(config.aggregation.shape_file_path)

    for index, shape_file_path_element in enumerate(config.aggregation.shape_file_path):
        gdf = gpd.read_file(shape_file_path_element)
        if gdf.crs is None:
            gdf = gdf.set_crs(f'EPSG:{config.data.epsg_code}')
        else:
            gdf = gdf.to_crs(f'EPSG:{config.data.epsg_code}')
        gdfs_shape_file.append(gdf)
        logger.info(f'Shape file {index + 1} / {shape_file_iterations} created')
    # endregion

    # region Aggregation
    if postprocessed_gdf is None:
        # noinspection PyTypeChecker
        aggregator = Aggregator(gdf=raw_gdf,
                                bounding_box=config.data.bounding_box)
    else:
        # noinspection PyTypeChecker
        aggregator = Aggregator(gdf=postprocessed_gdf,
                                bounding_box=config.data.bounding_box)
    logger.debug('Aggregator initialized')

    aggregation_gdfs_grid = []

    for index, gdf_grid in enumerate(gdfs_grid):
        aggregation_gdfs_grid.append(aggregator.aggregate_gdf(aggregation_gdf=gdf_grid,
                                                              boundary_gdf=boundary_gdf))
        logger.info(f'Grid {index + 1} / {grid_iterations} aggregated')

    aggregation_gdfs_shape_file = []

    for index, gdf_shape_file in enumerate(gdfs_shape_file):
        aggregation_gdfs_shape_file.append(aggregator.aggregate_gdf(aggregation_gdf=gdf_shape_file,
                                                                    boundary_gdf=boundary_gdf))
        logger.info(f'Shape file {index + 1} / {shape_file_iterations} aggregated')
    # endregion

    # region Export
    end_time = DateTime.now()

    # noinspection PyTypeChecker
    status_bar.update(stage='Export',
                      force=True)

    create_dir_structure(output_dir_path=config.export_settings.output_dir_path,
                         export_raw_shape_file=config.export_settings.export_raw_shape_file,
                         tile_sizes=config.aggregation.tile_size,
                         shape_file_paths=config.aggregation.shape_file_path)
    logger.debug('Directory structure in output directory created')

    metadata = get_metadata(config=config_parser.config_dict,
                            start_time=start_time,
                            end_time=end_time)
    logger.debug('Metadata created')

    export(output_dir_path=config.export_settings.output_dir_path,
           export_raw_shape_file=config.export_settings.export_raw_shape_file,
           raw_gdf=raw_gdf,
           postprocessed_gdf=postprocessed_gdf,
           prefix=config.export_settings.prefix,
           tile_sizes=config.aggregation.tile_size,
           aggregation_gdfs_grid=aggregation_gdfs_grid,
           shape_file_paths=config.aggregation.shape_file_path,
           aggregation_gdfs_shape_file=aggregation_gdfs_shape_file,
           metadata=metadata)
    logger.info('Shape files and metadata exported')
    # endregion


if __name__ == "__main__":
    main()
