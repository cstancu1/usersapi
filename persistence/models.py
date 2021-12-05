from datetime import datetime
from typing import Optional
from pydantic import BaseModel

####################################
# # # Object models
####################################
class Subscriptions(BaseModel):
    user_id: str
    valid_until: str
    application: str
    level: int

class Company(BaseModel):
    name: str
    created: str
    owner_id: str
    active_subscription: str

class Team(BaseModel):
    name: str
    description: Optional[str]
    company_id: str
    created: str
    owner_id: str

class ProfileHistory(BaseModel):
    username: str
    company_id: str
    full_name: Optional[str]
    disabled: bool
    created: str
    company_role: str
    team_role: str
    team_id: str
    phone: Optional[str]
    created: datetime

class Profile(BaseModel):
    username: str
    company_id: str
    full_name: Optional[str]
    disabled: bool
    created: str
    company_role: str
    team_role: str
    team_id: str
    phone: Optional[str]
    last_update: datetime
    updated_by: str

class UserFromDb(BaseModel):
    password_hash: str
    id: str
    username: str
    company_id: str
    team_id: str
    last_active: Optional[datetime]