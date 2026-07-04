from fastapi import FastAPI
from pydantic import BaseModel

import smtplib
import os

from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

app = FastAPI()


class EmailRequest(BaseModel):
    receiver: str
    newsletter: str
    topic: str


@app.post("/send-email")
def send_email(data: EmailRequest):

    msg = MIMEText(data.newsletter)

    msg["Subject"] = f"{data.topic} Newsletter"

    msg["From"] = EMAIL

    msg["To"] = data.receiver

    server = smtplib.SMTP("smtp.gmail.com",587)

    server.starttls()

    server.login(
        EMAIL,
        EMAIL_PASSWORD
    )

    server.sendmail(
        EMAIL,
        data.receiver,
        msg.as_string()
    )

    server.quit()

    return {
        "message":"Newsletter sent successfully!"
    }
print(EMAIL)
print(EMAIL_PASSWORD)