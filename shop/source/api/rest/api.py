from source.database import *
from source.api.purchases import PurchasesAPI
from . import app
from .utils import *
from flask import request
from datetime import datetime
from pytz import timezone
from functools import wraps
from core import api_config
from flask import abort
from random import randint
import re


def protected(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.headers.get('XXX-CODE') == api_config['password']:
            abort(403)
        return f(*args, **kwargs)

    return decorated_function


@app.route('/shop', methods=['GET'])
def on_root():
    return Reply.ok()


@app.route('/shop/create', methods=['POST'])
@protected
def on_create_shop():
    data = request.json
    if not data:
        return Reply.bad_request(error='Empty json')

    if not isinstance(data, dict):
        return Reply.bad_request(error='Invalid json. It must be a dict.')

    _check = check_args_important(('name', 'address', 'number'), **data)
    if not _check[0]:
        return Reply.bad_request(error=f'Empty important {_check[1]} field passed')

    if not isinstance(data['name'], str) or len(data['name']) > 50 or len(data['name']) < 3:
        return Reply.bad_request(error='Invalid name. Name must be str and len must be 3 < x < 50')

    if not isinstance(data['address'], str) or len(data['address']) > 100:
        return Reply.bad_request(error='Invalid address. Address must be str and len must be x < 100')

    if not isinstance(data['number'], str) or not re.match('^(\s*)?(\+)?([- _():=+]?\d[- _():=+]?){10,14}(\s*)?$',
                                                           data['number']):
        return Reply.bad_request(error='Invalid number')

    shop_methods = methods.ShopMethods()
    shop = shop_methods.add_shop(models.Shop(
        name=data['name'],
        address=data['address'],
        number=data['number']
    ))

    return Reply.created(shop_id=shop.id)


@app.route('/shop/<shop_id>/add_items', methods=['PUT'])
@protected
def on_add_items(shop_id):
    data = request.json
    if not data:
        return Reply.bad_request(error='Empty json')

    if not isinstance(data, dict):
        return Reply.bad_request(error='Invalid json. It must be a dict.')

    try:
        shop_id = int(shop_id)
    except ValueError:
        return Reply.bad_request(error='Invalid shop id. It must be int.')

    _check = check_args_important(('items',), **data)
    if not _check[0]:
        return Reply.bad_request(error=f'Empty important {_check[1]} field passed')

    slots_methods = methods.SlotMethods()

    for item in data['items']:
        if not isinstance(item, dict):
            return Reply.bad_request(error='Invalid item. It must be dict')

        _check = check_args_important(('name', 'category', 'count'), **item)
        if not _check[0]:
            return Reply.bad_request(error=f'Invalid item. {_check[1]} field is empty')

        if not isinstance(item['name'], str) or len(item['data']) > 100:
            return Reply.bad_request(error='Invalid item name')

        if not isinstance(item['category'], str) or len(item['category']) > 50:
            return Reply.bad_request(error='Invalid item category')

        if not isinstance(item['count'], int) or item['count'] > 2 ** 63 or item['count'] < 1:
            return Reply.bad_request(error='Invalid item count')

        slot = slots_methods.get_slots(name=item['name'].lower(), shop_id=shop_id)
        if slot:
            slot = slot[0]
            slot.count += item['count']
        else:
            slots_methods.add_slot(models.Slot(
                name=item['name'].lower(),
                description='From factory',
                price=randint(100, 1000000),
                category=item['category'],
                count=item['count'],
                shop_id=shop_id
            ))

    return Reply.created()


@app.route('/shop/<shop_id>/new_purchase', methods=['POST'])
def on_new_purchase(shop_id):
    p_api = PurchasesAPI()
    if not p_api.is_available():
        return Reply.failed_dependency(error='Purchases service is down')

    data = request.json
    if not data:
        return Reply.bad_request(error='Empty json')

    if not isinstance(data, dict):
        return Reply.bad_request(error='Invalid json. It must be a dict.')

    try:
        shop_id = int(shop_id)
        if not is_int_correct(shop_id):
            raise ValueError
    except ValueError:
        return Reply.bad_request(error='Invalid shop id. It must be int64 >= 0.')

    _check = check_args_important(('slot_id', 'count', 'user_id', 'method'), **data)
    if not _check[0]:
        return Reply.bad_request(error=f'Empty important {_check[1]} field passed')

    if not isinstance(data['slot_id'], int) or not is_int_correct(data['slot_id']):
        return Reply.bad_request(error='Invalid slot_id. It must be int64 >= 0.')
    elif not isinstance(data['count'], int) or not is_int_correct(data['count']):
        return Reply.bad_request(error='Invalid count. It must be int64 >= 0.')
    elif not isinstance(data['user_id'], int) or not is_int_correct(data['user_id']):
        return Reply.bad_request(error='Invalid user_id. It must be int64 >= 0.')
    elif not isinstance(data['method'], str):
        return Reply.bad_request(error='Invalid method. It must be str.')

    data['method'] = data['method'].lower().strip()
    if not is_method_correct(data['method']):
        return Reply.bad_request(error='Invalid payment method')

    shop_methods = methods.ShopMethods()
    slots_methods = methods.SlotMethods()
    trans_methods = methods.TransactionMethods()
    user_methods = methods.UserMethods()

    user = user_methods.get_users(id=data['user_id'])

    if not user:
        user_methods.add_user(models.User(id=data['user_id']))
    else:
        user = user[0]

    shop = shop_methods.get_shops(id=shop_id)

    if not shop:
        return Reply.not_found(error='Unknown shop id passed')

    shop = shop[0]
    slot = shop_methods.get_slot_by_id(shop, data['slot_id'])

    if not slot:
        return Reply.not_found(error='Unknown slot id passed')

    if slots_methods.buy_slot(slot, data['count']):
        if p_api.add_purchase(
                slot.name,
                slot.price * data['count'],
                data['user_id'],
                shop.id,
                data['method'],
                slot.category
        ) != 201:
            return Reply.failed_dependency(error='Purchases service is down')
        else:
            trans_methods.add_transaction(models.Transaction(
                user_id=data['user_id'],
                shop_id=shop_id,
                slot_id=slot.id,
                count=data['count'],
                total=slot.price * data['count'],
                ts=int(datetime.now(timezone('Europe/Moscow')).timestamp()),
                method=data['method']
            ))

            return Reply.ok()
    else:
        return Reply.failed_dependency(error='Not enough slots in the shop')


@app.route('/shop/<shop_id>/get_slots', methods=['GET'])
def on_get_purchase(shop_id):
    try:
        shop_id = int(shop_id)
        if not is_int_correct(shop_id):
            raise ValueError
    except ValueError:
        return Reply.bad_request(error='Invalid shop id. It must be int64 >= 0.')

    shop_methods = methods.ShopMethods()
    shop = shop_methods.get_shops(id=shop_id)

    if not shop:
        return Reply.not_found(error='Unknown shop id passed')

    shop = shop[0]

    return Reply.ok(result=[x.get_dict() for x in shop.slots])


@app.route('/shop/get_shops', methods=['GET'])
def on_get_shops():
    shop_methods = methods.ShopMethods()

    return Reply.ok(result=[x.get_dict() for x in shop_methods.get_shops()])
