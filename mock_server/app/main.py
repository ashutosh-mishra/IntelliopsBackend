"""
This is the main entrypoint
"""
from fastapi import FastAPI, HTTPException, status

from .db import models
from .api import api

VERSION=1.0
app = FastAPI()


@app.get("/", status_code=status.HTTP_200_OK)
def root():
    """Return OK"""
    return "ok"

@app.get("/status", status_code=status.HTTP_200_OK)
def get_status():
    """Return status"""
    return {"status":"healthy", "version":VERSION}

#Users
@app.get("/users")
def get_users():
    """Return all the users in the DB"""
    return api.all_users()

@app.get("/users/{user_id}")
def get_user(user_id: int):
    """Return the user by its ID"""
    req = api.user_by_id(user_id)
    if req != {}:
        return req
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="Store not found")

@app.post("/users", status_code=status.HTTP_201_CREATED)
def add_user(user: models.User):
    """Add a user to the DB"""
    try:
        api.add_new_user(user)
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=err) from None


@app.delete("/users/{user_id}", status_code=status.HTTP_201_CREATED)
def delete_user(user_id: int):
    """Delete user from the DB"""
    try:
        api.delete_user(user_id)
    except IndexError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="user not found") from None
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=err) from None


#Companies
@app.get("/companies")
def get_companies():
    """Return all the companies in the DB"""
    return api.all_companies()

@app.get("/companies/{company_id}")
def get_company(company_id: int):
    """Return the company by its ID"""
    req = api.company_by_id(company_id)
    if req != {}:
        return req
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="Store not found")

@app.post("/companies", status_code=status.HTTP_201_CREATED)
def add_company(company: models.Company):
    """Add a company to the DB"""
    try:
        api.add_new_company(company)
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=err) from None


@app.delete("/companies/{company_id}", status_code=status.HTTP_201_CREATED)
def delete_company(company_id: int):
    """Delete company from the DB"""
    try:
        api.delete_company(company_id)
    except IndexError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="company not found") from None
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=err) from None
