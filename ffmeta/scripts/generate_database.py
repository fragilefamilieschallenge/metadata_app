import os.path
import pymysql.cursors
import ffmeta
from ffmeta.settings import DB_HOST, DB_NAME, DB_PORT, DB_USER, DB_PASS


def execute_script(conn, script_path, quiet=False):
    if not quiet and input(
        f'Are you sure you want to execute the script at {script_path}? '
        'This may lead to loss of data! (yes|no) '
    ) != 'yes':
        return

    with open(script_path, 'r') as f:
        for statement in f.read().split(';'):
            if statement.strip():
                statement_singleline = statement.replace('\n', '')
                with conn.cursor() as cur:
                    try:
                        cur.execute(statement)
                    except:
                        print('ERROR: ' + statement_singleline)
                    else:
                        print(statement_singleline)


if __name__ == '__main__':

    conn = pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASS, db=DB_NAME)
    execute_script(conn, os.path.join(os.path.dirname(ffmeta.__file__), 'data', 'ffmetadata_ddl.sql'))
