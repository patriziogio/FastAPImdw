from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from schemas_pyd.profiles import ProfileCreate, ProfileUpdate, Profile
from db.session import get_db
from db.repository.profiles import create_new_profile, retrieve_profiles, retrieve_profiles_by_sistema
from db.repository.profiles import update_profile_by_id, delete_profile_by_id, retrieve_profile_by_id
from db.models.users import User
from apis.version1.route_login import get_current_user_from_token
import json

router = APIRouter()


@router.post("/create-profile/")
def create_profile(profile: ProfileCreate, db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user_from_token)):
    if current_user.super_user:
        create_new_profile(profile=profile, db=db)
        return {"msg": "Profile successfully created."}


@router.get("/get/")
def read_profiles(db: Session = Depends(get_db)):
    profiles_db = retrieve_profiles(db=db)
    # trasformo il campo permessi da str a json
    for i in range(len(profiles_db)):
        profiles_db[i].__dict__.update(permessi=json.loads(profiles_db[i].__dict__['permessi']))
        print(profiles_db[i].__dict__)
    if not profiles_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Profiles not found")
    return profiles_db


@router.get("/get/{sistema}")
def read_profiles_by_sistema(sistema: str, db: Session = Depends(get_db)):
    profiles_db = retrieve_profiles_by_sistema(sistema=sistema, db=db)
    # trasformo il campo permessi da str a json
    for i in range(len(profiles_db)):
        profiles_db[i].__dict__.update(permessi=json.loads(profiles_db[i].__dict__['permessi']))
        print(profiles_db[i].__dict__)
    if not profiles_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Profiles not found for {sistema}")
    return profiles_db


@router.put("/update/{id}")
def update_profile(id: int, profile: ProfileUpdate, db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user_from_token)):
    if current_user.super_user:
        message = update_profile_by_id(id=id, profile=profile, db=db)
        if not message:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Profile with id {id} not found")
        return {"msg": "Profile successfully updated"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail=f"You are not a super_user!!!!")


@router.delete("/delete/{id}")
def delete_profile(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_token)):
    if current_user.super_user:
        message = delete_profile_by_id(id=id, db=db)
        if not message:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Profile with id={id} not found")
        return {"msg": "Profile successfully deleted"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail=f"You are not a super_user!!!!")
