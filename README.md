![adois](data/images/adois_logo_light_mode.svg#gh-light-mode-only)
![adois](data/images/adois_logo_dark_mode.svg#gh-dark-mode-only)

---

[![Tests](https://img.shields.io/github/workflow/status/mrsmrynk/adois/Tests?event=push&label=Tests&logo=GitHub)](https://github.com/KLIMA-WH/adois_app/actions/workflows/tests.yaml "Tests Workflow")
[![Coverage](https://img.shields.io/codecov/c/github/mrsmrynk/adois/main?label=Coverage&logo=codecov&logoColor=white)](https://app.codecov.io/gh/mrsmrynk/adois "Codecov")
[![License](https://img.shields.io/github/license/mrsmrynk/adois?label=License)](https://gnu.org/licenses "GNU Licenses")

*adois* – automatic detection of impervious surfaces – ist eine Auftragsforschung des [Kreises Recklinghausen](https://kreis-re.de "Kreis Recklinghausen")
in Kooperation mit der [Westfälischen Hochschule Gelsenkirchen](https://w-hs.de "Westfälische Hochschule")
mit dem Ziel der automatisierten Erkennung versiegelter Flächen aus Fernerkundungsdaten mit Methoden des Deep Learnings.  
*adois* ermittelt aus RGB- und NIR-DOPs (Digital Orthophoto) hochauflösende Versiegelungskarten inklusive einer Aggregation auf nutzungsspezifische Flächen.
Die DOPs werden dabei über einen individuellen WMS (Web Map Service) bezogen.

# Installation

**Hardwarevoraussetzungen:** 8GB RAM

Installieren Sie zunächst [Git](https://git-scm.com/downloads "Get Git") und [Git LFS](https://git-lfs.github.com "Get Git LFS").  
Aktivieren Sie Git LFS.

```
git lfs install
```

Laden Sie anschließend das *adois* Repository in ein beliebiges Arbeitsverzeichnis herunter.

```
git clone https://github.com/mrsmrynk/adois
```

## Docker

Installieren Sie [Docker](https://docker.com/products/docker-desktop "Get Docker").  
Wechseln Sie in das *adois* Repository und erstellen Sie nun das *adois* Image.

```
docker build -t adois .
```

***Hinweis:*** Das Parent Image ist das [python:3.8-slim-bullseye](https://hub.docker.com/_/python "Docker Hub - Python") Image.
Die entsprechenden Lizenzbedingungen sind [hier](https://hub.docker.com/_/python "Docker Hub - Python") zu entnehmen.

<details>
<summary><b>Alternative Installationsmöglichkeit zu Docker</b></summary>

## Virtual Environment

Installieren Sie [Python 3.8](https://python.org/downloads "Get Python").  
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

*adois* wird durch ein Config File (.yaml) parametrisiert. Die Parameter werden in der [Dokumentation](docs/docs_config.md "Config File Dokumentation") erläutert.

Um die Software auszuführen, müssen Sie die lokalen Pfade Ihres Systems in den *adois* Container mounten.  
Verwenden Sie dazu die `-v` Flag und `</lokaler/Pfad>:</Pfad/im/Container>`.  
***Hinweis:*** Alle lokalen Pfade, die in dem Config File verwendet werden, müssen gemountet werden.
Nutzen Sie idealerweise das Basisverzeichnis Ihres Systems als Binding.

```
docker run -t -v </Pfad/zu/config.yaml>:/config.yaml -v </Pfad/zu/Basisverzeichnis>:</Pfad/zu/Basisverzeichnis> adois
```

<details>
<summary><b>Alternative Ausführungsmöglichkeiten</b></summary>

## Virtual Environment

Wechseln Sie zunächst in das *adois* Verzeichnis und aktivieren Sie gegebenenfalls die Virtual Environment.  
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

**Options:**
- `--debug`, `-d`: Debug Mode
- `--ignore_cached_tiles`, `-ict`: Überschreiben bereits verarbeiteter Gebiete
- zudem können alle Parameter des Config Files mit der entsprechenden Flag überschrieben werden.
  Die Options werden in der [Dokumentation](docs/docs_options.md "Options Dokumentation") erläutert.

# Ergebnisse

Die Versiegelungskarten inklusive der Aggregationen werden als Shape File ins [Ausgabeverzeichnis](docs/docs_config.md#output_dir_path "Config File Ausgabeverzeichnis") exportiert.  
Die Attribute der Shape Files werden in der [Dokumentation](docs/docs_shape_file_attributes.md "Shape File Attribute Dokumentation") erläutert.