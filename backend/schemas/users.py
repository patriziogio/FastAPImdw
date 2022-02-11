from pydantic import BaseModel, EmailStr


# properties required during user creation
class UserCreate(BaseModel):
    username: str


class ShowUser(BaseModel):
    username : str
    is_active : bool

    class Config():  # tells pydantic to convert even non dict obj to json
        orm_mode = True

