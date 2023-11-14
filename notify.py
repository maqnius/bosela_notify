import json
import locale
import smtplib
import os
from email.message import EmailMessage
from datetime import date

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

locale.setlocale(locale.LC_ALL, "de_DE.UTF-8")

url = "https://bosela.de/cb_item/derweisseblitz/?cb-location=217"
looking_n_days_forward = int(os.environ["NOTIFY_DAYS_BEFORE"])

# E-Mail Server Configuration
host = os.environ["NOTIFY_SMTP_HOST"]
port = os.environ["NOTIFY_SMTP_PORT"]
user = os.environ["NOTIFY_SMTP_USER"]
password = os.environ["NOTIFY_SMTP_PASSWORD"]

# E-Mail Sending Settings
mail_from = os.environ["NOTIFY_EMAIL_FROM"]
mail_to = os.environ["NOTIFY_EMAIL_TO"].split(",")

def get_data():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features="html.parser")

    # Get data from html script tag
    for match in soup.find_all(
        "div",
        {
            "class": [
                "cb-wrapper",
                "cb-timeframe-calendar",
                "template-timeframe-calendar",
                "post-cb_item",
                "has-post-thumbnail",
            ]
        },
    ):
        for child in match:
            if child.name == "script":
                text = (
                    child.string.replace("let calendarData = ", "")
                    .replace(";", "")
                    .strip()
                )
                return json.loads(text)


def get_upcoming_dates():
    data = get_data()
    if data is None:
        raise ValueError("Konnte Daten nicht parsen")

    today = date.today()
    upcoming = []
    for booking_date in data["bookedDays"]:
        booked_date = date.fromisoformat(booking_date)
        time_delta = booked_date - today
        if booked_date > today and time_delta.days < looking_n_days_forward:
            upcoming.append(booked_date)
    return upcoming


def send_mail():
    upcoming_dates = get_upcoming_dates()

    if not upcoming_dates:
        return

    content = "\n".join(
        [
            "Das Rad ist gebucht am:",
            *[f"- {d.strftime('%a (%d.%m.%y)')}" for d in upcoming_dates],
        ]
    )
    print(content)

    msg = EmailMessage()
    msg.set_content(content)
    msg["Subject"] = "[bosela.de] Anstehende Abholungen"
    msg["From"] = mail_from

    
    with smtplib.SMTP_SSL(host=host, port=port) as server:
        server.login(
            user=user,
            password=password,
        )
        for to_mail in mail_to:
            if "To" in msg:
                del msg["To"]
            msg["To"] = to_mail
            server.send_message(msg)


if __name__ == "__main__":
    send_mail()
