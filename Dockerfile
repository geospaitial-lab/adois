FROM python:3.8-bullseye

RUN mkdir /adois

COPY requirements.txt /adois

RUN python -m pip install -r /adois/requirements.txt --ignore-installed --no-warn-script-location --upgrade

COPY . /adois
WORKDIR /adois

ENV PYTHONPATH "${PYTHONPATH}:/adois"
ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python", "/adois/src/main.py", "/config.yaml"]