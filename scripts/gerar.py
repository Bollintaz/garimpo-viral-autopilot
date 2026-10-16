import json
import html
import pathlib
from datetime import datetime, timezone
from urllib.parse import urlparse

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs'
OUT.mkdir(exist_ok=True)
config = json.loads((ROOT / 'data/config.json').read_text(encoding='utf-8'))
ofertas = json.loads((ROOT / 'data/ofertas.json').read_text(encoding='utf-8'))

def valid_link(value, domains=None):
    if not isinstance(value, str) or not value.strip():
        return ''
    url = value.strip()
    parsed = urlparse(url)
    if parsed.scheme != 'https' or not parsed.hostname:
        return ''
    if domains and not any(parsed.hostname == d or parsed.hostname.endswith('.' + d) for d in domains):
        return ''
    return url

def esc(text):
    return html.escape(str(text or ''), quote=True)

wa = valid_link(config.get('whatsapp_grupo'), ('chat.whatsapp.com',))
fb = valid_link(config.get('facebook_grupo'), ('facebook.com', 'www.facebook.com', 'm.facebook.com', 'web.facebook.com'))
links = []
if wa:
    links.append(f'<a class="btn whatsapp" href="{esc(wa)}" rel="noopener noreferrer" target="_blank">Entrar no grupo de WhatsApp ↗</a>')
if fb:
    links.append(f'<a class="btn" href="{esc(fb)}" rel="noopener noreferrer" target="_blank">Entrar no grupo do Facebook ↗</a>')
if not links:
    links.append('<p class="notice">Os links de convite serão disponibilizados em breve.</p>')

cards = []
posts = []
for item in ofertas:
    if item.get('ativo') is not True:
        continue
    url = valid_link(item.get('url'))
    if not url:
        continue
    nome = str(item.get('nome', 'Oferta')).strip()[:130]
    descricao = str(item.get('descricao', '')).strip()[:280]
    preco = str(item.get('preco', '')).strip()[:50]
    categoria = str(item.get('categoria', 'Achadinho')).strip()[:60]
    cards.append(f'''<article class="card"><span class="categoria">{esc(categoria)}</span><h3>{esc(nome)}</h3><p>{esc(descricao)}</p><strong>{esc(preco)}</strong><a class="btn" href="{esc(url)}" rel="sponsored noopener noreferrer" target="_blank">Ver produto ↗</a></article>''')
    posts.append(f'''🏠 ACHADINHO CASA CONFORTO\n\n{nome}\n{descricao}\n{('Preço informado: ' + preco) if preco else 'Confira as condições na loja.'}\n\nVeja o produto: {url}\n\nEntre no nosso grupo para acompanhar mais achadinhos!\n{wa or fb or '[adicione o convite do grupo]'}\n\nPublicidade: link de afiliado. Preços e disponibilidade podem mudar.''')

page = f'''<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{esc(config.get('descricao'))}"><title>{esc(config.get('marca'))} | Achadinhos</title><style>:root{{color-scheme:dark}}*{{box-sizing:border-box}}body{{margin:0;font:16px system-ui,Arial;background:#10151a;color:#f4f6f8}}header{{padding:70px 20px 42px;background:linear-gradient(135deg,#15292b,#172026);text-align:center}}.wrap{{max-width:960px;margin:auto;padding:24px}}h1{{font-size:clamp(2rem,6vw,3.5rem);margin:0 0 12px}}h2{{font-size:1.6rem}}p{{line-height:1.6;color:#cbd4d7}}.lead{{max-width:550px;margin:0 auto 24px}}.buttons{{display:flex;justify-content:center;flex-wrap:wrap;gap:12px}}.btn{{display:inline-block;background:#ffbd48;color:#171717;text-decoration:none;font-weight:750;border-radius:13px;padding:13px 19px;margin-top:12px}}.btn:hover{{filter:brightness(1.1)}}.whatsapp{{background:#43d58b}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:18px}}.card{{background:#1c262e;padding:22px;border:1px solid #33434a;border-radius:18px;display:flex;flex-direction:column;align-items:start}}.card .btn{{margin-top:auto}}.categoria{{font-size:12px;color:#ffce6e;text-transform:uppercase;letter-spacing:1px}}footer{{text-align:center;border-top:1px solid #33434a;margin-top:36px;padding:20px}}.notice{{border:1px dashed #85959a;border-radius:12px;padding:16px}}strong{{margin-bottom:15px}}</style></head><body><header><h1>🏡 {esc(config.get('marca'))}</h1><p class="lead">{esc(config.get('descricao'))}</p><div class="buttons">{''.join(links)}</div></header><main class="wrap"><h2>Achadinhos selecionados</h2><div class="grid">{''.join(cards) if cards else '<p>As ofertas serão divulgadas aqui em breve.</p>'}</div></main><footer><p>{esc(config.get('aviso_afiliado'))}</p><small>Consulte preços, frete e disponibilidade na loja. Atualizado em {datetime.now(timezone.utc).strftime('%d/%m/%Y %H:%M')} UTC.</small></footer></body></html>'''
(OUT / 'index.html').write_text(page, encoding='utf-8')
(OUT / 'posts.txt').write_text('\n\n' + ('\n\n---\n\n'.join(posts) if posts else 'Cadastre e ative ofertas com links válidos em data/ofertas.json.'), encoding='utf-8')
print(f'Gerado: {len(cards)} ofertas, {len(posts)} posts e {len(links)} elemento(s) de convite.')
