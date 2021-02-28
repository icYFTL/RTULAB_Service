from source.database import *
from . import app
from .utils import *
from flask import request
from datetime import datetime
from pytz import timezone


@app.route('/', methods=['GET'])
def on_root():
    return Reply.ok()


@app.route('/new_purchase', methods=['POST'])
def on_new_purchase():
    data = request.json
    _check = check_args_important(('name', 'total'), **data)
    if not _check[0]:
        return Reply.bad_request(error=f'Empty important \'{_check[1]}\' field passed')

    items_methods = methods.ItemsMethods()
    purchase_methods = methods.PurchasesMethods()

    if data.get('ts') and not isinstance(data.get('ts'), int):
        return Reply.bad_request(error='Invalid \'ts\' field. It must be int.')
    elif not isinstance(data['name'], str):
        return Reply.bad_request(error='Invalid \'name\' field. It must be str.')
    elif not isinstance(data['total'], int):
        return Reply.bad_request(error='Invalid \'total\' field. It must be int.')

    ts = data.get('ts') or int(datetime.now(timezone('Europe/Moscow')).timestamp())
    item = items_methods.get_item(name=data['name']) or items_methods.add_new_item(models.Item(data['name']))
    total = data['total']

    purchase = purchase_methods.add_new_purchase(models.Purchase(item.id, ts, total))

    return Reply.created(id=purchase.id)


@app.route('/get_purchase', methods=['GET'])
def on_get_purchase():
    data = dict(request.args)
    _check = check_args_important(('id',), **data)
    if not _check[0]:
        return Reply.bad_request(error=f'Empty important \'{_check[1]}\' field passed')

    purchase_methods = methods.PurchasesMethods()

    try:
        data['id'] = int(data['id'])
    except:
        return Reply.bad_request(error='Invalid \'id\' field. It must be int.')

    purchase = purchase_methods.get_purchase(id=data['id'])
    if not purchase:
        return Reply.not_found(error='Unknown id passed')

    result = purchase.get_dict()
    result['item'] = purchase.item.get_dict()  # Up to the next refactoring
    del result['item_id']  # Ok, ok... Don't kick me

    return Reply.ok(result=result)
