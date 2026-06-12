# ⚡ Pulse — Daily Morning Bot

A bot that runs itself. Every morning at **8 AM IST**, Pulse fetches live weather and an inspirational quote, then emails you a clean daily summary — automatically, via GitHub Actions.

**No API keys required.** Uses wttr.in and ZenQuotes, both free with no signup.

---

## 📁 Files

```
pulse/
├── bot.py                          # main script
├── requirements.txt                # just: requests
└── .github/
    └── workflows/
        └── daily.yml               # GitHub Actions schedule
```

---

## 🚀 Setup

### 1. Gmail App Password
1. Go to https://myaccount.google.com/security
2. Enable **2-Step Verification**
3. Search **"App passwords"** → create one → copy the 16-char code

### 2. Add GitHub Secrets
Repo → **Settings → Secrets and variables → Actions → New repository secret**

| Secret | Value |
|--------|-------|
| `EMAIL_FROM` | your.email@gmail.com |
| `EMAIL_TO` | your.email@gmail.com |
| `EMAIL_PASS` | 16-char Gmail App Password |

### 3. Push to GitHub

```bash
git init
git add .
git commit -m "feat: pulse daily bot"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/pulse.git
git push -u origin main
```

### 4. Test manually
Repo → **Actions → Daily Pulse → Run workflow**

Check your inbox — you should get the email within ~30 seconds.

---

## ✏️ Customise

| What | Where | Default |
|------|-------|---------|
| City | `daily.yml` → `CITY` env var | `Kottayam` |
| Schedule | `daily.yml` → `cron` | `30 2 * * *` (8 AM IST) |

---

## 📧 What the email looks like

**Subject:** `⚡ Pulse — Fri 13 Jun | 31°C Partly Cloudy`

**Body:**
- 🌤️ Weather card — temp, feels like, high/low, humidity, wind
- 💡 Quote of the day — random quote from ZenQuotes

Clean, dark-header HTML email. No dependencies beyond `requests`.
