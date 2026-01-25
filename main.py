import requests
import time

# Script para atualizar preços de Bitcoin e Ethereum em USDT a cada 1 minuto
# e salvar em um arquivo texto chamado 'crypto_prices.txt'.
# Primeira linha: preço do BTC em USDT
# Segunda linha: preço do ETH em USDT

while True:
    try:
        # Requisição à API do CoinGecko para obter preços
        response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usdt")
        response.raise_for_status()  # Verifica se houve erro na requisição
        data = response.json()
        
        btc_price = data['bitcoin']['usdt']
        eth_price = data['ethereum']['usdt']
        
        # Escreve os preços no arquivo
        with open("crypto_prices.txt", "w") as file:
            file.write(f"{btc_price}\n")
            file.write(f"{eth_price}\n")
        
        print("Preços atualizados com sucesso.")
    
    except Exception as e:
        print(f"Erro ao atualizar preços: {e}")
    
    # Espera 60 segundos antes da próxima atualização
    time.sleep(60)
