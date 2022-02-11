from sqlalchemy.orm import Session
from schemas.users import UserCreate
from db.models.users import User


def create_new_user(user: UserCreate, db: Session):
    user = User(username=user.username, is_active=True)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
