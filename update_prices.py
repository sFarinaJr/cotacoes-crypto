import requests
import os
from datetime import datetime

FILE = "crypto_prices.txt"

try:
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin,ethereum",
        "vs_currencies": "usd"
    }
    
    response = requests.get(url, params=params, timeout=12)
    response.raise_for_status()
    
    data = response.json()
    
    btc = data["bitcoin"]["usd"]
    eth = data["ethereum"]["usd"]
    
    # Escreve com timestamp para facilitar debug
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    with open(FILE, "w", encoding="utf-8") as f:
        f.write(f"# Última atualização: {timestamp}\n")
        f.write(f"BTC: {btc:.2f}\n")
        f.write(f"ETH: {eth:.2f}\n")
    
    print(f"Sucesso → BTC: ${btc:,.2f} | ETH: ${eth:,.2f} | {timestamp}")

except requests.exceptions.RequestException as e:
    print(f"Erro na requisição à CoinGecko: {e}")
except KeyError as e:
    print(f"Erro ao ler resposta da API (chave faltando): {e}")
except Exception as e:
    print(f"Erro inesperado: {type(e).__name__} → {e}")
