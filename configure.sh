#!/bin/bash

# Install dependencies
python setup.py install

# Export environment variables
source ~/.aws/ff_metadata
export FLASK_APP=wireframe.py
