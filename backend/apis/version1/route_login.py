from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import Depends, APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta
from db.session import get_db
from schemas_pyd.token import Token
from db.repository.users import get_user
from db.ldap import auth_ldap
from core.security import create_access_token
from core.config import settings
from jose import JWTError, jwt


router = APIRouter()


def search_user_in_db(username: str, db: Session):
    user = get_user(username=username, db=db)
    if not user:
        return False
    return user


def authenticate_user_in_ldap(username: str, password: str):
    auth_ok = auth_ldap(username, password)
    if not auth_ok:
        return False
    return auth_ok


@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = search_user_in_db(form_data.username, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found in DB",
        )
    message = authenticate_user_in_ldap(form_data.username, form_data.password)
    if not message:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.nome_utente}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# token da usare come dipendenza
# appare un pulsante AUTHORIZE in /docs per fare dei test
# infatti passa le credenziali a questa tokenurl
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")


#funzione da usare come dipendenza
def get_current_user_from_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        print("username extracted is ", username)
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = search_user_in_db(username=username, db=db)
    if user is None:
        raise credentials_exception
    return user
