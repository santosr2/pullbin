FROM python:alpine

RUN apk add --upgrade gcc make musl-dev
RUN mkdir -p /data /opt/pullbin

ENV DOCKERNIZED 1

WORKDIR /opt/pullbin

COPY . .

RUN pip install -r requirements.txt

CMD gunicorn -w 4 -b 0.0.0.0:8080 wsgi:app