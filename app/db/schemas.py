from pydantic import BaseModel

class RegistrationCreate(BaseModel):
    name: str
    email: str
    telefono: str
    dni: str
