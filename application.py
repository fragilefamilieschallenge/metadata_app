#!/usr/bin/env python
# Application logic for FFCWS metadata browser.
# Author: Alex Kindel
# Last modified: 23 February 2018

import os
import re
import datetime
import random
from csv import DictReader, DictWriter
from collections import OrderedDict, Counter

from flask import Flask, render_template, url_for, request, send_from_directory, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_basicauth import BasicAuth

# Build app instance
application = Flask(__name__)

# Configure application
application.config.from_envvar('APP_CONFIG', silent=True)
db = SQLAlchemy(application)
auth = BasicAuth(application)


# Define data models
class Variable(db.Model):
    __tablename__ = "variable"

    # Define table fields
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    label = db.Column(db.Text)
    old_name = db.Column(db.Text)
    data_type = db.Column(db.Text)
    warning = db.Column(db.Integer)
    group_id = db.Column(db.Text)
    group_subid = db.Column(db.Text)
    data_source = db.Column(db.Text)
    respondent = db.Column(db.Text)
    wave = db.Column(db.Text)
    scope = db.Column(db.Text)
    section = db.Column(db.Text)
    leaf = db.Column(db.Text)

    def __init__(self, name, label, old_name, data_type, warning, group_id, group_subid, data_source, respondent, wave, scope, section, leaf):
        self.name = name
        self.label = label
        self.old_name = old_name
        self.data_type = data_type
        self.warning = warning
        self.group_id = group_id
        self.group_subid = group_subid
        self.data_source = data_source
        self.respondent = respondent
        self.wave = wave
        self.scope = scope
        self.section = section
        self.leaf = leaf

    def __repr__(self):
        return "<Variable %r>" % self.name

class Topic(db.Model):
    __tablename__ = "topic"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    topic = db.Column(db.Text)

    def __init__(self, name, topic):
        self.name = name
        self.topic = topic

    def __repr__(self):
        return "<Topic %r>" % self.topic

class Umbrella(db.Model):
    __tablename__ = "umbrella"

    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.Text)
    umbrella = db.Column(db.Text)

    def __init__(self, topic, umbrella):
        self.topic = topic
        self.umbrella = umbrella

    def __repr__(self):
        return "<Umbrella %r>" % self.umbrela

class Response(db.Model):
    __tablename__ = "response"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    label = db.Column(db.Text)
    value = db.Column(db.Integer)

    def __init__(self, name, label, value):
        self.name = name
        self.label = label
        self.value = value

    def __repr__(self):
        return "<Response %r>" % self.label

class Group(db.Model):
    __tablename__ = "group"

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Text)
    count = db.Column(db.Integer)

    def __init__(self, group_id, count):
        self.group_id = group_id
        self.count = count

    def __repr__(self):
        return "<Group %r>" % self.group_id

## Adminstration views ##

# Build database schema, if needed
@application.route('/admin/build')
@auth.required
def build_db():
    '''Construct database tables on the specified database.'''
    db.create_all()
    return "Rebuilt database tables."

# Load metadata to database
# TODO: Update to use new metadata file
# TODO: Test group table build
@application.route('/admin/load')
@auth.required
def load_db():
    '''Load metadata to the specified database.'''
    with open(application.config["METADATA_FILE"]) as t:
        rows = list(DictReader(t))
        vars_loaded = 0
        commit_increment = 1000
        group_ids = []
        umbrella_topics = set()
        for row in rows:
            # Determine group membership
            group_no = None
            group_sub = None
            groupclass = re.search("[A-z]+", str(row["group"]))
            if not groupclass:
                group_no = str(row["group"])
            else:
                group_sub = re.search("[A-z]+", str(row["group"])).group(0)
                group_no = str(row["group"]).replace(group_sub, "")

            # Write variable data
            var = Variable(name=row["new_name"],
                           label=row["varlab"].replace('"', "'"),
                           old_name=row["old_name"],
                           data_type=row["type"],
                           warning=int(row["warning"]),
                           group_id=group_no,
                           group_subid=group_sub,
                           data_source=row["source"],
                           respondent=row["respondent"],
                           wave=str(row["wave"]),
                           scope=str(row["scope"]),
                           section=row.get("section"),
                           leaf=str(row["leaf"]))
            db.session.add(var)

            # Write topic data
            # Also, save umbrella data (we add this table later)
            topic1 = Topic(name=row["new_name"], topic=row["topic1"])
            db.session.add(topic1)
            umbrella_topics.add((row["topic1"], row["umbrella1"]))
            if len(row["topic2"]) > 0:
                # Some rows have multiple topics (up to 2)
                topic2 = Topic(name=row["new_name"], topic=row["topic2"])
                db.session.add(topic2)
                umbrella_topics.add((row["topic2"], row["umbrella2"]))

            # Write response data
            for key in row.keys():
                if key.find("label") > -1 and len(row[key]) > 0:
                    # Clean up response label
                    respidx = key.replace("label", "")
                    try:
                        lab_pts = row[key].split(" ", 1)
                        lab_pref = lab_pts[0]
                        val = row["value" + respidx]
                        if lab_pref == val:
                            lab = lab_pts[1]  # Drop the prefix if it's the response value
                        else:
                            lab = row[key]
                    except IndexError:
                        lab = row[key]  # Default to the full entry if we can't clean up

                    # Append new response row
                    resp = Response(name=row["new_name"], label=lab, value=row["value" + respidx])
                    db.session.add(resp)

            # Add to group list
            group_ids.append(str(row["group"]))

            # Increment variable counter
            vars_loaded += 1

            # Commit in increments of k
            if vars_loaded % commit_increment == 0:
                db.session.commit()

        # Commit any remaining rows
        db.session.commit()

        # Build groups table
        # TODO: The groups quality is bad -- revisit this tomorrow
        groups = Counter(group_ids)
        for group_id, group_n in groups.items():
            grp = Group(group_id=group_id, count=group_n)
            db.session.add(grp)
        db.session.commit()

        # Build umbrellas table
        for topic, umbrella in umbrella_topics:
            umb = Umbrella(topic=topic, umbrella=umbrella)
            db.session.add(umb)
        db.session.commit()

    # Yield result
    return "Loaded {} rows to database.".format(str(vars_loaded))


## User views ##

# Define valid search filters
# This object determines what filter groups show up in the search view
filter_labels = OrderedDict([("wave", "Wave"),
                             ("respondent", "Respondent"),
                             ("data_source", "Source"),
                             ("scope", "City scope"),
                             ("data_type", "Variable type")])

# Define domain-label map for each filter
# This defines what values are valid to filter on for each filter group
valid_filters = {"wave": OrderedDict([("1", "Baseline"),
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
                 "scope": OrderedDict([("2", "2 cities"),
                                      ("15", "15 cities"),
                                      ("16", "16 cities"),
                                      ("18", "18 cities"),
                                      ("20", "20 cities")]),
                 "data_type": OrderedDict([("bin", "Binary"),
                                          ("uc", "Unordered categorical"),
                                          ("oc", "Ordered categorical"),
                                          ("cont", "Continuous"),
                                          ("string", "String"),
                                          ("id", "ID number")])}

@application.route('/variables', methods=['GET', 'POST'])
def search():
    results = None
    rnames = None
    constraints = None
    search_query = None
    if request.method == "POST":
        qobj = Variable.query

        # Filter by search query
        search_query = request.form["variable-search"]
        if len(search_query) > 0:
            qobj = qobj.filter(Variable.label.like('%%{}%%'.format(search_query)))
            # TODO: Should this search other fields?

        # Filter by fields
        constraints = dict()
        for field in set(valid_filters.keys()).intersection(request.form.keys()):
            domain = request.form.getlist(field)
            filt = "Variable.{}.in_(domain)".format(field)
            qobj = qobj.filter(eval(filt))
            constraints[field] = request.form.getlist(field)

        # Get all matches
        results = qobj.all()
        r2 = results

        # TODO: Maybe zero results should return something different from the blank search page
        # Can handle this with a yes/no flag?

        # Return variable names separately
        rnames = []
        for result in r2:
            rnames.append(str(unicode(result.name)))

        # Log query
        # TODO
    else:
        # Log that we're starting a new search
        # TODO
        pass

    return render_template('search.html', results=results, rnames=rnames, constraints=constraints,
                           search_query=search_query, filtermeta=valid_filters, filterlabs=filter_labels)

@application.route('/variables/<varname>')
def var_page(varname):
    if not varname:
        # Abort early if Flask tries to load this page with no variable
        return redirect(url_for('search'))
    else:
        # Get variable data
        var_data = Variable.query.filter(Variable.name == varname).first()

        # Grouped variables
        neighbors = Variable.query.filter(Variable.group_id == var_data.group_id).all()

        # Responses
        responses = Response.query.filter(Response.name == varname).group_by(Response.label).all()
        if responses:
            responses = sorted(responses, key=lambda x: int(x.value), reverse=True)

        # Topic
        topics = Topic.query.filter(Topic.name == varname).group_by(Topic.topic).all()

        # Umbrellas
        umbrellas = Umbrella.query.filter(Umbrella.topic.in_([str(t.topic) for t in topics])).all()

        # Log query
        # TODO

        # Render page
        return render_template('variable.html', var_data=var_data, neighbors=neighbors,
                               responses=responses, umbrellas=umbrellas, filtermeta=valid_filters, filterlabs=filter_labels)


## Static pages ##

# Favicon
@application.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(application.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

# Full metadata file download
@application.route('/get_metadata')
def metadata():
    return send_file(application.config["METADATA_FILE"], as_attachment=True),

@application.route("/feedback")
def feedback():
    return render_template('feedback.html')

# Main page
@application.route('/')
def index():
    return render_template('index.html')


# Execute app directly when invoked
if __name__ == "__main__":
    application.run(host="0.0.0.0")
