from email.policy import default
from faker import Faker
from faker_credit_score import CreditScore
import json
from random import random,randint
import decimal
from datetime import datetime
from multiprocessing import Pool
faker = Faker()
faker.add_provider(CreditScore)

odds = {'null':0.10,"not_comming":0.05}

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

def generate_data():

    base_columns = {
        'Spec':'@1.0.1',
        '_ID':faker.pyint()
    }

    variable_columns = {
        'email':faker.email(),
        'track':{
            'ipv4':faker.ipv4(),
            'user_agent':faker.user_agent(),
            'event_time':datetime.now(),
        },
        'credit_score':{
            'score':faker.credit_score(),
            'score_provider':faker.credit_score_provider(),
            'score_date':datetime.now(),
        },
        'conversion':faker.boolean(),
        'first_time':faker.boolean(),
        'source':[faker.uri() for x in range(randint(1,3))]
        
    }

    result = odds_columns(variable_columns)

    base_columns.update(result)

    return base_columns

for i in range(100):

    print(i)

    resultados.append(generate_data())


with open('result.json','w') as file:
    file.write(json.dumps(resultados,indent=2,default=str))
