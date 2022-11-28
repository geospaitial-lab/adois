<!-- @author: Maryniak, Marius - Fachbereich Elektrotechnik, Westfälische Hochschule Gelsenkirchen -->

# Dokumentation: Config File (.yaml)

Die Beispielwerte der Parameter entsprechen denen des [Example Config Files](../example_config.yaml "Example Config File").

## data

```yaml
data:
  rgb:
    wms_url: https://www.wms.nrw.de/geobasis/wms_nw_dop
    wms_layer: nw_dop_rgb
  nir:
    wms_url: https://www.wms.nrw.de/geobasis/wms_nw_dop
    wms_layer: nw_dop_nir
  epsg_code: 25832
  boundary_shape_file_path: /Pfad/zu/boundary_shape_file.shp
  bounding_box:
    - 363210
    - 5715455
    - 364210
    - 5716455
```

- ### wms_url
  - **type:** str
  - URL des WMS (Web Map Service) der RGB- und NIR-Fernerkundungsdaten
    *Hinweis:* Der WMS benötigt eine Bodenauflösung von mindestens 20cm (DOP20).

- ### wms_layer
  - **type:** str
  - Layer des WMS (Web Map Service) der RGB- und NIR-Fernerkundungsdaten

- ### epsg_code
  - **type:** int
  - EPSG Code des Koordinatenreferenzsystems

- ### boundary_shape_file_path
  - **type:** str (*optional*, ***default:*** null)
  - Pfad zum Shape File des Gebiets  
    *Hinweis:* Das Shape File darf nur ein Polygon beinhalten.

- ### bounding_box
  - **type:** list of int (*optional*, ***default:*** null)
  - 4 Koordinaten (x_min, y_min, x_max, y_max) des Gebiets

***Hinweis:*** Es muss entweder `boundary_shape_file_path` oder `bounding_box` definiert werden.
Werden beide Parameter definiert, wird das Gebiet des Shape Files genutzt.

## postprocessing

```yaml
  sieve_size: 2
  simplify: true
```

- ### sieve_size
  - **type:** int (*optional*, ***default:*** null, **valid range:** 0 <= sieve_size <= 10  )
  - Maximale Größe der Polygone in Quadratmetern, die aus dem Shape File entfernt werden sollen
    (Löcher dieser Größe in Polygonen werden aufgefüllt)

- ### simplify
  - **type:** bool (*optional*, ***default:*** false)  
  - Anwendung des Douglas Peucker Algorithmus, um die Datenmenge des Shape Files zu reduzieren

## aggregation

```yaml
  tile_size:
    - 50
    - 100
  shape_file_path:
    - /Pfad/zu/aggregation_shape_file_1.shp
    - /Pfad/zu/aggregation_shape_file_2.shp
```

- ### tile_size
  - **type:** int, list of int (*optional*, ***default:*** null)
  - Kantenlänge der quadratischen Kacheln zur Aggregation in Metern

- ### shape_file_path
  - **type:** string, list of string (*optional*, ***default:*** null)
  - Pfad zum Shape File zur Aggregation

## export_settings

```yaml
  output_dir_path: /Pfad/zu/Ausgabeverzeichnis
  prefix: example
  export_raw_shape_file: true
```

- ### output_dir_path
  - **type:** str
  - Pfad zum Ausgabeverzeichnis  
    *Hinweis:* Das Ausgabeverzeichnis muss entweder leer sein oder ein bereits genutztes Ausgabeverzeichnis sein.

- ### prefix
  - **type:** str
  - Präfix der Dateinamen

- ### export_raw_shape_file
  - **type:** bool (*optional*, ***default:*** false)
  - zusätzlicher Export des Shape Files ohne Nachbearbeitung