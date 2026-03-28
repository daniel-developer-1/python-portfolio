from sqlalchemy.orm import Session
import models
import schemas
from fastapi import HTTPException, status


def get_users(db: Session, skip: int = 0, limit: int = 100):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users


def get_user_by_id(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


def get_user_by_email(db: Session, user_email: str):
    user = db.query(models.User).filter(
        models.User.email == user_email).first()
    return user


def user_create(db: Session, new_user: schemas.UserCreate):
    email_existing = get_user_by_email(db, new_user.email)

    if email_existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )
    user = models.User(**new_user.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def user_update(db: Session, user_id: int, user_update_data: schemas.UserUpdate):
    user_existing = get_user_by_id(db, user_id)
    if not user_existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if user_update_data.email:
        email_existing = get_user_by_email(db, user_update_data.email)
        if email_existing and email_existing.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )

    update_data = user_update_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if hasattr(user_existing, field):
            setattr(user_existing, field, value)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="This field not found"
            )

    db.commit()
    db.refresh(user_existing)
    return user_existing


def user_delete(db: Session, user_id: int):
    user_existing = get_user_by_id(db, user_id)
    if not user_existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    db.delete(user_existing)
    db.commit()
    return {"Message": "User deleted successfully"}
