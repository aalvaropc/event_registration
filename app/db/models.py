from sqlalchemy import Column, Integer, String
from app.db.base_class import Base

class Registration(Base):
    __tablename__ = 'registrations'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    telefono = Column(String)
    dni = Column(String, unique=True)
    qr_code = Column(String)
