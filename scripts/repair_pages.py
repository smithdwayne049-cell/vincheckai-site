"""Repair-cost pages (data/repair/<lang>.json -> <lang>/<slug>.html + repair-costs.html hub).

Runs on the already built site: each language's decode.html is the page shell (head, header with
language switcher, footer). Safe to run again: pages are rewritten, footer links and sitemap
entries are not duplicated.

    python scripts/repair_pages.py
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = 'https://vincheckai.com/'
LANGS = ['en', 'ru', 'de', 'es', 'fr', 'it', 'pt', 'tr', 'ko', 'zh']
HUB = 'repair-costs.html'
PLAY = 'https://play.google.com/store/apps/details?id=com.vinai.app'
esc = html.escape


ALL_SLUGS = set()  # every slug in any data file, skipped or not (for sitemap cleanup)


def total_of(t):
    """Headline range: an explicit 'total' [label, low, high], else the last table row."""
    return t.get('total') or t['rows'][-1]


def load():
    data = {}
    for lang in LANGS:
        path = ROOT / 'data' / 'repair' / f'{lang}.json'
        if path.exists():
            d = json.loads(path.read_text(encoding='utf-8'))
            for t in d['topics']:
                ALL_SLUGS.add(t['slug'])
                old = folder(lang) / (t['slug'] + '.html')
                if t.get('skip') and old.exists():
                    old.unlink()  # a topic switched to skip loses its old page
            d['topics'] = [t for t in d['topics'] if not t.get('skip')]
            data[lang] = d
    return data


def folder(lang):
    return ROOT if lang == 'en' else ROOT / lang


def url(lang, file):
    return SITE + ('' if lang == 'en' else lang + '/') + file


def money(d, n):
    s = f'{int(n):,}'.replace(',', d['thousands'])
    return d['price_format'].replace('{n}', s)


def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False).replace('<', '\\u003c') + '</script>'


def shell(lang):
    src = (folder(lang) / 'decode.html').read_text(encoding='utf-8')
    head, rest = src.split('<main', 1)
    head = re.sub(r'<script type="application/ld\+json">.*?</script>', '', head, flags=re.S)
    head = re.sub(r'<link rel="alternate" hreflang="[^"]+" href="[^"]+">', '', head)
    header = head[head.index('<body>'):]
    head = head[:head.index('<body>')]
    footer = src[src.index('<footer'):].replace('<script src="../decoder.js" defer></script>', '').replace('<script src="decoder.js" defer></script>', '')
    return head, header, footer


def make_head(head, lang, file, title, description, alternates, schemas):
    h = re.sub(r'<title>.*?</title>', lambda _: '<title>' + esc(title) + '</title>', head, flags=re.S)
    h = re.sub(r'(<meta (?:name|property)="(?:description|og:description|twitter:description)" content=")[^"]*', lambda m: m[1] + esc(description, quote=True), h)
    h = re.sub(r'(<meta (?:name|property)="(?:og:title|twitter:title)" content=")[^"]*', lambda m: m[1] + esc(title, quote=True), h)
    h = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda m: m[1] + url(lang, file), h)
    h = re.sub(r'(<meta property="og:url" content=")[^"]*', lambda m: m[1] + url(lang, file), h)
    h = re.sub(r'(<meta property="og:type" content=")[^"]*', lambda m: m[1] + 'article', h)
    alt = ''.join(f'<link rel="alternate" hreflang="{l}" href="{url(l, file)}">' for l in alternates)
    if 'en' in alternates:
        alt += f'<link rel="alternate" hreflang="x-default" href="{url("en", file)}">'
    return h.replace('</head>', '') + alt + ''.join(ld(s) for s in schemas) + '</head>'


def make_header(header, file, alternates):
    def fix(m):
        block = m[0]
        return re.sub(r'(<a lang="([a-z]{2})"[^>]*href="[^"]*?)decode\.html"',
                      lambda a: a[1] + (file if a[2] in alternates else '') + '"', block)
    return re.sub(r'<details class="language-switcher">.*?</details>', fix, header, flags=re.S)


def available(data, slug):
    return [l for l in LANGS if l in data and any(t['slug'] == slug for t in data[l]['topics'])]


def topic_page(data, lang, t, head, header, footer):
    d, ui = data[lang], data[lang]['ui']
    file = t['slug'] + '.html'
    alts = available(data, t['slug'])
    total = total_of(t)
    faq = t['faq']
    schemas = [
        {'@context': 'https://schema.org', '@type': 'Article', 'headline': t['h1'], 'description': t['description'],
         'inLanguage': lang, 'dateModified': '2026-11-24', 'mainEntityOfPage': url(lang, file),
         'author': {'@type': 'Organization', 'name': 'Vin AI', 'url': SITE},
         'publisher': {'@type': 'Organization', 'name': 'Vin AI', 'logo': {'@type': 'ImageObject', 'url': SITE + 'assets/icon.png'}}},
        {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
            {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faq]},
        {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': ui['home'], 'item': url(lang, '')},
            {'@type': 'ListItem', 'position': 2, 'name': ui['hub_h1'], 'item': url(lang, HUB)},
            {'@type': 'ListItem', 'position': 3, 'name': t['h1'], 'item': url(lang, file)}]},
    ]
    rows = ''.join(
        f'<tr{" class=total" if i == len(t["rows"]) - 1 else ""}><th scope="row">{esc(r[0])}</th><td>{money(d, r[1])}</td><td>{money(d, r[2])}</td></tr>'
        for i, r in enumerate(t['rows']))
    others = [o for o in d['topics'] if o['slug'] != t['slug']]
    i = next(k for k, o in enumerate(d['topics']) if o['slug'] == t['slug'])
    related = [others[(i + k) % len(others)] for k in range(4)] if others else []
    body = (
        f'<nav class="crumbs" aria-label="breadcrumb"><a href="./">{esc(ui["home"])}</a><span aria-hidden="true">/</span><a href="{HUB}">{esc(ui["hub_h1"])}</a></nav>'
        f'<div class="tool-heading"><h1>{esc(t["h1"])}</h1><p class="repair-answer">{esc(t["answer"])}</p></div>'
        f'<div class="repair-total"><span>{esc(total[0])}</span><strong>{money(d, total[1])} – {money(d, total[2])}</strong></div>'
        f'<table class="repair-table"><thead><tr><th scope="col">{esc(ui["table_item"])}</th><th scope="col">{esc(ui["table_low"])}</th><th scope="col">{esc(ui["table_high"])}</th></tr></thead><tbody>{rows}</tbody></table>'
        f'<p class="micro">{esc(ui["disclaimer"].replace("{country}", d["country"]))}</p>'
        f'<section class="pricing-explainer"><h2>{esc(ui["factors_title"])}</h2><ul>{"".join("<li>" + esc(x) + "</li>" for x in t["factors"])}</ul></section>'
        f'<section class="pricing-explainer"><h2>{esc(ui["tips_title"])}</h2><ul>{"".join("<li>" + esc(x) + "</li>" for x in t["tips"])}</ul></section>'
        f'<section class="repair-cta"><h2>{esc(ui["cta_title"])}</h2><p>{esc(ui["cta_text"])}</p><a class="play" href="{PLAY}&amp;hl={lang}">{esc(ui["cta_button"])} <span aria-hidden="true">↗</span></a></section>'
        f'<section class="pricing-explainer"><h2>{esc(ui["faq_title"])}</h2>{"".join("<details><summary>" + esc(q) + "</summary><p>" + esc(a) + "</p></details>" for q, a in faq)}</section>'
        f'<p class="micro repair-sources">{esc(ui["sources_label"])}: '
        + ', '.join(f'<a href="{esc(s["url"], quote=True)}" rel="nofollow noopener" target="_blank">{esc(s["name"])}</a>' for s in t['sources']) + '</p>'
        f'<section class="pricing-explainer"><h2>{esc(ui["related_title"])}</h2><ul class="repair-links">'
        + ''.join(f'<li><a href="{o["slug"]}.html">{esc(o["h1"])}</a></li>' for o in related)
        + f'<li><a href="{HUB}">{esc(ui["hub_h1"])}</a></li></ul></section>'
    )
    page = make_head(head, lang, file, t['title'], t['description'], alts, schemas) + make_header(header, file, alts) \
        + '<main id="main" class="tool-page wrap search-page repair-page">' + body + '</main>' + footer
    (folder(lang) / file).write_text(page, encoding='utf-8')


def hub_page(data, lang, head, header, footer):
    d, ui = data[lang], data[lang]['ui']
    alts = [l for l in LANGS if l in data]
    items = [{'@type': 'ListItem', 'position': k + 1, 'url': url(lang, t['slug'] + '.html'), 'name': t['h1']} for k, t in enumerate(d['topics'])]
    schemas = [{'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': ui['hub_title'], 'description': ui['hub_description'],
                'inLanguage': lang, 'mainEntity': {'@type': 'ItemList', 'itemListElement': items}}]
    cards = ''.join(
        f'<li><a href="{t["slug"]}.html"><span>{esc(t["h1"])}</span><strong>{money(d, total_of(t)[1])} – {money(d, total_of(t)[2])}</strong></a></li>'
        for t in d['topics'])
    body = (f'<div class="tool-heading"><h1>{esc(ui["hub_h1"])}</h1><p>{esc(ui["hub_intro"])}</p></div>'
            f'<ul class="repair-hub">{cards}</ul>'
            f'<p class="micro">{esc(ui["disclaimer"].replace("{country}", d["country"]))}</p>'
            f'<section class="repair-cta"><h2>{esc(ui["cta_title"])}</h2><p>{esc(ui["cta_text"])}</p><a class="play" href="{PLAY}&amp;hl={lang}">{esc(ui["cta_button"])} <span aria-hidden="true">↗</span></a></section>')
    page = make_head(head, lang, HUB, ui['hub_title'], ui['hub_description'], alts, schemas) + make_header(header, HUB, alts) \
        + '<main id="main" class="tool-page wrap search-page repair-page">' + body + '</main>' + footer
    (folder(lang) / HUB).write_text(page, encoding='utf-8')


def footer_links(data):
    """Add the hub link to the footer row of every page of each language (once)."""
    for lang in data:
        link = f'<a class="repair-hub-link" href="{HUB}">{esc(data[lang]["ui"]["footer_link"])}</a>'
        for path in folder(lang).glob('*.html'):
            text = path.read_text(encoding='utf-8')
            if 'repair-hub-link' in text or '<nav class="brand-decoder-links"' not in text:
                continue
            text = re.sub(r'(<nav class="brand-decoder-links".*?)(</nav>)', lambda m: m[1] + link + m[2], text, count=1, flags=re.S)
            path.write_text(text, encoding='utf-8')


def sitemap(data):
    path = ROOT / 'sitemap.xml'
    text = path.read_text(encoding='utf-8')
    files = {HUB} | {t['slug'] + '.html' for d in data.values() for t in d['topics']}
    stale = {slug + '.html' for slug in ALL_SLUGS} | files
    entries = re.findall(r'<url>.*?</url>', text, flags=re.S)
    keep = [e for e in entries if not any(re.search(r'<loc>' + re.escape(SITE) + r'(?:[a-z]{2}/)?' + re.escape(f) + '</loc>', e) for f in stale)]
    new = []
    for f in sorted(files):
        langs = [l for l in LANGS if l in data and (f == HUB or any(t['slug'] + '.html' == f for t in data[l]['topics']))]
        alt = ''.join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{url(l, f)}" />' for l in langs)
        if 'en' in langs:
            alt += f'<xhtml:link rel="alternate" hreflang="x-default" href="{url("en", f)}" />'
        for l in langs:
            new.append(f'<url><loc>{url(l, f)}</loc><lastmod>2026-11-24</lastmod>{alt}</url>')
    start = text[:text.index('<url>')]
    path.write_text(start + ''.join(keep + new) + '</urlset>', encoding='utf-8')
    return len(keep) + len(new)


def main():
    data = load()
    for lang, d in data.items():
        head, header, footer = shell(lang)
        for t in d['topics']:
            topic_page(data, lang, t, head, header, footer)
        hub_page(data, lang, head, header, footer)
    footer_links(data)
    n = sitemap(data)
    print('languages:', ', '.join(f'{l}={len(d["topics"])}' for l, d in data.items()), '| sitemap urls:', n)


if __name__ == '__main__':
    main()
