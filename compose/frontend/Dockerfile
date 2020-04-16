FROM node:10.15.3-alpine

LABEL Name=mysite/frontend Version=1.0.0

ENV NEXT_TELEMETRY_DEBUG 1
ENV NEXT_TELEMETRY_DISABLED 1

RUN apk add --no-cache \
        -X https://mirrors.ustc.edu.cn/alpine/v$(cat /etc/issue | tr -d '[a-zA-Z\(\)\ \\\n]')/main \
        # for the dependency of gulp-imagemin package
        build-base libtool automake autoconf zlib-dev libpng-dev libjpeg-turbo-dev

# For the sake of time and the Great Fucking Wall,
# I Have to set npm registry mirror
RUN npm config set registry http://mirrors.cloud.tencent.com/npm/

# create frontend code directory
RUN mkdir /frontend

# copy start and entrypoint script
COPY ./compose/frontend/ /

# copy frontend code
COPY ./frontend /frontend

# change permissions
RUN chmod +x /entrypoint /start

# User run the following instrucstions, only for RUN, CMD and ENTRYPOINT
WORKDIR /frontend
RUN npm install
