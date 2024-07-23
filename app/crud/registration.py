from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.registration import Registration
from app.schemas.registration import RegistrationCreate

async def create_registration(db: AsyncSession, registration: RegistrationCreate):
    db_registration = Registration(**registration.dict())
    db.add(db_registration)
    await db.commit()
    await db.refresh(db_registration)
    return db_registration

async def get_registration_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(Registration).filter(Registration.email == email))
    return result.scalars().first()
