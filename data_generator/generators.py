from faker import Faker
from faker_credit_score import CreditScore

from random import random,randint

from datetime import datetime

import yaml

faker = Faker()
faker.add_provider(CreditScore)
class FakeCreditGenerator:
    def __init__(self):
        self.odds = self._read_odds_file()

    def _read_odds_file(self):
        with open('./data_generator/odds.yaml','r') as f:
            return yaml.load(f)
    
    def _pick_random_columns(self,columns: dict):
            
        picked_columns = {}

        for key, item in columns.items():
            
            if self.odds['not_coming_odd'] < random():
                if self.odds['null_odd'] < random():
                    if isinstance(columns[key],dict):
                        picked_columns[key] = self._pick_random_columns(columns[key])
                    elif isinstance(columns[key],list):
                        picked_columns[key] = [self._pick_random_columns(x) if isinstance(x,dict) else x for x in columns[key]]
                    else:
                        picked_columns[key] = item
                else:
                    if isinstance(columns[key],dict):
                        picked_columns[key] = self._pick_random_columns(columns[key])
                    elif isinstance(columns[key],list):
                        picked_columns[key] = [self._pick_random_columns(x) for x in columns[key] if isinstance(x,dict)]
                    else:
                        picked_columns[key] = None

        return picked_columns
    
    def _return_variable_columns(self):
        return {
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
    
    def _return_base_columns(self):
        return {
            'Spec':'@1.0.1',
            '_ID':faker.pyint()
        }
    
    def generate_row(self):
        
        base_columns = self._return_base_columns()

        variable_columns = self._return_variable_columns()

        picked_columns = self._pick_random_columns(variable_columns)

        columns = {**base_columns,**picked_columns}

        return columns
