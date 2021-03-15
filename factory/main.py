from source.api.rest import *
from source.static import *
from time import sleep

sleep(2)  # Avoid " the database system is starting up"

factory_obj.start()
provider_obj.start()

app.run('0.0.0.0', 8003, False)