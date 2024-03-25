import os


DEBUG = False
SERVER_NAME = 'metadata.ffcws.princeton.edu'

# Database credentials. The following are just placeholders - replace with real credentials.
DB_USER = os.environ.get("DB_USER", "travis")
DB_PASS = os.environ.get("DB_PASS", "")
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = int(os.environ.get("DB_PORT", "3306")
DB_NAME = os.environ.get("DB_NAME", "FFMeta")

# SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME)
SQLALCHEMY_TRACK_MODIFICATIONS = False
