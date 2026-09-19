import os
import time
import requests

# Fill in your Telegram details
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# Target Details
TARGET_MODEL_CODE = "MJRR4ZA/A"
TARGET_MODEL_NAME = "iPhone 18 Pro 256GB Burgundy"

HK_STORES = {
    "R428": "Central (ifc mall)",
    "R485": "Tsim Sha Tsui (Canton Road)",
    "R499": "Causeway Bay (Hysan Place)",
    "R409": "Kowloon Tong (Festival Walk)",
    "R610": "Sha Tin (New Town Plaza)",
    "R673": "Kwun Tong (apm)",
}

STOCK_URL = (
    f"https://www.apple.com/hk/shop/fulfillment-messages"
    f"?pl=true&mts.0=regular&parts.0={TARGET_MODEL_CODE}"
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36"
    ),
}


def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
    }

    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"Telegram error: {e}")


def check_stock():
    try:
        res = requests.get(STOCK_URL, headers=HEADERS, timeout=5)

        if res.status_code == 200:
            stores = (
                res.json()
                .get("body", {})
                .get("content", {})
                .get("pickupMessage", {})
                .get("stores", [])
            )

            for store in stores:
                s_id = store.get("storeNumber")

                if s_id in HK_STORES:
                    s_name = HK_STORES[s_id]
                    parts = store.get("partsAvailability", {})

                    if TARGET_MODEL_CODE in parts:
                        if (
                            parts[TARGET_MODEL_CODE]
                            .get("pickupDisplay")
                            == "available"
                        ):
                            msg = (
                                f"🚨 *STOCK ALERT!*\n\n"
                                f"{TARGET_MODEL_NAME} is AVAILABLE at "
                                f"*{s_name}*!\n\n"
                                f"Open Apple Store App immediately!"
                            )

                            print(f"[FOUND] {s_name}")
                            send_telegram_alert(msg)
                        else:
                            print(f"[{s_name}] Out of stock")

    except Exception as e:
        print(f"Checking error: {e}")


if __name__ == "__main__":
    print("Cloud Stock Checker Running...")

    while True:
        check_stock()
        time.sleep(15)
