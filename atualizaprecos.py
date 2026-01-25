name: Atualiza preços BTC e ETH a cada 5 min

on:
  schedule:
    - cron: '*/5 * * * *'          # a cada 5 minutos
  workflow_dispatch:               # permite rodar manualmente também

jobs:
  update:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repo
        uses: actions/checkout@v4
        with:
          token: ${{ secrets.GITHUB_TOKEN }}   # necessário para commitar depois

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Instalar dependências
        run: |
          python -m pip install --upgrade pip
          pip install requests

      - name: Atualizar preços
        run: python update_prices.py

      - name: Commit & Push se houver mudança
        run: |
          git config --global user.name "GitHub Action"
          git config --global user.email "action@github.com"
          
          git add crypto_prices.txt
          git commit -m "Atualização automática: preços BTC e ETH (a cada 5 min)" || echo "Nenhuma mudança para commitar"
          git push
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
