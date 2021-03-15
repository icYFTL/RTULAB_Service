from source.api import *
from time import sleep

sleep(2)  # Avoid " the database system is starting up"

app.run('0.0.0.0', 8001, False)