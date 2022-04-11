import logging
from passlib.context import CryptContext
from fastapi import HTTPException
from persistence.models import UserFromDb
from common.error_codes import INVALID_CREDENTIALS
from common.token_module import access_token
from persistence.dbaccess import database

async def get_user(username: str):
    user_result = await database.retrieve('users', {"username": username})
    if user_result:
        return UserFromDb(**user_result)
    else:
        return None

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto", sha256_crypt__default_rounds=12000)

def hash_password(password: str) -> str:
    pass_hash = pwd_context.hash(password)
    return pass_hash

def verify_password(plain_password: str, hashed_password: str):
    password_hash = hashed_password
    return pwd_context.verify(plain_password, password_hash)

async def authenticate_user(username: str, password: str):
    user = await get_user(username)
    if user: 
        success = verify_password(password, user.password_hash)
        if success:
            data = {
                'success': True,
                'access_token': access_token(user)
            }
            return data
        else:
            raise HTTPException(status_code=400, detail=INVALID_CREDENTIALS)
    else:
        raise HTTPException(status_code=400, detail=INVALID_CREDENTIALS)
