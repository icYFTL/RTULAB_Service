from . import app
from .utils import *
from source.static import *
from flask import request


@app.route('/factory/', methods=['GET'])
def on_root():
    return Reply.ok()


@app.route('/factory/self/status', methods=['GET'])
def on_factory_status():
    reply = []
    for obj in factory_objs:
        state = 'online' if obj.isAlive() else 'offline'
        reply.append({'category': obj.category, 'state': state, 'status': obj.status, 'defected': obj.defected})

    return Reply.ok(result=reply)


@app.route('/factory/provider/status', methods=['GET'])
def on_provider_status():
    state = 'online' if provider_obj.isAlive() else 'offline'
    return Reply.ok(state=state, status=provider_obj.status, unsynced=provider_obj.unsynced)


@app.route('/factory/provider/toggle', methods=['PATCH'])
def on_provider_toggle():
    return Reply.forbidden(error='Not implemented')
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


@app.route('/factory/self/toggle', methods=['PATCH'])
def on_factory_toggle():
    return Reply.forbidden(error='Not implemented')
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
