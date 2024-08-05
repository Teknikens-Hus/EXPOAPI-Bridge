#!/bin/ash

# Enable debugging
set -x

# Check if CRON_SCHEDULE is set
if [ -z "$CRON_SCHEDULE" ]; then
  echo "Error: CRON_SCHEDULE is not set, using default of every hour. 0 * * * *"
  CRON_SCHEDULE="0 * * * *"
fi

# Setup cron job in the user's home directory
echo -e "$CRON_SCHEDULE /home/app/expoapi-bridge/venv/bin/python3 /home/app/expoapi-bridge/run.py &" > /home/app/cronjob
echo "Cron job scheduled: $CRON_SCHEDULE"

# Run serve_json to start the web server
/home/app/expoapi-bridge/venv/bin/python3 /home/app/expoapi-bridge/serve_json.py &

# Make an initial request to the Expo API before cron job starts
/home/app/expoapi-bridge/venv/bin/python3 /home/app/expoapi-bridge/run.py &

supercronic /home/app/cronjob
echo "supercronic started"