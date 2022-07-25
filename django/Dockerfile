FROM python:3.8-slim-buster

RUN set -ex \
    && buildDeps='gcc libbz2-dev libc6-dev libgdbm-dev liblzma-dev libncurses-dev libreadline-dev libsqlite3-dev libssl-dev libpcre3-dev make tcl-dev tk-dev wget xz-utils zlib1g-dev default-libmysqlclient-dev inotify-tools procps' \
    && deps='libexpat1' \
    && apt update && apt install -y awscli && apt install -y $buildDeps $deps --no-install-recommends && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip && pip install pipenv

COPY ./django/Pipfile /usr/src/app/Pipfile
COPY ./django /usr/src/app

RUN pipenv install --system
RUN if [ "${APP_ENV}" = "dev" ]; then \
    pipenv install --dev --system; \
    fi