"""
    Code is poetry
"""
from flask_restful import Resource


class Home(Resource):
    def get(self):
        return {
            "msg": "Welcome to AIT ERP REST API",
            "error": "No/Invalid route requested. Please refer to the documentation."
        }
