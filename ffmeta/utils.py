import datetime
from flask import jsonify

from ffmeta.models import Response, Variable
from ffmeta.models.db import session

# Datetime helper
epoch_base = datetime.datetime.utcfromtimestamp(0)


def epochalypse_now():
    return int((datetime.datetime.now() - epoch_base).total_seconds())


# Throw informative API errors as JSON
def api_error(code=None, description=None):
    # error = jsonify({"error code": code, "error_description": description})
    # return error
    raise AppException(status_code=code, message=description)


# Deduplicate a list
def dedupe_varlist(varlist):
    seen = set()
    seen_add = seen.add
    return [x for x in varlist if not (x in seen or seen_add(x))]


# Search database for variable names where field matches value at least partially
# Secretly, both filter and search use this functionality!
def search_db(field, value):
    if field == "umbrella":
        matches = session.query(Variable).filter(Variable.topics.like('%%{}%%'.format(value))).all()
    elif field == "topic":
        matches = session.query(Variable).filter(Variable.subtopics.like('%%{}%%'.format(value))).all()
    elif field == "responses":
        matches = session.query(Response).filter(Response.label.like('%%{}%%'.format(value))).all()
    else:
        # Throw out anything else that's not in Variable
        if field not in Variable.__table__.columns:
            return api_error(400, "Invalid field name.")

        # All other variable metadata is stored with the variables
        fieldobj = eval("Variable.{}".format(field))
        matches = session.query(Variable).filter(fieldobj.like('%%{}%%'.format(value))).all()

    # Return variable names found, deduplicated
    distinct = dedupe_varlist([m.name for m in matches])
    return distinct


# API Exceptions #
# http://flask.pocoo.org/docs/1.0/patterns/apierrors/ #
class AppException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

