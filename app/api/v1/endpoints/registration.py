from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.schemas import RegistrationCreate
from app.services.registration_service import register_user
from app.db.session import get_db

router = APIRouter()

@router.post("/register")
async def register(registration: RegistrationCreate, db: AsyncSession = Depends(get_db)):
    try:
        new_registration = await register_user(registration, db)
        return {
            "id": new_registration.id,
            "name": new_registration.name,
            "email": new_registration.email,
            "telefono": new_registration.telefono,
            "dni": new_registration.dni,
            "qr_code": new_registration.qr_code
        }
    except HTTPException as e:
        raise e
