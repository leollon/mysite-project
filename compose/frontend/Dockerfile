FROM node:10.15.3-alpine

LABEL Name=backend/frontend Version=1.0.0

RUN mkdir /frontend
COPY ./compose/frontend/entrypoint ./compose/frontend/start /
COPY ./frontend /frontend

WORKDIR /frontend

RUN chmod +x /entrypoint /start
RUN chmod -R 755 /frontend
