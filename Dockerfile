FROM python:3.7-alpine

RUN apk add --no-cache -X http://dl-cdn.alpinelinux.org/alpine/edge/main redis=5.0.4-r0

ADD . /code
WORKDIR /code

RUN pip install -r requirements.txt
CMD redis-server & python app.py
