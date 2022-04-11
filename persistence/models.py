from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class Subscription(BaseModel):
    company_id: str
    user_id: str
    valid_until: str
    application: str
    level: int
    id: str = Field( alias="_id")

class UserHistory(BaseModel):
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
    user_id: str
    id: str = Field( alias="_id")

class Team(BaseModel):
    name: str
    description: Optional[str]
    modules: list
    company_id: str
    created: str
    owner_id: str
    id: str = Field( alias="_id")
    members: list[dict]

class Company(BaseModel):
    name: str
    created: str
    owner_id: str
    active_subscription: str
    id: str = Field( alias="_id")
    teams: list[Team]
    subscriptions: list[Subscription]

class UserFromDb(BaseModel):
    password_hash: str
    id: str = Field( alias="_id")
    username: str
    company_id: str
    last_active: Optional[datetime]
    full_name: str
    disabled: bool
    created: datetime
    team_id: str
    phone: Optional[str]
    last_update: Optional[datetime]
    updated_by: Optional[str]
    access: list[str]

class UserRegisterSchema(BaseModel):
    password: Optional[str]
    username: str
    full_name: str
    company_id: Optional[str]
    team_id: Optional[str]
    access: list[dict]