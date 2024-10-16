> :loudspeaker: **This repository is no longer actively maintained**<br />
> Have a look at [aviary](https://www.github.com/geospaitial-lab/aviary),
> our new composable inference and postprocessing pipeline for remote sensing data.

![adois](data/images/adois_logo_light_mode.svg#gh-light-mode-only)
![adois](data/images/adois_logo_dark_mode.svg#gh-dark-mode-only)

---

<div align="center">

[![Tests](https://img.shields.io/github/actions/workflow/status/geospaitial-lab/adois/tests.yaml?branch=main&event=push&label=Tests&logo=GitHub)](https://github.com/geospaitial-lab/adois/actions/workflows/tests.yaml "Tests Workflow")
[![Coverage](https://img.shields.io/codecov/c/github/geospaitial-lab/adois/main?label=Coverage&logo=codecov&logoColor=white)](https://app.codecov.io/gh/geospaitial-lab/adois "Codecov")
[![Issues](https://img.shields.io/github/issues/geospaitial-lab/adois?label=Issues)](https://github.com/geospaitial-lab/adois/issues "Issues")
[![License](https://img.shields.io/github/license/geospaitial-lab/adois?color=blue&label=License)](https://gnu.org/licenses "GNU Licenses")

</div>

*adois* – automatic detection of impervious surfaces – ist eine Auftragsforschung des [Kreises Recklinghausen](https://kreis-re.de "Kreis Recklinghausen")
in Kooperation mit der [Westfälischen Hochschule Gelsenkirchen](https://w-hs.de "Westfälische Hochschule")
mit dem Ziel der automatisierten Erkennung versiegelter Flächen aus Fernerkundungsdaten mit Methoden des Deep Learnings.  
*adois* ermittelt aus RGB- und NIR-DOPs (Digital Orthophoto) hochauflösende Versiegelungskarten inklusive einer Aggregation auf nutzungsspezifische Flächen.
Die DOPs werden dabei über einen konfigurierbaren WMS (Web Map Service) bezogen.  
Das Modell ist auf manuell erhobenen Daten des [Emschergenossenschaft Lippeverbands](https://eglv.de "Emschergenossenschaft Lippeverband") trainiert worden.

In unserem Fachartikel [Wie eine Maschine Versiegelungskarten erstellt](https://www.webgis-re.de/cms/fileadmin/user_upload/artikel_wie_eine_maschine_versiegelungskarten_erstellt_aus_vdvmagazin_3_23.pdf "Wie eine Maschine Versiegelungskarten erstellt")
im [VDVmagazin](https://www.vdv-online.de "VDVmagazin") 03/23 finden Sie weitere Informationen zum Projekt, technische Details und beispielhafte praktische Anwendungen der Ergebnisse auf kommunaler Ebene.

# Installation

**Hardwarevoraussetzung:** 8GB RAM

Installieren Sie zunächst [Docker](https://docker.com/products/docker-desktop "Get Docker").  
Laden Sie anschließend das [*adois* Dockerfile](Dockerfile "Get adois Dockerfile") herunter.  
Erstellen Sie nun das *adois* Image.

```
docker build -f </Pfad/zu/Dockerfile> -t adois .
```

***Hinweis:*** Das Parent Image ist das [python:3.8-slim-bullseye](https://hub.docker.com/_/python "Docker Hub - Python") Image.
Die entsprechenden Lizenzbedingungen sind [hier](https://hub.docker.com/_/python "Docker Hub - Python") zu entnehmen.

<details>
<summary><b>Alternative Installationsmöglichkeit zu Docker</b></summary>

### Virtual Environment

Installieren Sie zunächst [Git](https://git-scm.com/downloads "Get Git") und [Python 3.8](https://python.org/downloads "Get Python").

Laden Sie anschließend das *adois* Repository in ein beliebiges Arbeitsverzeichnis herunter.

```
git clone https://github.com/geospaitial-lab/adois --depth 1
```

Laden Sie das [*adois* Modell](https://huggingface.co/geospaitial-lab/adois "Get adois model") herunter und speichern Sie es in dem Arbeitsverzeichnis unter `data/model/model.onnx` ab.

Wechseln Sie in das *adois* Repository und erstellen Sie nun eine Virtual Environment.

```
python3 -m venv venv
```

Aktivieren Sie die Virtual Environment.  
**MacOS/ Linux:**

```
source venv/bin/activate
```

**Windows:**

```
venv\Scripts\activate.bat
```

Installieren Sie die Requirements.

```
pip install -r requirements.txt
```

</details>

# Ausführen

Laden Sie zunächst das [*adois* Example Config File](example_config.yaml "Get adois example config file") herunter.
Die Beispielwerte der Parameter werden in der [Dokumentation](docs/docs_config.md "Dokumentation: Config File") erläutert.

Um die Software auszuführen, müssen Sie die lokalen Pfade Ihres Systems in den *adois* Container mounten.  
Verwenden Sie dazu die `-v` Flag und `</lokaler/Pfad>:</Pfad/im/Container>`.  
***Hinweis:*** Alle lokalen Pfade, die in dem Config File verwendet werden, müssen gemountet werden.
Nutzen Sie idealerweise das Basisverzeichnis Ihres Systems als Binding.

```
docker run -t -v </Pfad/zu/config.yaml>:/config.yaml -v </Pfad/zu/Basisverzeichnis>:</Pfad/zu/Basisverzeichnis> adois
```

<details>
<summary><b>Alternative Ausführungsmöglichkeit zu Docker</b></summary>

### Virtual Environment

Wechseln Sie zunächst in das *adois* Repository und aktivieren Sie gegebenenfalls die Virtual Environment.  
**MacOS/ Linux:**

```
source venv/bin/activate
```

**Windows:**

```
venv\Scripts\activate.bat
```

Führen Sie anschließend die Software aus.

```
python3 -m src.main </Pfad/zu/config.yaml>
```

</details>

# Ergebnisse

Die Versiegelungskarten inklusive der Aggregationen werden als Shape File ins Ausgabeverzeichnis exportiert.  
Die Attribute der Shape Files werden in der [Dokumentation](docs/docs_shape_file_attributes.md "Dokumentation: Shape File Attribute") erläutert.

<div align="center">

<a href="https://drive.google.com/uc?export=view&id=1y87uh01FHTbK_77JRaP7ogNpBSh646yJ">
    <img src="https://imgur.com/D72Nkgz.jpg" alt="Impervious surfaces" width="50%">
</a>

</div>

<div align="center">

<a href="https://drive.google.com/uc?export=view&id=1kx64aBW-fCq2RNU667XkTvhWfp5UWUjp">
    <img src="https://imgur.com/Klw2eb2.jpg" alt="Impervious surfaces Recklinghausen" width="50%">
</a>

</div>

<div align="center">

<a href="https://drive.google.com/uc?export=view&id=10Xqof6MPwVCqXA6oVg4OOBUixXO6IJ4m">
    <img src="https://imgur.com/0A6eJzd.jpg" alt="Aggregated tiles" width="37.5%">
</a>

<a href="https://drive.google.com/uc?export=view&id=1A3WGVZt-158-sdsGr0md1uo_zGZ7hk8D">
    <img src="https://imgur.com/Io0OT6C.jpg" alt="Aggregated parcels" width="37.5%">
</a>

</div>

<div align="center">

<a href="https://drive.google.com/uc?export=view&id=1tjVd-kcS6m5z8FKqb3U48sEKaGqMrRXC">
    <img src="https://imgur.com/gF0CB27.jpg" alt="Aggregated tiles Recklinghausen" width="37.5%">
</a>

<a href="https://drive.google.com/uc?export=view&id=1mmfJYP2WRRywCS_HxAsptgw7pUkLXxJh">
    <img src="https://imgur.com/Rqh0OHY.jpg" alt="Aggregated parcels Recklinghausen" width="37.5%">
</a>

</div>

Im [Web GIS](https://www.webgis-re.de/cms/versiegelte-flaechen "Web GIS - Kreis Recklinghausen") des Kreises Recklinghausen sind die Versiegelungsgrade der Flurstücke des gesamten Kreisgebiets visuell dargestellt.

# Kontakt

Marius Maryniak ([Westfälische Hochschule Gelsenkirchen](https://w-hs.de "Westfälische Hochschule")): <marius.maryniak@w-hs.de>