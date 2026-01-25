name: Atualiza preços BTC e ETH a cada 5 minutos

on:
  schedule:
    - cron: '*/5 * * * *'
  workflow_dispatch:

permissions:
  contents: write

jobs:
  update:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repositório (branch padrão)
        uses: actions/checkout@v4
        with:
          fetch-depth: 0          # traz todo o histórico (ajuda em alguns casos)
          token: ${{ secrets.GITHUB_TOKEN }}

      - name: Configura Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Instala requests
        run: |
          python -m pip install --upgrade pip
          pip install requests

      - name: Roda o script de preços
        run: python update_prices.py

      - name: Mostra debug (importante para ver o que está acontecendo)
        run: |
          echo "Branch atual:"
          git branch --show-current
          echo "Remote branches:"
          git branch -r
          echo "Status completo:"
          git status --short --branch
          echo ""
          echo "Conteúdo atual do crypto_prices.txt:"
          cat crypto_prices.txt || echo "Arquivo NÃO existe ainda!"
          echo ""
          echo "Diff staged:"
          git diff --staged || true

      - name: Commit e Push (forçando branch correta)
        run: |
          # Config git
          git config user.name "GitHub Actions Bot"
          git config user.email "actions@github.com"

          # Mostra branch atual para debug
          CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
          echo "Branch atual detectada: $CURRENT_BRANCH"

          # Sempre add o arquivo
          git add crypto_prices.txt || true

          # Verifica se há mesmo diferença
          if git diff --staged --quiet; then
            echo "→ Sem alterações reais no arquivo. Pulando commit."
            exit 0
          fi

          # Commit
          git commit -m "Atualização automática: preços BTC/ETH ($(date -u +'%Y-%m-%d %H:%M UTC'))" || {
            echo "→ Commit ignorado (nenhuma mudança ou erro)"
            exit 0
          }

          # Push explícito para a branch atual
          git push origin "$CURRENT_BRANCH" || {
            echo "→ Push falhou! Verifique permissões ou se a branch existe no remote."
            echo "Tente rodar manualmente e veja o log completo."
            exit 1   # falha o job para você notar
          }

          echo "→ Commit e push OK na branch $CURRENT_BRANCH"
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
