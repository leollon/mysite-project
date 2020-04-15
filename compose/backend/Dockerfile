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

# remove man page and documentation
# for reducing image size
RUN rm -rf \
        /usr/local/share/doc \
        /usr/local/share/man \
    && find /usr/local -name '*.a' -delete

# Start building backend image

# create an normal user
RUN adduser -s /bin/bash -DH blog
RUN echo 'blog ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
RUN echo 'blog:producion' | chpasswd


# copy start and entrypoint script
COPY ./compose/backend/ /
# copy backend requirements
COPY ./requirements.txt /

RUN pip install --no-cache-dir -r requirements.txt \
    && rm -f requirements.txt

# code directory
RUN mkdir /backend

# current work directory for the following commands
WORKDIR /backend

# copy backend code
COPY backend/        ./

# change mode to rwxr-xr-x
RUN chmod 755 -R /entrypoint /start /backend
RUN chown -R blog:blog /entrypoint \
        /backend \
        /start \
        /uwsgi.ini

# change ownership, username:group name
RUN chown -R blog:blog /entrypoint /start /backend


# User run the following instrucstions, only for RUN, CMD and ENTRYPOINT
USER blog:blog

RUN echo "uid=blog" >> /uwsgi.ini && \
    echo "gid=blog" >> /uwsgi.ini && \
    echo "home=/usr/local"  >> /uwsgi.ini && \
    echo "chdir=/backend" >> /uwsgi.ini && \
    echo "pidfile=${PIDFILE}"  >> /uwsgi.ini

# prepare neccessary data directories,
# in case when starting backend, it occurrs some
# denied permissions.
RUN mkdir -p var/log data run assets

# create log for django running log
RUN touch var/log/backend.log
