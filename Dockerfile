###################
#
# Docker build and run command instruction:
# 1. To build an image:
#    docker build -t cbbb-app:latest .
#
# 2. To launch a container:
#    docker run -dit -p 5000:5000 cbbb-app
#
#
#
# (Tips:) 1. docker exec -it 7ce7653e3774 /bin/sh
#         2. docker image ls
#         3. docker ps -a
#         4. Host_IP should be set to 0.0.0.0. 127.0.0.1 doesn't work for unknown
#            reason
###################


FROM python:3.6-alpine

ENV PYTHONUNBUFFERED 1

RUN apk update
RUN apk upgrade
RUN apk add --update --no-cache --virtual .tmp-build-deps \
		musl-dev \
        gcc


COPY requirements/ requirements/
RUN pip install -r requirements/base.txt

RUN mkdir /dockerApp
COPY . dockerApp
WORKDIR /dockerApp

CMD python application.py && tail -f /dev/null
