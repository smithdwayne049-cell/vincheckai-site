"""Halo redesign (2026-11-22): token packs on pricing.html in all 10 languages.
Runs last in build.py, after revision7 writes the old two-card grid.
Labels come from the app's own translations (vin_app_v2/assets/translations)."""
import re, json
from pathlib import Path
APP = Path('C:/dev/projects/vin_app_v2/assets/translations')
CARS = {'en':('1 car','2 cars','5 cars','What tokens pay for'),'ru':('1 машина','2 машины','5 машин','На что идут токены'),'de':('1 Auto','2 Autos','5 Autos','Wofür Tokens'),'es':('1 coche','2 coches','5 coches','Para qué sirven los tokens'),'fr':('1 voiture','2 voitures','5 voitures','À quoi servent les jetons'),'it':('1 auto','2 auto','5 auto','A cosa servono i token'),'pt':('1 carro','2 carros','5 carros','Para que servem os tokens'),'tr':('1 araç','2 araç','5 araç','Jetonlar ne için'),'ko':('자동차 1대','자동차 2대','자동차 5대','토큰 사용처'),'zh':('1 辆车','2 辆车','5 辆车','代币用途')}
PACKS = [(0,'4.99',50,'$4.99',False),(1,'8.99',100,'$4.50',False),(2,'10.99',250,'$2.20',True)]
def revise(root):
    root = Path(root)
    for lang in CARS:
        p = root / ('pricing.html' if lang == 'en' else f'{lang}/pricing.html')
        s = p.read_text(encoding='utf8')
        m = re.search(r'<div class="pricing-grid">(.*?)</div><section class="pricing-explainer">', s, re.S)
        if not m: continue  # already packs
        d = json.loads((APP / f'{lang}.json').read_text(encoding='utf8'))
        cards = re.findall(r'<section class="pricing-card"><h2>(.*?)</h2>.*?<p class="micro">(.*?)</p><ul>(.*?)</ul><a class="play" href="([^"]+)">(.*?)</a></section>', m.group(1), re.S)
        (rep, once, feat, href, btn), (cmp_, _, cfeat, _, _) = cards
        names = CARS[lang]
        tok = lambda n: d['wallet_pack_tokens'].replace('{}', str(n))
        per = lambda v: d['wallet_per_car'].replace('{}', v)
        html = '<div class="pricing-grid packs">'
        for i, price, n, pc, best in PACKS:
            html += f'<section class="pricing-card{" best" if best else ""}">' + (f'<span class="pack-badge">{d["wallet_best"]}</span>' if best else '') + f'<h2>{names[i]}</h2><p class="price-tag">${price} <span>USD</span></p><p class="pack-tokens">{tok(n)} · {per(pc)}</p><p class="micro">{once}</p><a class="play" href="{href}">{btn}</a></section>'
        html += f'</div><section class="token-uses-wrap"><h2 style="font-size:30px;letter-spacing:-1px;margin-top:48px">{names[3]}</h2><div class="token-uses"><div><b>{rep}</b><span class="pack-tokens">{tok(50)}</span><ul>{feat}</ul></div><div><b>{cmp_}</b><span class="pack-tokens">{tok(100)}</span><ul>{cfeat}</ul></div><div><b>{d["photo_check_title"]}</b><span class="pack-tokens">{tok(25)}</span></div></div></section>'
        p.write_text(s.replace(m.group(0), html + '<section class="pricing-explainer">'), encoding='utf8')
if __name__ == '__main__':
    revise(Path(__file__).resolve().parent.parent)
