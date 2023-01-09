## Fragile Families Metadata

[![Build Status](https://travis-ci.org/fragilefamilieschallenge/metadata_app.svg?branch=master)](https://travis-ci.org/fragilefamilieschallenge/metadata_app)

This is a Python Flask app that provides a GUI for searching and browsing metadata on FFCWS variables.

This app also provides access to the Fragile Families Metadata through HTTP endpoints that return JSON results. The web endpoints allow web users to query, select and filter the metadata variables in several ways.

Access to the 'raw' metadata CSV file is also provided. The latest CSV files are available in the 'data' folder of the ffmeta package.

The web interface is available at:
[http://metadata.ffcws.princeton.edu](http://metadata.ffcws.princeton.edu)

The API interface is made available at:
[http://api.metadata.ffcws.princeton.edu](http://api.metadata.ffcws.princeton.edu)

## API

The Base URI for the API interface is:
[http://api.metadata.ffcws.princeton.edu](http://api.metadata.ffcws.princeton.edu)

At this URI, we provide 2 API endpoints:

### Select
If you know the name of the variable you're interested in, this endpoint is to be used to retrieve metadata for a variable, given its name.

#### Returns metadata for variable with name \<varName\>.
General Format: `/variable/<varName>`

`/variable/m1a3`
```
{
    "data_source": "questionnaire",
    "data_type": "bin",
    "fp_PCG": 0,
    "fp_father": 0,
    "fp_fchild": 1,
    "fp_mother": 1,
    "fp_other": 0,
    "fp_partner": 0,
    "group_id": "221",
    "group_subid": null,
    "id": 85890,
    "label": "Have you picked up a (name/names) for the (baby/babies) yet?",
    "leaf": "3",
    "scale": null,
    "name": "m1a3",
    "old_name": "m1a3",
    "probe": null,
    "qtext": null,
    "respondent": "Mother",
    "responses": {
        "1": "Yes",
        "2": "No",
        "-9": "Not in wave",
        "-8": "Out of range",
        "-7": "N/A",
        "-6": "Skip",
        "-5": "Not asked",
        "-4": "Multiple ans",
        "-3": "Missing",
        "-2": "Don't know",
        "-1": "Refuse"
    },
    "n_cities_asked": "20",
    "section": "a",
    "survey": "m",
    "topics": [
        {
            "topic": "parenting abilities",
            "umbrella": "Parenting"
        }
    ],
    "warning": 0,
    "wave": "1"
}
```

#### Optionally, if you also know the name of the field(s) you're interested in, it can return data corresponding to these field(s).

General Format: `/variable/<varName>?<fieldName>` or `/variable/<varName>?<fieldName1>&<fieldName2>&<fieldName3>..`

`/variable/m1a3?label`
```
{
    "label": "Have you picked up a (name/names) for the (baby/babies) yet?"
}
```

`/variable/m1a3?label&data_source`
```
{
    "data_source": "questionnaire",
    "label": "Have you picked up a (name/names) for the (baby/babies) yet?"
}
```

### Search
You can search for variables given one or more search criteria.

#### General Format
`/variable?q={"filters":[<filter>, <filter>, ..]}`

where `<filter>` is an individual filter, described below.

#### `filter` Specification

A `filter` is a dictionary of the form `{"name":<attributeName>,"op":<operator>,"val":<value>}`
 
`<attributeName>` is the name of the attribute that forms the basis for the search.

`<operator>` is the comparison *operator* for the search. The most commonly used operators are `eq` (for exact comparison) and `like` (for fuzzy comparison).

`<value>` is the value against which you want the comparison to work.

##### Supported Operators

**eq**: equals
    
    Search for variables where "name" is exactly "m1a3"
    {"name":"name","op":"eq","val":"m1a3"}

**like**: search for a pattern

With the `like` operator, you can use the `%` character to match any character.

    Search for variables where "name" starts with "f1"
    {"name":"name","op":"like","val":"f1%"}

    Search for variables where "qtext" has the word "financial" somewhere in it
    {"name":"qtext","op":"like","val":"%financial%"}

**lt**: less-than, **le**: less-than-or-equal-to, **gt**: greater-than, **gte**: greater-than-or-equal-to
    
    Search for variables where "warning" <= 1
    {"name":"warning","op":"leq","val":1}

**neq**: not equals
    
    Search for variables where "data_source" is not "questionnaire"
    {"name":"data_source","op":"neq","val":"questionnaire"}

**in**: is in (is one of ..)
    
    Search for variables where "respondent" is in ["Father", "Mother"] (i.e. it is either "Father" or "Mother")
    {"name":"respondent","op":"in","val":["Father","Mother"]}

**not_in**: is not in (is not any of ..)
    
    Search for variables where "wave" is neither "Year 1" nor "Year 3"
    {"name":"wave","op":"no_in","val":["Year 1","Year 3"]}

**is_null**: is null (is missing)

**is_not_null**: is not null (is not missing)

For most fields, a special "null" value denotes a missing value.

    Search for variables where "wave" is missing
    {"name":"wave","op":"is_null"}

    Search for variables where there is a "focal_person"
    {"name":"focal_person","op":"is_not_null"}

For `is_null` and `is_not_null` operators, you need not supply a `val`, since it has no meaning. (A `val` is ignored if found).

#### Multiple Filters

It is possible to search on multiple criteria (combined using AND), simply by providing more than one `filter`.

    Search for variables where "wave" is "Year 1" AND "name" starts with "f"
    /variable?q={"filters":[{"name":"wave,"op":"eq","val":"Year 1"}, {"name":"name,"op":"like","val":"f%"}]}

##### OR Filters

By default, `filters` is a list of individual filters, combined using the **AND** operation (i.e. all filter conditions must be met), as in the example above.

To specify an **OR** operation on multiple filters, `filters` can be specified as a dictionary instead, with the key "or", and the values as a list of individual `filter` objects. For example:

    Search for variables where "wave" is "Year 5" OR "respondent" is "Father"
    /variable?q={"filters":{"or": [{"name":"wave,"op":"eq","val":"Year 5"}, {"name":"respondent,"op":"eq","val":"Father"}] }}

Unsurprisingly, it also works in a similar way for **AND** searches:

    Search for variables where "wave" is "Year 9" AND "respondent" is missing
    /variable?q={"filters":{"and": [{"name":"wave,"op":"eq","val":"Year 9"}, {"name":"respondent,"op":"is_null"}] }}

However, for **AND** searches, you may find it easier to stick to the simpler syntax above.

More complicated search criteria involving multiple and nested AND/OR filters can be constructed in the same way (i.e. by replacing a `filter` at any point with a dictionary of filters keyed by `and` or `or`). However, in these cases, you may find using the Interactive <a href="http://metadata.ffcws.princeton.edu/search">Advanced Search Tool</a> helpful, which generates and displays the API call corresponding to your search.

##### Notes

  - Note that `val` field in a `filter` needs to be the literal value that you're searching for. It cannot be the name of another attribute (i.e. you cannot search for variables where `name` is equal to `old_name`, for example.)
  - With most modern browsers, you can simply type or copy-paste URLs with characters like `%`, `[`, `]`, `{` in them. However, note that when using the API programmatically, you would need to properly <a href="https://en.wikipedia.org/wiki/Percent-encoding">URL Encode</a> your query string to the API endpoint. Most HTTP libraries will do this automatically for you, but this is something to be aware of.
  
## Errors

API calls can generate errors if not used correctly. In all such cases, the returned HTTP Response code is 400, indicating a Bad Request.
For example:

#### Getting the metadata for a variable that doesn't exist:

`/variable/m1a2` (no variable by name `m1a2` exists)

returns an HTTP 400 (Bad Request) Response with the message body:
```
{
    "message": "Invalid variable name."
}
```
