FROM python:3.8-slim-bullseye

ARG MODEL_ID="18aUSp1UYW5vVXbwZlVrRJHchuB7uvKxj"

RUN apt-get update && \
    apt-get install -y git wget

RUN git clone https://github.com/mrsmrynk/adois --depth 1 && \
    python -m pip install -r /adois/requirements.txt --ignore-installed --no-warn-script-location --upgrade

RUN wget --load-cookies /tmp/cookies.txt \
    "https://drive.google.com/uc?export=download&confirm=$( \
        wget --quiet --save-cookies /tmp/cookies.txt \
        --keep-session-cookies --no-check-certificate \
        'https://drive.google.com/uc?export=download&id=${MODEL_ID}' \
        -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p' \
    )&id=${MODEL_ID}" \
    -O /adois/data/model/model.onnx && \
    rm -rf /tmp/cookies.txt

WORKDIR /adois

ENV PYTHONPATH "${PYTHONPATH}:/adois"
ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python", "/adois/src/main.py", "/config.yaml"]