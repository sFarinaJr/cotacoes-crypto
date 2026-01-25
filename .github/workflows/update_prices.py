name: Atualiza preços BTC e ETH a cada 5 minutos

on:
  schedule:
    - cron: '*/5 * * * *'
  workflow_dispatch:

jobs:
  update-prices:
    runs-on: ubuntu-latest
    permissions:
      contents: write          # ← muito importante para permitir commit/push

    steps:
      - name: Checkout repositório
        uses: actions/checkout@v4
        with:
          ref: main              # ← force a branch correta (mude se sua branch padrão for outra)
          token: ${{ secrets.GITHUB_TOKEN }}

      - name: Configura Python 3.11
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Instala dependências
        run: |
          python -m pip install --upgrade pip
          pip install --no-cache-dir requests

      - name: Executa script de atualização
        run: python update_prices.py

      - name: Debug (estado do repositório)
        run: |
          ls -la
          git status
          echo "Conteúdo do crypto_prices.txt:"
          cat crypto_prices.txt || echo "(arquivo não encontrado)"

      - name: Commit e Push das alterações (se houver)
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"

          git add crypto_prices.txt || true

          # Só commit se houver alteração real
          git diff --staged --quiet
          if [ $? -eq 0 ]; then
            echo "→ Nenhuma alteração. Pulando commit."
            exit 0
          fi

          git commit -m "chore: atualiza preços BTC/ETH automaticamente ($(date -u +'%Y-%m-%d %H:%M UTC'))" || {
            echo "→ Commit falhou (provavelmente sem mudanças)"
            exit 0
          }

          git push origin HEAD || {
            echo "→ Push falhou"
            exit 0
          }

          echo "→ Commit & push realizados com sucesso"
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
