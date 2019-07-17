FROM python:3.6

LABEL Name=mysite Version=1.0.0

ENV PYTHONUNBUFFERED 1

RUN useradd -s /bin/bash -M blog
RUN echo 'blog ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
RUN echo 'blog:local' | chpasswd

COPY ./requirements.txt /
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.douban.com/simple && rm -f requirements.txt

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
