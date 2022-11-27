<!-- @author: Maryniak, Marius - Fachbereich Elektrotechnik, Westfälische Hochschule Gelsenkirchen -->

# Dokumentation: Options

## data

- `--wms_url_rgb`: str
- `--wms_layer_rgb`: str
- `--wms_url_nir`: str
- `--wms_layer_nir`: str
- `--epsg_code`: int
- `--boundary_shape_file_path`: str
- `--no-boundary_shape_file_path`: no arguments
- `--bounding_box`: list of int
- `--no-bounding_box`: no arguments

## postprocessing

- `--sieve_size`: int
- `--no-sieve_size`: no arguments
- `--simplify`: no arguments
- `--no-simplify`: no arguments

## aggregation

- `--tile_size`: list of int
- `--no-tile_size`: no arguments
- `--shape_file_path`: list of str
- `--no-shape_file_path`: no arguments

## export_settings

- `--output_dir_path`: str
- `--prefix`: str
- `--export_raw_shape_file`: str
- `--no-export_raw_shape_file`: no arguments