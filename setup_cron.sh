#!/bin/bash
# setup_cron.sh — schedules birthday_reminder.py to run every day at 8:00 AM

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON=$(which python3)
SCRIPT="$SCRIPT_DIR/birthday_reminder.py"
CRON_JOB="0 8 * * * $PYTHON $SCRIPT >> $SCRIPT_DIR/birthday_log.txt 2>&1"

echo "Setting up daily cron job..."
echo "  Script : $SCRIPT"
echo "  Python : $PYTHON"
echo "  Schedule: every day at 8:00 AM"
echo ""

# Check if job already exists
if crontab -l 2>/dev/null | grep -qF "$SCRIPT"; then
    echo "✅ Cron job already exists. No changes made."
else
    # Append the new job to existing crontab
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
    echo "✅ Cron job added successfully!"
fi

echo ""
echo "Current crontab:"
crontab -l
