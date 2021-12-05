from fastapi import Depends, FastAPI
from pydantic import BaseModel

from common import auth
from common.token_module import TokenRequired
from persistence.models import UserFromDb

profiles_router = FastAPI()

class UserLoginCredentials(BaseModel):
    username:str
    password:str

@profiles_router.post('/token/')
def login_user(user_details: UserLoginCredentials):
    #further security chechs

    result = auth.authenticate_user(
        user_details.username,
        user_details.password
    )
    
    return result

@profiles_router.get('/test-token-restricted/')
def test_token_restricted(
    current_user: UserFromDb = Depends(TokenRequired.user_active)
    ):
    return current_user

@profiles_router.get('/permission/{app}/{action}')
def test_permission(
    current_user: UserFromDb = Depends(TokenRequired.has_permission)
    ):
    return current_user

@profiles_router.get('/')
def get_user_profile():
    return {'user':'profile'}