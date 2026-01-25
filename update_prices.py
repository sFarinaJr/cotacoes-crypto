import requests
import os

FILE = "crypto_prices.txt"

try:
    response = requests.get(
        "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd",
        timeout=10
    )
    response.raise_for_status()
    data = response.json()

    btc = data["bitcoin"]["usd"]
    eth = data["ethereum"]["usd"]

    with open(FILE, "w", encoding="utf-8") as f:
        f.write(f"{btc:.2f}\n")  # BTC em USD
        f.write(f"{eth:.2f}\n")  # ETH em USD

    print(f"Atualizado (CoinGecko USD) → BTC: {btc:.2f} | ETH: {eth:.2f}")

except Exception as e:
    print(f"Erro ao obter preços: {e}")
