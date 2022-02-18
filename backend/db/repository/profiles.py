from sqlalchemy.orm import Session
from schemas_pyd.profiles import ProfileCreate
from db.models.profiles import Profile
import json


def create_new_profile(profile: ProfileCreate, db: Session):
    profile_db = Profile(sistema=profile.sistema, profilo=profile.profilo, permessi=json.dumps(profile.permessi))
    db.add(profile_db)
    db.commit()
    db.refresh(profile_db)
    return profile_db


def retrieve_profiles(db: Session):
    #db.query() è la select, con .all() ho i dati
    profiles_db = db.query(Profile).all()
    return profiles_db


def retrieve_profiles_by_sistema(sistema: str, db: Session):
    profiles_db = db.query(Profile).filter(Profile.sistema == sistema).all()
    return profiles_db


def retrieve_profile_by_id(id: int, db: Session):
    # db.query() è la select, con .first() ho il record
    profile_db = db.query(Profile).filter(Profile.id == id).first()
    return profile_db


def update_profile_by_id(id: int, profile: ProfileCreate, db: Session):
    profile_db = db.query(Profile).filter(Profile.id == id)
    if not profile_db.first():
        return 0
    profile.__dict__.update(permessi=json.dumps(profile.permessi))
    profile_db.update(profile.dict(exclude_unset=True))
    db.commit()
    return 1


def delete_profile_by_id(id: int, db: Session):
    profile_db = db.query(Profile).filter(Profile.id == id)
    if not profile_db.first():
        return 0
    profile_db.delete(synchronize_session=False)
    db.commit()
    return 1
