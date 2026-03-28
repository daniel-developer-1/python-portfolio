from fastapi import FastAPI, Depends, HTTPException, status
from typing import List
from database import get_db, engine
from sqlalchemy.orm import Session
import models
import schemas
import crud

models.Base.metadata.create_all(bind=engine)

model_tags = [
    {"name": "root"},
    {"name": "get"},
    {"name": "post"},
    {"name": "put"},
    {"name": "delete"}
]

app = FastAPI(
    title="Mi_API_6.4",
    description="Prueba",
    version="1.4.0",
    openapi_tags=model_tags
)


@app.get("/", tags=["root"])
def get_root():
    return {"Message": "Welcome to my API"}


@app.get("/users", response_model=List[schemas.UserResponse], tags=["get"])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip, limit)
    return users


@app.get("/user/id/{user_id}", response_model=schemas.UserResponse, tags=["get"])
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, user_id)
    return user


@app.get("/user/email/{user_email}", response_model=schemas.UserResponse, tags=["get"])
def get_user_by_email(user_email: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, user_email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@app.post("/user/create", response_model=schemas.UserResponse, tags=["post"])
def create_user(new_user: schemas.UserCreate, db: Session = Depends(get_db)):
    user = crud.user_create(db, new_user)
    return user


@app.put("/user/update/{user_id}", response_model=schemas.UserResponse, tags=["put"])
def update_user(user_id: int, user_update_data: schemas.UserUpdate, db: Session = Depends(get_db)):
    user_updated = crud.user_update(db, user_id, user_update_data)
    return user_updated


@app.delete("/user/delete/{user_id}", tags=["delete"])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_deleted = crud.user_delete(db, user_id)
    return user_deleted
