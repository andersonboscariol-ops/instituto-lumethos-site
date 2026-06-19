#!/usr/bin/env python3
"""
FIX: cursos.html — 9 stacked <a> tags no card #1, cards #2-#9 sem wrapper <a>.

O HTML atual tem:
  <a href="/cursos/capelania..." class="curso-card-link"><a href="/cursos/teologia..." ...>...9 stacked...</a>
  <div class="curso-card">   <- card 1
    ...</a>                   <- closes card 1
  </div></div>

  <div class="curso-card">   <- card 2, SEM wrapper <a>
    ...</a>                   <- orphaned </a>

Fix: cada card ganha seu próprio <a wrapper>, removendo as 8 extras do início.
"""

import re

PATH = '/var/www/lumethos/cursos.html'

with open(PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# ============================================================
# 1. Identificar o bloco dos cursos-grid
# ============================================================
start_marker = '<!-- 1. CAPELANIA CRISTÃ -->'
end_marker = '<!-- ===== CTA ===== -->'

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print("❌ Não encontrou markers delimitadores")
    exit(1)

grid_block = content[start_idx:end_idx]

# ============================================================
# 2. Fixar o card #1: remover os 8 <a> extras do início
# ============================================================
# Padrão: os 9 <a> seguidos, mantendo só o 1º (capelania)
card1_pattern = r'^(\s*)<a href="/cursos/capelania\.html" class="curso-card-link"><a href="/cursos/teologia\.html" class="curso-card-link"><a href="/cursos/pastoral\.html" class="curso-card-link"><a href="/cursos/diaconal\.html" class="curso-card-link"><a href="/cursos/hinologia\.html" class="curso-card-link"><a href="/cursos/jovens\.html" class="curso-card-link"><a href="/cursos/infantil\.html" class="curso-card-link"><a href="/cursos/patristica\.html" class="curso-card-link"><a href="/cursos/historia-igreja\.html" class="curso-card-link">'

fixed = re.sub(card1_pattern, r'\1<a href="/cursos/capelania.html" class="curso-card-link">', grid_block, count=1, flags=re.MULTILINE)

if fixed == grid_block:
    print("⚠️  Não substituiu card 1 (padrão não encontrado)")
else:
    print("✅ Card 1: removidos 8 <a> extras")

# ============================================================
# 3. Envolver cards #2-#9 em seus próprios <a href>
# ============================================================
card_links = {
    'teologia':    ('<!-- 2. TEOLOGIA -->',     '/cursos/teologia.html'),
    'pastoral':    ('<!-- 3. MINISTÉRIO PASTORAL -->', '/cursos/pastoral.html'),
    'diaconal':    ('<!-- 4. MINISTÉRIO DIACONAL -->', '/cursos/diaconal.html'),
    'hinologia':   ('<!-- 5. HINOLOGIA CRISTÃ -->',    '/cursos/hinologia.html'),
    'jovens':      ('<!-- 6. MINISTÉRIO DOS JOVENS -->', '/cursos/jovens.html'),
    'infantil':    ('<!-- 7. MINISTÉRIO INFANTIL -->', '/cursos/infantil.html'),
    'patristica':  ('<!-- 8. PATRÍSTICA -->',    '/cursos/patristica.html'),
    'historia':    ('<!-- 9. HISTÓRIA DA IGREJA -->', '/cursos/historia-igreja.html'),
}

for key, (comment, href) in card_links.items():
    # Procurar: comment + newline + whitespace + <div class="curso-card">
    pat = re.compile(
        rf'({re.escape(comment)}\s*\n)(\s*)(<div class="curso-card">)'
    )
    repl = rf'\1\2<a href="{href}" class="curso-card-link">\n\2\3'
    new_fixed = re.sub(pat, repl, fixed, count=1)
    if new_fixed == fixed:
        print(f"⚠️  Card {key}: não encontrou padrão")
    else:
        print(f"✅ Card {key}: wrapper adicionado")
        fixed = new_fixed

# ============================================================
# 4. Escrever de volta
# ============================================================
new_content = content[:start_idx] + fixed + content[end_idx:]

# Backup
import shutil
from datetime import datetime
backup = f'{PATH}.bak.{datetime.now().strftime("%Y%m%d_%H%M%S")}'
shutil.copy2(PATH, backup)
print(f"📦 Backup salvo: {backup}")

with open(PATH, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("✅ cursos.html reescrito com sucesso!")

# ============================================================
# 5. Validar estrutura HTML
# ============================================================
with open(PATH, 'r', encoding='utf-8') as f:
    final = f.read()

# Contar <a> abertos
open_a = final.count('<a href=')
close_a = final.count('</a>')
print(f"\n📊 Validação: <a open={open_a}, </a> close={close_a}")

# Verificar cada card
for key, (comment, href) in {'capelania': ('<!-- 1. CAPELANIA CRISTÃ -->', '/cursos/capelania.html'), **card_links}.items():
    if comment in final:
        print(f"  ✓ {key}: comentário presente")
    else:
        print(f"  ✗ {key}: comentário AUSENTE")

print("\n✅ FIX CONCLUÍDO")
