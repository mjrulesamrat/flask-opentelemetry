# Flask Opentelemetry

Distributed HTTP request-response tracing with Opentelemetry.

# Project setup guidelines

Create Python Virtual environment and run projec locally.

- Create virtual environment

    ```bash
    python3.6 -m venv venv
    ```

- Install dependencies

    ```bash
    . venv/bin/active

    pip install -r requirements.txt
    ```

- Copy and Set environment variables

    ```bash
    cp sample.env .env
    ```

- Export flask application

    ```bash
    export FLASK_APP=app.py
    ```

- Run project locally

    ```bash
    flask run
    ```

## Jaeger setup guidelines

Run Jaeger container locally to collect tracing data from Flask application

```bash
docker run -p 16686:16686 -p 6831:6831/udp jaegertracing/all-in-one
```

## Features

*ToDo
