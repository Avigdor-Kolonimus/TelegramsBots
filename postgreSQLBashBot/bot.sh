#!/bin/bash

# Read telegram credentials into variables
TELEGRAM_BOT_TOKEN="YOUR BOT TOKEN"
CHAT_ID="CHANNEL_ID OR GROUP_ID"
URL="https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage"

# Read query into variable
sql_query="SELECT current_date - 1 AS Yesterday;"

# Read database name into a variable
POSTGRES_DATABASE="NAME OF DATABASE"

# If psql is not installed, then exit
if ! command -v psql > /dev/null; then
  echo "PostgreSQL is required..."
  exit 1
fi

# Connect to the database, run the queries, then disconnect
yestarday_date=$(psql -t -A -d "$POSTGRES_DATABASE" -c "$sql_query")

MESSAGE_YESTERDAY="Example: ${yestarday_date} was yesterday"

# Send messages to telegram
status_code=$(curl -s -o /dev/null -w "%{http_code}" -X POST $URL -d chat_id=$CHAT_ID -d text="$MESSAGE_YESTERDAY")
if [[ "$status_code" == 200 ]]; then
  echo "Send message Success"
else
  echo "Send message Failure"
fi