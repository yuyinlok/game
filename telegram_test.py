import os
import requests

# Fill in your credentials
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

payload = {
    "chat_id": TELEGRAM_CHAT_ID,
    "text": "🎉 *TEST SUCCESSFUL!*\n\nYour Python script is correctly connected to Telegram.",
    "parse_mode": "Markdown"
}

print("Sending test message to your Telegram...")
response = requests.post(url, json=payload, timeout=5)

if response.status_code == 200:
    print("✅ Message sent! Check your Telegram app on your iPhone.")
else:
    print(f"❌ Failed to send message. Response: {response.text}")
