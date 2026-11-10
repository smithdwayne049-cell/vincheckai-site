"""Free, browser-only vPIC decoder and app pricing; composed before localization."""
import json
import re

PLAY = 'https://play.google.com/store/apps/details?id=com.vinai.app'

def revise(root):
    def play():
        return f'<a class="play" href="{PLAY}">Get it on Google Play</a>'

    def form(hero=False):
        return '''<section class="vin-decoder" aria-label="Free VIN decoder"><form class="vin-form" novalidate>
<label for="vin-input">Enter a VIN</label><div class="vin-controls"><input id="vin-input" type="text" autocomplete="off" autocapitalize="characters" spellcheck="false" aria-describedby="vin-hint vin-status" placeholder="17 characters" required><button type="submit">Decode VIN</button></div>
<p class="micro" id="vin-hint">Free basic specifications · Source: NHTSA (US data). Coverage varies.</p>
<p class="vin-status" id="vin-status" role="status" aria-live="polite"></p></form>
<div class="vin-output" aria-live="polite" aria-atomic="true"></div>
<div class="decoder-copy" hidden>''' + ''.join(f'<span data-copy="{k}">{v}</span>' for k,v in {
        'invalid':'Enter 17 letters and digits. I, O and Q are not allowed.',
        'loading':'Decoding VIN…', 'decode':'Decode VIN', 'retry':'Retry',
        'unavailable':'Detailed data for this VIN is available in the Vin AI app',
        'network':'Could not reach NHTSA. Check your connection and retry.',
        'result':'Basic vehicle specifications', 'make':'Make', 'model':'Model',
        'year':'Model year', 'trim':'Trim', 'engine':'Engine specifications', 'cylinders':'cylinders',
        'transmission':'Transmission', 'drive':'Drive type', 'body':'Body class',
        'country':'Plant country', 'source':'Source: NHTSA vPIC. Specifications only; availability varies by vehicle.'
        }.items()) + '</div>' + ('<template class="vin-upsell">'+locked()+'</template>' if hero else '') + '</section>'

    def locked():
        labels = ['AI verdict + score 0–100', 'Red flags', 'What to check', 'Questions to ask the seller',
                  'Negotiation tips', 'Market value', 'Safety recalls & owner complaints', 'Crash rating', 'Fuel economy']
        return '<section class="locked-report"><div class="eyebrow">Full AI report</div><h2>Get the full report in the Vin AI app</h2><div class="locked-rows">' + ''.join(f'<div><span>{s}</span><i aria-hidden="true"></i></div>' for s in labels) + '</div><p class="micro">Report preview is locked. Data availability varies by vehicle and source.</p>' + play() + '</section>'

    index = (root/'index.html').read_text(encoding='utf-8')
    old = re.search(r'<a class="text-link" href="sample.html">.*?</a>', index).group()
    index = index.replace(old, '')
    index = index.replace('</div><p class="micro">Free VIN decode.', '</div>'+form(hero=True)+'<a class="text-link" href="sample.html">Sample report</a><p class="micro">Free VIN decode.', 1)
    index = index.replace('</body>', '<script src="decoder.js" defer></script></body>')
    # Reuse the existing brand, footer, accessibility and metadata skeleton.
    head = index[:index.index('<main')]
    footer = index[index.index('<footer'):]
    footer = re.sub(r'<script src="decoder.js" defer></script>', '', footer)
    def page(filename, title, description, body, schema=None):
        opening = re.sub(r'<title>.*?</title>', '<title>'+title+'</title>', head)
        opening = re.sub(r'<script type="application/ld\+json">.*?</script>', '', opening)
        opening = re.sub(r'(<meta (?:name|property)="(?:description|og:description|twitter:description)" content=")[^"]*', lambda m:m[1]+description, opening)
        opening = re.sub(r'(<meta (?:name|property)="(?:og:title|twitter:title)" content=")[^"]*', lambda m:m[1]+title, opening)
        opening = opening.replace('https://vincheckai.com/"', 'https://vincheckai.com/'+filename+'"')
        if schema:
            opening = opening.replace('</head>', '<script type="application/ld+json">'+json.dumps(schema)+'</script></head>')
        text = opening+'<main id="main" class="tool-page wrap">'+body+'</main>'+footer
        if filename == 'decode.html':
            text = text.replace('</body>', '<script src="decoder.js" defer></script></body>')
        (root/filename).write_text(text, encoding='utf-8')

    page('decode.html', 'Free VIN Decoder | Vin AI', 'Decode your VIN for free: make, model, engine and basic specifications from NHTSA. Get a full AI report in the Vin AI app.',
         '<div class="tool-heading"><div class="eyebrow">Free VIN decoder</div><h1>Start with the VIN.</h1><p>Decode basic vehicle specifications for free.</p></div>'+form()+locked())
    common = ['AI verdict + score 0–100', 'Red flags', 'What to check', 'Questions to ask the seller', 'Negotiation tips', 'Market value', 'Safety recalls & owner complaints', 'Crash rating', 'Fuel economy']
    body = '<div class="tool-heading"><div class="eyebrow">Pricing</div><h1>A clearer decision.<br><span class="chrome">One-time payment.</span></h1><p>No subscription.</p></div><div class="pricing-grid">'
    for name,price,unit,features in [('Full AI report','3.99','One VIN',common), ('Compare two cars','5.99','Two cars', ['Two cars side by side', 'Vehicle specifications and AI insights'])]:
        body += f'<section class="pricing-card"><h2>{name}</h2><p class="price-tag">${price} <span>USD</span></p><p>{unit}</p><p class="micro">One-time payment. No subscription.</p><ul>'+''.join('<li>'+s+'</li>' for s in features)+'</ul>'+play()+'</section>'
    body += '</div><section class="pricing-explainer"><h2>How it works</h2><p>Buy in the app — your next decoded VIN opens as a full report.</p><p>Free: basic VIN decode.</p><a class="text-link" href="decode.html">Free VIN decoder</a><p class="micro">Data availability varies by vehicle and source.</p></section>'
    schema = {'@context':'https://schema.org','@graph':[{'@type':'Product','name':name,'description':unit,'brand':{'@type':'Brand','name':'Vin AI'},'offers':{'@type':'Offer','price':price,'priceCurrency':'USD','url':PLAY}} for name,price,unit in [('Full AI report','3.99','One VIN'),('Compare two cars','5.99','Two cars')]]}
    page('pricing.html','Vin AI Pricing | Full AI Reports & Car Comparison','Free basic VIN decode. Full AI report $3.99 for one VIN or compare two cars $5.99. One-time purchases in the Vin AI app. No subscription.',body,schema)
    (root/'index.html').write_text(index,encoding='utf-8')
    for filename in ('index.html','sample.html','404.html','decode.html','pricing.html'):
        path=root/filename
        text=path.read_text(encoding='utf-8')
        text=text.replace('<a class="nav-cta"', '<a href="decode.html">VIN decoder</a><a href="pricing.html">Pricing</a><a class="nav-cta"', 1)
        path.write_text(text,encoding='utf-8')
