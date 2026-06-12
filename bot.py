import os
import smtplib
from email.message import EmailMessage
import requests

def get_weather():
    try:
        # format=3 gives a nice single-line weather summary
        response = requests.get('https://wttr.in/?format=3', timeout=10)
        return response.text.strip()
    except Exception as e:
        return f"Could not fetch weather: {e}"

def get_quote():
    try:
        response = requests.get('https://zenquotes.io/api/random', timeout=10)
        data = response.json()
        return f'"{data[0]["q"]}" - {data[0]["a"]}'
    except Exception as e:
        return f"Could not fetch quote: {e}"

def send_email(weather, quote):
    email_from = os.environ.get('EMAIL_FROM')
    email_to = os.environ.get('EMAIL_TO')
    email_pass = os.environ.get('EMAIL_PASS')

    if not all([email_from, email_to, email_pass]):
        print("Error: Missing email credentials in environment variables (EMAIL_FROM, EMAIL_TO, EMAIL_PASS).")
        return

    msg = EmailMessage()
    msg['Subject'] = 'Daily Pulse ⚡'
    msg['From'] = email_from
    msg['To'] = email_to

    content = f"""Good morning! Here is your Daily Pulse:

🌤️ Weather:
{weather}

💡 Quote of the Day:
{quote}

Have a wonderful day!
- Pulse Bot
"""
    msg.set_content(content)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email_from, email_pass)
            smtp.send_message(msg)
            print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == '__main__':
    print("Fetching weather...")
    weather = get_weather()
    print("Fetching quote...")
    quote = get_quote()
    
    print("\n--- Daily Pulse ---")
    print(f"Weather: {weather}")
    print(f"Quote: {quote}")
    print("-------------------\n")
    
    print("Sending email...")
    send_email(weather, quote)
