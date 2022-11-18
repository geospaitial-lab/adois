# @author: Maryniak, Marius - Fachbereich Elektrotechnik, Westfälische Hochschule Gelsenkirchen

parameters_get_coordinates = \
    [
        # region no quantization, no remainder
        ((512, 512, 1024, 1024),
         [(512, 768), (768, 768), (512, 1024), (768, 1024)]),
        ((512, -1024, 1024, -512),
         [(512, -768), (768, -768), (512, -512), (768, -512)]),
        ((-1024, -1024, -512, -512),
         [(-1024, -768), (-768, -768), (-1024, -512), (-768, -512)]),
        ((-1024, 512, -512, 1024),
         [(-1024, 768), (-768, 768), (-1024, 1024), (-768, 1024)]),
        ((-256, -256, 256, 256),
         [(-256, 0), (0, 0), (-256, 256), (0, 256)]),
        # endregion

        # region quantization, no remainder
        ((640, 640, 1024, 1024),
         [(512, 768), (768, 768), (512, 1024), (768, 1024)]),
        ((640, -896, 1024, -512),
         [(512, -768), (768, -768), (512, -512), (768, -512)]),
        ((-896, -896, -512, -512),
         [(-1024, -768), (-768, -768), (-1024, -512), (-768, -512)]),
        ((-896, 640, -512, 1024),
         [(-1024, 768), (-768, 768), (-1024, 1024), (-768, 1024)]),
        ((-128, -128, 256, 256),
         [(-256, 0), (0, 0), (-256, 256), (0, 256)]),
        # endregion

        # region no quantization, remainder
        ((512, 512, 896, 896),
         [(512, 768), (768, 768), (512, 1024), (768, 1024)]),
        ((512, -1024, 896, -640),
         [(512, -768), (768, -768), (512, -512), (768, -512)]),
        ((-1024, -1024, -640, -640),
         [(-1024, -768), (-768, -768), (-1024, -512), (-768, -512)]),
        ((-1024, 512, -640, 896),
         [(-1024, 768), (-768, 768), (-1024, 1024), (-768, 1024)]),
        ((-256, -256, 128, 128),
         [(-256, 0), (0, 0), (-256, 256), (0, 256)]),
        # endregion

        # region quantization, remainder
        ((640, 640, 896, 896),
         [(512, 768), (768, 768), (512, 1024), (768, 1024)]),
        ((640, -896, 896, -640),
         [(512, -768), (768, -768), (512, -512), (768, -512)]),
        ((-896, -896, -640, -640),
         [(-1024, -768), (-768, -768), (-1024, -512), (-768, -512)]),
        ((-896, 640, -640, 896),
         [(-1024, 768), (-768, 768), (-1024, 1024), (-768, 1024)]),
        ((-128, -128, 128, 128),
         [(-256, 0), (0, 0), (-256, 256), (0, 256)])
        # endregion
    ]

parameters_filter_cached_coordinates_empty_tiles_dir = \
    [([(512, 768), (768, 768), (512, 1024), (768, 1024)],
      [(512, 768), (768, 768), (512, 1024), (768, 1024)]),
     ([(512, -768), (768, -768), (512, -512), (768, -512)],
      [(512, -768), (768, -768), (512, -512), (768, -512)]),
     ([(-1024, -768), (-768, -768), (-1024, -512), (-768, -512)],
      [(-1024, -768), (-768, -768), (-1024, -512), (-768, -512)]),
     ([(-1024, 768), (-768, 768), (-1024, 1024), (-768, 1024)],
      [(-1024, 768), (-768, 768), (-1024, 1024), (-768, 1024)]),
     ([(-256, 0), (0, 0), (-256, 256), (0, 256)],
      [(-256, 0), (0, 0), (-256, 256), (0, 256)])]

parameters_filter_cached_coordinates_not_empty_tiles_dir = \
    [
        # region some tiles have already been downloaded
        ([(512, 768), (768, 768), (512, 1024), (768, 1024)],
         [(512, 768), (768, 768)]),
        ([(512, -768), (768, -768), (512, -512), (768, -512)],
         [(512, -768), (768, -768)]),
        ([(-1024, -768), (-768, -768), (-1024, -512), (-768, -512)],
         [(-1024, -768), (-768, -768)]),
        ([(-1024, 768), (-768, 768), (-1024, 1024), (-768, 1024)],
         [(-1024, 768), (-768, 768)]),
        ([(-256, 0), (0, 0), (-256, 256), (0, 256)],
         [(-256, 0), (0, 0)]),
        # endregion

        # region all tiles have already been downloaded
        ([(512, 1024), (768, 1024)],
         []),
        ([(512, -512), (768, -512)],
         []),
        ([(-1024, -512), (-768, -512)],
         []),
        ([(-1024, 1024), (-768, 1024)],
         []),
        ([(-256, 256), (0, 256)],
         [])
        # endregion
    ]

parameters_get_valid_coordinates = \
    [
        # region bounding box is smaller than boundary polygon
        ((-256, -256, 256, 256),
         [(-256, 0), (0, 0), (-256, 256), (0, 256)]),
        # endregion

        # region bounding box is equal to boundary polygon
        ((-512, -512, 512, 512),
         [(-512, -256), (-256, -256), (0, -256), (256, -256),
          (-512, 0), (-256, 0), (0, 0), (256, 0),
          (-512, 256), (-256, 256), (0, 256), (256, 256),
          (-512, 512), (-256, 512), (0, 512), (256, 512)]),
        # endregion

        # region bounding box is larger than boundary polygon
        ((-768, -768, 768, 768),
         [(-768, -512), (-512, -512), (-256, -512), (0, -512), (256, -512), (512, -512),
          (-768, -256), (-512, -256), (-256, -256), (0, -256), (256, -256), (512, -256),
          (-768, 0), (-512, 0), (-256, 0), (0, 0), (256, 0), (512, 0),
          (-768, 256), (-512, 256), (-256, 256), (0, 256), (256, 256), (512, 256),
          (-768, 512), (-512, 512), (-256, 512), (0, 512), (256, 512), (512, 512),
          (-768, 768), (-512, 768), (-256, 768), (0, 768), (256, 768), (512, 768)]),
        ((-1024, -1024, 1024, 1024),
         [(-768, -512), (-512, -512), (-256, -512), (0, -512), (256, -512), (512, -512),
          (-768, -256), (-512, -256), (-256, -256), (0, -256), (256, -256), (512, -256),
          (-768, 0), (-512, 0), (-256, 0), (0, 0), (256, 0), (512, 0),
          (-768, 256), (-512, 256), (-256, 256), (0, 256), (256, 256), (512, 256),
          (-768, 512), (-512, 512), (-256, 512), (0, 512), (256, 512), (512, 512),
          (-768, 768), (-512, 768), (-256, 768), (0, 768), (256, 768), (512, 768)]),
        # endregion

        # region bounding box is not inside the boundary polygon
        ((768, 768, 1024, 1024),
         []),
        ((768, -768, 1024, -1024),
         []),
        ((-768, -768, -1024, -1024),
         []),
        ((-768, 768, -1024, 1024),
         []),
        # endregion
    ]

parameters_get_argument_parser = \
    [
        # region data
        (['/path/to/config_file.yaml'],
         {'config_file_path': '/path/to/config_file.yaml',
          'debug': False,
          'ignore_cached_tiles': False}),
        (['/path/to/config_file.yaml', '-d', '-ict'],
         {'config_file_path': '/path/to/config_file.yaml',
          'debug': True,
          'ignore_cached_tiles': True}),
        (['/path/to/config_file.yaml', '--debug', '--ignore_cached_tiles'],
         {'config_file_path': '/path/to/config_file.yaml',
          'debug': True,
          'ignore_cached_tiles': True}),
        (['/path/to/config_file.yaml', '--wms_url_rgb', 'https://www.wms.de/wms_url_rgb'],
         {'config_file_path': '/path/to/config_file.yaml',
          'debug': False,
          'ignore_cached_tiles': False,
          'wms_url_rgb': 'https://www.wms.de/wms_url_rgb'}),
        (['/path/to/config_file.yaml', '--wms_layer_rgb', 'wms_layer_rgb'],
         {'config_file_path': '/path/to/config_file.yaml',
          'debug': False,
          'ignore_cached_tiles': False,
          'wms_layer_rgb': 'wms_layer_rgb'}),
        (['/path/to/config_file.yaml', '--wms_url_nir', 'https://www.wms.de/wms_url_nir'],
         {'config_file_path': '/path/to/config_file.yaml',
          'debug': False,
          'ignore_cached_tiles': False,
          'wms_url_nir': 'https://www.wms.de/wms_url_nir'}),
        (['/path/to/config_file.yaml', '--wms_layer_nir', 'wms_layer_nir'],
         {'config_file_path': '/path/to/config_file.yaml',
          'debug': False,
          'ignore_cached_tiles': False,
          'wms_layer_nir': 'wms_layer_nir'}),
        (['/path/to/config_file.yaml', '--epsg_code', '25832'],
         {'config_file_path': '/path/to/config_file.yaml',
          'debug': False,
          'ignore_cached_tiles': False,
          'epsg_code': 25832}),
        (['/path/to/config_file.yaml', '--boundary_shape_file_path', '/path/to/boundary_shape_file.shp'],
         {'config_file_path': '/path/to/config_file.yaml',
          'debug': False,
          'ignore_cached_tiles': False,
          'boundary_shape_file_path': '/path/to/boundary_shape_file.shp'}),
        (['/path/to/config_file.yaml', '--no-boundary_shape_file_path'],
         {'config_file_path': '/path/to/config_file.yaml',
          'debug': False,
          'ignore_cached_tiles': False,
          'boundary_shape_file_path': None}),
        (['/path/to/config_file.yaml', '--bounding_box', '-512', '-512', '512', '512'],
         {'config_file_path': '/path/to/config_file.yaml',
          'debug': False,
          'ignore_cached_tiles': False,
          'bounding_box': [-512, -512, 512, 512]}),
        (['/path/to/config_file.yaml', '--no-bounding_box'],
         {'config_file_path': '/path/to/config_file.yaml',
          'debug': False,
          'ignore_cached_tiles': False,
          'bounding_box': None}),
        # endregion

        # region postprocessing
        (['/path/to/config_file.yaml', '--sieve_size', '1'],
         {'config_file_path': '/path/to/config_file.yaml',
          'debug': False,
          'ignore_cached_tiles': False,
          'sieve_size': 1}),
        (['/path/to/config_file.yaml', '--no-sieve_size'],
         {'config_file_path': '/path/to/config_file.yaml',
          'debug': False,
          'ignore_cached_tiles': False,
          'sieve_size': None}),
        (['/path/to/config_file.yaml', '--simplify'],
         {'config_file_path': '/path/to/config_file.yaml',
          'debug': False,
          'ignore_cached_tiles': False,
          'simplify': True}),
        (['/path/to/config_file.yaml', '--no-simplify'],
         {'config_file_path': '/path/to/config_file.yaml',
          'debug': False,
          'ignore_cached_tiles': False,
          'simplify': False}),
        # endregion

        # region aggregation
        (['/path/to/config_file.yaml', '--tile_size'],
         {'config_file_path': '/path/to/config_file.yaml',
          'debug': False,
          'ignore_cached_tiles': False,
          'tile_size': []}),
        (['/path/to/config_file.yaml', '--tile_size', '128'],
         {'config_file_path': '/path/to/config_file.yaml',
          'debug': False,
          'ignore_cached_tiles': False,
          'tile_size': [128]}),
        (['/path/to/config_file.yaml', '--tile_size', '128', '256', '512', '1024'],
         {'config_file_path': '/path/to/config_file.yaml',
          'debug': False,
          'ignore_cached_tiles': False,
          'tile_size': [128, 256, 512, 1024]}),
        (['/path/to/config_file.yaml', '--no-tile_size'],
         {'config_file_path': '/path/to/config_file.yaml',
          'debug': False,
          'ignore_cached_tiles': False,
          'tile_size': None}),
        (['/path/to/config_file.yaml', '--shape_file_path'],
         {'config_file_path': '/path/to/config_file.yaml',
          'debug': False,
          'ignore_cached_tiles': False,
          'shape_file_path': []}),
        (['/path/to/config_file.yaml', '--shape_file_path', '/path/to/shape_file.shp'],
         {'config_file_path': '/path/to/config_file.yaml',
          'debug': False,
          'ignore_cached_tiles': False,
          'shape_file_path': ['/path/to/shape_file.shp']}),
        (['/path/to/config_file.yaml', '--shape_file_path', '/path/to/shape_file_1.shp', '/path/to/shape_file_2.shp',
          '/path/to/shape_file_3.shp', '/path/to/shape_file_4.shp'],
         {'config_file_path': '/path/to/config_file.yaml',
          'debug': False,
          'ignore_cached_tiles': False,
          'shape_file_path': ['/path/to/shape_file_1.shp', '/path/to/shape_file_2.shp',
                              '/path/to/shape_file_3.shp', '/path/to/shape_file_4.shp']}),
        (['/path/to/config_file.yaml', '--no-shape_file_path'],
         {'config_file_path': '/path/to/config_file.yaml',
          'debug': False,
          'ignore_cached_tiles': False,
          'shape_file_path': None}),
        # endregion

        # region export settings
        (['/path/to/config_file.yaml', '--output_dir_path', '/path/to/output_dir'],
         {'config_file_path': '/path/to/config_file.yaml',
          'debug': False,
          'ignore_cached_tiles': False,
          'output_dir_path': '/path/to/output_dir'}),
        (['/path/to/config_file.yaml', '--prefix', 'prefix'],
         {'config_file_path': '/path/to/config_file.yaml',
          'debug': False,
          'ignore_cached_tiles': False,
          'prefix': 'prefix'}),
        (['/path/to/config_file.yaml', '--export_raw_shape_file'],
         {'config_file_path': '/path/to/config_file.yaml',
          'debug': False,
          'ignore_cached_tiles': False,
          'export_raw_shape_file': True}),
        (['/path/to/config_file.yaml', '--no-export_raw_shape_file'],
         {'config_file_path': '/path/to/config_file.yaml',
          'debug': False,
          'ignore_cached_tiles': False,
          'export_raw_shape_file': False}),
        # endregion
    ]

parameters_WMSLayerError = \
    [
        (['valid_wms_layer'],
         r'Invalid wms_layer of WMS \(https://www.wms.de/wms_url\) in config file!'
         r'\n  Expected valid_wms_layer, got invalid_wms_layer instead\.'),
        (['valid_wms_layer_4', 'valid_wms_layer_3', 'valid_wms_layer_2', 'valid_wms_layer_1'],
         r'Invalid wms_layer of WMS \(https://www.wms.de/wms_url\) in config file!'
         r'\n  Expected valid_wms_layer_1, valid_wms_layer_2, valid_wms_layer_3 or valid_wms_layer_4, '
         r'got invalid_wms_layer instead\.')
    ]

parameters_EPSGCodeError = \
    [
        ([1],
         r'Invalid epsg_code in config file!\n  Expected 1, got 0 instead\.'),
        ([1, 2, 3, 4],
         r'Invalid epsg_code in config file!\n  Expected 1, 2, 3 or 4, got 0 instead\.')
    ]

parameters_validate_sieve_size = [(None, None), (0, None), (1, 1), (10, 10)]

parameters_validate_sieve_size_exception = [-1, 11]

parameters_validate_simplify = [(None, False), (True, True), (False, False)]

parameters_Postprocessing = [([None, None], [None, False]),
                             ([0, True], [None, True]),
                             ([1, False], [1, False]),
                             ([10, None], [10, False])]

parameters_validate_tile_size = \
    [
        (None, []),
        (0, []),
        (1, [1]),
        ([1, 2, 3, 4], [1, 2, 3, 4]),
        ([0, 1, 2, 3, 4], [1, 2, 3, 4]),
        ([0, 1, None, 2, None, 3, None, 4], [1, 2, 3, 4]),
        ([0, 3, 1, None, 4, 2, None, 1, 3, None, 2, 4], [1, 2, 3, 4])
    ]

parameters_validate_tile_size_exception = \
    [
        -1,
        [-1, 2, 3, 4],
        [0, -1, 2, 3, 4],
        [0, -1, None, 2, None, 3, None, 4],
        [0, 3, -1, None, 4, 2, None, 1, 3, None, 2, 4]
    ]

parameters_validate_shape_file_path = \
    [
        (None, []),
        ('shape_file.shp', ['shape_file.shp']),
        (['shape_file_1.shp', 'shape_file_2.shp',
          'shape_file_3.shp', 'shape_file_4.shp'],
         ['shape_file_1.shp', 'shape_file_2.shp',
          'shape_file_3.shp', 'shape_file_4.shp']),
        (['shape_file_1.shp', None, 'shape_file_2.shp', None,
          'shape_file_3.shp', None, 'shape_file_4.shp'],
         ['shape_file_1.shp', 'shape_file_2.shp',
          'shape_file_3.shp', 'shape_file_4.shp']),
        (['shape_file_3.shp', 'shape_file_1.shp', None,
          'shape_file_4.shp', 'shape_file_2.shp', None,
          'shape_file_1.shp', 'shape_file_3.shp', None,
          'shape_file_2.shp', 'shape_file_4.shp', None],
         ['shape_file_1.shp', 'shape_file_2.shp',
          'shape_file_3.shp', 'shape_file_4.shp'])
    ]

parameters_validate_shape_file_path_exception_1 = \
    [
        'invalid_shape_file.shp',
        ['invalid_shape_file.shp', 'shape_file_2.shp',
         'shape_file_3.shp', 'shape_file_4.shp'],
        ['invalid_shape_file.shp', None, 'shape_file_2.shp', None,
         'shape_file_3.shp', None, 'shape_file_4.shp'],
        ['shape_file_3.shp', 'invalid_shape_file.shp', None,
         'shape_file_4.shp', 'shape_file_2.shp', None,
         'invalid_shape_file.shp', 'shape_file_3.shp', None,
         'shape_file_2.shp', 'shape_file_4.shp', None]
    ]

parameters_validate_shape_file_path_exception_2 = \
    [
        'invalid_shape_file.py',
        ['invalid_shape_file.py', 'shape_file_2.shp',
         'shape_file_3.shp', 'shape_file_4.shp'],
        ['invalid_shape_file.py', None, 'shape_file_2.shp', None,
         'shape_file_3.shp', None, 'shape_file_4.shp'],
        ['shape_file_3.shp', 'invalid_shape_file.py', None,
         'shape_file_4.shp', 'shape_file_2.shp', None,
         'invalid_shape_file.py', 'shape_file_3.shp', None,
         'shape_file_2.shp', 'shape_file_4.shp', None]
    ]

parameters_Aggregation = \
    [
        ([None, None], [[], []]),
        ([0, 'shape_file.shp'], [[], ['shape_file.shp']]),
        ([1, ['shape_file_1.shp', 'shape_file_2.shp', 'shape_file_3.shp', 'shape_file_4.shp']],
         [[1], ['shape_file_1.shp', 'shape_file_2.shp', 'shape_file_3.shp', 'shape_file_4.shp']]),
        ([[1, 2, 3, 4], ['shape_file_1.shp', None, 'shape_file_2.shp', None,
                         'shape_file_3.shp', None, 'shape_file_4.shp']],
         [[1, 2, 3, 4], ['shape_file_1.shp', 'shape_file_2.shp', 'shape_file_3.shp', 'shape_file_4.shp']]),
        ([[0, 1, 2, 3, 4], ['shape_file_3.shp', 'shape_file_1.shp', None,
                            'shape_file_4.shp', 'shape_file_2.shp', None,
                            'shape_file_1.shp', 'shape_file_3.shp', None,
                            'shape_file_2.shp', 'shape_file_4.shp', None]],
         [[1, 2, 3, 4], ['shape_file_1.shp', 'shape_file_2.shp', 'shape_file_3.shp', 'shape_file_4.shp']]),
        ([[0, 1, None, 2, None, 3, None, 4], None], [[1, 2, 3, 4], []]),
        ([[0, 3, 1, None, 4, 2, None, 1, 3, None, 2, 4], None], [[1, 2, 3, 4], []])
    ]
