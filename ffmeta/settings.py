DEBUG = False
SERVER_NAME = 'metadata.ffcws.princeton.edu'

# Database credentials. The following are just placeholders - replace with real credentials.
DB_USER = "travis"
DB_PASS = ""
DB_HOST = "localhost"
DB_PORT = 3306
DB_NAME = "FFMeta"

# SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME)
SQLALCHEMY_TRACK_MODIFICATIONS = False
