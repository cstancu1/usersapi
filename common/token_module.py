from datetime import datetime, timedelta
from fastapi import HTTPException, Header
import jwt
import config
from common.error_codes import INVALID_OR_MISSING_TOKEN, EXPIRED_TOKEN
from persistence.models import UserFromDb

def access_token(user: UserFromDb):
    exp_time = datetime.now() + timedelta(minutes=30)
    key = config.JWT_PRIVATE_KEY
    token_data = {
        "exp": datetime.timestamp(exp_time),
        'user_id': user.id,
        'user_name': user.username,
        'company_id': user.company_id,
        'team_id': user.team_id
    }
    encoded_jwt = jwt.encode(
        token_data, 
        key, 
        algorithm="RS256"
        )
    return encoded_jwt

def check_token(token: str):
    decoded = jwt.decode(token, config.JWT_PUBLIC_KEY, algorithms=["RS256"])
    if decoded["exp"] < datetime.timestamp(datetime.now()):
        raise HTTPException(status_code=400, detail=EXPIRED_TOKEN)
    return {
        'valid': True,
        'token_data': decoded
    }


class TokenRequired:

    @staticmethod
    def user_active(X_Authentication_Token: str = Header(None)):
        try:
            data = check_token(X_Authentication_Token)
            return data
        except Exception:
            raise HTTPException(status_code=400, detail=INVALID_OR_MISSING_TOKEN)

    @staticmethod
    def has_permission(
        app: str = None, 
        action: str = None,
        X_Authentication_Token: str = Header(None),
        ):
        try:
            data = check_token(X_Authentication_Token)
            return data
        except Exception:
            raise HTTPException(status_code=401, detail=INVALID_OR_MISSING_TOKEN)
