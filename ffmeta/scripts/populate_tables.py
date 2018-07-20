import re
from ffmeta import create_app
from ffmeta.models import Variable, Response
from ffmeta.models.db import session

# Dictionary mappings from what we expect in the 'raw' file to verbose string representations of attributes
# (that we store directly in the variable table in the denormalized form)
wave_dict = dict(iter(session.execute('SELECT id, name FROM wave')))
survey_dict = dict(iter(session.execute('SELECT id, name FROM survey')))
type_dict = dict(iter(session.execute('SELECT id, name FROM data_type')))


def populate_tables():
    '''Load metadata from the `raw` table to other tables.'''

    if input(
        'This operation will import data from the "raw" table and will WIPE OUT data from all other tables. ARE YOU SURE you want to proceed (yes/no)? '
    ) != 'yes':
        return

    session.execute('DELETE FROM `group`')
    session.execute('DELETE FROM `umbrella`')
    session.execute('DELETE FROM `response`')
    session.execute('DELETE FROM `topic`')
    session.execute('DELETE FROM `variable`')
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
            'fp_child': 'Focal Child',
            'fp_mother': 'Mother',
            'fp_father': 'Father',
            'fp_PCG': 'Primary Caregiver',
            'fp_partner': 'Partner',
            'fp_other': 'Other'
        }
        focal_person = ', '.join(v for k, v in focal_person_dict.items() if eval(k))

        variable = Variable(
            name=name,
            label=label,
            old_name=old_name,
            data_type=data_type,
            warning=warning,
            group_id=group_id,
            group_subid=group_subid,
            data_source=data_source,
            respondent=respondent,
            wave=wave,
            scope=scope,
            section=section,
            leaf=leaf,
            measures=measures,
            probe=probe,
            qText=qText,
            survey=survey,
            fp_fchild=fp_fchild,
            fp_mother=fp_mother,
            fp_father=fp_father,
            fp_PCG=fp_PCG,
            fp_partner=fp_partner,
            fp_other=fp_other,

            focal_person=focal_person,
            survey2=survey_dict(survey),
            wave2=wave_dict(wave),
            type=type_dict(data_type)

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

        if not i%200:
            print(str(i) + " rows added.")
            session.commit()

    session.commit()
    session.execute("INSERT INTO topic (name, topic) SELECT new_name, topic1 FROM raw WHERE topic1 IS NOT NULL")
    session.execute("INSERT INTO topic (name, topic) SELECT new_name, topic2 FROM raw WHERE topic2 IS NOT NULL")
    session.execute("INSERT INTO umbrella (topic, umbrella) (SELECT DISTINCT topic1, umbrella1 FROM raw WHERE umbrella1 IS NOT NULL) UNION (SELECT DISTINCT topic2, umbrella2 FROM raw WHERE umbrella2 IS NOT NULL)")

    session.commit()


if __name__ == '__main__':

    application = create_app(debug=True)
    with application.app_context():
        # populate_tables()
        print(wave_dict)
