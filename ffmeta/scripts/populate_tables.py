import os.path
import csv
from sqlalchemy import Table

import ffmeta
from ffmeta.settings import METADATA_FILE
from ffmeta import create_app
from ffmeta.models import Variable, Response
from ffmeta.models.db import session, Base


def populate_raw(csv_path):
    '''Load metadata from a csv file into the "raw" table'''

    if input(
        'This operation will delete all data fom the "raw" table and re-import it. ARE YOU SURE you want to proceed (yes/no)? '
    ) != 'yes':
        return

    session.execute("DELETE FROM `raw2`")
    raw_table = Table("raw2", Base.metadata, autoload=True)
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

    session.execute('DELETE FROM `response2`')
    session.execute('DELETE FROM `variable3`')
    session.execute('DELETE FROM `topics`')

    session.commit()

    distinct_topics = set()

    for i, row in enumerate(session.execute('SELECT * FROM `raw2`'), start=1):
        name = row['new_name']
        if row['varlab'] is not None:
            label = row['varlab'].replace('"', "'")  # replacement logic carried over from old import function
        else:
            label = row['varlab']
        old_name = row['old_name']
        data_type = row['type']
        warning = row['warning']
        group_id = row['group']
        data_source = row['source']
        respondent = row['respondent']
        wave = row['wave']
        n_cities_asked = row['n_cities_asked']
        section = row['section']
        leaf = row['leaf']

        scale = row['scale']
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

        topics = row['topics']
        subtopics = row['subtopics']

        if topics is not None:
            for t in topics.split(';'):
                t = t.strip()
                if t:
                    distinct_topics.add(t)

        in_FFC_file = row['in_FFC_file']

        variable = Variable(
            name=name,
            label=label,
            old_name=old_name,
            data_type=data_type,
            warning=warning,
            group_id=group_id,
            data_source=data_source,
            respondent=respondent,
            n_cities_asked=n_cities_asked,
            section=section,
            leaf=leaf,
            scale=scale,
            probe=probe,
            qText=qText,
            fp_fchild=fp_fchild,
            fp_mother=fp_mother,
            fp_father=fp_father,
            fp_PCG=fp_PCG,
            fp_partner=fp_partner,
            fp_other=fp_other,

            focal_person=focal_person,
            survey=survey,
            wave=wave,

            topics=topics,
            subtopics=subtopics,

            in_FFC_file=in_FFC_file
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

    for topic in distinct_topics:
        session.execute("INSERT INTO topics (topic) VALUES ('{}')".format(topic))

    session.commit()


if __name__ == '__main__':

    application = create_app(debug=True)
    with application.app_context():
        CSV_FILE_PATH = os.path.join(os.path.dirname(ffmeta.__file__), METADATA_FILE)
        populate_raw(CSV_FILE_PATH)
        populate_tables()
