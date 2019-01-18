FROM python:3.6

LABEL Name=mysite Version=1.0.0

ENV PYTHONUNBUFFERED 1
ENV PIDFILE /mysite/mysite-manager.pid

RUN useradd -s /bin/bash -M blog
RUN echo 'blog ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
RUN echo 'blog:producion' | chpasswd


COPY ./requirements.txt /
RUN pip install --no-cache-dir -r requirements.txt && rm -f requirements.txt

RUN mkdir /mysite
WORKDIR /mysite

COPY mysite/apps       apps
COPY mysite/utils      utils
COPY mysite/templates  templates
COPY mysite/static     static
COPY mysite/mysite     mysite
COPY mysite/manage.py  manage.py

COPY ./compose/mysite/entrypoint \
    ./compose/mysite/start \
    ./compose/mysite/uwsgi.ini /

RUN chmod 755 -R /entrypoint /start /mysite
RUN chown -R blog:blog /entrypoint \
    /mysite \
    /start \
    /uwsgi.ini

USER blog:blog
RUN mkdir log data
RUN touch log/mysite.log


RUN echo "uid=blog\ngid=blog\nhome=/usr/local\nchdir=/mysite\npidfile=$PIDFILE\n" \
    >> /uwsgi.ini

