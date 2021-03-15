import requests
from random import randint, choice

HOST = 'http://localhost:8004/'
PURCHASES_HOST = HOST + 'purchases'
SHOP_HOST = HOST + 'shop'
FACTORY_HOST = HOST + 'factory'

SHOP_PASSWORD = 'lol'

AlNUM_VOCAB = [chr(x) for x in range(97, 123)] + [chr(x) for x in range(65, 91)] + [chr(x) for x in range(48, 57)]


def random_alnum(length: int) -> str:
    return ''.join([choice(AlNUM_VOCAB) for _ in range(length)])


def random_phone_number() -> str:
    return ''.join([str(randint(0, 9)) for _ in range(11)])


def create_shops(count: int) -> bool:
    for _ in range(count):
        try:
            r = requests.post(SHOP_HOST + '/create', json={
                'name': random_alnum(randint(5, 15)),
                'address': random_alnum(randint(5, 15)),
                'number': random_phone_number()
            }, headers={'XXX-CODE': SHOP_PASSWORD})
            if r.status_code != 201:
                raise Exception
        except:
            return False

    return True


try:
    _count = int(input('Count of shops: '))
except ValueError:
    print('Do not play with me.')
    exit(-1)

if not create_shops(_count):
    print('Something went wrong')
else:
    print('OK')
