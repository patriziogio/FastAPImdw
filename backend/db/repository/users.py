from sqlalchemy import true
from sqlalchemy.orm import Session
from schemas_pyd.users import UserCreate
from schemas_pyd.profiles import ProfileCreate
from db.models.users import User
from db.repository.profiles import create_new_profile
from core.config import settings

super_user_name = settings.SUPER_USER


def get_user(username: str, db: Session):
    user = db.query(User).filter(User.nome_utente == username).first()
    return user


def create_new_user(user: UserCreate, db: Session):
    user_db = User(**user.dict())
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db


def retrieve_users(db: Session):
    # db.query() è la select, con .all() ho i dati
    users_db = db.query(User).all()
    return users_db


def retrieve_users_by_id_profilo(id_profilo: int, db: Session):
    users_db = db.query(User).filter(User.id_profilo == id_profilo).all()
    return users_db


def retrieve_users_by_user_name(nome_utente: str, db: Session):
    users_db = db.query(User).filter(User.nome_utente == nome_utente).all()
    return users_db


def delete_users_by_user_name(nome_utente: str, db: Session):
    users_db = db.query(User).filter(User.nome_utente == nome_utente)
    if not users_db.first():
        return 0
    for user in users_db:
        user.delete(synchronize_session=False)
    db.commit()
    return 1


def create_super_user(db: Session):
    user_db = db.query(User).filter(User.nome_utente == super_user_name).first()
    if user_db:
        print(f"super user: {super_user_name} already exists")
        return 1
    profile = ProfileCreate(
        sistema='Automation FARM',
        profilo='Admin',
        permessi={"roles": "Admin"}
    )
    create_new_profile(profile=profile, db=db)
    user = UserCreate(
        nome_utente=super_user_name,
        id_profilo=1,
        super_user=True
    )
    create_new_user(user=user, db=db)
    print(f"super user: {super_user_name} created")
    return 1
