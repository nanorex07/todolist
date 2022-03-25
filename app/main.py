from fastapi import FastAPI
from .routers import user, auth, todo
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials= True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(todo.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def home():
    return {"message": " /docs for documentation "}