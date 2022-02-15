from pydantic import BaseModel


class UserBase(BaseModel):
    nome_utente: str


# properties required during user creation
class UserCreate(UserBase):
    id_profilo: int

    class Config:
        orm_mode = True

