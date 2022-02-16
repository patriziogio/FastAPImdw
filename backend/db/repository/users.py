from sqlalchemy.orm import Session
from schemas_pyd.users import UserCreate
from db.models.users import User


def create_new_user(user: UserCreate, db: Session):
    user_db = User(**user.dict())
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db


def retrieve_users(db: Session) -> list[UserCreate]:
    # db.query() è la select, con .all() ho i dati
    users_db = db.query(User).all()
    return users_db
