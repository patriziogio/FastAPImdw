from sqlalchemy import Column, Integer, String, BOOLEAN, ForeignKey
from sqlalchemy.orm import relationship
from db.session import Base


class User(Base):
    __tablename__ = "Utenti"
    id_profilo = Column(Integer, ForeignKey("Profili.id", ondelete="CASCADE"), primary_key=True)
    nome_utente = Column(String, primary_key=True)
    super_user = Column(BOOLEAN, default=False)
    profilo = relationship("Profile", back_populates="utenti")
