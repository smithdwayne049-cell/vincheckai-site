"""Offline static localization, applied after the English page composition."""
import html
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
from xml.etree import ElementTree as ET

LANGUAGES = {'en': 'English', 'ru': 'Русский', 'de': 'Deutsch', 'es': 'Español',
             'fr': 'Français', 'it': 'Italiano', 'pt': 'Português', 'tr': 'Türkçe',
             'ko': '한국어', 'zh': '中文'}
BASE = 'https://vincheckai.com/'
LOCALES = {'zh': 'zh-CN', 'pt': 'pt-BR'}
ATTRS = {'alt', 'aria-label', 'title', 'placeholder'}

def route(lang, page):
    return ('' if lang == 'en' else lang + '/') + page

def translatable(value):
    return bool(re.search(r'[a-zA-Z]{2}', value)) and not value.startswith(('http', '#'))

class Localizer(HTMLParser):
    def __init__(self, source, lang, page, strings):
        super().__init__(convert_charrefs=True)
        self.lang, self.page, self.strings = lang, page, strings
        self.output, self.collected = [], set()
        self.in_script = False
        self.feed(source)

    def t(self, value):
        text = value.strip()
        if not text or not translatable(text):
            return value
        self.collected.add(text)
        if self.lang != 'en' and (text not in self.strings or not self.strings[text].strip()):
            raise ValueError(f'Missing {self.lang} translation: {text}')
        return value.replace(text, self.strings.get(text, text))

    def handle_decl(self, decl):
        self.output.append('<!' + decl + '>')

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'html':
            attrs['lang'] = self.lang
        if tag == 'script':
            self.in_script = True
        for key in ATTRS & attrs.keys():
            attrs[key] = self.t(attrs[key])
        if tag == 'meta':
            name = attrs.get('name', attrs.get('property', ''))
            if name in ('description', 'og:title', 'og:description', 'og:image:alt', 'twitter:title', 'twitter:description'):
                attrs['content'] = self.t(attrs['content'])
            if name == 'og:url':
                attrs['content'] = BASE + route(self.lang, self.page)
        if tag == 'link' and attrs.get('rel') == 'canonical':
            attrs['href'] = BASE + route(self.lang, self.page)
        for key in ('src', 'srcset', 'href'):
            value = attrs.get(key, '')
            if key == 'src':
                # Rebuilding starts from English assets; localization selects its own set.
                match = re.fullmatch(r'assets/web/(?:screens/en/)?(phone(?:-specs|-flags|-compare)?|scan|specs|flags|compare)\.webp', value)
                if match:
                    value = f'assets/web/screens/{self.lang}/{match[1]}.webp'
                    attrs[key] = value
            if self.lang != 'en' and (value.startswith('assets/') or value in ('styles.css', 'app.js', 'report.js', 'decoder.js')):
                attrs[key] = '../' + value
            if value.startswith('https://play.google.com/'):
                parts = urlsplit(value)
                attrs[key] = urlunsplit(parts._replace(query=urlencode(dict(parse_qsl(parts.query)) | {'hl': LOCALES.get(self.lang, self.lang)})))
        self.output.append('<' + tag + ''.join(' ' + k + ('' if v is None else '="' + html.escape(v, quote=True) + '"') for k, v in attrs.items()) + '>')

    def handle_endtag(self, tag):
        if tag == 'script':
            self.in_script = False
        if tag == 'head':
            for lang in [*LANGUAGES, 'x-default']:
                self.output.append(f'<link rel="alternate" hreflang="{lang}" href="{BASE + route("en" if lang == "x-default" else lang, self.page)}">')
        if tag == 'header':
            links = ''.join(f'<a lang="{lang}" hreflang="{lang}" href="{("../" if self.lang != "en" else "./") + route(lang, self.page)}"' + (' aria-current="page"' if lang == self.lang else '') + f'>{name}</a>' for lang, name in LANGUAGES.items())
            label = self.t('Choose language')
            self.output.append(f'<details class="language-switcher"><summary aria-label="{html.escape(label)}"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><path d="M3 12h18"/></svg><span>{LANGUAGES[self.lang]}</span></summary><nav aria-label="{html.escape(label)}">{links}</nav></details>')
        self.output.append('</' + tag + '>')

    def handle_data(self, value):
        if self.in_script:
            def walk(obj):
                if isinstance(obj, dict):
                    result = {k: (self.t(v) if k in ('name', 'description', 'text') and isinstance(v, str) else walk(v)) for k, v in obj.items()}
                    if obj.get('@type') == 'SoftwareApplication':
                        result['inLanguage'] = self.lang
                        result['url'] = BASE + route(self.lang, '')
                        result['downloadUrl'] += '&hl=' + LOCALES.get(self.lang, self.lang)
                    return result
                if isinstance(obj, list):
                    return [walk(x) for x in obj]
                return obj
            self.output.append(json.dumps(walk(json.loads(value)), ensure_ascii=False).replace('<', '\\u003c'))
        else:
            self.output.append(html.escape(self.t(value), quote=False))

    def handle_entityref(self, name):
        self.output.append('&' + name + ';')

    def handle_charref(self, name):
        self.output.append('&#' + name + ';')

    def handle_comment(self, data):
        self.output.append('<!--' + data + '-->')

def build(root):
    sources = {page: (root / (page or 'index.html')).read_text(encoding='utf-8') for page in ('', 'sample.html', 'decode.html', 'pricing.html')}
    english = {}
    # NHTSA official text is explicitly marked and kept verbatim in all languages.
    nhtsa = json.loads((root / 'data/nhtsa_ford_escape_2018.json').read_text(encoding='utf-8'))
    official = {row.get(key, '') for row in nhtsa['recalls']['results'] for key in ('Component', 'Summary', 'NHTSACampaignNumber')}
    official |= {'Engine', 'Power Train', 'Electrical System', 'Structure', 'Service Brakes', 'Fuel/Propulsion System'}
    for source in sources.values():
        parser = Localizer(source, 'en', '', {})
        english.update({text: text for text in parser.collected})
    english['(official NHTSA text, English)'] = '(official NHTSA text, English)'
    i18n = root / 'i18n'
    i18n.mkdir(exist_ok=True)
    existing = json.loads((i18n / 'en.json').read_text(encoding='utf-8')) if (i18n / 'en.json').exists() else {}
    english = {key: existing.get(key, key) for key in english}
    (i18n / 'en.json').write_text(json.dumps(dict(sorted(english.items())), ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    for lang in LANGUAGES:
        strings = json.loads((i18n / f'{lang}.json').read_text(encoding='utf-8'))
        strings.update({text: text for text in official})
        for page, source in sources.items():
            if lang != 'en':
                source = source.replace('<div class="safety-grid">', '<p class="micro">(official NHTSA text, English)</p><div class="safety-grid">')
            parser = Localizer(source, lang, page, strings)
            target = root / route(lang, page or 'index.html')
            target.parent.mkdir(exist_ok=True)
            target.write_text(''.join(parser.output), encoding='utf-8')
    ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    ET.register_namespace('xhtml', 'http://www.w3.org/1999/xhtml')
    ns = '{http://www.sitemaps.org/schemas/sitemap/0.9}'
    sitemap = ET.Element(ns + 'urlset')
    for lang in LANGUAGES:
        for page in sources:
            node = ET.SubElement(sitemap, ns + 'url')
            ET.SubElement(node, ns + 'loc').text = BASE + route(lang, page)
            for alt in [*LANGUAGES, 'x-default']:
                ET.SubElement(node, '{http://www.w3.org/1999/xhtml}link', rel='alternate', hreflang=alt, href=BASE + route('en' if alt == 'x-default' else alt, page))
    ET.ElementTree(sitemap).write(root / 'sitemap.xml', encoding='utf-8', xml_declaration=True)
    print('Built 40 localized pages and multilingual sitemap.')
