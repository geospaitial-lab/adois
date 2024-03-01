FROM python:3.11-slim-bullseye

RUN apt-get update

COPY requirements_dev.txt .

RUN pip install --upgrade pip && \
    pip install --root-user-action ignore --upgrade -r requirements_dev.txt

WORKDIR /adois

ENV PYTHONPATH "${PYTHONPATH}:/adois"
ENV PYTHONUNBUFFERED 1