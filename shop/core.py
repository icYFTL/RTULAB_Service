import json
from os import environ

config = json.load(open('config.json', 'r'))

api_config = config['api']
purchases_config = config['purchases']

db_config = {
    'host': environ.get('PGHOST'),
    'db': environ.get('PGDATABASE'),
    'user': environ.get('PGUSER'),
    'password': environ.get('PGPASSWORD')
}