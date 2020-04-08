FROM python:3.7-alpine

LABEL Name=mysite/backend Version=1.0.0

ENV PYTHONUNBUFFERED 1
ENV PIDFILE /backend/run/backend-manager.pid

RUN apk add --no-cache \
        # build base
        gcc linux-headers libc-dev \
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
RUN echo 'blog:producion' | chpasswd


COPY ./compose/backend/ /
COPY ./requirements.txt /

RUN pip install --no-cache-dir -r requirements.txt \
    && rm -f requirements.txt
RUN mkdir /backend

WORKDIR /backend

COPY backend/        ./

RUN chmod 755 -R /entrypoint /start /backend
RUN chown -R blog:blog /entrypoint \
        /backend \
        /start \
        /uwsgi.ini

USER blog:blog

RUN echo "uid=blog" >> /uwsgi.ini && \
    echo "gid=blog" >> /uwsgi.ini && \
    echo "home=/usr/local"  >> /uwsgi.ini && \
    echo "chdir=/backend" >> /uwsgi.ini && \
    echo "pidfile=${PIDFILE}"  >> /uwsgi.ini

RUN mkdir -p var/log data run
RUN touch var/log/backend.log
