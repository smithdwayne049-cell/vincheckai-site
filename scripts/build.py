"""Build static HTML and presentation assets. Requires Pillow 13.0.0."""
import json, html, shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / 'assets'
WEB = ASSETS / 'web'
WEB.mkdir(exist_ok=True)
esc = lambda value: html.escape(str(value), quote=True)
PLAY = 'https://play.google.com/store/apps/details?id=com.vinai.app'
SVG = '<svg viewBox="0 0 24 28" aria-hidden="true"><path fill="#7030bb" d="M2 1 17 14 2 27Z"/><path fill="#f536b9" d="m2 1 19 11-4 2Z"/><path fill="#a774e6" d="m2 27 19-11-4-2Z"/><path fill="#3a1668" d="m17 14 4-2 3 2-3 2Z"/></svg>'
def play():
    return f'<a class="play" href="{PLAY}">{SVG}<span>Get it on Google Play</span></a>'

for source, name in [('00_enter_vin.png','scan'),('01_vehicle_info_specs.png','specs'),('07_ai_red_flags.png','flags'),('c01_side_by_side_winner.png','compare')]:
    image = Image.open(ASSETS / 'screens' / source).convert('RGB')
    image.thumbnail((540,1170))
    image.save(WEB / f'{name}.webp', quality=85, method=6)
screen = Image.open(WEB/'scan.webp').convert('RGBA')
screen = screen.resize((270,585))
phone = Image.new('RGBA',(300,620))
d = ImageDraw.Draw(phone)
d.rounded_rectangle((0,0,299,619),radius=43,fill='#91849d')
d.rounded_rectangle((2,2,296,617),radius=41,fill='#24212c')
d.rounded_rectangle((7,7,290,612),radius=37,fill='#050409')
mask = Image.new('L',screen.size)
ImageDraw.Draw(mask).rounded_rectangle((0,0,269,584),radius=29,fill=255)
phone.paste(screen,(14,18),mask)
d.rounded_rectangle((109,20,190,34),radius=7,fill='#07060c')
phone = phone.resize((600,1240),Image.Resampling.LANCZOS)
high_screen=Image.open(WEB/'scan.webp').convert('RGBA').resize((540,1170))
high_mask=Image.new('L',(540,1170))
ImageDraw.Draw(high_mask).rounded_rectangle((0,0,539,1169),radius=58,fill=255)
phone.paste(high_screen,(28,36),high_mask)
ImageDraw.Draw(phone).rounded_rectangle((218,40,380,68),radius=14,fill='#07060c')
phone.save(WEB/'phone.webp',quality=90)
for name in ('specs','flags','compare'):
    framed = phone.copy()
    screen = Image.open(WEB/f'{name}.webp').convert('RGBA').resize((540,1170))
    framed.paste(screen,(28,36),high_mask)
    ImageDraw.Draw(framed).rounded_rectangle((218,40,380,68),radius=14,fill='#07060c')
    framed.save(WEB/f'phone-{name}.webp',quality=85,method=6)
icon=Image.open(ASSETS/'icon.png').convert('RGBA')
icon.resize((64,64)).save(ASSETS/'favicon.png')
icon.resize((180,180)).save(ASSETS/'apple-touch-icon.png')

def font(size,bold=False):
    path=Path('C:/Windows/Fonts') / ('arialbd.ttf' if bold else 'arial.ttf')
    return ImageFont.truetype(str(path),size) if path.exists() else ImageFont.load_default(size=size)
og=Image.new('RGB',(1200,630),'#07060e')
glow=Image.new('RGB',og.size)
gd=ImageDraw.Draw(glow)
gd.ellipse((520,50,1170,750),fill='#48136c')
glow=glow.filter(ImageFilter.GaussianBlur(100))
og=Image.blend(og,glow,.75)
od=ImageDraw.Draw(og)
og.paste(icon.resize((52,52)),(70,60),icon.resize((52,52)))
od.text((138,66),'Vin AI',font=font(31,True),fill='white')
od.text((70,177),'Know the car.',font=font(66,True),fill='white')
od.text((70,255),'Before you pay.',font=font(66,True),fill='#c6a6ff')
od.text((73,365),'VIN decode. AI insight. A clearer decision.',font=font(24),fill='#c1b7ce')
od.rounded_rectangle((70,442,390,500),radius=7,fill='#f7f2ff')
od.text((94,456),'Get it on Google Play',font=font(23,True),fill='#21132f')
op=phone.resize((247,510)).rotate(-9,expand=True,resample=Image.Resampling.BICUBIC)
og.paste(op,(855,58),op)
od.text((73,558),'vincheckai.com',font=font(19),fill='#a694bc')
og.save(ROOT/'og.png',optimize=True)

FAQ=[
('What is a VIN?', 'A vehicle identification number (VIN) is a unique 17-character identifier used on modern vehicles. A VIN decoder turns that identifier into vehicle specifications such as model, engine and drivetrain.'),
('Where can I find my VIN?', 'Look at the bottom of the windshield on the driver’s side, on the driver’s door jamb, or on the vehicle registration and insurance documents. In the app, scan it with your camera or type it in.'),
('What does a Vin AI report include?', 'A full AI report brings together decoded specifications, an AI buy / caution / walk verdict and inspection score, red flags, things to inspect, seller questions and negotiation tips. The app also offers market value and mileage information, NHTSA safety recalls, owner complaints and crash ratings, and EPA fuel economy. Coverage and availability vary by vehicle and source.'),
('Is a VIN check free?', 'Basic VIN decode is free in the app. A full AI report costs $3.99 as a one-time purchase, with no subscription needed.')]

def head(title,description,path,schema=None,noindex=False):
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(description)}"><meta name="theme-color" content="#07060e">
<link rel="canonical" href="https://vincheckai.com/{path}"><link rel="icon" href="assets/favicon.png"><link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<meta property="og:type" content="website"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}"><meta property="og:url" content="https://vincheckai.com/{path}"><meta property="og:image" content="https://vincheckai.com/og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Vin AI — Know the car. Before you pay."><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(description)}"><meta name="twitter:image" content="https://vincheckai.com/og.png">
{'<meta name="robots" content="noindex">' if noindex else ''}
<link rel="stylesheet" href="styles.css">{f'<script type="application/ld+json">{json.dumps(schema)}</script>' if schema else ''}</head><body>
<a href="#main" class="skip">Skip to content</a><header class="nav wrap"><a class="brand" href="./" aria-label="Vin AI home"><img src="assets/favicon.png" width="38" height="38" alt=""><span>Vin <span>AI</span></span></a><nav class="navlinks" aria-label="Main navigation"><a href="./#features">Features</a><a href="sample.html">Sample report</a><a href="./#faq">FAQ</a><a class="nav-cta" href="{PLAY}">Get the app <span aria-hidden="true">↗</span></a></nav></header>'''
def footer():
    return '<footer class="footer wrap"><span>© 2026 Vin AI. A little insight. A better decision.</span><div class="footer-links"><a href="https://privacy.vincheckai.com">Privacy policy</a><a href="sample.html">Sample report</a><a href="./#faq">FAQ</a></div></footer></body></html>'
def finalcta():
    return f'<section class="final-cta"><div class="eyebrow">Your next car. Your call.</div><h2>Good decisions start<br>with <span class="chrome">better questions.</span></h2><p>Want this for YOUR car? Enter your own VIN in the app.</p>{play()}<p class="micro">Free basic decode · $3.99 full AI report · No subscription needed</p></section>'

schema={'@context':'https://schema.org','@graph':[{'@type':'SoftwareApplication','name':'Vin AI','applicationCategory':'UtilitiesApplication','operatingSystem':'Android','url':'https://vincheckai.com/','downloadUrl':PLAY,'description':'AI used-car VIN checker. Free basic VIN decode; a full AI report is a one-time $3.99 purchase.','offers':[{'@type':'Offer','name':'Basic VIN decode','price':'0','priceCurrency':'USD'},{'@type':'Offer','name':'Full AI report — one-time purchase','price':'3.99','priceCurrency':'USD'}]},{'@type':'FAQPage','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in FAQ]}]}
index=head('Vin AI — Free VIN Decoder & AI Used Car VIN Check','Check a used car by VIN before you pay. Free VIN decoder, AI insights, red flags and buying advice. Get Vin AI for Android.','',schema)
index+=f'''<main id="main"><div class="wrap"><section class="hero" aria-labelledby="hero-title"><div class="hero-copy"><div class="eyebrow">The AI used-car VIN checker</div><h1 id="hero-title">Know the car.<br><span class="chrome">Before you pay.</span></h1><p class="lead">That used car has a story. Start with its VIN.<br>Get the specs, spot the red flags, and walk into the conversation prepared.</p><div class="actions">{play()}<a class="text-link" href="sample.html">Explore a real report <span aria-hidden="true">↗</span></a></div><p class="micro">Free VIN decode. $3.99 full AI report. No subscription.</p></div><div class="hero-stage" id="phone-stage" role="img" aria-label="3D phone showing the real Vin AI VIN scanner screen"><div class="ring"></div><div class="ring two"></div><img class="phone-fallback" src="assets/web/phone.webp" width="300" height="620" fetchpriority="high" alt="Vin AI app on a phone, ready to scan or enter a VIN"><canvas class="scene" aria-hidden="true"></canvas><div class="float-label first"><small>Less guesswork</small><strong>More confidence.</strong></div><div class="float-label last"><small>Your next move</small><strong><span class="status-dot"></span>Check it. Then decide.</strong></div></div><div class="hero-bottom"><span><i></i> Scroll to look under the hood</span><span>Built for the moment before you buy</span></div></section><div class="capabilities" aria-label="App highlights"><span>Real vehicle specs</span><span>AI buying insights</span><span>10 languages</span><span>Made for Android</span></div></div>
<section class="section wrap" id="features"><div class="section-heading"><div><div class="eyebrow">From VIN to a clearer picture</div><h2>Five moves.<br><span class="chrome">One smarter decision.</span></h2></div><p>Go beyond a VIN lookup. Turn the details into questions worth asking.</p></div><div class="features">'''
features=[('01','⌁','Scan The VIN','Point your camera at the VIN or type it in. Start with a free VIN check of the vehicle’s basic specifications.'),('02','◇','See The Specs','Decode the engine, trim, drivetrain and more. Explore NHTSA recalls, owner complaints and crash ratings, plus EPA fuel economy.'),('03','↗','Know The Price','See market value and mileage information. Put the asking price in context before you start negotiating.'),('04','◎','Spot The Red Flags','Get an AI buy / caution / walk verdict with an inspection score, potential weak points and what to check in person.'),('05','↳','Make The Call','Bring better questions to the seller. Use inspection advice and negotiation tips to plan your next move.')]
for n,icon,title,copy in features:
    index+=f'<article class="feature"><span class="number">{n} / VIN AI</span><span class="feature-icon" aria-hidden="true">{icon}</span><h3>{title}</h3><p>{copy}</p></article>'
index+='<article class="feature"><span class="number">A SECOND OPINION</span><span class="feature-icon" aria-hidden="true">✧</span><h3>Ask a little more.</h3><p>Chat with the AI assistant, including about photos. Get help understanding the details, in any of 10 supported languages.</p></article></div></section>'
index+=f'''<section class="showcase wrap"><div class="screen-stack"><img src="assets/web/flags.webp" width="540" height="1170" loading="lazy" alt="Real Vin AI screen showing red flags and seller questions"><img src="assets/web/compare.webp" width="540" height="1170" loading="lazy" alt="Real Vin AI screen comparing two cars side by side"></div><div><div class="eyebrow">When the shortlist gets shorter</div><h2>Two cars.<br><span class="chrome">A clearer choice.</span></h2><p>Compare two cars side by side. Put their specifications and AI insights next to each other, so you can see the trade-offs before you make the trip.</p><div class="tags"><span>Side-by-side comparison</span><span>AI insights</span><span>Real app screens</span></div></div></section>
<section class="section wrap" id="how-it-works"><div class="eyebrow">Less homework. More headway.</div><h2 style="margin-top:17px">From “looks good”<br>to <span class="chrome">“let’s check.”</span></h2><div class="steps"><article class="step"><b>01 / ENTER</b><h3>Scan or type the VIN.</h3><p>Find the 17-character VIN on the windshield, door jamb or vehicle documents.</p></article><article class="step"><b>02 / UNDERSTAND</b><h3>Let AI connect the dots.</h3><p>Review the decoded specs and get an AI report with risks, questions and practical advice.</p></article><article class="step"><b>03 / DECIDE</b><h3>Go in with confidence.</h3><p>Ask the right questions. Verify the records. Arrange an inspection before you commit.</p></article></div><div class="price-line"><div><strong>$3.99</strong> <span> / full AI report</span><p>One-time purchase. No subscription needed.</p></div><p>Just need the basics? VIN decode is free in the app.</p></div><div class="sample-banner"><div><div class="eyebrow">Try a real example</div><h3>A 2018 Ford Escape. The full picture.</h3><p>A real sample report. An inspection score of 55. See why AI says “caution.”</p></div><a class="sample-button" href="sample.html">See the full report for a 2018 Ford Escape <span aria-hidden="true">↗</span></a></div></section>
<section class="section wrap" id="faq"><div class="faq-layout"><div><div class="eyebrow">A few things to know</div><h2>Good questions.<br><span class="chrome">Clear answers.</span></h2><p>Know what you’re getting before you check your next car.</p></div><div>'''
for q,a in FAQ:
    index+=f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>'
index+='</div></div></section>'+finalcta()+'</main><script type="module" src="app.js"></script>'+footer()
(ROOT/'index.html').write_text(index,encoding='utf-8')

data=json.loads((ROOT/'data/sample_report_ford_escape_2018.json').read_text(encoding='utf-8'))
ai=data['ai']
sample=head('2018 Ford Escape SEL — Full AI Sample Report | Vin AI','Read a real Vin AI report for a 2018 Ford Escape SEL: caution verdict, inspection score 55, risks, weak points and buying advice.','sample.html')
sample+=f'<main id="main" class="wrap"><section class="report-head"><div class="eyebrow">Real report / 2018 Ford Escape SEL</div><h1>Before the test drive,<br><span class="chrome">read between the lines.</span></h1><p>A real Vin AI sample report. The AI guidance below is a snapshot, not proof of this individual vehicle’s condition or history.</p><div class="actions">{play()}<span class="micro">Want this for YOUR car? Enter your own VIN in the app.</span></div></section><div class="report-grid">'
sample+=f'<section class="report-card wide verdict"><div class="score"><b>{ai["inspection_score"]}</b><small>INSPECTION / 100</small></div><div><span class="badge">{esc(ai["verdict_level"].upper())}</span><h2>Proceed with caution.</h2><p>{esc(ai["verdict"])}</p></div></section>'
labels={'year':'Year','make':'Make','model':'Model','trim':'Trim','body':'Body type','fuel':'Fuel','doors':'Doors','cylinders':'Cylinders','displacement':'Engine displacement (L)','driveType':'Drivetrain','transmission':'Transmission','manufacturer':'Manufacturer','country':'Country'}
sample+='<section class="report-card wide"><h2>Vehicle specifications</h2><dl class="specs"><div><dt>VIN</dt><dd>'+esc(data['vin'])+'</dd></div>'
for key,val in data['vehicle'].items():
    sample+=f'<div><dt>{labels[key]}</dt><dd>{esc(val)}</dd></div>'
sample+='</dl></section>'
for key,title in [('summary','The overview'),('reliability','Reliability'),('risk','Risk'),('ownership_cost','Ownership cost'),('budget_warning','Budget warning'),('best_for','Who this car suits'),('should_visit','Worth a visit?'),('red_flags','Red flags'),('weak_points','Weak points'),('what_to_check','What to check'),('questions_to_ask','Questions to ask the seller'),('negotiation_tips','Negotiation tips'),('advice','Your next steps')]:
    value=ai[key]
    content='<ul>'+''.join(f'<li>{esc(v)}</li>' for v in value)+'</ul>' if isinstance(value,list) else f'<p>{esc(value)}</p>'
    sample+=f'<section class="report-card{" wide" if key=="advice" else ""}"><h2>{title}</h2>{content}</section>'
sample+='</div><aside class="report-note">Sample report for illustration.</aside></main>'+finalcta()+footer()
(ROOT/'sample.html').write_text(sample,encoding='utf-8')
notfound=head('Page Not Found | Vin AI','This page could not be found. Return to Vin AI to explore the AI used-car VIN checker.','404.html',noindex=True)
notfound+='<main id="main" class="not-found wrap"><div class="eyebrow">404 / Wrong turn</div><h1>Let’s get you<br><span class="chrome">back on the road.</span></h1><p>We couldn’t find that page.</p><div class="actions"><a class="play" href="./">Back to Vin AI <span aria-hidden="true">↗</span></a><a class="text-link" href="sample.html">See a sample report</a></div></main>'+footer()
(ROOT/'404.html').write_text(notfound,encoding='utf-8')
(ROOT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: https://vincheckai.com/sitemap.xml\n',encoding='utf-8')
(ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://vincheckai.com/</loc></url><url><loc>https://vincheckai.com/sample.html</loc></url></urlset>\n',encoding='utf-8')
(ROOT/'CNAME').write_text('vincheckai.com\n',encoding='utf-8')
vendor=ASSETS/'vendor'
vendor.mkdir(exist_ok=True)
for name in ['three.module.min.js']:
    source=ROOT/'node_modules/three/build'/name
    if source.exists(): shutil.copyfile(source,vendor/name)
shutil.copyfile(ROOT/'node_modules/three/LICENSE',vendor/'THREE-LICENSE.txt')
print('Built index.html, sample.html, 404.html, SEO files and optimized assets.')

from revision import revise
revise(ROOT)
from revision5 import revise as revision5
revision5(ROOT)
from localize import build as localize
from revision7 import revise as revision7
revision7(ROOT)
localize(ROOT)
