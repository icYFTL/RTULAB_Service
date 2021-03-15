from source.api.rest import *
from source.static import *
from time import sleep
from core import production

sleep(2)  # Avoid " the database system is starting up"

for category in list(production):
    _fac = Factory(category)
    factory_objs.append(_fac)
    _fac.start()

provider_obj.start()

app.run('0.0.0.0', 8003, False)
