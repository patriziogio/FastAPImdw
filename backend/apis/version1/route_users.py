from fastapi import APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from fastapi import Depends
from schemas_pyd.users import UserCreate
from db.session import get_db
from db.repository.users import create_new_user, retrieve_users, delete_users_by_user_name
from db.repository.users import retrieve_users_by_id_profilo, retrieve_users_by_user_name, create_super_user
from db.repository.profiles import retrieve_profile_by_id
from apis.version1.route_login import get_current_user_from_token
from db.models.users import User

router = APIRouter()

@router.post("/create-superuser/")
def create_user(db: Session = Depends(get_db)):
    create_super_user(db=db)
    return {"msg": "Superuser successfully created"}


@router.post("/create-user/")
def create_user(user: UserCreate, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user_from_token)):
    if current_user.super_user:
        profile_db = retrieve_profile_by_id(id=user.id_profilo, db=db)
        if not profile_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Profile with id {user.id_profilo} not found")
        create_new_user(user=user, db=db)
        return {"msg": "User successfully created"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail=f"You are not a super_user!!!!")


@router.get("/get/")
def read_users(db: Session = Depends(get_db)):
    users_db = retrieve_users(db=db)
    if not users_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Users not found")
    return users_db


@router.get("/get/{id_profilo}")
def read_users_by_id_profilo(id_profilo: int, db: Session = Depends(get_db)):
    users_db = retrieve_users_by_id_profilo(id_profilo=id_profilo, db=db)
    if not users_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Users not found for id_profilo:{id_profilo}")
    return users_db


@router.get("/get/{user_name}")
def read_users_by_user_name(user_name: str, db: Session = Depends(get_db)):
    users_db = retrieve_users_by_user_name(user_name=user_name, db=db)
    if not users_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Users not found for id_profilo:{id_profilo}")
    return users_db


@router.delete("/delete/{nome_utente}")
def delete_user(nome_utente: str, db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user_from_token)):
    if current_user.super_user:
        message = delete_users_by_user_name(nome_utente=nome_utente, db=db)
        if not message:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"User with nome_utente={nome_utente} not found")
        return {"msg": "User successfully deleted"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail=f"You are not a super_user!!!!")
