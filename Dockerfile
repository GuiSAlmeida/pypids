# https://docs.docker.com/develop/develop-images/dockerfile_best-practices/

# https://hub.docker.com/layers/python/library/python/3/images/sha256-3ff3760e13a5d0ffef21e072a0b05025a0847be10de1ef218aa819a2ed0fd7b4
FROM python:3

LABEL maintainer="Guilherme Almeida <guisalmeida.com>"

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 5000

VOLUME /static

CMD python main.py