from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.session import Base


class Profile(Base):
    __tablename__ = "Profili"
    id = Column(Integer, primary_key=True, autoincrement=True)
    sistema = Column(String)
    profilo = Column(String)
    permessi = Column(String)
    utenti = relationship("User", back_populates="profilo",
                          cascade="all, delete",
                          passive_deletes=True
                          )
