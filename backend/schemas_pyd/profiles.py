from pydantic import BaseModel
from schemas_pyd.users import UserBase


# properties required during profile creation
class ProfileCreate(BaseModel):
    sistema: str
    profilo: str
    permessi: dict


class Profile(ProfileCreate):
    id: int
    utenti: list[UserBase] = []

    class Config:
        orm_mode = True
