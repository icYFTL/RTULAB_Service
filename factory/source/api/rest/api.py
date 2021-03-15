from . import app
from .utils import *
from source.static import *
from flask import request


@app.route('/', methods=['GET'])
def on_root():
    return Reply.ok()


@app.route('/factory/status', methods=['GET'])
def on_factory_status():
    return Reply.ok(state=factory_obj.state, status=factory_obj.status)


@app.route('/provider/status', methods=['GET'])
def on_provider_status():
    return Reply.ok(state=provider_obj.state, status=provider_obj.status, unsynced=provider_obj.unsynced)


@app.route('/provider/toggle', methods=['PATCH'])
def on_provider_toggle():
    data = request.json

    if not data:
        return Reply.bad_request(error='Empty json')

    if not data.get('state') or data.get('state') not in ['on', 'off']:
        return Reply.bad_request()

    if data['state'] == 'on':
        if not provider_obj.lock.locked():
            return Reply.bad_request(error='Provider is already running')
        provider_obj.lock.release()

    elif data['state'] == 'off':
        if provider_obj.lock.locked():
            return Reply.bad_request(error='Provider is already down')
        provider_obj.lock.acquire()

    else:
        return Reply.bad_request(error='Invalid state')

    return Reply.ok()


@app.route('/factory/toggle', methods=['PATCH'])
def on_factory_toggle():
    data = request.json

    if not data:
        return Reply.bad_request(error='Empty json')

    if not data.get('state') or data.get('state') not in ['on', 'off']:
        return Reply.bad_request()

    if data['state'] == 'on':
        if not factory_obj.lock.locked():
            return Reply.failed_dependency(error='Factory is already running')
        factory_obj.lock.release()

    elif data['state'] == 'off':
        if factory_obj.lock.locked():
            return Reply.failed_dependency(error='Factory is already down')
        factory_obj.lock.acquire()

    else:
        return Reply.bad_request(error='Invalid state')

    return Reply.ok()
