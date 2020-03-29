"""
    Code is poetry

    Created by Nick aka black.dragon74
"""
from flask import (Flask, url_for, redirect)

# Create a new instance of the flask app
flaskAppInstance = Flask(__name__)


# Define the error handler
@flaskAppInstance.errorhandler(404)
def error(e):
    return redirect(url_for('home'))


# Register the error handler
flaskAppInstance.register_error_handler(404, error)

# Bundle all the errors into a single object
flaskAppInstance.config['BUNDLE_ERRORS'] = True

if __name__ == '__main__':

    # Call the initializer of the Api
    from api import *

    # Run the server
    flaskAppInstance.run(
        debug=True,
        port=8000,
        threaded=True
    )
