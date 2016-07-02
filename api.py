from eve import Eve
from eve_mongoengine import EveMongoengine

# init application
from public.models import *
from user.models import User

MONGODB_SETTINGS = {

    # 'MONGO_HOST': 'localhost',
    #     'MONGO_PORT': 27017,
    #     'MONGO_USERNAME' : None,
    # 'MONGO_PASSWORD': None,
    'MONGO_DBNAME': 'ashrm3',
    'X_DOMAINS': '*',
    'ALLOW_OVERRIDE_HTTP_METHOD':'true',
    'JSON_SORT_KEYS	':'true',
                   'DOMAIN': {'resident': {}}
}

app = Eve(settings=MONGODB_SETTINGS)
# init extension
ext = EveMongoengine(app)
# register model to eve
ext.add_model(Resident)
ext.add_model(BusRoute)
ext.add_model(Transportation)
ext.add_model(Hostel)
ext.add_model(HostelRoom)
ext.add_model(User)
ext.add_model(Subject)
ext.add_model(Teacher)
ext.add_model(ClassRoom)
ext.add_model(BusStop)
ext.add_model(Driver)
ext.add_model(Conveyance)



# let's roll
app.run(host='127.0.0.1', port=8001)
