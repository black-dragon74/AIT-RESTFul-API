"""
    Code is poetry
"""
from flask_restful import Api
from app import flaskAppInstance

from .student import (
    Home,
    Attendance
)

# Create a RESTFul server wrapper around Flask app's instance
apiServer = Api(flaskAppInstance)

# Add API endpoints
apiServer.add_resource(Home, '/')
apiServer.add_resource(Attendance, '/attendance')
