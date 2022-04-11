from datetime import datetime, timedelta
import logging
from fastapi import HTTPException, Header
import jwt
import config
from common.error_codes import INVALID_OR_MISSING_TOKEN, EXPIRED_TOKEN
from persistence.models import UserFromDb
from persistence.dbaccess import database

def access_token(user: UserFromDb):
    exp_time = datetime.now() + timedelta(minutes=30)
    key = config.JWT_PRIVATE_KEY
    token_data = {
        "exp": datetime.timestamp(exp_time),
        'user_id': user.id,
        'user_name': user.username,
        'company_id': user.company_id,
        'team_id': user.team_id,
        'access': user.access
    }
    encoded_jwt = jwt.encode(
        token_data, 
        key, 
        algorithm="RS256"
        )
    return encoded_jwt

def check_token(token: str):
    try:
        decoded = jwt.decode(token, config.JWT_PUBLIC_KEY, algorithms=["RS256"])
    except Exception:
        raise HTTPException(status_code=400, detail=EXPIRED_TOKEN)
    if decoded["exp"] < datetime.timestamp(datetime.now()):
        raise HTTPException(status_code=400, detail=EXPIRED_TOKEN)
    return {
        'valid': True,
        'token_data': decoded
    }


class TokenRequired:

    @staticmethod
    async def user_active(X_Authentication_Token: str = Header(None)):
        try:
            data = check_token(X_Authentication_Token)
            #Retrieve user from db and return it as dict
            user_object = await database.retrieve('users', {"_id":data["token_data"]["user_id"]})
            return user_object
        except Exception as ex:
            logging.exception(ex)
            raise HTTPException(status_code=400, detail=INVALID_OR_MISSING_TOKEN)

    @staticmethod
    async def has_permission(
        app: str = None, 
        company: str = None,
        action: str = None,
        X_Authentication_Token: str = Header(None),
        ):
        try:
            data = check_token(X_Authentication_Token)
            user_object = await database.retrieve('users', {"_id":data.token_data.user_id})
            return user_object
        except Exception:
            raise HTTPException(status_code=401, detail=INVALID_OR_MISSING_TOKEN)

