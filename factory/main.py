from source.api.rest import *
from source.static import *

factory_obj.start()
provider_obj.start()

app.run('localhost', 8003, False)