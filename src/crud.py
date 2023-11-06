from typing import Annotated
from sqlalchemy.orm import Session

from . import models, schemas, utils

def get_user(db: Session, user_id: int):
    """Return user with matching ID. """

    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    """Return user with matching username."""

    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    """Return user with matching email."""

    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    """Get users from database."""

    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    """Create a new user in the database. Automatically hashes the password."""

    hashed_pwd = utils.get_password_hash(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_pwd, alias = user.alias)
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except:
        db.rollback()
        raise Exception("Error while creating user")

def remove_user(db: Session, user_id: int):
    """Remove user from database."""

    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False