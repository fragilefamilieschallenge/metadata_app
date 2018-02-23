#!/usr/bin/env python

from flask import Flask

application = Flask(__name__)

@application.route('/')
def index():
    return "Hello, world!"


# Execute app directly when invoked
if __name__ == "__main__":
    application.run(host="0.0.0.0")
