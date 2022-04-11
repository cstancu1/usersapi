from fastapi import Depends, FastAPI
from pydantic import BaseModel

from common import auth
from common.token_module import TokenRequired
from persistence.models import UserFromDb, UserRegisterSchema
from services.user_service import add_user, self_register_user, get_user_profile

profiles_router = FastAPI()

class UserLoginCredentials(BaseModel):
    username:str
    password:str

@profiles_router.post('/token/')
async def login_user(user_details: UserLoginCredentials):
    #further security chechs

    result = await auth.authenticate_user(
        user_details.username,
        user_details.password
    )
    
    return result

@profiles_router.get('/test-token-restricted/')
def test_token_restricted(
    current_user: UserFromDb = Depends(TokenRequired.user_active)
    ):
    return {
        "success": True,
        "data": current_user
    }

@profiles_router.get('/permission/{app}/{company}/{action}')
def test_permission(
    current_user: UserFromDb = Depends(TokenRequired.has_permission)
    ):
    return {
        "success":True
    }

@profiles_router.post('/user/register/')
async def register_user(user: UserRegisterSchema):
    registered_user = await self_register_user(user)
    return registered_user

@profiles_router.post('/user/create/')
async def create_user(
    user: UserRegisterSchema,
    current_user: UserFromDb = Depends(TokenRequired.user_active)
    ):
    return add_user(user)

@profiles_router.get('/')
async def get_profile(
    current_user: UserFromDb = Depends(TokenRequired.user_active)
    ):
    del current_user['password_hash']
    user_profile = await get_user_profile(current_user['_id'])
    current_user['company_role'] = user_profile['company_role']
    current_user['team_role'] = user_profile['team_role']
    return{
        'success': True,
        'data': current_user
    }
