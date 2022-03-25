from fastapi import HTTPException, status, Depends, APIRouter
from ..schemas import Todo, TodoOut
from ..database import todo_db
from .. import oauth2
from ..utils import bsonToJson, jsonToBson
from typing import List

router = APIRouter(
    prefix="/api/todos",
    tags = ["Todos"]
)

@router.get("/", response_model=List[TodoOut])
async def get_todos(current_user: int = Depends(oauth2.get_current_user)):
    listout = []
    cluster = todo_db.find({"user": bsonToJson(current_user['_id'])})
    async for doc in cluster:
        listout.append(doc)
    return listout

@router.get("/{id}", response_model=TodoOut)
async def get_todo(id: str, current_user: int = Depends(oauth2.get_current_user)):
    
    todo = await todo_db.find_one({"_id": jsonToBson(id)})
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo with id {id} does not exist.")
    if todo["user"] != bsonToJson(current_user["_id"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform the requested action.")
        
    return todo

@router.post("/",status_code=status.HTTP_201_CREATED, response_model=TodoOut)
async def add_todo(todo: Todo, current_user : int = Depends(oauth2.get_current_user)):
    td = todo.dict()
    td["user"] = bsonToJson(current_user["_id"])
    res = await todo_db.insert_one(td)
    return td

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(id: str, current_user: int = Depends(oauth2.get_current_user)):
    todo = await todo_db.find_one({"_id": jsonToBson(id)})
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo with id {id} does not exist.")
    if todo["user"] != bsonToJson(current_user["_id"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform the requested action.")
   
    await todo_db.delete_one({"_id": jsonToBson(id)})


@router.put("/{id}", response_model=TodoOut)
async def update_todo(up_todo: Todo, id: str, current_user: int = Depends(oauth2.get_current_user)):
    todo = await todo_db.find_one({"_id": jsonToBson(id)})
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo with id {id} does not exist.")
    if todo["user"] != bsonToJson(current_user["_id"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform the requested action.")
   
    await todo_db.update_one({"_id": jsonToBson(id)}, {"$set": {"desc": up_todo.desc, "completed": up_todo.completed}})

    return await todo_db.find_one({"_id": jsonToBson(id)})