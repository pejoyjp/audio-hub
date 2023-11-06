from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session
from typing import Annotated
from typing import Union
from . import crud, models, schemas, utils
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/hello/{name}")
async def say_hello(name:str):
    return {"message":f"Hello{name}"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#################### ENDPOINTS ####################

@app.post("/users", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    if not user.alias or len(user.alias) == 0:
        user.alias = user.username
    return crud.create_user(db=db, user=user)

@app.post('/login', response_model=schemas.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

   user = crud.get_user_by_username(db=db, username = form_data.username)

   if not user:
       raise HTTPException(status_code=404, detail="User not found")

   if not utils.verify_password(form_data.password, user.hashed_password):
       raise HTTPException(status_code=401, detail="Invalid username or password")

   return {
        "access_token": utils.create_access_token(user.username),
        "refresh_token": utils.create_refresh_token(user.username),
        "token_type": "bearer"
    }
