from source.database import *
from . import app
from .utils import *
from flask import request
from datetime import datetime
from pytz import timezone


@app.route('/purchases', methods=['GET'])
def on_root():
    return Reply.ok()


@app.route('/purchases/new_purchase', methods=['POST'])
def on_new_purchase():
    data = request.json
    if not data:
        return Reply.bad_request(error='Empty json')

    if not isinstance(data, dict):
        return Reply.bad_request(error='Invalid json. It must be a dict.')

    _check = check_args_important(('name', 'total', 'user_id', 'shop_id', 'method'), **data)
    if not _check[0]:
        return Reply.bad_request(error=f'Empty important {_check[1]} field passed')

    items_methods = methods.ItemsMethods()
    purchase_methods = methods.PurchasesMethods()
    users_methods = methods.UsersMethods()

    if data.get('ts') and not isinstance(data.get('ts'), int):
        return Reply.bad_request(error='Invalid ts field. It must be int.')
    elif not isinstance(data['name'], str):
        return Reply.bad_request(error='Invalid name field. It must be str.')
    elif not isinstance(data['total'], int):
        return Reply.bad_request(error='Invalid total field. It must be int.')
    elif not isinstance(data['method'], str):
        return Reply.bad_request(error='Invalid method field. It must be str.')
    elif not isinstance(data['shop_id'], int):
        return Reply.bad_request(error='Invalid shop_id field. It must be int.')

    ts = data.get('ts') or int(datetime.now(timezone('Europe/Moscow')).timestamp())
    item = items_methods.get_item(name=data['name']) or items_methods.add_item(models.Item(data['name']))
    total = abs(data['total'])
    method = data.get('method')
    shop_id = data['shop_id']

    user = users_methods.get_user(id=data['user_id'])
    if not user:
        user = users_methods.add_user(models.User(id=data['user_id']))

    purchase = purchase_methods.add_purchase(models.Purchase(item.id, ts, total, user.id, shop_id, method))

    return Reply.created(purchase_id=purchase.id)


@app.route('/purchases/get_purchases', methods=['GET'])
def on_get_purchase():
    data = request.args
    if not data:
        return Reply.bad_request(error='Empty args')

    _check = check_args_non_important(('user_id', 'purchase_id'), **data)

    if not _check:
        return Reply.bad_request(error='Empty or invalid required query string params')

    purchase_methods = methods.PurchasesMethods()
    items_methods = methods.ItemsMethods()

    if data.get('user_id'):
        result = purchase_methods.get_purchases(user_id=data['user_id'])
    elif data.get('purchase_id'):
        result = purchase_methods.get_purchases(id=data['purchase_id'])
    else:
        return Reply.bad_request(error='Invalid args passed')

    if not result:
        return Reply.not_found()

    result = [x.get_dict() for x in result]
    for x in result:
        x['item'] = items_methods.get_item(id=x['item_id']).get_dict()
        del x['item_id']

    return Reply.ok(purchases=result)
