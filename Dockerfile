FROM python:alpine

COPY . .

ENV DOCKERNIZED 1

RUN apk add --upgrade gcc make musl-dev
RUN pip install -r requirements.txt
RUN mkdir -p /data

CMD gunicorn -w 4 -b 0.0.0.0:8080 wsgi:app