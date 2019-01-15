FROM python:3.6

LABEL Name=mysite Version=1.0.0

ENV PYTHONUNBUFFERED 1
ENV PIDFILE /mysite/mysite-manager.pid

RUN useradd -s /bin/bash -M blog
RUN echo 'blog ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
RUN echo 'blog:local' | chpasswd

COPY ./requirements.txt /
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.douban.com/simple && rm -f requirements.txt


COPY mysite /mysite
COPY ./compose/mysite/entrypoint \
    ./compose/mysite/start /


RUN chmod 755 -R /entrypoint /start /mysite
RUN chmod +x /entrypoint /start
RUN chown -R blog:blog /entrypoint \
    /start \
    /mysite

WORKDIR /mysite
USER blog:blog
RUN mkdir log data
RUN touch log/mysite.log
