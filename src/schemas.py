import datetime
from pydantic import BaseModel, validator, ValidationError

class UserBase(BaseModel):
    username: str
    email: str
    alias: str    

class UserCreate(UserBase):
    password: str

    @validator("password")
    def password_secure(cls, v):
        if len(v) < 8:
            raise ValueError('password must be at least 8 characters')
        if not any(char.isdigit() for char in v):
            raise ValueError('password must contain at least one digit')
        if not any(char.isalpha() for char in v):
            raise ValueError('password must contain at least one letter')
        if not any(char.isupper() for char in v):
            raise ValueError('password must contain at least one uppercase letter')
        if not any(char.islower() for char in v):
            raise ValueError('password must contain at least one lowercase letter')
        return v

class User(UserBase):    
    id: int
    ts_created: datetime.datetime
    ts_last_login: datetime.datetime
    is_active: bool

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
