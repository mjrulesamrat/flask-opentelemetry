__author__ = "Jay Modi"

import os
import requests

from flask import Flask
from flask_restful import Resource as REST_Resource, Api
from dotenv import load_dotenv

from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    SimpleSpanProcessor,
    BatchSpanProcessor
)
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

load_dotenv()  # take environment variables from .env

# set trace provider as default one
trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({SERVICE_NAME: "my-helloworld-service"})
    )
)

# jaeger exporter
jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)

# add exporter to trace
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(jaeger_exporter)
)

app = Flask(__name__)
api = Api(app)

FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()


class HelloWorld(REST_Resource):
    def get(self):
        tracer = trace.get_tracer(__name__)
        with tracer.start_as_current_span("example-request"):
            requests.get("http://www.example.com")
        with tracer.start_as_current_span("get-oranges"):
            data = 100*100
            print("Hello World", data)
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')


if __name__ == "__main__":
    app.run(
        debug=os.getenv("DEBUG"),
        port=os.getenv("API_PORT")
    )
