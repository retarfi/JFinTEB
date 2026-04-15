FROM nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04 as base

### Install python 3.10 and set it as default python interpreter
RUN apt update && \
apt install curl python3.10 python3.10-venv python3.10-dev build-essential vim -y && \
update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1 && \
update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1 && \
curl -Ss https://bootstrap.pypa.io/get-pip.py | python3.10 && \
apt-get clean && rm -rf /var/lib/apt/lists/*

FROM base as build

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM base as runtime

WORKDIR /app

COPY --from=build /tmp/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir -r /code/requirements.txt
RUN python -m unidic download

# アプリケーションのコードをコピー
COPY src /app/src
COPY README.md /app/README.md
COPY ./pyproject.toml /app/
RUN pip install --no-cache-dir -e .
