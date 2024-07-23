from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Registration
from app.utils.qr_code_generator import generate_qr_code
from app.db.schemas import RegistrationCreate
from sqlalchemy.future import select
async def register_user(registration: RegistrationCreate, db: AsyncSession):

    existing_user = await db.execute(select(Registration).filter(Registration.email == registration.email))
    if existing_user.scalars().first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    qr_code = generate_qr_code(f"{registration.email}-{registration.telefono}-{registration.dni}")
    
    new_registration = Registration(
        name=registration.name,
        email=registration.email,
        telefono=registration.telefono,
        dni=registration.dni,
        qr_code=qr_code
    )
    
    db.add(new_registration)
    await db.commit()
    await db.refresh(new_registration)
    
    return new_registration
