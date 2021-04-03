__author__ = "Jay Modi"

import os
import requests

from flask import Flask
from flask_restful import Resource, Api
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')


if __name__ == "__main__":
    app.run(
        debug=os.getenv("DEBUG"),
        port=os.getenv("API_PORT")
    )
