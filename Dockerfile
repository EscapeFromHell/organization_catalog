FROM python:3.12

RUN apt-get update \
    && apt-get install -y python3-dev build-essential libssl-dev libffi-dev \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip setuptools

RUN mkdir /src

COPY ./ /src

WORKDIR /src

RUN python -m pip install --upgrade pip \
    && python -m pip install --no-cache-dir poetry==1.4.2 \
    && poetry config virtualenvs.create false \
    && poetry install --without dev,test --no-interaction --no-ansi \
    && rm -rf $(poetry config cache-dir)/{cache,artifacts}

ENV PYTHONPATH=/src
