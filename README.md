# PULLBIN

[![Python 3+](https://img.shields.io/badge/python-3+-blue.svg)](https://www.python.org/download/releases/3.0/)

pullbin is a script for downloading artifacts from Pastebin or Ghostbin.

- __[Features](#features)__
- __[Usage](#usage)__
    - __[Interactive](#interactive)__
    - __[Command Line](#cli)__
    - __[API](#api)__
        - __[Tests](#tests)__
        - __[Persistence](#persistence)__

## <a name="features"></a>Features

It is possible to use pullbin in three modes:

- interactive
- command line
- API

## <a name="usage"></a>Usage

nomenclature:

    Key - for set endpoint of URL on domains (i.e: https://pastebin.com/<KEY> or https://ghostbin.co/paste/<KEY>)
    Domain - is the pastebin or ghostbin [default=pastebin]
    Path - is the path for write artifact - API mode not support this feature
    Filename - for set file name [default=<KEY>]

### <a name="interactive"></a>Interactive

For this mode just run the command below and input data

    python3 main.py

### <a name="cli"></a>Command Line

    python3 main.py -k <KEY>

For more information, run:

    python3 main.py -h

### <a name="api"></a>API

For this mode, its possible using Docker or in CLI.

In docker mode, your required docker and docker-compose installed.

    docker-compose up --build -d

In CLI mode, your required pip installed.

    pip3 install -r requirements.txt
    gunicorn -w 4 -b 0.0.0.0:8080 wsgi:app

#### <a name="tests"></a>Test

for test the api, just run:

    curl -XPOST -H 'Content-Type: application/json' --data '{"key": "<KEY>"}' <HOST>:8080

#### <a name="persistence"></a>Persistence

For docker mode, all data is write in folder /data.

section of docker compose:

    volumes:
        - ./data:/data
