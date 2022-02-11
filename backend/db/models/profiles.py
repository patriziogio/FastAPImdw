from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from db.base_class import Base


class Profile(Base):
    id = Column(Integer, primary_key=True, index=True)
    permission = Column(String, nullable=False)
    profile_name = Column(String, nullable=False)
    aap_name = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("user.id"))
    user_rel = relationship("User", back_populates="prof_rel")

