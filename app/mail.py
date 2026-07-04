from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import requests
from dotenv import load_dotenv

load_dotenv()

BREVO_API_KEY = os.getenv("BREVO_API_KEY")
BREVO_SENDER = os.getenv("BREVO_SENDER")

app = FastAPI()


class EmailRequest(BaseModel):
    receiver: str
    newsletter: str
    topic: str


@app.post("/send-email")
def send_email(data: EmailRequest):

    url = "https://api.brevo.com/v3/smtp/email"

    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json",
    }

    payload = {
        "sender": {
            "name": "AI Newsletter",
            "email": BREVO_SENDER
        },
        "to": [
            {
                "email": data.receiver
            }
        ],
        "subject": f"{data.topic} Newsletter",
        "textContent": data.newsletter
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=30
    )

    if response.status_code not in [200, 201]:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text
        )

    return {
        "message": "Newsletter sent successfully!"
    }