import json, re, glob, os, sys
here0 = os.path.dirname(os.path.abspath(__file__))
src = os.path.dirname(here0)
here = os.path.dirname(os.path.abspath(__file__))
order = ['README.md'] + sorted(f for f in os.listdir(src) if re.match(r'\d\d-', f)) + sorted(f for f in os.listdir(src) if f.startswith('appendix-'))
parts = {range(1, 5): '第1部 基礎', range(5, 8): '第2部 安全に任せる', range(8, 14): '第3部 育てる', range(14, 16): '第4部 実践'}
docs = []
for f in order:
    md = open(os.path.join(src, f), encoding='utf-8').read()
    h1 = re.search(r'^# (.+)$', md, re.M).group(1).strip()
    if f == 'README.md':
        docs.append(dict(id='top', file=f, kind='top', part='', num='', name='はじめに', short='はじめに・目次', md=md)); continue
    m = re.match(r'(\d\d)-', f)
    if m:
        n = int(m.group(1))
        part = next(v for k, v in parts.items() if n in k)
        name = re.sub(r'^第\d+章\s*', '', h1).split('：')[0]
        docs.append(dict(id='ch%02d' % n, file=f, kind='ch', part=part, num=str(n), name=name, short='第%d章 %s' % (n, name), md=md))
    else:
        L = f.split('-')[1].upper()
        name = re.sub(r'^付録[A-Z]\s*', '', h1).split('（')[0]
        docs.append(dict(id='app-' + L.lower(), file=f, kind='app', part='付録', num=L, name=name, short='付録%s %s' % (L, name), md=md))
data = json.dumps(docs, ensure_ascii=False).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
tpl = open(os.path.join(here, 'template.html'), encoding='utf-8').read()
out = tpl.replace('__DOCS__', data)
open(os.path.join(here, 'claude-code-textbook.html'), 'w', encoding='utf-8').write(out)
print(len(docs), 'docs', len(out.encode()) // 1024, 'KB')
for d in docs: print(d['id'], '|', d['short'])
