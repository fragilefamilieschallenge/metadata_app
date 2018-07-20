import operator
from sqlalchemy import inspect, and_, or_


from flask import Blueprint, request, Response, json, jsonify

from ffmeta.models.db import session
from ffmeta.models import Response, Variable, Umbrella, Topic
from ffmeta.utils import api_error

bp = Blueprint('apiv2', __name__)

# All available (searchable) attributes for a 'Variable'. Determined here once to avoid repeated queries.
variable_attrs = [c_attr.key for c_attr in inspect(Variable).mapper.column_attrs]


def variable_details(obj, attrs=None, as_json=False):
    d = dict((attr, getattr(obj, attr, '')) for attr in variable_attrs)

    # TODO: The following structure is used to maintain compatibility with old behavior
    # Probably it makes sense to reverse the keys/values
    d['responses'] = dict((r.value, r.label) for r in obj.responses)

    # TODO: The following structure is used to maintain compatibility with old behavior
    # A better structure to this would be to simply return an <umbrella_name>: [<topic_names>] dictionary here
    d['topics'] = [{'umbrella': str(t.umbrella), 'topic': str(t)} for t in obj.topics]

    keys = attrs or d.keys()
    d = dict((k, d[k]) for k in keys if k in d.keys())

    if as_json:
        return jsonify(d)
    else:
        return d


def select(variable_name, attrs=None, as_json=False):
    """
    Return a dictionary of variable attributes, given the variable's name
    :param variable_name: The name of the variable we're interested in
    :param attrs: optional, a list of attributes that we're interested in. If unspecified, all attributes of the
        variable are returned. Unrecognized attributes are ignored.
    :return: A dictionary with attribute names as the keys, and attribute value as the values.

    This function raises an AppException if no variable with the given name is found
    """
    obj = session.query(Variable).filter(Variable.name == variable_name).first()
    if obj:
        return variable_details(obj, attrs=attrs, as_json=as_json)
    else:
        return api_error(400, "Invalid variable name.")


def _pred(filter):
    """
    Create a SqlAlchemy Binary Expression given a single search criteria.

    :param filter: A dictionary with keys 'name', 'op' and 'val', indicating the attribute name, comparison operation
        and the comparison value we wish to use.
        'name' can be any supported attribute name of a variable (e.g. 'name'/'data_source'),
            or one of 'response'/'topic'/'umbrella'.
        'op' can be one of 'like','eq','neq','gt','gte','lt','lte' (where the op name corresponds to the usual
            semantics of these binary comparison operators.
            Note that specifying 'like' performs a fuzzy (LIKE) query in the database. Corresponding wildcards ('%')
            must be provided in the 'val' attribute for this to take effect.
        'val' is the value we wish to compare against. This is either a string or a numeric, corresponding to the
            type of the attribute specified by 'name'. Comparison against values work as expected, but
            comparison against another attribute is not supported.

    :return: A SqlAlchemy BinaryExpression object corresponding to given search criteria.
    """
    name, op, val = filter['name'], filter['op'], filter['val']
    op = op.lower().strip()

    if name in variable_attrs:
        column = getattr(Variable, name)
    elif name == 'response':
        column = Response.label
    elif name == 'topic':
        column = Topic.topic
    elif name == 'umbrella':
        column = Umbrella.umbrella
    else:
        return api_error(400, "Invalid name for search.")

    if op == 'like':
        pred = column.like(val)
    elif op in ('eq', '=='):
        pred = operator.eq(column, val)
    elif op in ('neq', 'ne', '!='):
        pred = operator.ne(column, val)
    elif op in ('gt', '>'):
        pred = operator.gt(column, val)
    elif op in ('gte', 'ge', '>='):
        pred = operator.ge(column, val)
    elif op in ('lt', '<'):
        pred = operator.lt(column, val)
    elif op in ('lte', 'le', '<='):
        pred = operator.le(column, val)
    else:
        return api_error(400, "Unrecognized operator")

    return pred


def _filters(filters, aggFn=and_):
    """
    Recursive function returning a SqlAlchemy Binary Expression given a list or dictionary of filters
    :param filters:

        A list or dictionary of <filter>(s).
        (A <filter> is simply a dict with keys 'name'/'op'/'val')

        If 'filters' is a list, then individual filter(s) are combined with an 'AND'.
        'filters' can also be a dict, keyed by either an 'and' or an 'or', with the values of the dict
        being valid 'filters' themselves (defined recursively).

    :param aggFn: Aggregate function to use if filters is a list, 'AND' by default.
    :return: A SqlAlchemy BinaryExpression object corresponding to given search criteria.
    """

    res = []
    if type(filters) == list:
        res = aggFn(*[_filters(f) for f in filters])
    elif type(filters) == dict:
        if 'and' in filters or 'or' in filters:  # a recursive filter with key 'and' or 'or'
            assert(len(filters) == 1)
            key = list(filters.keys())[0]
            val = filters[key]
            aggFn = {'and': and_, 'or': or_}[key]
            res = _filters(val, aggFn)
        else:
            res = _pred(filters)
    return res


def search(filters, details=False, as_json=True):
    """
    Search variables given search criteria
    :param filters:

        A list or dictionary of <filter>(s).
        (A <filter> is simply a dict with keys 'name'/'op'/'val')

        If 'filters' is a list, then individual filter(s) are combined with an 'AND'.
        'filters' can also be a dict, keyed by either an 'and' or an 'or', with the values of the dict
        being valid 'filters' themselves (defined recursively).

    :return: A list of unique variable names corresponding to the search criteria.
    """
    filters = _filters(filters)

    query = session.query(Variable)\
        .outerjoin(Response, Variable.name == Response.name).\
        outerjoin(Topic, Variable.name == Topic.name).\
        outerjoin(Umbrella, Topic.topic == Umbrella.topic)
    query = query.filter(filters)

    # TODO: Do we need to remove duplicates??
    if details:
        results = [variable_details(o) for o in query]
    else:
        results = [o.name for o in query]

    if as_json:
        return jsonify(results)
    else:
        return results


@bp.route("/variable/<variable_name>")
def select_variable(variable_name):
    """Web endpoint for variable selection given it's name, and an optional list of attribute we're interested in."""
    return select(variable_name, list(request.args.keys()), as_json=True)


@bp.route("/variable")
def search_variable():
    """
    Web endpoint for variable searching given one or more search criteria (list of clauses or nested clauses).
    The web endpoint is called with a 'q' query string, which is a dictionary with the following supported keys:

        'filters':
            A list or dictionary of <filter>(s).
            (A <filter> is simply a dict with keys 'name'/'op'/'val')

            If 'filters' is a list, then individual filter(s) are combined with an 'AND'.
            'filters' can also be a dict, keyed by either an 'and' or an 'or', with the values of the dict
            being valid 'filters' themselves (defined recursively).

    Some example search queries are (Note that the fuzzy comparison wildcard '%' is url-encoded as '%25')

        <url>?q={"filters":[{"name":"wave","op":"eq","val":3}]}
        <url>?q={"filters":{"or":[{"name":"wave","op":"gt","val":3}]}}
        <url>?q={"filters":[{"name":"response","op":"eq","val":"refuse"}]}
        <url>?q={"filters":[{"name":"topic","op":"eq","val":"age"}]}

        <url>?q={"filters":[{"name":"wave","op":"eq","val":3},{"name":"name","op":"like","val":"%25fb%25"}]}
        <url>?q={"filters":{"or":[{"name":"wave","op":"gt","val":3},{"name":"name","op":"like","val":"%25fb%25"}]}}

        <url>?q={"filters":[{"name":"wave","op":"gt","val":3}, {"or": [{"name":"name","op":"like","val":"%25fb%25"},{"name":"data_source","op":"eq","val":"constructed"}]}]}
        <url>?q={"filters":{"and": [{"name":"wave","op":"gt","val":3}, {"or": [{"name":"name","op":"like","val":"%25fb%25"},{"name":"data_source","op":"eq","val":"constructed"}]}]}}
        <url>?q={"filters":[{"name":"umbrella","op":"eq","val":"parenting"},{"name":"topic","op":"like","val":"%25parenting%25"}]}
        <url>?q={"filters":[{"name":"umbrella","op":"eq","val":"parenting"},{"or": [{"name":"topic","op":"like","val":"%25parenting%25"}, {"name":"name","op":"like","val":"%25f%25"}]}]}

    This Search behavior is largely inspired by Flask-Restless (https://flask-restless.readthedocs.io/en/stable/)
    but does not purport to emulate it completely (Ordering / Grouping /Paging / Searching against fieldnames and
    across relationships is not supported, for example).
    """
    results = []
    if 'q' in request.args:
        q = json.loads(request.args['q'])
        filters = q.get('filters', [])
        return search(filters, details='details' in request.args, as_json=True)

    return jsonify(results)