# ⚡ Pulse — Daily Morning Bot

A bot that runs itself. Every morning at 8 AM IST, Pulse fetches live weather and an inspirational quote, then emails you a clean daily summary — automatically, via GitHub Actions.

No API keys required. Uses wttr.in and ZenQuotes, both free with no signup.

## 📁 Files

```text
pulse/
├── bot.py                  # main script
├── requirements.txt        # just: requests
└── .github/
    └── workflows/
        └── daily.yml       # GitHub Actions schedule
```

## 🚀 Setup

### 1. Gmail App Password
1. Go to https://myaccount.google.com/security
2. Enable 2-Step Verification
3. Search "App passwords" -> create one -> copy the 16-char code

### 2. GitHub Secrets
Go to your GitHub repository -> **Settings** -> **Secrets and variables** -> **Actions** -> **New repository secret**.

Add these 3 secrets:
- `EMAIL_FROM`: your Gmail address (e.g. `you@gmail.com`)
- `EMAIL_TO`: your Gmail address (or wherever you want the email sent)
- `EMAIL_PASS`: the 16-character App Password generated in step 1

### 3. Run and Test
1. Push your code to GitHub.
2. Go to the **Actions** tab in your repository.
3. Click on **Daily Pulse** on the left sidebar.
4. Click **Run workflow** to test it out right away!
