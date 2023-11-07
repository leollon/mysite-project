FROM postgres:9.6-alpine

ENV INIT_DIR docker-entrypoint-initdb.d

RUN mkdir -p ${INIT_DIR}

COPY ./compose/local/postgres/init-db.sh ${INIT_DIR}

RUN chmod +x ${INIT_DIR}/init-db.sh
