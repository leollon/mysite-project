FROM node:10.15.3-alpine AS node-alpine

LABEL Name=mysite/frontend Version=1.0.0

WORKDIR /

COPY ./frontend/package.json ./
RUN npm config set registry https://registry.npm.taobao.org
RUN npm install
RUN npx next telemetry disable

FROM node-alpine

RUN mkdir /frontend
COPY ./compose/frontend/entrypoint ./compose/frontend/start /
COPY ./frontend /frontend

RUN chmod +x /entrypoint /start
RUN chmod -R 755 /frontend

WORKDIR /frontend
