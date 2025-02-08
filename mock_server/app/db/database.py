import json
import random

def generate_user_db():
    with open('api_server/data/users.json') as stream:
        return json.load(stream)

def generate_company_db():
    with open('api_server/data/companies.json') as stream:
        return json.load(stream)




