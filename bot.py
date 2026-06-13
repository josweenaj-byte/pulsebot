import requests
from datetime import date
import os
import smtplib
from email.message import EmailMessage

API_KEY = os.getenv("OPENWEATHER_API_KEY")
EMAIL = os.getenv("EMAIL_ADDRESS")
PASSWORD = os.getenv("EMAIL_PASSWORD")


def get_weather(city='Thiruvananthapuram'):
    url=f'https://wttr.in/{city}?format=3'
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text.strip()
    except Exception as e:
        return f"Weather unavailable ({e})"

def get_quote():
    url="https://zenquotes.io/api/random"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data=response.json()
        quote=data[0]["q"]
        author=data[0]['a']

        return f'"{quote}" {author}'
    except Exception as e:
        return f"Quote unavailable ({e})"

def get_openweather():
    city = "Thiruvananthapuram"

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    response = requests.get(url, timeout=10)

    print("OpenWeather response:")
    print(response.text)

    data = response.json()

    temp = data["main"]["temp"]
    weather = data["weather"][0]["main"]

    return temp, weather


def send_email_alert(temp, weather):
    msg = EmailMessage()
    msg["Subject"] = "Weather Alert"
    msg["From"] = EMAIL
    msg["To"] = EMAIL

    msg.set_content(
        f"Temperature: {temp}°C\nWeather: {weather}\n\nWeather alert triggered."
    )

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.send_message(msg)


def build_summary():
    today=date.today().strftime("%A,%d,%B,%Y")
    weather=get_weather()
    Quote=get_quote()

    summary= f"""
=====================================================
    Pulse Daily Summary
    {today}
=====================================================

    WEATHER
    {weather}

    TODAY'S QUOTE
    {Quote}
=====================================================


"""
    return summary


def run():
    summary = build_summary()
    print(summary)

    with open("daily_summary.txt", "w", encoding="utf-8") as f:
        f.write(summary)

    temp, weather = get_openweather()

if True:
    send_email_alert(temp, weather)
    print("Weather alert email sent.")

    print("Pulse ran successfully.")


if __name__ == "__main__":
    run()
