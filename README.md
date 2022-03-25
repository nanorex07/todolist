# todolist

### Add .env file with following variables
  - SECRET_KEY=JWT_TOKEN_SECRET_KEY
  - ALGORITHM=HS256
  - ACCESS_TOKEN_EXPIRE_MINUTES=<access token expire minutes> like 1440
  - MONGO_URI=<mongo db url>
  - DB_NAME=<database name> like FastAPI-Todo
  
### To run locally

`
  uvicorn app.main:app
`
  
