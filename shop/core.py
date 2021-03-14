import json

config = json.load(open('config.json', 'r'))

api_config = config['api']
purchases_config = config['purchases']