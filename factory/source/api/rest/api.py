from . import app
from .utils import *
from source.static import *


@app.route('/', methods=['GET'])
def on_root():
    return Reply.ok()


@app.route('/factory/status', methods=['GET'])
def on_status():
    return Reply.ok(status=factory_obj.status)