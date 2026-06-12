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
