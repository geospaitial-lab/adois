<!-- @author: Maryniak, Marius - Fachbereich Elektrotechnik, Westfälische Hochschule Gelsenkirchen -->

![adois](data/images/adois_logo_light_mode.svg#gh-light-mode-only)
![adois](data/images/adois_logo_dark_mode.svg#gh-dark-mode-only)

---

[![Tests](https://github.com/KLIMA-WH/adois_app/actions/workflows/tests.yaml/badge.svg)](https://github.com/KLIMA-WH/adois_app/actions/workflows/tests.yaml)
[![Build and deploy](https://github.com/KLIMA-WH/adois_app/actions/workflows/build_and_deploy.yaml/badge.svg)](https://github.com/KLIMA-WH/adois_app/actions/workflows/build_and_deploy.yaml)

*adois* – automatic detection of impervious surfaces – ist eine Auftragsforschung des [Kreises Recklinghausen](https://www.kreis-re.de "Kreis Recklinghausen")
in Kooperation mit der [Westfälischen Hochschule Gelsenkirchen](https://www.w-hs.de "Westfälische Hochschule")
mit dem Ziel der automatisierten Erkennung versiegelter Flächen aus Fernerkundungsdaten mit Methoden des Deep Learnings.  
*adois* ermittelt aus RGB- und NIR-DOPs hochauflösende Versiegelungskarten inklusive einer Aggregation auf nutzungsspezifische Flächen.
Die DOPs werden dabei über einen individuellen WMS bezogen.

# Installation

**Hardwarevoraussetzungen:** 16GB RAM

Installieren Sie zunächst [Docker](https://www.docker.com/products/docker-desktop "Get Docker").  
Laden Sie anschließend das *adois* Image herunter.

```
docker pull ghcr.io/klima-wh/adois
```

***Hinweis:*** Das Parent Image ist das [python:3.8](https://hub.docker.com/_/python "Docker Hub - Python") Image.
Die entsprechenden Lizenzbedingungen sind [hier](https://hub.docker.com/_/python "Docker Hub - Python") zu entnehmen.

<details>
<summary><b>Alternative Installationsmöglichkeiten</b></summary>

## Docker Build From Source

Installieren Sie zunächst [Docker](https://www.docker.com/products/docker-desktop "Get Docker").  
Laden Sie anschließend das *adois* Repository in ein beliebiges Arbeitsverzeichnis herunter.

```
git clone https://github.com/klima-wh/adois
```

Wechseln Sie in das Verzeichnis und erstellen Sie nun das *adois* Image.

```
docker build -t adois .
```

## Virtual Environment

Installieren Sie zunächst [Python 3.8](https://www.python.org/downloads "Get Python").  
Laden Sie anschließend das adois Repository in ein beliebiges Arbeitsverzeichnis herunter.

```
git clone https://github.com/klima-wh/adois
```

Wechseln Sie in das Verzeichnis und erstellen Sie nun eine Virtual Environment.

```
python3 -m venv venv
```

Aktivieren Sie die Virtual Environment.  
**Mac/ Linux:**

```
source venv/bin/activate
```

**Windows:**

```
venv\Scripts\activate.bat
```

Installieren Sie die Packages.

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

Wechseln Sie in das *adois* Verzeichnis und führen Sie die Software aus.

```
python3 src/main.py </Pfad/zu/config.yaml>
```

</details>

**Options:**
- `--debug`, `-d`: Debug Mode
- `--ignore_cached_tiles`, `-ict`: Überschreiben bereits verarbeiteter Gebiete
- zudem können alle Parameter des Config Files mit der entsprechenden Flag überschrieben werden.
  Die Options werden in der [Dokumentation](docs/docs_options.md "Options Dokumentation") erläutert.