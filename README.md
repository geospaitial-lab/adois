<!-- @author: Maryniak, Marius - Fachbereich Elektrotechnik, Westfälische Hochschule Gelsenkirchen -->

![adois](data/images/adois_logo_light_mode.svg#gh-light-mode-only)
![adois](data/images/adois_logo_dark_mode.svg#gh-dark-mode-only)

---

[![Tests](https://github.com/KLIMA-WH/adois_app/actions/workflows/tests.yaml/badge.svg)](https://github.com/KLIMA-WH/adois_app/actions/workflows/tests.yaml)
[![Build and deploy](https://github.com/KLIMA-WH/adois_app/actions/workflows/build_and_deploy.yaml/badge.svg)](https://github.com/KLIMA-WH/adois_app/actions/workflows/build_and_deploy.yaml)

# Installation

Installieren Sie zunächst [Docker](https://www.docker.com/products/docker-desktop "Get Docker").  
Laden Sie anschließend das *adois* Image herunter.

```shell
docker pull ghcr.io/klima-wh/adois
```

***Hinweis:*** Das Parent Image ist das [python:3.8](https://hub.docker.com/_/python "Docker Hub - Python") Image.
Die entsprechenden Lizenzbedingungen sind [hier](https://hub.docker.com/_/python "Docker Hub - Python") zu entnehmen.

<details>
<summary>Alternative Installationsmöglichkeiten</summary>

## Docker Build From Source

Laden Sie zunächst das *adois* Repository in ein beliebiges Arbeitsverzeichnis herunter.

```shell
git clone https://github.com/klima-wh/adois
```

Wechseln Sie in das Verzeichnis und erstellen Sie anschließend das *adois* Image.

```shell
docker build -t adois .
```

## Virtual Environment

Installieren Sie zunächst [Python 3.8](https://www.python.org/downloads "Get Python").  
Laden Sie anschließend das adois Repository in ein beliebiges Arbeitsverzeichnis herunter.

```shell
git clone https://github.com/klima-wh/adois
```

Wechseln Sie in das Verzeichnis und erstellen Sie nun eine Virtual Environment.

```shell
python3 -m venv venv
```

Aktivieren Sie die Virtual Environment.  
**Mac/ Linux:**

```shell
source venv/bin/activate
```

**Windows:**

```shell
venv\Scripts\activate.bat
```

Installieren Sie die Packages.

```shell
pip install -r requirements.txt
```

</details>