FROM node:10.15.3-alpine

LABEL Name=mysite/frontend Version=1.0.0

RUN apk add --no-cache \
        -X https://mirrors.ustc.edu.cn/alpine/v$(cat /etc/issue | tr -d '[a-zA-Z\(\)\ \\\n]')/main \
        # for the dependency of gulp-imagemin package
        build-base libtool automake autoconf zlib-dev libpng-dev libjpeg-turbo-dev

# create frontend code directory
RUN mkdir /frontend

# copy start and entrypoint script
COPY ./compose/production/frontend/ /

# copy frontend code
COPY ./frontend /frontend

# change permissions
RUN chmod +x /entrypoint /start

# User run the following instrucstions, only for RUN, CMD and ENTRYPOINT
WORKDIR /frontend

RUN npm install && npx next telemetry disable
RUN npm run build
