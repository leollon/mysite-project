FROM node:10.15.3-alpine

LABEL Name=mysite/frontend Version=1.0.0

RUN apk add --no-cache \
        -X https://mirrors.ustc.edu.cn/alpine/v$(cat /etc/issue | tr -d '[a-zA-Z\(\)\ \\\n]')/main \
        build-base libtool automake autoconf nasm zlib-dev

RUN npm config set registry http://mirrors.cloud.tencent.com/npm/

RUN mkdir /frontend

# copy scripts
COPY ./compose/frontend/ /

# copy code
COPY ./frontend /frontend

# change permissions
RUN chmod +x /entrypoint /start
RUN chmod -R 755 /frontend


WORKDIR /frontend
RUN npm install
RUN npx next telemetry disable
