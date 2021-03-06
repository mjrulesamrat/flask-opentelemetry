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

- Fire up another console and run second flask service locally

    ```bash
    python app1.py
    ```

## Jaeger setup guidelines

Run Jaeger container locally to collect tracing data from Flask application

```bash
docker run -p 16686:16686 -p 6831:6831/udp jaegertracing/all-in-one
```

## Demo

Make sure you have Both Flask applications running and jaeger running.

- Make GET requests to below APIs

    ```
    localhost:5000/hello
    localhost:5000/zero
    localhost:5000/zero-unhandled
    localhost:5000/zero-trace
    ```

- Go to jaeger home page and select service `my-helloworld-service` to find trace

    ```
    http://localhost:16686/search
    ```

- Notice the number of spans for each request. We can add more spans to each
REST API for better detailed traces.

- With first request, we can notice that it calls internally second service. As
second service also have tracing enabled, we have more in-depth tracing information.
