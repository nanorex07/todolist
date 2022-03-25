from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from bson.objectid import ObjectId

class PyObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')


class Todo(BaseModel):
    desc: str
    completed: bool = False

class TodoOut(Todo):
    id: Optional[PyObjectId] = Field(alias='_id')
    user: str
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        } 

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime
    email: EmailStr
    class Config:
        json_encoders = {ObjectId: str}
        orm_mode = True

class Token(BaseModel):
    access_token: str 
    token_type: str 

class TokenData(BaseModel):
    id: Optional[str] = None
    