from email.policy import default
from faker import Faker
import json
from random import random,randint
import decimal
from datetime import datetime
from multiprocessing import Pool
faker = Faker()

odds = {'null':0.05,"not_comming":0.05}

def odds_columns(columns: dict):

    result = {}

    for key, item in columns.items():

        if odds['not_comming'] < random():
            if odds['null'] < random():
                if isinstance(columns[key],dict):
                    result[key] = odds_columns(columns[key])
                elif isinstance(columns[key],list):
                    result[key] = [odds_columns(x) if isinstance(x,dict) else x for x in columns[key]]
                else:
                    result[key] = item
            else:
                if isinstance(columns[key],dict):
                    result[key] = odds_columns(columns[key])
                elif isinstance(columns[key],list):
                    result[key] = [odds_columns(x) for x in columns[key] if isinstance(x,dict)]
                else:
                    result[key] = None

    
    return result

resultados = []

iterations = [i for i in range(10)]

def generate_data():

    base_columns = {
        'Spec':'@1.0.1',
        '_ID':faker.pyint()
    }

    profile = faker.profile()

    variable_columns = {
        'events':[
            {'user_agent':faker.user_agent(),
            'event_time':datetime.now(),
            'first_time':faker.boolean(),
            'ipv4':faker.ipv4(),
            'uris':[faker.uri() for x in range(randint(1,6))]}
        for x in range(randint(1,10))],
        'father':faker.profile(),
        'mother':faker.profile()
    }

    profile.update(variable_columns)

    result = odds_columns(profile)

    base_columns.update(result)

    return base_columns

for i in range(1000):

    print(i)

    resultados.append(generate_data())


with open('result.json','w') as file:
    file.write(json.dumps(resultados,indent=2,default=str))

'''
data = []

nested_struct = {
    ""
}

_json = {
    "name":faker.name(),
    "address":faker.address(),
}

data.append(_json)

print(random())



'''