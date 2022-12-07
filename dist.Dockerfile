FROM python:3.8-slim-bullseye

RUN apt-get update && apt-get install -y git curl
RUN curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash
RUN apt-get install -y git-lfs
RUN git lfs install

RUN git clone https://github.com/mrsmrynk/adois --depth 1

RUN python -m pip install -r /adois/requirements.txt --ignore-installed --no-warn-script-location --upgrade

WORKDIR /adois

ENV PYTHONPATH "${PYTHONPATH}:/adois"
ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python", "/adois/src/main.py", "/config.yaml"]