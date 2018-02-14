#!/usr/bin/env python
# wireframe.py
# Prototype for FFCWS metadata front-end.
#
# Author: Alex Kindel
# Date: 10 August 2017

from csv import DictReader
import subprocess
import os
import logging

from flask import Flask, render_template, url_for, g, redirect, request
from dbutils import with_db, query

application = Flask(__name__)

# Configure app data backend
metadata_flat = 'data/FFMetadata20171102.csv'
dbms = {'username': os.environ['DB_USER'],
        'password': os.environ['DB_PASS'],
        'db': os.environ['DB_NAME'],
        'host': os.environ['DB_HOST'],
        'port': int(os.environ['DB_PORT'])}
application.config.from_object(__name__)


## Data management tools ##

# Build database schema
@application.cli.command('build')
def build_db():
    subprocess.call("mysql -h %s -P %d -D %s -u %s -p%s < ./data/schema.sql" % (dbms['host'], dbms['port'], dbms['db'], dbms['username'], dbms['password']), shell=True)

# Load metadata to relational schema
@application.cli.command('load')
@with_db(dbms)
def load_db(db):
    with open(metadata_flat) as t:
        rows = list(DictReader(t))
        for row in rows:
            # Write variable data
            variable = dict()
            variable["new_name"] = row["new_name"]
            variable["varlab"] = row["varlab"].replace('"', "'")  # Handle quotes
            variable["old_name"] = row["old_name"]
            variable["data_type"] = row["type"]
            variable["warning"] = row["warning"]
            variable["group_id"] = str(row["group"])
            variable["data_source"] = row["source"]
            variable["respondent"] = row["respondent"]
            variable["wave"] = str(row["wave"])
            variable["scope"] = str(row["scope"])
            if row["section"]:
                variable["section"] = row["section"]  # Leave this out if empty
            variable["leaf"] = str(row["leaf"])
            query(db, 'INSERT INTO variable(%s) VALUES ("%s")' % (','.join(variable.keys()), '","'.join(variable.values())))


            # Write topic data
            topic1 = dict()
            topic1["new_name"] = row["new_name"]
            topic1["topic"] = row["topic1"]
            if row["topic1"] == "* topic1 coming soon! *":
                topic1["topic"] = "TBD"  # Use "TBD" topic if not assigned
            else:
                topic1["topic"] = row["topic1"]
            query(db, 'INSERT INTO topic(%s) VALUES ("%s")' % (','.join(topic1.keys()), '","'.join(topic1.values())))

            # Add data from second topic, if exists
            if len(row["topic2"]) > 0:
                topic2 = dict()
                topic2["new_name"] = row["new_name"]
                topic2["topic"] = row["topic2"]
                query(db, 'INSERT INTO topic(%s) VALUES ("%s")' % (','.join(topic2.keys()), '","'.join(topic2.values())))

            # Write response data
            response = dict()
            for key in row.keys():
                # Write every valid labeln to row
                if key.find("label") > -1 and len(row[key]) > 0:
                    query(db, 'INSERT INTO response(label, new_name) VALUES ("%s","%s")' % (row[key], row["new_name"]))


## Variable metadata search and display logic ##

@application.route('/variables', methods=['GET', 'POST'])
@with_db(dbms)
def search(db):
    results = None
    constraints = None
    search_query = None
    if request.method == "POST":
        search_query = request.form["variable-search"]

        # Set filtering constraints
        constraints = dict()
        constraints["wave"] = request.form.getlist("wave") if "wave" in request.form.keys() else ["1", "2", "3", "4", "5", "6"]
        constraints["respondent"] = request.form.getlist("respondent") if "respondent" in request.form.keys() else ["k", "f", "m", "q", "t", "n", "d", "e", "h", "o", "r", "s", "u"]
        constraints["data_source"] = request.form.getlist("data_source") if "data_source" in request.form.keys() else ["questionnaire", "constructed", "weight", "idnum"]
        constraints["scope"] = request.form.getlist("scope") if "scope" in request.form.keys() else ["2", "18", "19", "20"]
        constraints["data_type"] = request.form.getlist("data_type") if "data_type" in request.form.keys() else ["bin", "uc", "oc", "cont", "string"]

        # Find results matching search string
        if len(request.form["variable-search"]) > 0 or len(request.form.keys()) > 0:
            q = """SELECT *
                   FROM (SELECT DISTINCT new_name
                         FROM variable
                         WHERE ((new_name LIKE CONCAT('%%','%s','%%'))
                             OR (varlab LIKE CONCAT('%%','%s','%%')))
                         UNION ALL
                         SELECT DISTINCT new_name
                         FROM response
                         WHERE label LIKE CONCAT('%%','%s','%%')) q
                   LEFT JOIN variable v
                   ON q.new_name = v.new_name
                   WHERE wave IN %s
                   AND respondent IN %s
                   AND data_source IN %s
                   AND scope IN %s
                   AND data_type IN %s;
                   """ % (request.form["variable-search"],
                          request.form["variable-search"],
                          request.form["variable-search"],
                          repr(constraints["wave"]).replace("[", "(").replace("]", ")").replace("u'", "'"),
                          repr(constraints["respondent"]).replace("[", "(").replace("]", ")").replace("u'", "'"),
                          repr(constraints["data_source"]).replace("[", "(").replace("]", ")").replace("u'", "'"),
                          repr(constraints["scope"]).replace("[", "(").replace("]", ")").replace("u'", "'"),
                          repr(constraints["data_type"]).replace("[", "(").replace("]", ")").replace("u'", "'"))
            results = query(db, q, fetchall=True)

            # for result in results:
            #   for key in result.keys()
            #       if key = "wave":
            #           if result[key] = 1:
            #

            # Log query
            print "\n Session ID: %s" % request.cookies["session"]
            print "Searched for: %s" % request.form["variable-search"]
            print "Filters: %s \n" % repr(constraints)
            application.logger.info("Searched: %s" % q)
    else:
        # Log that we're starting a new search
        print "\n Session ID: %s" % request.cookies["session"]
        print "Navigated to search \n"
        application.logger.info("Navigated to search")

    return render_template('search.html', results=results, constraints=constraints, search_query=search_query)

@application.route('/<new_name>')
@with_db(dbms)
def var_page(db, new_name):
    # Get variable data
    q1 = "SELECT * FROM variable WHERE new_name = '%s'" % new_name
    var_data = query(db, q1).next()
    var_data["varlab"] = var_data["varlab"].decode("utf-8", 'ignore')

    # Grouped variables
    q2 = "SELECT * FROM variable WHERE group_id = '%s'" % var_data["group_id"]
    neighbors = list(query(db, q2, fetchall=True))
    for i, nvar in enumerate(neighbors):
        nvar["varlab"] = nvar["varlab"].decode("utf-8", 'ignore')
        neighbors[i] = nvar

    # Responses
    q3 = "SELECT * FROM response WHERE new_name = '%s'" % new_name
    responses = query(db, q3, fetchall=True)
    if responses:
        responses = sorted(responses, key=lambda x: int(x["label"].strip().replace(":", "").split(" ")[0]), reverse=True)

    # Topic
    q4 = "SELECT * FROM topic WHERE new_name = '%s'" % new_name
    topics = query(db, q4, fetchall=True)

    # Log query
    print "\n Session ID: %s" % request.cookies["session"]
    print "Variable displayed: %s \n" % new_name
    application.logger.info("Variable displayed: %s" % new_name)

    # Render page
    return render_template('variable.html', var_data=var_data, neighbors=neighbors, responses=responses, topics=topics)


## Static pages ##

# Full metadata file download page
@application.route('/metadata')
def metadata():
    return render_template('metadata.html')

# About page
@application.route('/about')
def about():
    return render_template('about.html')

# Main page
@application.route('/')
def index():
    return render_template('index.html')


# Execute app directly when invoked
if __name__ == "__main__":
    application.run()
