###################
#
# Docker build and run command instruction:
# 1. To build an image:
#    docker build -t huxin-app:latest .    
#
# 2. To launch a container:
#    docker run -dit -p 5000:5000 huxin-app
#
#
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
