import os
basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'super secret key'
WTF_CRSF_ENAVLED = True
# Database
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'book.db')
# SQLALCHEMY_DATABASE_URI =  'sqlite:///site.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False