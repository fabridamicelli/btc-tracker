import json
from datetime import datetime
import requests
import time

import fire


def get_current_bitcoin_price():
    data = requests.get("https://api.coinbase.com/v2/prices/BTC-USD/spot").json()
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "value": float(data["data"]["amount"]),
        "currency": data["data"]["currency"],
    }


def main(freq=1):
    while True:
        print(json.dumps(get_current_bitcoin_price()), flush=True)
        time.sleep(freq)


if __name__ == "__main__":
    fire.Fire(main)
