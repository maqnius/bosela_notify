Erzeugt und verschickt Erinnerung für Bosela Buchungen derart:

```
Das Rad ist gebucht am:
- 24.11.23
- 25.11.23
- 26.11.23
```

**1. Setup**

```shell
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**2. Configure**

Configure using `.env` file. `cp .env.example .env` and adopt. Eg.:

```ini
NOTIFY_EMAIL_TO="sarahgollek@aol.de,mark.niehues@posteo.de"
NOTIFY_EMAIL_FROM="maqnius@uber.space"
NOTIFY_DAYS_BEFORE=7
NOTIFY_SMTP_HOST="spica.uberspace.de"
NOTIFY_SMTP_PORT="465"
NOTIFY_SMTP_USER="maqnius@uber.space.de"
NOTIFY_SMTP_PASSWORD="password"
```

**3. Run**

```shell
python notify.py
```