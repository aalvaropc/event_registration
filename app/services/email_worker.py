import aio_pika
import asyncio
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email_validator import validate_email, EmailNotValidError
from dotenv import load_dotenv

load_dotenv()

async def on_message(message: aio_pika.IncomingMessage):
    async with message.process():
        email_body = message.body.decode()
        recipient_email = email_body.split()[0]
        send_email(recipient_email)

def send_email(recipient_email: str):
    try:
        validate_email(recipient_email)

        msg = MIMEMultipart()
        msg['From'] = os.getenv('EMAIL_SENDER')
        msg['To'] = recipient_email
        msg['Subject'] = "Confirmación de registro del evento"

        body = f"Gracias por registrarte, {recipient_email}!!"
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP('smtp.office365.com', 587) as server:
            server.starttls()
            server.login(os.getenv('EMAIL_SENDER'), os.getenv('EMAIL_PASSWORD'))
            server.sendmail(msg['From'], recipient_email, msg.as_string())
            print(f"Email sent to {recipient_email}")

    except EmailNotValidError as e:
        print(f"Invalid email: {e}")
    except Exception as e:
        print(f"Error sending email: {e}")

async def main():
    connection = await aio_pika.connect_robust("amqp://guest:guest@rabbitmq/")
    async with connection:
        async with connection.channel() as channel:
            queue = await channel.declare_queue("registration_queue", durable=True)
            async for message in queue:
                await on_message(message)

if __name__ == "__main__":
    asyncio.run(main())
