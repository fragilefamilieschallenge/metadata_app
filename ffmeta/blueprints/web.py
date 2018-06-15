import os
import re
import datetime
import random
import logging
import uuid
from logging.handlers import RotatingFileHandler
from csv import DictReader, DictWriter
from collections import OrderedDict, Counter

from flask import Flask, Blueprint, render_template, url_for, request, send_from_directory, send_file, make_response, current_app, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_basicauth import BasicAuth

from ffmeta.models import Response, Variable, Umbrella, Topic
from ffmeta.models.db import session
from ffmeta.utils import epochalypse_now


bp = Blueprint('web', __name__)
# auth = BasicAuth(current_app)

##########################


## User views ##

# Define valid search filters
# This object determines what filter groups show up in the search view
filter_labels = OrderedDict([("topic", "Topic"),
                             ("wave", "Wave"),
                             ("respondent", "Respondent"),
                             ("data_source", "Source"),
                             ("data_type", "Variable type")])

# Define domain-label map for each filter
# This defines what values are valid to filter on for each filter group
valid_filters = {"topic": OrderedDict([("Attitudes and expectations", "Attitudes and expectations"),
                                      ("Childcare", "Childcare"),
                                      ("Cognitive and behavioral development", "Cognitive and behavioral development"),
                                      ("Community", "Community"),
                                      ("Demographics", "Demographics"),
                                      ("Education and school", "Education and school"),
                                      ("Employment", "Employment"),
                                      ("Family and social support", "Family and social support"),
                                      ("Finances", "Finances"),
                                      ("Health and health behavior", "Health and health behavior"),
                                      ("Home and housing", "Home and housing"),
                                      ("Legal system", "Legal system"),
                                      ("Paradata and weights", "Paradata and weights"),
                                      ("Parental relationships", "Parental relationships"),
                                      ("Parenting", "Parenting")]),
                 "wave": OrderedDict([("1", "Baseline"),
                                     ("2", "Year 1"),
                                     ("3", "Year 3"),
                                     ("4", "Year 5"),
                                     ("5", "Year 9"),
                                     ("6", "Year 15")]),
                 "respondent": OrderedDict([("k", "Child"),
                                           ("f", "Father"),
                                           ("m", "Mother"),
                                           ("q", "Couple"),
                                           ("t", "Teacher"),
                                           ("p", "Primary caregiver"),
                                           ("n", "Non-parental primary caregiver"),
                                           ("d", "Child care center (survey)"),
                                           ("e", "Child care center (observation)"),
                                           ("h", "In-home (survey)"),
                                           ("o", "In-home (observation)"),
                                           ("r", "Family care (survey)"),
                                           ("s", "Family care (observation)"),
                                           ("u", "Post child and family care observation")]),
                 "data_source": OrderedDict([("questionnaire", "Questionnaire"),
                                            ("constructed", "Constructed"),
                                            ("weight", "Survey weight"),
                                            ("idnum", "ID number")]),
                 "data_type": OrderedDict([("bin", "Binary"),
                                          ("uc", "Unordered categorical"),
                                          ("oc", "Ordered categorical"),
                                          ("cont", "Continuous"),
                                          ("string", "String"),
                                          ("id", "ID number")])}

@bp.route('/variables', methods=['GET', 'POST'])
def search():
    # Set cookie data if not found
    if not request.cookies.get("user_id"):
        expire_date = datetime.datetime.now() + datetime.timedelta(days=90)
        g_uuid = str(uuid.uuid4())
        resp.set_cookie("user_id", g_uuid, expires=expire_date)

    # Build data objects
    results = None
    rnames = None
    constraints = None
    search_query = None
    topics = None
    zero_found = False
    if request.method == "POST":
        qobj = session.query(Variable)

        # Filter by search query
        search_query = request.form["variable-search"]
        if len(search_query) > 0:
            qobj = qobj.filter(Variable.label.like('%%{}%%'.format(search_query)) | Variable.name.like('%%{}%%'.format(search_query)))
            # TODO: Should this search other fields?

        # Filter by fields
        constraints = dict()
        for field in set(valid_filters.keys()).intersection(request.form.keys()):
            if field == "topic":
                # Get list of names in provided umbrellas
                # XXX: This works but could be much cleaner (also I think this query is expensive)
                ulist = str([str(x) for x in request.form.getlist(field)]).strip("[]")
                vquery = "SELECT DISTINCT `name` \
                          FROM topic LEFT JOIN umbrella \
                          ON topic.topic = umbrella.topic \
                          WHERE umbrella IN ({})".format(ulist)
                vnames = [v["name"] for v in session.execute(vquery).fetchall()]

                # Filter by name list
                qobj = qobj.filter(Variable.name.in_(vnames))
            else:
                # Filter by metadata field in variables table
                domain = request.form.getlist(field)
                filt = "Variable.{}.in_(domain)".format(field)
                qobj = qobj.filter(eval(filt))
            constraints[field] = request.form.getlist(field)

        # Get all unique matches
        results = qobj.group_by(Variable.name).all()
        r2 = results

        # Determine variable names
        rnames = []
        for result in r2:
            rnames.append(str(result.name))

        if len(rnames) == 0:
            zero_found = True

        # Get topic data
        tdat = session.query(Topic).filter(Topic.name.in_(rnames)).group_by(Topic.topic, Topic.name).all()
        topics = {}
        for t in tdat:
            if t.name in topics.keys():
                topics[t.name] = "{}, {}".format(topics[t.name], t.topic)
            else:
                topics[t.name] = t.topic

        # Log query
        current_app.logger.info("[{}] {} searched with filters {}".format(epochalypse_now(), request.cookies.get("user_id"), constraints.items(), str(rnames)))
    else:
        # Log that we're starting a new search
        current_app.logger.info("[{}] {} started new search.".format(epochalypse_now(), request.cookies.get("user_id")))

    return render_template('web/search.html', results=results, rnames=rnames, constraints=constraints, topics=topics,
                           search_query=search_query, filtermeta=valid_filters, filterlabs=filter_labels, zero_found=zero_found)

@bp.route('/variables/<varname>')
def var_page(varname):
    # Set cookie data if not found
    if not request.cookies.get("user_id"):
        expire_date = datetime.datetime.now() + datetime.timedelta(days=90)
        g_uuid = str(uuid.uuid4())
        resp.set_cookie("user_id", g_uuid, expires=expire_date)

    if not varname:
        # Abort early if Flask tries to load this page with no variable
        return redirect(url_for('search'))
    else:
        # Get variable data
        var_data = session.query(Variable).filter(Variable.name == varname).first()

        # Grouped variables + topic membership
        neighbors = session.query(Variable).filter(Variable.group_id == var_data.group_id).all()
        neighbor_names = [n.name for n in neighbors]
        neighbor_tdat = session.query(Topic).filter(Topic.name.in_(neighbor_names)).group_by(Topic.topic, Topic.name).all()
        neighbor_topics = {}
        for t in neighbor_tdat:
            if t.name in neighbor_topics.keys():
                neighbor_topics[t.name] = "{}, {}".format(neighbor_topics[t.name], t.topic)
            else:
                neighbor_topics[t.name] = t.topic

        # Responses
        responses = session.query(Response).filter(Response.name == varname).group_by(Response.label).all()
        if responses:
            responses = sorted(responses, key=lambda x: int(x.value), reverse=True)

        # Umbrella data
        topics = session.query(Topic).filter(Topic.name == varname).group_by(Topic.topic).all()
        umbrellas = session.query(Umbrella).filter(Umbrella.topic.in_([str(t.topic) for t in topics])).all()

        # Log query
        current_app.logger.info("[{}] {} viewed variable: {}".format(epochalypse_now(), request.cookies.get("user_id"), varname))

        # Render page
        return render_template('web/variable.html', var_data=var_data, neighbors=neighbors, neighbor_topics=neighbor_topics,
                               responses=responses, umbrellas=umbrellas, filtermeta=valid_filters, filterlabs=filter_labels)


## Static pages ##

# Favicon
@bp.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(current_app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

# Full metadata file download
@bp.route('/get_metadata')
def metadata():
    # Log query
    current_app.logger.info("[{}] {} downloaded raw file.".format(epochalypse_now(), request.cookies.get("user_id")))
    return send_file(os.path.join(current_app.root_path, current_app.config["METADATA_FILE"]), as_attachment=True)

@bp.route("/feedback")
def feedback():
    return render_template('web/feedback.html')

# About Page
@bp.route('/about')
def about():
    resp = make_response(render_template('web/about.html'))

    # Set cookie data if not found
    if not request.cookies.get('user_id'):
        expire_date = datetime.datetime.now() + datetime.timedelta(days=90)
        g_uuid = str(uuid.uuid4())

    # Log query
    current_app.logger.info("[{}] {} looked at the about page.".format(epochalypse_now(), request.cookies.get('user_id')))

    # Render about page

    return resp

# Main page
# Also, set a unique ID for this user
@bp.route('/')
def index():
    resp = make_response(render_template('web/index.html'))

    # Set cookie data if not found
    if not request.cookies.get("user_id"):
        expire_date = datetime.datetime.now() + datetime.timedelta(days=90)
        g_uuid = str(uuid.uuid4())
        resp.set_cookie("user_id", g_uuid, expires=expire_date)

    # Log query
    current_app.logger.info("[{}] {} went home.".format(epochalypse_now(), request.cookies.get("user_id")))

    # Render index page
    return resp


