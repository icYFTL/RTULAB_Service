from source.api.rest import *
from time import sleep

sleep(2)  # Avoid " the database system is starting up"

app.run('0.0.0.0', 8002, False)