import json
from os import environ
import logging

config = json.load(open('config.json', 'r'))

api_config = config['api']
shop_config = config['shop']

db_config = {
    'host': environ.get('PGHOST'),
    'db': environ.get('PGDATABASE'),
    'user': environ.get('PGUSER'),
    'password': environ.get('PGPASSWORD')
}

logging.basicConfig(filename='factory.log', level=logging.INFO,
                    format='%(asctime)-15s | [%(name)s] %(levelname)s => %(message)s')

logging.getLogger('sqlalchemy.engine').setLevel(logging.FATAL)
logging.getLogger('werkzeug').setLevel(logging.FATAL)

production = json.load(open('production.json', 'r'))
