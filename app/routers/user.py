from .. import utils
from fastapi import HTTPException, status, Depends, APIRouter
from ..schemas import UserCreate, UserOut
from ..database import users_db
from datetime import datetime
from typing import List
from .. import oauth2

router = APIRouter(
    prefix="/api/users",
    tags = ["Users"]
)

@router.post("/",status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def add_user(user: UserCreate):
    exists = await users_db.find_one({"email": user.email})
    print(exists)
    if exists:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="User with that email already exists.")
    new_user = user.dict()
    new_user['created_at'] = datetime.utcnow()
    new_user['password'] = utils.hash(new_user['password'])
    res = await users_db.insert_one(new_user)
    return new_user

@router.get("/", response_model=List[UserOut])
async def get_users(current_user : int = Depends(oauth2.get_current_user)):
    listout = []
    cluster = users_db.find({})
    async for doc in cluster:
        listout.append(doc)
    return listout