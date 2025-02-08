from api_server.app.db import database, models

users =  sorted(database.generate_user_db(), key=lambda d: d['id']) #always return sorted by id
companies = database.generate_company_db()

#user
def all_users():
    return users

def user_by_id(id: int):
    for user in users:
        print("user: ", user)
        if user['id'] == id:
            return user
    return {}

def add_new_user(user: models.User):
    new_id = users[-1]['id'] + 1
    new_user = {
        "id": new_id,
        "name": user.name,
        "email": user.email
    }
    return users.append(new_user)

def delete_user(id: int):
    if id <= 0:
        raise IndexError
    try:    
        for user in users:
            if user['id'] == id:
                users.remove(user)
    except:
        raise

#company
def all_companies():
    return companies

def company_by_id(id: int):
    for company in companies:
        if company['id'] == id:
            return company
    return {}

def add_new_company(company: models.Company):
    new_id = companies[-1]['id'] + 1
    new_company = {
        "id": new_id,
        "name": company.name,
        "userId": company.userId
    }
    return companies.append(new_company)

def delete_company(id: int):
    if id <= 0:
        raise IndexError
    try:    
        for company in companies:
            if company['id'] == id:
                companies.remove(company)
    except:
        raise


