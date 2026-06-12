import requests
import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# ── Config ────────────────────────────────────────────────────────────────────
CITY       = os.environ.get("CITY", "Kottayam")
EMAIL_FROM = os.environ["EMAIL_FROM"]
EMAIL_TO   = os.environ["EMAIL_TO"]
EMAIL_PASS = os.environ["EMAIL_PASS"]   # Gmail App Password

# ── 1. Fetch Weather from wttr.in (no API key needed) ─────────────────────────
def get_weather(city):
    url = f"https://wttr.in/{city}?format=j1"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    data = r.json()

    current    = data["current_condition"][0]
    temp_c     = current["temp_C"]
    feels_like = current["FeelsLikeC"]
    humidity   = current["humidity"]
    wind_kmph  = current["windspeedKmph"]
    desc       = current["weatherDesc"][0]["value"]

    # Today's forecast (max/min)
    today      = data["weather"][0]
    max_temp   = today["maxtempC"]
    min_temp   = today["mintempC"]

    return {
        "temp":       temp_c,
        "feels_like": feels_like,
        "humidity":   humidity,
        "wind":       wind_kmph,
        "desc":       desc,
        "max":        max_temp,
        "min":        min_temp,
    }

# ── 2. Fetch Quote from ZenQuotes (no API key needed) ─────────────────────────
def get_quote():
    url = "https://zenquotes.io/api/random"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    data = r.json()[0]
    return data["q"], data["a"]   # quote, author

# ── 3. Build HTML Summary ─────────────────────────────────────────────────────
def build_html(weather, quote, author):
    now      = datetime.now().strftime("%A, %d %B %Y")
    greeting = "Good morning" if datetime.now().hour < 12 else "Hello"

    # Weather emoji based on description
    desc_lower = weather["desc"].lower()
    if "rain" in desc_lower or "drizzle" in desc_lower:
        w_emoji = "🌧️"
    elif "cloud" in desc_lower or "overcast" in desc_lower:
        w_emoji = "☁️"
    elif "sun" in desc_lower or "clear" in desc_lower:
        w_emoji = "☀️"
    elif "thunder" in desc_lower or "storm" in desc_lower:
        w_emoji = "⛈️"
    elif "fog" in desc_lower or "mist" in desc_lower:
        w_emoji = "🌫️"
    else:
        w_emoji = "🌤️"

    html = f"""
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background:#f0f2f5;font-family:'Segoe UI',Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f0f2f5;padding:32px 0;">
    <tr><td align="center">
      <table width="520" cellpadding="0" cellspacing="0"
             style="background:#ffffff;border-radius:16px;overflow:hidden;
                    box-shadow:0 4px 24px rgba(0,0,0,0.08);">

        <!-- Header -->
        <tr>
          <td style="background:linear-gradient(135deg,#1a1a2e 0%,#16213e 100%);
                     padding:28px 32px;text-align:center;">
            <p style="margin:0;color:#a0aec0;font-size:12px;letter-spacing:2px;
                      text-transform:uppercase;">Daily Summary</p>
            <h1 style="margin:6px 0 0;color:#ffffff;font-size:26px;font-weight:700;">
              ⚡ Pulse
            </h1>
            <p style="margin:6px 0 0;color:#718096;font-size:13px;">{now}</p>
          </td>
        </tr>

        <!-- Greeting -->
        <tr>
          <td style="padding:24px 32px 0;">
            <p style="margin:0;font-size:18px;color:#2d3748;font-weight:600;">
              {greeting}, Derin! 👋
            </p>
            <p style="margin:6px 0 0;color:#718096;font-size:14px;">
              Here's your daily brief for {CITY}.
            </p>
          </td>
        </tr>

        <!-- Weather Card -->
        <tr>
          <td style="padding:20px 32px 0;">
            <div style="background:#f7fafc;border-radius:12px;padding:20px;
                        border-left:4px solid #4299e1;">
              <p style="margin:0 0 12px;font-size:13px;font-weight:700;color:#4299e1;
                        letter-spacing:1px;text-transform:uppercase;">
                {w_emoji} Weather — {CITY}
              </p>
              <table width="100%" cellpadding="0" cellspacing="0">
                <tr>
                  <td style="padding:4px 0;">
                    <span style="font-size:36px;font-weight:700;color:#2d3748;">
                      {weather["temp"]}°C
                    </span>
                    <span style="color:#718096;font-size:14px;margin-left:8px;">
                      {weather["desc"]}
                    </span>
                  </td>
                </tr>
                <tr>
                  <td style="padding-top:12px;">
                    <table width="100%" cellpadding="0" cellspacing="0">
                      <tr>
                        <td style="color:#718096;font-size:13px;padding:3px 0;">
                          🤔 Feels like
                        </td>
                        <td style="color:#2d3748;font-size:13px;font-weight:600;
                                   text-align:right;">
                          {weather["feels_like"]}°C
                        </td>
                      </tr>
                      <tr>
                        <td style="color:#718096;font-size:13px;padding:3px 0;">
                          📈 High / Low
                        </td>
                        <td style="color:#2d3748;font-size:13px;font-weight:600;
                                   text-align:right;">
                          {weather["max"]}° / {weather["min"]}°
                        </td>
                      </tr>
                      <tr>
                        <td style="color:#718096;font-size:13px;padding:3px 0;">
                          💧 Humidity
                        </td>
                        <td style="color:#2d3748;font-size:13px;font-weight:600;
                                   text-align:right;">
                          {weather["humidity"]}%
                        </td>
                      </tr>
                      <tr>
                        <td style="color:#718096;font-size:13px;padding:3px 0;">
                          💨 Wind
                        </td>
                        <td style="color:#2d3748;font-size:13px;font-weight:600;
                                   text-align:right;">
                          {weather["wind"]} km/h
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>
              </table>
            </div>
          </td>
        </tr>

        <!-- Quote Card -->
        <tr>
          <td style="padding:20px 32px 0;">
            <div style="background:#fffaf0;border-radius:12px;padding:20px;
                        border-left:4px solid #ed8936;">
              <p style="margin:0 0 12px;font-size:13px;font-weight:700;color:#ed8936;
                        letter-spacing:1px;text-transform:uppercase;">
                💡 Quote of the Day
              </p>
              <p style="margin:0;font-size:16px;color:#2d3748;line-height:1.6;
                        font-style:italic;">
                "{quote}"
              </p>
              <p style="margin:10px 0 0;font-size:13px;color:#718096;text-align:right;">
                — {author}
              </p>
            </div>
          </td>
        </tr>

        <!-- Footer -->
        <tr>
          <td style="padding:24px 32px 28px;text-align:center;">
            <p style="margin:0;font-size:12px;color:#a0aec0;">
              Sent automatically by <strong>Pulse</strong> every morning at 8 AM IST 🤖<br>
              Powered by wttr.in + ZenQuotes + GitHub Actions
            </p>
          </td>
        </tr>

      </table>
    </td></tr>
  </table>
</body>
</html>
"""
    return html

# ── 4. Send Email ─────────────────────────────────────────────────────────────
def send_email(subject, html_body):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = EMAIL_FROM
    msg["To"]      = EMAIL_TO
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_FROM, EMAIL_PASS)
        server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())

    print(f"✅ Pulse email sent to {EMAIL_TO}")

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print("🌅 Pulse bot starting …")

    print("  → Fetching weather …")
    weather = get_weather(CITY)
    print(f"     {weather['temp']}°C, {weather['desc']}")

    print("  → Fetching quote …")
    quote, author = get_quote()
    print(f"     \"{quote[:60]}…\" — {author}")

    print("  → Building email …")
    html    = build_html(weather, quote, author)
    subject = f"⚡ Pulse — {datetime.now().strftime('%a %d %b')} | {weather['temp']}°C {weather['desc']}"

    print("  → Sending …")
    send_email(subject, html)

    print("✅ Done.")

if __name__ == "__main__":
    main()
