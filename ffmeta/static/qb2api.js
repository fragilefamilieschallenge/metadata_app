function qb2apiFilter(qbElement) {
    var query = qbElement.queryBuilder('getRules');
    if ($.isEmptyObject(query.rules)) {
        return [];
    } else {
        var x = convertCondition(query);
        return [x];
    }
}

function convertCondition(node) {
    if (node.condition==undefined) {
        return convertSingleRule(node);
    } else {
        var _condition = node.condition.toLowerCase(); // 'and' or 'or'
        var _rules = node.rules.map(convertCondition);
        d = {};
        d[_condition] = _rules;
        return d;
    }
}

function convertSingleRule(rule) {
    var _field = rule.field;
    var _operator = rule.operator;
    var _value = rule.value;

    var _name = _field;
    var _op;
    var _val = _value;

    switch (_operator) {
        case 'equal':
            _op = 'eq';
            break;
        case 'not_equal':
            _op = 'ne';
            break;
        case 'is_null':
            _op = 'is_null';
            break;
        case 'is_not_null':
            _op = 'is_not_null';
            break;
        case 'in':
            _op = 'in';
            break;
        case 'not_in':
            _op = 'not_in';
            break;
        case 'begins_with':
            _op = 'like';
            _val = _val + '%';
            break;
        case 'ends_with':
            _op = 'like';
            _val = '%' + _val;
            break;
        case 'contains':
            _op = 'like';
            _val = '%' + _val + '%';
            break;
        case 'less':
            _op = 'lt';
            break;
        case 'less_or_equal':
            _op = 'le';
            break;
        case 'greater':
            _op = 'gt';
            break;
        case 'greater_or_equal':
            _op = 'ge';
            break;
        case 'between':
            return {'and': [{'name': _name, 'op': 'ge', 'val': _val[0]}, {'name': _name, 'op': 'le', 'val': _val[1]}]};
    }

    return {'name': _name, 'op': _op, 'val': _val};
}