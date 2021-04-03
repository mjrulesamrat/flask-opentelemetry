__author__ = "Jay Modi"

import os
import requests

from flask import Flask
from flask_restful import Resource, Api
from dotenv import load_dotenv

from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    SimpleSpanProcessor,
)

load_dotenv()  # take environment variables from .env

# set trace provider as default one
trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(
    SimpleSpanProcessor(ConsoleSpanExporter())
)

app = Flask(__name__)
api = Api(app)

FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()


class HelloWorld(Resource):
    def get(self):
        tracer = trace.get_tracer(__name__)
        with tracer.start_as_current_span("example-request"):
            requests.get("http://www.example.com")
            print("Hello World")
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')


if __name__ == "__main__":
    app.run(
        debug=os.getenv("DEBUG"),
        port=os.getenv("API_PORT")
    )
