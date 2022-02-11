from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from db.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean(), default=True)
    prof_rel = relationship("Profile", back_populates="user_rel")