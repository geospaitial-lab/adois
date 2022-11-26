<!-- @author: Maryniak, Marius - Fachbereich Elektrotechnik, Westfälische Hochschule Gelsenkirchen -->

![adois](data/images/adois_logo_light_mode.svg#gh-light-mode-only)
![adois](data/images/adois_logo_dark_mode.svg#gh-dark-mode-only)

---

[![Tests](https://github.com/KLIMA-WH/adois_app/actions/workflows/tests.yaml/badge.svg)](https://github.com/KLIMA-WH/adois_app/actions/workflows/tests.yaml)
[![Build and deploy](https://github.com/KLIMA-WH/adois_app/actions/workflows/build_and_deploy.yaml/badge.svg)](https://github.com/KLIMA-WH/adois_app/actions/workflows/build_and_deploy.yaml)

# Installation

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

Laden Sie zunächst das *adois* Repository in ein beliebiges Arbeitsverzeichnis herunter.

```
git clone https://github.com/klima-wh/adois
```

Wechseln Sie in das Verzeichnis und erstellen Sie anschließend das *adois* Image.

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

Um die Software auszuführen, müssen Sie lokale Pfade in den *adois* Container mounten.  
Verwenden Sie dazu die `-v` Flag und `</lokaler/Pfad>:</Pfad/im/Container>`.

```
docker run -t -v </Pfad/zu/config.yaml>:/config.yaml -v </Pfad/zu/Basisverzeichnis>:</Pfad/zu/Basisverzeichnis> adois
```