from passlib.context import CryptContext
from fastapi import HTTPException
from persistence.models import UserFromDb
from common.error_codes import INVALID_CREDENTIALS
from common.token_module import access_token

fake_users_db = {
    "johndoe": {
        "password_hash": "$5$rounds=32000$DknHY2mDgrnFV6Pr$YMcE3fu8E0hFlZAVODySDVtxS2OYYTVjCWuPHUITYF8",
        "id": "123",
        "username": "claudiustancu@outlook.com",
        "company_id": "rqt23yt4w4g",
        "team_id": "ateyh423yh"
    }
}

def get_user(username: str):
    if username in fake_users_db:
        user_dict = fake_users_db[username]
        return UserFromDb(**user_dict)

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto", sha256_crypt__default_rounds=12000)

def verify_password(plain_password: str, hashed_password: str):
    password_hash = hashed_password
    return pwd_context.verify(plain_password, password_hash)

def authenticate_user(username: str, password: str):
    user = get_user(username)
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
