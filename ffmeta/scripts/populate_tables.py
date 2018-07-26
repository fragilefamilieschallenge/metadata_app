import os.path
import re
import csv
from sqlalchemy import Table

import ffmeta
from ffmeta.settings import METADATA_FILE
from ffmeta import create_app
from ffmeta.models import Variable, Response
from ffmeta.models.db import session, Base

# Dictionary mappings from what we expect in the 'raw' file to verbose string representations of attributes
# (that we store directly in the variable table in the denormalized form)
wave_dict = {1: 'Baseline', 2: 'Year 1', 3: 'Year 3', 4: 'Year 5', 5: 'Year 9', 6: 'Year 15', None: None}
survey_dict = {'d': 'Child care center (survey)', 'e': 'Child care center (observation)', 'f': 'Father',
               'h': 'In-home (survey)', 'i': 'ID Number', 'k': 'Child', 'm': 'Mother',
               'n': 'Non-parental primary caregiver', 'o': 'In-home (observation)', 'p': 'Primary caregiver',
               'q': 'Couple', 'r': 'Family care (survey)', 's': 'Family care (observation)', 't': 'Teacher',
               'u': 'Post child and family care observation', 'z': 'Couple'}
type_dict = {'bin': 'Binary', 'cont': 'Continuous', 'ID Number': 'ID Number', 'oc': 'Ordered categorical',
             'string': 'String', 'uc': 'Unordered categorical'}


def populate_raw(csv_path):
    '''Load metadata from a csv file into the "raw" table'''

    if input(
        'This operation will delete all data fom the "raw" table and re-import it. ARE YOU SURE you want to proceed (yes/no)? '
    ) != 'yes':
        return

    session.execute("DELETE FROM `raw`")
    raw_table = Table("raw", Base.metadata, autoload=True)
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for i, _d in enumerate(reader, start=1):
            # Remove keys with empty values
            d = dict((k, _d[k]) for k in _d if _d[k] != '')
            session.execute(raw_table.insert(), [d])
            if i % 500 == 0:
                print('Added {} rows'.format(i))
                session.commit()
        session.commit()


def populate_tables():
    '''Load metadata from the `raw` table to other tables.'''

    if input(
        'This operation will import data from the "raw" table and will WIPE OUT data from all other tables. ARE YOU SURE you want to proceed (yes/no)? '
    ) != 'yes':
        return

    # session.execute('DELETE FROM `group`')
    # session.execute('DELETE FROM `umbrella`')
    session.execute('DELETE FROM `response2`')
    # session.execute('DELETE FROM `topic`')
    session.execute('DELETE FROM `variable2`')
    session.commit()

    for i, row in enumerate(session.execute('SELECT * FROM `raw`'), start=1):
        name = row['new_name']
        label = row['varlab'].replace('"', "'")  # replacement logic carried over from old import function
        old_name = row['old_name']
        data_type = row['type']
        warning = int(row['warning'])

        try:
            group_id = int(row['group'])
            group_subid = None
        except ValueError:
            group_subid = re.search("[A-z]+", row['group']).group(0)
            group_id = row['group'].replace(group_subid, '')

        data_source = row['source']
        respondent = row['respondent']
        wave = row['wave']
        scope = row['scope']
        section = row['section']
        leaf = row['leaf']

        measures = row['measures']
        probe = row['probe']
        qText = row['qText']
        survey = row['survey']

        fp_fchild = row['fp_fchild']
        fp_mother = row['fp_mother']
        fp_father = row['fp_father']
        fp_PCG = row['fp_PCG']
        fp_partner = row['fp_partner']
        fp_other = row['fp_other']

        focal_person_dict = {
            'fp_fchild': 'Focal Child',
            'fp_mother': 'Mother',
            'fp_father': 'Father',
            'fp_PCG': 'Primary Caregiver',
            'fp_partner': 'Partner',
            'fp_other': 'Other'
        }
        l = locals()
        focal_person = ', '.join(v for k, v in focal_person_dict.items() if l[k])

        topic1 = row['umbrella1']
        subtopic1 = row['topic1']
        topic2 = row['umbrella2']
        subtopic2 = row['topic2']

        variable = Variable(
            name=name,
            label=label,
            old_name=old_name,
            data_type=type_dict[data_type],
            warning=warning,
            group_id=group_id,
            group_subid=group_subid,
            data_source=data_source,
            respondent=respondent,
            scope=scope,
            section=section,
            leaf=leaf,
            measures=measures,
            probe=probe,
            qText=qText,
            fp_fchild=fp_fchild,
            fp_mother=fp_mother,
            fp_father=fp_father,
            fp_PCG=fp_PCG,
            fp_partner=fp_partner,
            fp_other=fp_other,

            focal_person=focal_person,
            survey=survey_dict[survey],
            wave=wave_dict[wave],

            topic1=topic1,
            subtopic1=subtopic1,
            topic2=topic2,
            subtopic2=subtopic2,
            topics=', '.join(x for x in set([topic1, topic2]) if x is not None),
            subtopics=', '.join(x for x in set([subtopic1, subtopic2]) if x is not None),
        )

        session.add(variable)

        # Write response data
        for key in row.keys():
            if key.find("label") > -1 and row[key] is not None and len(row[key]) > 0:
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
                session.add(resp)

        if not i % 200:
            print(str(i) + " rows added.")
            session.commit()

    session.commit()
    # session.execute("INSERT INTO topic (name, topic) SELECT new_name, topic1 FROM raw WHERE topic1 IS NOT NULL")
    # session.execute("INSERT INTO topic (name, topic) SELECT new_name, topic2 FROM raw WHERE topic2 IS NOT NULL")
    # session.execute("INSERT INTO umbrella (topic, umbrella) (SELECT DISTINCT topic1, umbrella1 FROM raw WHERE umbrella1 IS NOT NULL) UNION (SELECT DISTINCT topic2, umbrella2 FROM raw WHERE umbrella2 IS NOT NULL)")

    # session.commit()


if __name__ == '__main__':

    application = create_app(debug=True)
    with application.app_context():
        CSV_FILE_PATH = os.path.join(os.path.dirname(ffmeta.__file__), METADATA_FILE)
        populate_raw(CSV_FILE_PATH)
        populate_tables()
