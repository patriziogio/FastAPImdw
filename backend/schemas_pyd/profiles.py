from pydantic import BaseModel
from schemas_pyd.users import UserBase
from typing import Optional


# properties required during profile creation
class ProfileCreate(BaseModel):
    sistema: str
    profilo: str
    permessi: dict


class ProfileUpdate(BaseModel):
    sistema: Optional[str] = None
    profilo: Optional[str] = None
    permessi: Optional[dict] = {}


class Profile(ProfileCreate):
    id: int
    utenti: list[UserBase] = []

    class Config:
        orm_mode = True
