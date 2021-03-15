import json
from threading import Event

config = json.load(open('config.json', 'r'))

api_config = config['api']
shop_config = config['shop']

factory_state = Event()
provider_state = Event()

production = json.load(open('production.json', 'r'))
