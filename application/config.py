import os

PETITIONS_API_URL = os.getenv('PETITIONS_API_URL', 'https://petition.parliament.uk/petitions')
TWFY_API_URL = os.getenv('TWFY_API_URL', 'http://www.theyworkforyou.com/api')
TWFY_API_KEY = os.getenv('TWFY_API_KEY')
MAPIT_API_URL = os.getenv('MAPIT_API_URL', 'http://mapit.mysociety.org')
GA_KEY = os.getenv('GA_KEY')
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql+psycopg2://vagrant:vagrant@localhost:5432/vagrant')
SQLALCHEMY_TRACK_MODIFICATIONS = False
