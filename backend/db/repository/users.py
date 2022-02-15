from sqlalchemy.orm import Session
from schemas_pyd.users import UserCreate
from db.models.users import User


def create_new_user(user: UserCreate, db: Session):
    utente_db = User(**user.dict())
    db.add(utente_db)
    db.commit()
    db.refresh(utente_db)
    return utente_db
