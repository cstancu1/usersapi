import datetime
import logging
import uuid
from persistence.dbaccess import database
from common.error_codes import ERROR_REGISTER_USER,\
    USERNAME_IN_USE, ERROR_REGISTER_USER, ERROR_RETRIEVE_PROFILE
from fastapi.exceptions import HTTPException
from common import auth, utils

async def create_profile(username, user_id, company_id, team_role,
                         team_id, full_name, company_role):
    profile_object = {
        "username": username,
        "user_id":  user_id,
        "company_id": company_id,
        "team_id": team_id,
        "full_name": full_name,
        "company_role": company_role,
        "team_role": team_role,
        "phone": None,
        "_id": str(uuid.uuid4())
    }

    profile = await database.insert_data("profiles", profile_object)
    return profile.inserted_id

async def self_register_user(user: dict):
    try:
        existing_username = await database.retrieve("users", {"username": user.username})
        if existing_username:
            return HTTPException(status_code=400, detail=USERNAME_IN_USE)
        user_object = {
            "password_hash": auth.hash_password(user.password),
            "_id": str(uuid.uuid4()),
            "username": user.username,
            "company_id": str(uuid.uuid4()),
            "team_id": str(uuid.uuid4()),
            "access": [{"general":"owner"}],
            "full_name": user.full_name,
            "disabled": False,
            "created" : datetime.datetime.now(),
        }
        created_user = await database.insert_data("users", user_object)
        created_profile_id = await create_profile(user.username,
                                          created_user.inserted_id, 
                                          user_object["company_id"],
                                          "owner", 
                                          user_object["team_id"],
                                          user_object["full_name"],
                                          "owner")

        #IMPLEMENT TEAM AND COMPANY CREATION IF OWNER
        return {    
            "success":True,
            "data": {
                "username": user.username,
                "user_id": created_user.inserted_id,
                "profile_id": created_profile_id
            }
        }
    except Exception as ex:
        logging.info("[*] Error creating user!")
        logging.exception(ex)
        raise HTTPException(status_code=500, detail=ERROR_REGISTER_USER)

async def add_user(user:dict):
    password = utils.gen_random_password(user.username)
    user_object = {
        "password_hash": auth.hash_password(password),
        "_id": str(uuid.uuid4()),
        "username": user.username,
        "company_id": user.company_id,
        "team_id": user.team_id,
        "access": user.access
    }  
    try:
        existing_username = await database.retrieve("users", {"username": user.username})
        if existing_username:
            raise HTTPException(status_code=400, detail=USERNAME_IN_USE)
        result = await database.insert_data("users", user_object)
        return {
            "success":True,
            "data": {
                "username": user.username,
                "id": result.inserted_id
            }
        }
    except Exception:
        raise HTTPException(status_code=500, detail=ERROR_REGISTER_USER)

async def get_user_profile(user_id: str):
    try:
        profile = await database.retrieve("profiles", {"user_id": user_id})
        if profile:
            return profile
        return None
    except Exception:
       raise HTTPException(status_code=500, detail=ERROR_RETRIEVE_PROFILE) 