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
  clip_border: false
  ignore_cached_tiles: false
```

- ### wms_url
  - **type:** str
  - URL des WMSs (Web Map Service) der unbelaubten RGB- und NIR-Fernerkundungsdaten  
    *Hinweis:* Der WMS benötigt eine Bodenauflösung von mindestens 20cm (DOP20).  
    Zur Einbindung lokaler Daten können Sie mit einer Map Server Software (z. B. [GeoServer](https://geoserver.org "Get GeoServer")) einen lokalen WMS einrichten.

- ### wms_layer
  - **type:** str
  - Layer des WMSs (Web Map Service) der RGB- und NIR-Fernerkundungsdaten

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

- ### clip_border
  - **type:** bool (*optional*, ***default:*** false)
  - Anwendung von Border Clipping, um die Qualität der Versiegelungskarte zu erhöhen  
    *Hinweis:* Die Hardwarevoraussetzung ändert sich (8GB RAM &rarr; 12GB RAM) und die Laufzeit erhöht sich um 50%.

- ### ignore_cached_tiles
  - **type:** bool (*optional*, ***default:*** false)
  - Neuberechnung bereits verarbeiteter Kacheln (`.tiles` Verzeichnis)

***Hinweis:*** Es muss entweder `boundary_shape_file_path` oder `bounding_box` definiert werden.
Werden beide Parameter definiert, wird das Gebiet des Shape Files genutzt.

## postprocessing

```yaml
  sieve_size: 2
  simplify: true
```

- ### sieve_size
  - **type:** int (*optional*, ***default:*** null, **valid range:** 0 <= sieve_size <= 10)
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
    *Hinweis:* Das Ausgabeverzeichnis muss leer sein, kann jedoch ein leeres, bereits genutztes Ausgabeverzeichnis sein.
    Bereits verarbeitete Kacheln sind dort im ausgeblendeten `.tiles` Verzeichnis gespeichert.
    Dieses kann wie folgt eingeblendet werden:  
    **Mac:**
    <kbd>cmd</kbd> + <kbd>Shift</kbd> + <kbd>.</kbd>  
    **Linux:**
    <kbd>Strg</kbd> + <kbd>H</kbd>  
    **Windows 11:**
    `Anzeigen` &rarr; `Einblenden` &rarr; `Ausgeblendete Elemente`  
    **Windows 10 & 8:**
    `Ansicht` &rarr; `Ein-/ ausblenden` &rarr; `Ausgeblendete Elemente`

- ### prefix
  - **type:** str
  - Präfix der Dateinamen

- ### export_raw_shape_file
  - **type:** bool (*optional*, ***default:*** false)
  - zusätzlicher Export des Shape Files ohne Postprocessing