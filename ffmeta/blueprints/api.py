import datetime
import os.path
import uuid

from flask import Blueprint, request, Response, jsonify, make_response, send_file, redirect, url_for, current_app

from ffmeta.models.db import session
from ffmeta.models import Response, Variable
from ffmeta.utils import api_error, epochalypse_now, dedupe_varlist, search_db
from ffmeta.blueprints.api2 import variable_details

bp = Blueprint('api', __name__)


@bp.route("/select")
def selectMetadata():
    # Get request data
    varname = request.args.get("varName")
    fieldname = request.args.get('fieldName', default=None)

    # Error out if varname not provided
    if not varname:
        return api_error(400, "Variable name not provided.")

    # Get variable data (abort if not valid)
    var = session.query(Variable).filter(Variable.name == varname).first()
    if not var:
        return api_error(400, "Invalid variable name.")
    var_data = variable_details(var)

    topics = []
    if var.subtopic1 is not None:
        topics.append({"umbrella": var.topic1, "topic": var.subtopic1})
    if var.subtopic2 is not None:
        topics.append({"umbrella": var.topic2, "topic": var.subtopic2})
    var_data["topics"] = topics

    # Append responses
    responses = session.query(Response).filter(Response.name == varname).group_by(Response.label).all()
    var_data["responses"] = {value: label for (value, label) in [(r.value, r.label) for r in responses]}

    # Error out if field name not valid
    if fieldname and fieldname not in var_data.keys():
        return api_error(400, "Invalid field name.")

    # Return only a single field if specified
    if not fieldname:
        rv = jsonify(var_data)
    else:
        result = {fieldname: var_data[fieldname]}
        rv = jsonify(result)

    resp = make_response(rv)

    return resp


@bp.route("/filter")
def filterMetadata():
    # Get request data
    fields = request.args.keys()

    # Error out if no fields provided
    if not fields:
        return api_error(400, "Fields to search not provided.")

    # Construct filter object
    found = []
    for field in fields:
        for value in request.args.getlist(field):
            found.extend(search_db(field, value))

    # Log query
    current_app.logger.info("{}\t{}\tfilterMetadata\tfilters: {}".format(epochalypse_now(), request.cookies.get("user_id"), list(request.args.items())))

    # Return list of matches
    if not found:
        rv = jsonify({"matches": []})
    else:
        varlist = dedupe_varlist(found)
        rv = jsonify({"matches": varlist})

    resp = make_response(rv)
    return resp


@bp.route("/search")
def searchMetadata():
    # Get request data
    querystr = request.args.get("query")
    fieldname = request.args.get('fieldName', default=None)

    # Error out if query or field not provided
    if not querystr:
        return api_error(400, "Query string not specified.")
    if not fieldname:
        return api_error(400, "Field name to search not specified.")

    # Search by table
    matches = search_db(fieldname, querystr)

    # Log query
    current_app.logger.info("{}\t{}\tsearchMetadata\tquery: {}\tfieldname: {}".format(epochalypse_now(), request.cookies.get("user_id"), querystr, fieldname))

    # Yield a list of variable names
    if not matches:
        rv = jsonify({"matches": []})
    else:
        rv = jsonify({"matches": matches})

    resp = make_response(rv)

    return resp


# Static pages #

@bp.route("/")
def index():
    return redirect(url_for('web.api'))


# Full metadata file download
@bp.route('/get_metadata')
def metadata():
    # Log query
    current_app.logger.info("{}\t{}\tfull-file-download".format(epochalypse_now(), request.cookies.get("user_id")))
    return send_file(current_app.config["METADATA_FILE"], as_attachment=True)