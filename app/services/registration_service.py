from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Registration
from app.utils.qr_code_generator import generate_qr_code
from app.db.schemas import RegistrationCreate
from sqlalchemy.future import select
import aio_pika

async def register_user(registration: RegistrationCreate, db: AsyncSession):
    existing_user = await db.execute(select(Registration).filter(Registration.email == registration.email))
    if existing_user.scalars().first():
        raise HTTPException(status_code=400, detail="Email ya registrado")
    
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
    
    await send_message_to_queue(new_registration)
    return new_registration

async def send_message_to_queue(registration: Registration):
    connection = await aio_pika.connect_robust("amqp://guest:guest@rabbitmq/")
    async with connection:
        async with connection.channel() as channel:
            await channel.default_exchange.publish(
                aio_pika.Message(body=f"{registration.email} registered".encode()),
                routing_key="registration_queue"
            )
