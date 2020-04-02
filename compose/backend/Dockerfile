FROM python:3.7-alpine

LABEL Name=mysite/backend Version=1.0.0

ENV PYTHONUNBUFFERED 1

RUN apk add --no-cache \
        -X https://mirrors.ustc.edu.cn/alpine/v$(cat /etc/issue | tr -d '[a-zA-Z\(\)\ \\\n]')/main \
        # build base
        gcc libc-dev \
        # postgresql client dependency
        postgresql-dev \
        # cffi dependecies
        python3-dev libffi-dev \
        # pillow dependency
        jpeg-dev zlib-dev freetype-dev \
        lcms2-dev openjpeg-dev harfbuzz-dev \
        fribidi-dev \
        # shell to used
        bash

RUN rm -rf \
        /usr/local/share/doc \
        /usr/local/share/man \
    && find /usr/local -name '*.a' -delete

# Start building backend image
RUN adduser -s /bin/bash -DH blog
RUN echo 'blog ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
RUN echo 'blog:local' | chpasswd

COPY ./compose/backend/ /
COPY ./requirements.txt /

RUN pip install -r requirements.txt -i https://pypi.douban.com/simple \
    && rm -f requirements.txt
RUN mkdir /backend

WORKDIR /backend

COPY backend/apps       apps
COPY backend/templates  templates
COPY backend/static     static
COPY backend/backend    backend
COPY backend/manage.py  manage.py

RUN chmod 755 -R /entrypoint /start /backend
RUN chown -R blog:blog /entrypoint /start /backend

USER blog:blog

RUN mkdir -p var/log data run
RUN touch var/log/backend.log
