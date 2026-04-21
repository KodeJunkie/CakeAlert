"""
Birthday Reminder (BlowTheCandles)
- Sends a personal WhatsApp message to the birthday person
- Sends a random group announcement to the WhatsApp group
Reads contacts from contacts.csv. Runs daily via cron / Task Scheduler.
"""

import csv
import logging
import random
import time
from datetime import datetime
from pathlib import Path

import pywhatkit as kit

# ── Config ────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
CONTACTS_FILE = BASE_DIR / "contacts.csv"
LOG_FILE = BASE_DIR / "birthday_log.txt"

# Your WhatsApp group name — must match EXACTLY as it appears in WhatsApp
WHATSAPP_GROUP_NAME = "GXq8afG1DcrLl2X7gbmKU0"

# Personal message sent directly to the birthday person
PERSONAL_MESSAGE = (
    "🎂 Happy Birthday, {name}! 🎉\n"
    "Wishing you a wonderful day filled with joy and blessings. "
    "May God bless you abundantly! 🙏 With Love - St. Patricks Choir"
)

# Group messages — one is picked at random for each birthday
GROUP_MESSAGES = [
    "Happy Birthday {name}! 🎂 May God's blessings overflow in your life today and always. So grateful He placed you in our lives! 🙏✨ \n With Love - St. Patricks Choir",
    "Breaking news: {name} has successfully completed another lap around the sun! 🌍☀️ Happy Birthday!  \n With Love - St. Patricks Choir",
    "Sending all our love to {name} on their special day! From your second family! 💕🎉  \n With Love - St. Patricks Choir",
    "God looked down and said this group needs a {name}. And honestly? Best decision ever. Happy Birthday! 😄🙏🎂 🎊🔥  \n With Love - St. Patricks Choir",
    "The birthday energy is UNMATCHED today because {name} exists and we are so grateful. HAPPY BIRTHDAY! 🙌🎉  \n With Love - St. Patricks Choir",
    "Today is {name}'s birthday! They have officially completed another year of putting up with all of us. That alone deserves a medal. 🥇😂  \n With Love - St. Patricks Choir",
    "Happy Birthday {name}! 🎉 Praying that this new year of your life is filled with joy, peace, and every good thing God has in store for you. 🙏  \n With Love - St. Patricks Choir",
    "Today we celebrate {name} and all the joy they bring into our lives. Wishing you a beautiful birthday and an even more beautiful year ahead! 🎉💛  \n With Love - St. Patricks Choir",
    "Another year of grace for our dear {name}! May God continue to guide and bless you in every step. Happy Birthday! 🙏🎂  \n With Love - St. Patricks Choir",
    "To {name} on your birthday, may your blessings be many, your worries be few, and your cake be plentiful. Priorities! 😄🎂✨  \n With Love - St. Patricks Choir",
    "Happy Birthday {name}! Another year of being an absolute blessing to this group, whether you like it or not. 😄🙏🎉 \n With Love - St. Patricks Choir",
    "Happy Birthday {name}! May today be full of love, laughter, and people who actually remember to wish you before the day ends. 😄🎉🙏 \n With Love - St. Patricks Choir",
    "Happy Birthday {name}! Another year of being an absolute blessing to this group, whether you like it or not. 😄🙏🎉 \n With Love - St. Patricks Choir",
]

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)


# ── Helpers ───────────────────────────────────────────────────────────────────
def load_contacts():
    """Load contacts from CSV. Returns list of dicts."""
    if not CONTACTS_FILE.exists():
        log.warning(f"contacts.csv not found. Creating a sample file.")
        create_sample_csv()

    contacts = []
    with open(CONTACTS_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=2):
            name = row.get("name", "").strip()
            phone = row.get("phone", "").strip()
            birthday = row.get("birthday", "").strip()

            if not name or not phone or not birthday:
                log.warning(f"Row {i}: skipping incomplete entry — {row}")
                continue

            phone = phone.replace(" ", "").replace("-", "")
            if not phone.startswith("+"):
                phone = "+91" + phone  # default India; change if needed

            try:
                datetime.strptime(birthday, "%Y-%m-%d")
            except ValueError:
                log.warning(f"Row {i}: invalid date '{birthday}' for {name}. Use YYYY-MM-DD.")
                continue

            contacts.append({"name": name, "phone": phone, "birthday": birthday})

    log.info(f"Loaded {len(contacts)} contacts from {CONTACTS_FILE.name}")
    return contacts


def create_sample_csv():
    """Create a starter contacts.csv."""
    with open(CONTACTS_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "phone", "birthday"])
        writer.writeheader()
        writer.writerow({"name": "John Mathew", "phone": "+919876543210", "birthday": "1990-03-19"})
        writer.writerow({"name": "Mary Joseph", "phone": "+919123456789", "birthday": "1985-12-25"})
    log.info(f"Created sample contacts.csv — edit it with your real contacts.")


def is_birthday_today(birthday_str: str) -> bool:
    today = datetime.now()
    bday = datetime.strptime(birthday_str, "%Y-%m-%d")
    return bday.month == today.month and bday.day == today.day


def send_to_person(phone: str, name: str):
    """Send personal birthday wish directly to the birthday person."""
    message = PERSONAL_MESSAGE.format(name=name)
    try:
        kit.sendwhatmsg_instantly(
            phone_no=phone,
            message=message,
            wait_time=15,
            tab_close=True,
            close_time=3,
        )
        log.info(f"✅  Personal message sent to {name} ({phone})")
        return True
    except Exception as e:
        log.error(f"❌  Failed to message {name} ({phone}): {e}")
        return False


def send_to_group(name: str):
    """Send a random group announcement for the birthday person."""
    message = random.choice(GROUP_MESSAGES).format(name=name)
    try:
        kit.sendwhatmsg_to_group_instantly(
            group_id=WHATSAPP_GROUP_NAME,
            message=message,
            wait_time=15,
            tab_close=True,
            close_time=3,
        )
        log.info(f"✅  Group message sent for {name} → \"{message[:60]}...\"")
        return True
    except Exception as e:
        log.error(f"❌  Failed to send group message for {name}: {e}")
        return False


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    today_str = datetime.now().strftime("%Y-%m-%d")
    log.info(f"━━━ Birthday check for {today_str} ━━━")

    contacts = load_contacts()
    birthday_contacts = [c for c in contacts if is_birthday_today(c["birthday"])]

    if not birthday_contacts:
        log.info("No birthdays today. Nothing to send.")
        return

    names_today = ", ".join(c["name"] for c in birthday_contacts)
    log.info(f"🎂  {len(birthday_contacts)} birthday(s) today: {names_today}")

    for contact in birthday_contacts:
        name = contact["name"]

        # 1. Send personal message to the birthday person
        send_to_person(contact["phone"], name)

        # Small pause between messages so WhatsApp Web doesn't get overwhelmed
        time.sleep(1)

        # 2. Send group announcement
        send_to_group(name)

        # Pause between contacts if there are multiple birthdays today
        time.sleep(1)

    log.info("━━━ Done ━━━")


if __name__ == "__main__":
    main()
