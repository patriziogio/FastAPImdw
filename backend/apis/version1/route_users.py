from fastapi import APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from fastapi import Depends
from schemas_pyd.users import UserCreate
from db.session import get_db
from db.repository.users import create_new_user, retrieve_users
from db.repository.profiles import retrieve_profile_by_id

router = APIRouter()


@router.post("/create-user/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    profile_db = retrieve_profile_by_id(id=user.id_profilo, db=db)
    if not profile_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Profile with id {user.id_profilo} not found")
    create_new_user(user=user, db=db)
    return {"msg": "User successfully created"}


@router.get("/get/")
def read_users(db: Session = Depends(get_db)):
    users_db = retrieve_users(db=db)
    return users_db
