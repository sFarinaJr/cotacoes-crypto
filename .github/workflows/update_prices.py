      - name: Commit & Push se houver mudança ou arquivo novo
        run: |
          git config --global user.name "GitHub Action"
          git config --global user.email "github-action@users.noreply.github.com"
          
          # Tenta adicionar o arquivo (não falha se já existe ou não mudou)
          git add crypto_prices.txt || true
          
          # Verifica se há algo para commitar
          git diff --staged --quiet
          if [ $? -eq 0 ]; then
            echo "Nenhuma mudança detectada → pulando commit"
            exit 0
          fi
          
          git commit -m "Atualização automática: preços BTC e ETH (GitHub Actions)" || echo "Commit ignorado (provavelmente sem mudança)"
          git push || echo "Push ignorado (já atualizado ou sem permissão)"
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
