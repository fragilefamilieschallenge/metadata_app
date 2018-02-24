#!/usr/bin/env python
# Application logic for FFCWS metadata browser.
# Author: Alex Kindel
# Last modified: 23 February 2018

from csv import DictReader

from flask import Flask, render_template, url_for, request
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
    data_source = db.Column(db.Text)
    respondent = db.Column(db.Text)
    wave = db.Column(db.Text)
    scope = db.Column(db.Text)
    section = db.Column(db.Text)
    leaf = db.Column(db.Text)

    def __init__(self, name, label, old_name, data_type, warning, group_id, data_source, respondent, wave, scope, section, leaf):
        self.name = name
        self.label = label
        self.old_name = old_name
        self.data_type = data_type
        self.warning = warning
        self.group_id = group_id
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

class Response(db.Model):
    __tablename__ = "response"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    label = db.Column(db.Text)

    def __init__(self, name, label):
        self.name = name
        self.label = label

    def __repr__(self):
        return "<Response %r>" % self.label


## Adminstration views ##

# Build database schema, if needed
@application.route('/admin/build')
@auth.required
def build_db():
    '''Construct database tables on the specified database.'''
    db.create_all()
    return "Rebuilt database tables."

# Load metadata to database
@application.route('/admin/load')
@auth.required
def load_db():
    '''Load metadata to the specified database.'''
    with open(application.config["METADATA_FILE"]) as t:
        rows = list(DictReader(t))
        vars_loaded = 0
        commit_increment = 1000
        for row in rows:
            # Write variable data
            var = Variable(name=row["new_name"],
                           label=row["varlab"].replace('"', "'"),
                           old_name=row["old_name"],
                           data_type=row["type"],
                           warning=int(row["warning"]),
                           group_id=str(row["group"]),
                           data_source=row["source"],
                           respondent=row["respondent"],
                           wave=str(row["wave"]),
                           scope=str(row["scope"]),
                           section=row.get("section"),
                           leaf=str(row["leaf"]))
            db.session.add(var)

            # Write topic data
            t1 = "TBD"
            if row["topic1"] != "* topic1 coming soon! *":
                t1 = row["topic1"]
            topic1 = Topic(name=row["new_name"], topic=t1)
            db.session.add(topic1)
            if len(row["topic2"]) > 0:
                topic2 = Topic(name=row["new_name"], topic=row["topic2"])
                db.session.add(topic2)

            # Write response data
            for key in row.keys():
                if key.find("label") > -1 and len(row[key]) > 0:
                    resp = Response(name=row["new_name"], label=row[key])
                    db.session.add(resp)

            # Increment variable counter
            vars_loaded += 1

            # Commit in k increments
            if vars_loaded % commit_increment == 0:
                db.session.commit()

        # Commit any remaining rows
        db.session.commit()

    # Yield result
    return "Loaded {} rows to database.".format(str(vars_loaded))


## User views ##

valid_filters = {"wave": ["1", "2", "3", "4", "5", "6"],
                 "respondent": ["k", "f", "m", "q", "t", "n", "d", "e", "h", "o", "r", "s", "u"],
                 "data_source": ["questionnaire", "constructed", "weight", "idnum"],
                 "scope": ["2", "18", "19", "20"],
                 "data_type": ["bin", "uc", "oc", "cont", "string"]}

def filter_x(query_obj, field, domain):
    # Construct argument to filter for each value in domain
    for d in domain:
        filt = 'eval("Variable.{}") == "{}"'.format(field, d)
        query_obj = query_obj.filter(eval(filt))

    # Return modified query
    return query_obj

@application.route('/variables', methods=['GET', 'POST'])
def search():
    results = None
    constraints = None
    search_query = None
    if request.method == "POST":
        qobj = Variable.query

        # Filter by search query
        search_query = request.form["variable-search"]
        if len(search_query) > 0:
            qobj = qobj.filter(Variable.label.like('%{}%'.format(search_query)))

        # Filter by fields
        constraints = dict()
        for field in set(valid_filters.keys()).intersection(request.form.keys()):
            qobj = filter_x(qobj, field, request.form.getlist(field))
            constraints[field] = request.form.getlist(field)

        # Get all matches
        results = qobj.all()

        #     # Log query
        #     print "\n Session ID: %s" % request.cookies["session"]
        #     print "Searched for: %s" % request.form["variable-search"]
        #     print "Filters: %s \n" % repr(constraints)
        #     application.logger.info("Searched: %s" % q)
    else:
        # Log that we're starting a new search
        # print "\n Session ID: %s" % request.cookies["session"]
        # print "Navigated to search \n"
        # application.logger.info("Navigated to search")
        pass

    return render_template('search.html', results=results, constraints=constraints, search_query=search_query)


## Static pages ##

# Full metadata file download page
@application.route('/metadata')
def metadata():
    return render_template('metadata.html')

# Main page
@application.route('/')
def index():
    return render_template('index.html')


# Execute app directly when invoked
if __name__ == "__main__":
    application.run(host="0.0.0.0")
