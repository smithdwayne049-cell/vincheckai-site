"""Search pages composed from the existing decoder skeleton before localization."""
import html
import json
import re
from task9_copy import BRANDS, COPY

PAGES = [brand.lower()+'-vin-decoder.html' for brand in BRANDS] + ['vin-check-no-subscription.html']

def revise(root):
    source = (root/'decode.html').read_text(encoding='utf-8')
    head, rest = source.split('<main', 1)
    footer = source[source.index('<footer'):]
    form = re.search(r'<section class="vin-decoder".*?</section>', rest, re.S)[0]
    play = '<a class="play" href="https://play.google.com/store/apps/details?id=com.vinai.app">Get it on Google Play</a>'
    esc = html.escape
    copy = COPY['en']
    def section(title, text, extra=''):
        return f'<section class="pricing-explainer"><h2>{esc(title)}</h2><p>{esc(text)}</p>{extra}</section>'
    def page(file, title, description, body, faq=None):
        opening = re.sub(r'<title>.*?</title>', lambda _: '<title>'+esc(title)+'</title>', head)
        opening = re.sub(r'<script type="application/ld\+json">.*?</script>', '', opening, flags=re.S)
        opening = re.sub(r'(<meta (?:name|property)="(?:description|og:description|twitter:description)" content=")[^"]*', lambda m:m[1]+esc(description, quote=True), opening)
        opening = re.sub(r'(<meta (?:name|property)="(?:og:title|twitter:title)" content=")[^"]*', lambda m:m[1]+esc(title, quote=True), opening)
        opening = opening.replace('https://vincheckai.com/decode.html', 'https://vincheckai.com/'+file)
        schema = {'@context':'https://schema.org','@type':'WebPage','name':title,'description':description}
        schemas = [schema]
        if faq:
            schemas.append({'@context':'https://schema.org','@type':'FAQPage','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in faq]})
        opening = opening.replace('</head>', ''.join('<script type="application/ld+json">'+json.dumps(s,ensure_ascii=False).replace('<','\\u003c')+'</script>' for s in schemas)+'</head>')
        ending = footer if faq else footer.replace('<script src="decoder.js" defer></script>', '')
        (root/file).write_text(opening+'<main id="main" class="tool-page wrap search-page">'+body+'</main>'+ending, encoding='utf-8')
    for brand, file in zip(BRANDS, PAGES):
        c = [s.format(brand=brand) for s in copy]
        body = f'<div class="tool-heading"><h1>{esc(c[0])}</h1><p>{esc(c[2])}</p></div>'+form
        body += section(c[3],c[4]) + section(c[5],c[6], '<a class="text-link" href="https://vpic.nhtsa.dot.gov/documents/ManufacturerHandbook.pdf">Source: NHTSA vPIC. Specifications only; availability varies by vehicle.</a>')
        body += section(c[7],c[8],'<p class="micro">'+esc(c[9])+'</p>'+play)
        faq = [(c[i],c[i+1]) for i in (10,12,14)]
        body += '<section class="pricing-explainer"><h2>FAQ</h2>'+''.join('<details><summary>'+esc(q)+'</summary><p>'+esc(a)+'</p></details>' for q,a in faq)+'</section>'
        page(file,c[0],c[1],body,faq)
    body = f'<div class="tool-heading"><h1>{esc(copy[16])}</h1><p>{esc(copy[18])}</p></div>'
    body += ''.join(section(copy[i],copy[i+1]) for i in (19,21,23))
    body += '<div class="actions">'+play+'<a class="text-link" href="decode.html">Free VIN decoder</a></div>'
    page(PAGES[-1],copy[16],copy[17],body)
    # Relative links stay in the current language directory after localization.
    row = '<nav class="brand-decoder-links" aria-label="'+copy[25]+'"><span>'+copy[25]+'</span>'+''.join('<a href="'+file+'">'+esc(copy[0].format(brand=brand))+'</a>' for brand,file in zip(BRANDS,PAGES))+'<a href="'+PAGES[-1]+'">'+copy[16]+'</a></nav>'
    for file in ['index.html','sample.html','decode.html','pricing.html','404.html',*PAGES]:
        path = root/file
        text = path.read_text(encoding='utf-8').replace('</footer>',row+'</footer>')
        path.write_text(text,encoding='utf-8')
