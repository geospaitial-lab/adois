from pathlib import Path

data_test_BoundingBoxLengthError = (
    [([],
      r'Invalid bounding_box in the config!\n'
      r'Expected 4 coordinates \(x_min, y_min, x_max, y_max\), got 0 coordinates instead.'),
     ([1, 2, 3],
      r'Invalid bounding_box in the config!\n'
      r'Expected 4 coordinates \(x_min, y_min, x_max, y_max\), got 3 coordinates instead.'),
     ([1, 2, 3, 4, 5],
      r'Invalid bounding_box in the config!\n'
      r'Expected 4 coordinates \(x_min, y_min, x_max, y_max\), got 5 coordinates instead.')])

data_test_BoundingBoxValueError = (
    [([2, 2, 1, 1],
      r'Invalid bounding_box in the config!\n'
      r'Expected 4 coordinates \(x_min, y_min, x_max, y_max\) with x_min < x_max and y_min < y_max, '
      r'got \(2, 2, 1, 1\) instead.'),
     ([-1, -1, -2, -2],
      r'Invalid bounding_box in the config!\n'
      r'Expected 4 coordinates \(x_min, y_min, x_max, y_max\) with x_min < x_max and y_min < y_max, '
      r'got \(-1, -1, -2, -2\) instead.')])

data_test_GeoDataEmptyError = (
    [(('path_test', Path(r'path\to\geo_data.gpkg')),
      r'Invalid path_test in the config!\n'
      r'The geo data at path\\to\\geo_data.gpkg is empty.'),
     (('path_test', Path('path/to/geo_data.gpkg')),
      r'Invalid path_test in the config!\n'
      'The geo data at path/to/geo_data.gpkg is empty.')])

data_test_GeoDataFormatError = (
    [(('path_test', Path(r'path\to\geo_data.invalid')),
      r'Invalid path_test in the config!\n'
      'Expected file extension .gpkg or .shp, got .invalid instead.'),
     (('path_test', Path('path/to/geo_data.invalid')),
      r'Invalid path_test in the config!\n'
      'Expected file extension .gpkg or .shp, got .invalid instead.')])

data_test_GeoDataGeometryError = (
    [(('path_test', Path(r'path\to\geo_data.gpkg')),
      r'Invalid path_test in the config!\n'
      r'The geo data at path\\to\\geo_data.gpkg contains invalid polygons.'),
     (('path_test', Path('path/to/geo_data.gpkg')),
      r'Invalid path_test in the config!\n'
      'The geo data at path/to/geo_data.gpkg contains invalid polygons.')])

data_test_GeoDataLoadingError = (
    [(('path_test', Path(r'path\to\geo_data.gpkg'), Exception('Test message.')),
      r'Invalid path_test in the config!\n'
      r'An exception is raised while loading the geo data at path\\to\\geo_data.gpkg.\n'
      'Test message.'),
     (('path_test', Path('path/to/geo_data.gpkg'), Exception('Test message.')),
      r'Invalid path_test in the config!\n'
      r'An exception is raised while loading the geo data at path/to/geo_data.gpkg.\n'
      'Test message.')])

data_test_GeoDataNotFoundError = (
    [(('path_test', Path(r'path\to\geo_data.gpkg')),
      r'Invalid path_test in the config!\n'
      r'The geo data at path\\to\\geo_data.gpkg does not exist.'),
     (('path_test', Path('path/to/geo_data.gpkg')),
      r'Invalid path_test in the config!\n'
      'The geo data at path/to/geo_data.gpkg does not exist.')])

data_test_GeoDataTypeError = (
    [(('path_test', Path(r'path\to\geo_data.gpkg')),
      r'Invalid path_test in the config!\n'
      r'The geo data at path\\to\\geo_data.gpkg contains geometries other than polygons.'),
     (('path_test', Path('path/to/geo_data.gpkg')),
      r'Invalid path_test in the config!\n'
      'The geo data at path/to/geo_data.gpkg contains geometries other than polygons.')])

data_test_OutputDirNotFoundError = (
    [(Path(r'path\to\output_dir'),
      r'Invalid path_output_dir in the config!\n'
      r'The output directory at path\\to\\output_dir does not exist.'),
     (Path('path/to/output_dir'),
      r'Invalid path_output_dir in the config!\n'
      'The output directory at path/to/output_dir does not exist.')])

data_test_SieveSizeError = (
    [(-1,
      r'Invalid sieve_size in the config!\n'
      'Expected a number in the range of 0 to 10, got -1 instead.'),
     (11,
      r'Invalid sieve_size in the config!\n'
      'Expected a number in the range of 0 to 10, got 11 instead.')])
