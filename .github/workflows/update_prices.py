import requests
import os

FILE = "crypto_prices.txt"

try:
    # Usando Binance API (mais confiável para pares USDT)
    # BTC/USDT
    btc_resp = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=10)
    btc_resp.raise_for_status()
    btc = float(btc_resp.json()["price"])

    # ETH/USDT
    eth_resp = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT", timeout=10)
    eth_resp.raise_for_status()
    eth = float(eth_resp.json()["price"])

    # Escreve no arquivo com 2 casas decimais
    with open(FILE, "w", encoding="utf-8") as f:
        f.write(f"{btc:.2f}\n")
        f.write(f"{eth:.2f}\n")

    print(f"Atualizado com sucesso (Binance) → BTC: {btc:.2f} USDT | ETH: {eth:.2f} USDT")

except Exception as e:
    print(f"Erro ao obter preços: {e}")
    # Se der erro, não cria arquivo vazio – mantém o anterior
