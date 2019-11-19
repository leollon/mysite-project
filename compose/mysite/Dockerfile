FROM python:3.7-alpine

LABEL Name=mysite Version=1.0.0

ENV PYTHONUNBUFFERED 1

# To support compiling uwsgi
RUN apk add --no-cache \
        -X https://mirrors.ustc.edu.cn/alpine/v$(cat /etc/issue | tr -d '[a-zA-Z\(\)\ \\\n]')/main \
        gcc linux-headers libc-dev \
        mariadb-dev python3-dev libffi-dev openssl-dev \
        jpeg-dev zlib-dev \
        postgresql-dev \
        bash

RUN rm -rf \
        /usr/local/share/doc \
        /usr/local/share/man \
    && find /usr/local -name '*.a' -delete

# Start building mysite image
RUN adduser -s /bin/bash -DH blog
RUN echo 'blog ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
RUN echo 'blog:local' | chpasswd

COPY ./requirements.txt /
RUN pip install -r requirements.txt -i https://pypi.douban.com/simple && rm -f requirements.txt

RUN mkdir /mysite
WORKDIR /mysite

COPY mysite/apps       apps
COPY mysite/utils      utils
COPY mysite/templates  templates
COPY mysite/static     static
COPY mysite/mysite     mysite
COPY mysite/manage.py  manage.py

COPY ./compose/mysite/entrypoint ./compose/mysite/start /

RUN chmod 755 -R /entrypoint /start /mysite
RUN chown -R blog:blog /entrypoint /start /mysite

USER blog:blog

RUN mkdir -p var/log data run
RUN touch var/log/mysite.log
