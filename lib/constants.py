import os
import sys

# Load settings from environment variables
OPEN_AI_TOKEN = str(os.environ.get('OPEN_AI_TOKEN')).strip()
SLACK_BOT_TOKEN = str(os.environ.get('SLACK_BOT_TOKEN')).strip()
CHANNEL_ID = str(os.environ.get('SLACK_POST_CHANNEL_ID')).strip()
LANGUAGE = str(os.environ.get('LANGUAGE') or "Japanese").strip()
TIMEZONE_STR = str(os.environ.get('TIMEZONE') or 'Asia/Tokyo').strip()
TEMPERATURE = float(os.environ.get('TEMPERATURE') or 0.3)
CHAT_MODEL = str(os.environ.get('CHAT_MODEL') or "gpt-3.5-turbo").strip()
DEBUG = str(os.environ.get('DEBUG') or "").strip() != ""
MAX_BODY_TOKENS = 3000

if OPEN_AI_TOKEN == "" or SLACK_BOT_TOKEN == "" or CHANNEL_ID == "":
    print("OPEN_AI_TOKEN, SLACK_BOT_TOKEN, CHANNEL_ID must be set.")
    sys.exit(1)
