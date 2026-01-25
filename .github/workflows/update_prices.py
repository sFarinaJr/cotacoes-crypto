import requests
import os

FILE = "crypto_prices.txt"

try:
    response = requests.get(
        "https://api.coingecko.com/api/v3/simple/price",
        params={
            "ids": "bitcoin,ethereum",
            "vs_currencies": "usdt"
        },
        timeout=10
    )
    response.raise_for_status()
    data = response.json()

    btc = data["bitcoin"]["usdt"]
    eth = data["ethereum"]["usdt"]

    # Escreve sempre (mesmo se for o mesmo valor)
    with open(FILE, "w", encoding="utf-8") as f:
        f.write(f"{btc:.2f}\n")   # 2 casas decimais
        f.write(f"{eth:.2f}\n")

    print(f"Atualizado → BTC: {btc:.2f} | ETH: {eth:.2f}")

except Exception as e:
    print(f"Erro ao obter preços: {e}")
    # Não para o workflow se der erro (ex: rate limit momentâneo)
