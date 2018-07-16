## Fragile Families Metadata

[![Build Status](https://travis-ci.org/fragilefamilieschallenge/metadata_app.svg?branch=master)](https://travis-ci.org/fragilefamilieschallenge/metadata_app)

This is a Python Flask app that provides a GUI for searching and browsing metadata on FFCWS variables.

This app also provides access to the Fragile Families Metadata through HTTP endpoints that return JSON results. The web endpoints allow web users to query, select and filter the metadata variables in several ways.

Access to the 'raw' metadata CSV file is also provided. The latest CSV files are available in the 'data' folder of the ffmeta package.

The web interface is available at:
[http://metadata.fragilefamilies.princeton.edu](http://metadata.fragilefamilies.princeton.edu)

The API interface is made available at:
[http://api.metadata.fragilefamilies.princeton.edu](http://api.metadata.fragilefamilies.princeton.edu)

### Installation

The web interface and api can be used directly using the links above. However, if you wish to replicate the setup on your own servers:

1. Ensure Docker is installed and running.
2. `git clone https://github.com/fragilefamilieschallenge/metadata_app.git`
3. `cd metadata_app/`
4. Ensure gui.config.cfg (private keys file) exists in current directory.
5. `docker build -t metadata_app .`
6. `docker run -p 5000:5000 metadata_app` You may need to change the second port number if you're running multiple Flask apps in Docker containers

## API

The Base URI for the API interface is:
[http://api.metadata.fragilefamilies.princeton.edu](http://api.metadata.fragilefamilies.princeton.edu)

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
    "measures": null,
    "name": "m1a3",
    "old_name": "m1a3",
    "probe": null,
    "qText": null,
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
    "scope": "20",
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

General Format: 
`/variable/<varName>?<fieldName>`
or
`/variable/<varName>?<fieldName1>&<fieldName2>&<fieldName3>..`

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

General Format:
`/variable?q={"filters":[{"name":<attributeName>,"op":<operator>,"val":<value>}], ..}`

Search for variables where "name" equals "m1a3"
`/variable?q={"filters":[{"name":"name","op":"eq","val":"m1a3"}]}`
```
[
    "m1a3"
]
```

Search for variables where "wave" equals 3
`/variable?q={"filters":[{"name":"wave","op":"eq","val":3}]}`
```
[
    "f3f2e7",
    "m3f2e1",
    "m3k25a1",
    "e3i15",
    ...
```

Search for variables where "data_source" equals "constructed"
`/variable?q={"filters":[{"name":"data_source","op":"eq","val":"constructed"}]}`
```
[
    "ch3emp_csrot3_9",
    "ch3att_x",
    "ch3emp_csrot4_4",
    "ch4emp_leave_6",
    ...
```

For fuzzy or inexact queries, we use 'like' as the operator (instead of 'eq'), in conjunction with the *wildcard* **%** to match any character(s).

Search for variables where "name" starts with "m".
`/variable?q={"filters":[{"name":"name","op":"like","val":"m%"}]}`
```
[
    "m2j13c2",
    "m3f2e1",
    "m3k25a1",
    "m5k2b",
    "m1b4g",
    ...
```

Search for variables where "qText" (question text) has the world "financial" somewhere in it.
`/variable?q={"filters":[{"name":"qText","op":"like","val":"%financial%"}]}`
```
[
    "m2j13c2",
    "m3f2e1",
    "m3k25a1",
    "m5k2b",
    "m1b4g",
    ...
```

## Errors

### Getting the metadata for a variable that doesn't exist:

`/variable/m1a2` (no variable by name `m1a2` exists)

returns an HTTP 400 (Bad Request) Response with the message body:
```
{
    "message": "Invalid variable name."
}
```
