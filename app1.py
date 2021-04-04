__author__ = "Jay Modi"

import os
import requests

from flask import Flask
from flask_restful import Resource as REST_Resource, Api
from dotenv import load_dotenv

# opentelemetry
from opentelemetry import trace
from opentelemetry.trace.status import StatusCode
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider

# flask and requests instrumentation
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

# exporters
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    SimpleSpanProcessor,
    BatchSpanProcessor
)
from opentelemetry.exporter.jaeger.thrift import JaegerExporter

# propagator
from opentelemetry.propagate import set_global_textmap
from opentelemetry.propagators.b3 import B3Format

load_dotenv()  # take environment variables from .env

# Set global propagator
set_global_textmap(B3Format())

# set trace provider as default one
trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({SERVICE_NAME: "my-other-service"})
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
    # SimpleSpanProcessor(ConsoleSpanExporter)
)

app = Flask(__name__)
api = Api(app)

FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()


class GetHelloWorld(REST_Resource):
    def get(self):
        tracer = trace.get_tracer(__name__)
        world = None
        with tracer.start_as_current_span("get-hello-request"):
            world = "World!"
        return {'hello': world}


api.add_resource(GetHelloWorld, '/get-hello')


if __name__ == "__main__":
    app.run(
        debug=os.getenv("DEBUG"),
        port=3000
    )
