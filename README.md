# Garimpo Viral AutoPilot — Casa Conforto

Versão inicial gratuita, sem automação de envio de mensagens ou adição de pessoas a grupos.

## Começar

1. Crie um repositório novo no GitHub e envie o conteúdo desta pasta (incluindo `.github`). Pode ser público **somente se os dados de ofertas e links forem públicos**.
2. Em `data/config.json`, informe os links HTTPS reais dos convites do WhatsApp (`https://chat.whatsapp.com/...`) e Facebook (`https://www.facebook.com/groups/...`). O link de convite deve ser divulgado apenas quando você quiser que seja público.
3. Em `data/ofertas.json`, cadastre os produtos reais com seus próprios links de afiliado HTTPS e altere `ativo` para `true`.
4. Abra **Actions > Atualizar vitrine e textos > Run workflow**. Espere a conclusão e verifique `docs/index.html` e `docs/posts.txt`.
5. Em **Settings > Pages**, selecione **Deploy from a branch** e escolha `main` (ou sua branch padrão) e a pasta `/docs`.
6. Divulgue voluntariamente a URL do GitHub Pages na sua página Casa Conforto, bio e postagens apropriadas. Copie as legendas de `docs/posts.txt` para seus canais.

## Estrutura

- `data/config.json`: identidade e convites.
- `data/ofertas.json`: produtos e links autorizados.
- `scripts/gerar.py`: gerador seguro de vitrine e legendas.
- `.github/workflows/atualizar.yml`: execução manual ou diária às 09:17 de Brasília (sujeito a atraso do GitHub).
- `docs/index.html`: vitrine pública.
- `docs/posts.txt`: rascunhos, **não** publica automaticamente.

## Limites

- Não coleta automaticamente produtos da Shopee; cadastre manualmente ou integre futuramente uma fonte oficialmente autorizada.
- Não publica em grupos do Facebook, não envia mensagens de WhatsApp e não adiciona usuários automaticamente.
- Não mede membros novos. Métricas precisas exigem uma integração de análise com aviso de privacidade e/ou dados administrativos dos grupos.
- Não armazene tokens ou senhas em arquivos do repositório. Para integração futura, use GitHub Actions Secrets.
- Crie conteúdo original e divulgue em espaços nos quais você tenha permissão. Declare links de afiliado.
