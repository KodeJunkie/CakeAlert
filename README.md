# Birthday Reminder (Python)

Sends WhatsApp birthday wishes automatically every day. No UI, no server — just a Python script.

---

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Add your contacts
Edit `contacts.csv` in any spreadsheet app (Excel, LibreOffice, Numbers):

| name        | phone          | birthday   |
|-------------|----------------|------------|
| John Mathew | +919876543210  | 1990-03-19 |
| Mary Joseph | +919123456789  | 1985-12-25 |

- **phone**: must include country code (e.g. `+91` for India). If you enter just 10 digits, `+91` is added automatically.
- **birthday**: must be in `YYYY-MM-DD` format.

### 3. Log in to WhatsApp Web once
Open your browser and go to https://web.whatsapp.com — scan the QR code with your phone. Your session is saved so you only need to do this once.

### 4. Schedule it to run daily

**Linux / Mac:**
```bash
chmod +x setup_cron.sh
./setup_cron.sh
```

**Windows:**
Run `setup_task.bat` as Administrator (right-click → Run as administrator).

Both scripts schedule the reminder to run at **8:00 AM daily**.

---

## Test it manually
```bash
python birthday_reminder.py
```

---

## Customise the message
Edit `MESSAGE_TEMPLATE` in `birthday_reminder.py`:

```python
MESSAGE_TEMPLATE = (
    "🎂 Happy Birthday, {name}! 🎉\n"
    "Wishing you a wonderful day filled with joy and blessings. "
    "May God bless you abundantly! 🙏"
)
```

`{name}` is replaced with the contact's name automatically.

---

## Logs
All activity is saved to `birthday_log.txt` in the same folder.

---

## How it works
1. Script runs at 8:00 AM via cron (Mac/Linux) or Task Scheduler (Windows)
2. Reads `contacts.csv`, finds anyone whose birthday is today
3. Opens WhatsApp Web in your browser, sends the message, closes the tab
4. Logs success/failure to `birthday_log.txt`

> **Note:** pywhatkit uses WhatsApp Web, so your computer must be on and your browser session active when the script runs.
