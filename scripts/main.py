from models.city import City
import json
from requests import request, Session

login_url = 'https://politicsandwar.com/login/'

with open('..\\env.json') as j:
    params = json.load(j)

with Session() as session:
    session.post(login_url, data=params)
    test_city = City()
    test_city.import_city_from_id(session, 369356)


