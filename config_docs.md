# Dokumentation: Config File (.yaml)

Im Folgenden werden die Parameter des Config Files erläutert.  
Die Beispielwerte der Parameter entsprechen denen des [Example Config Files](example_config.yaml).


## data

```yaml
data:
  rgb:
    wms_url: https://www.wms.nrw.de/geobasis/wms_nw_dop
    wms_layer: nw_dop_rgb
  nir:
    wms_url: https://www.wms.nrw.de/geobasis/wms_nw_dop
    wms_layer: nw_dop_nir
  ndsm:
    wms_url: https://www.wms.nrw.de/geobasis/wms_nw_ndom
    wms_layer: nw_ndom
  epsg_code: 25832
  boundary_shape_file_path:
  bounding_box:
    - 363210
    - 5715455
    - 364210
    - 5716455
```

- ### wms_url
  - **type:** str
  - URL des WMS (Web Map Service) der RGB-, NIR- und NDSM-Fernerkundungsdaten

- ### wms_layer
  - **type:** str
  - Layer des WMS (Web Map Service) der RGB-, NIR- und NDSM-Fernerkundungsdaten

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


## preprocessing

```yaml
  color_codes_ndsm:
    - (0, 0, 0) - 0         # 0.0m  - 1.0m
    - (255, 255, 255) - 28  # 1.0m  - 1.5m
    - (31, 120, 180) - 57   # 1.5m  - 3.0m
    - (54, 214, 209) - 85   # 3.0m  - 5.0m
    - (64, 207, 39) - 113   # 5.0m  - 10.0m
    - (255, 255, 71) - 142  # 10.0m - 15.0m
    - (255, 206, 71) - 170  # 15.0m - 20.0m
    - (255, 127, 0) - 198   # 20.0m - 25.0m
    - (215, 25, 28) - 227   # 25.0m - 50.0m
    - (114, 0, 11) - 255    # > 50.0m
```

- ### color_codes_ndsm
  - **type:** list of str
  - Mapping von RGB-Werten auf einen 1-Kanal-Wert, um die Datenmenge der NDSM-Fernerkundungsdaten zu reduzieren
    (jedes Listenelement enthält ein RGB-Wert Tupel und einen dazugehörigen Wert zwischen 0 und 255.


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
  - Anwendung des Douglas Peucker Algorithmus, um die Datenmenge des Shape Files zu reduzieren und die Polygone
    zu glätten


## aggregation

```yaml
  tile_size:
    - 50
    - 100
  shape_file_path:
```

- ### tile_size
  - **type:** int, list of int (*optional*, ***default:*** null)
  - Kantenlänge der quadratischen Kacheln in Metern

- ### shape_file_path
  - **type:** string, list of string (*optional*, ***default:*** null)
  - Pfad zum Shape File zur Aggregation


## export_settings

```yaml
  output_dir_path: /Users/mrsmrynk/PycharmProjects/adois_app/output_dir
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