import os
from collections import OrderedDict

from sqlalchemy import or_, and_
from flask import Blueprint, render_template, request, send_from_directory, send_file, make_response, current_app

from ffmeta.models import Response, Variable
from ffmeta.models.db import session
from ffmeta.utils import epochalypse_now


bp = Blueprint('web', __name__)


# Define valid search filters
# This object determines what filter groups show up in the search view
filter_labels = OrderedDict([
    ("topic", "Topic"),
    ("wave", "Wave"),
    ("respondent", "Respondent"),
    ("data_source", "Source"),
    ("data_type", "Variable type"),
    ("measures", "Scales"),
    ("survey", "Survey"),
    ("focal_person", "Focal Person")
])

# Define domain-label map for each filter
# This defines what values are valid to filter on for each filter group
valid_filters = {
    "topic": OrderedDict([
        (row.topic1, row.topic1) for row in session.execute("SELECT DISTINCT(topic1) FROM variable2 WHERE topic1 IS NOT NULL UNION SELECT DISTINCT(topic2) FROM variable2 WHERE topic2 IS NOT NULL ORDER BY 1")
    ]),
    "wave": OrderedDict([
        (row.wave, row.wave) for row in session.execute("SELECT DISTINCT(wave) FROM variable2 WHERE wave IS NOT NULL ORDER BY 1")
    ]),
    "respondent": OrderedDict([
        (row.respondent, row.respondent) for row in session.execute("SELECT DISTINCT(respondent) FROM variable2 WHERE respondent IS NOT NULL ORDER BY 1")
    ]),
    "data_source": OrderedDict([
        (row.data_source, row.data_source) for row in session.execute("SELECT DISTINCT(data_source) FROM variable2 ORDER BY 1")
    ]),
    "data_type": OrderedDict([
        (row.data_type, row.data_type) for row in session.execute("SELECT DISTINCT(data_type) FROM variable2 ORDER BY 1")
    ]),
    "measures": OrderedDict([
        (row.measures, row.measures) for row in session.execute("SELECT DISTINCT(measures) FROM variable2 WHERE measures IS NOT NULL ORDER BY 1")
    ]),
    "survey": OrderedDict([
        (row.survey, row.survey) for row in session.execute("SELECT DISTINCT(survey) FROM variable2 ORDER BY 1")
    ]),
    "focal_person": OrderedDict([
        ("fp_fchild", "Focal Child"),
        ("fp_mother", "Mother"),
        ("fp_father", "Father"),
        ("fp_PCG", "Primary Caregiver"),
        ("fp_partner", "Partner"),
        ("fp_other", "Other"),
        ("fp_none", "None")
    ])
}


@bp.route('/variables', methods=['GET', 'POST'])
def search():
    results = None
    variable_names = None
    constraints = None
    search_query = None
    zero_found = False

    if request.method == "POST":
        query = session.query(Variable)

        # Filter by search query
        search_query = request.form["variable-search"]
        if len(search_query) > 0:
            query = query.filter(Variable.label.like('%%{}%%'.format(search_query)) | Variable.name.like('%%{}%%'.format(search_query)) | Variable.old_name.like('%%{}%%'.format(search_query)))

        # Filter by fields
        constraints = dict()
        for field in set(valid_filters.keys()).intersection(request.form.keys()):
            if field == "topic":
                topic_list = request.form.getlist("topic")
                query = query.filter(Variable.topic1.in_(topic_list) | Variable.topic2.in_(topic_list))
            elif field == "focal_person":
                fp_filters = []
                for fp in request.form.getlist(field):
                    if fp == 'fp_none':
                        fp_filters.append(and_(
                            Variable.fp_fchild == 0,
                            Variable.fp_mother == 0,
                            Variable.fp_father == 0,
                            Variable.fp_PCG == 0,
                            Variable.fp_partner == 0,
                            Variable.fp_other == 0
                        ))
                    else:
                        fp_filters.append(getattr(Variable, fp) == 1)
                query = query.filter(or_(*fp_filters))
            else:
                query = query.filter(getattr(Variable, field).in_(request.form.getlist(field)))
            constraints[field] = request.form.getlist(field)

        results = query.all()
        variable_names = [result.name for result in results]
        zero_found = len(variable_names) == 0

    resp = make_response(render_template('web/search.html', results=results, rnames=variable_names, constraints=constraints,
                           search_query=search_query, filtermeta=valid_filters, filterlabs=filter_labels, zero_found=zero_found))

    return resp


@bp.route('/search', methods=['GET', 'POST'])
def search2():
    return render_template('web/search2.html')


@bp.route("/variables")
@bp.route('/variables/<varname>')
def var_page(varname=None):
    this_variable = session.query(Variable).filter(Variable.name == varname).first()
    neighbors = session.query(Variable).filter(Variable.group_id == this_variable.group_id).filter(Variable.name != this_variable.name).all()
    responses = session.query(Response).filter(Response.name == varname).group_by(Response.label).all()
    if responses:
        responses = sorted(responses, key=lambda x: int(x.value), reverse=True)

    return make_response(render_template('web/variable.html', var_data=this_variable, neighbors=neighbors, responses=responses, filtermeta=valid_filters, filterlabs=filter_labels))


@bp.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(current_app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@bp.route('/get_metadata')
def metadata():
    return send_file(os.path.join(current_app.root_path, current_app.config["METADATA_FILE"]), as_attachment=True)


@bp.route("/feedback")
def feedback():
    return render_template('web/feedback.html')


@bp.route('/about')
def about():
    resp = make_response(render_template('web/about.html'))
    return resp


# Main page
# Also, set a unique ID for this user
@bp.route('/')
def index():
    resp = make_response(render_template('web/index.html'))
    return resp


@bp.route('/api')
def api():
    return render_template("web/api.html")


