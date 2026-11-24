"""Titles without the word "free" (owner decision 2026-11-24: the full report is paid, so a
"free" title misleads). The body text still says the basic web decode is free, which is true.
Runs on the built HTML: replaces the old title text (title, og/twitter, h1, JSON-LD, footer links).

    python scripts/seo_titles.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BRANDS = ['Ford', 'Toyota', 'Chevrolet', 'Honda', 'Nissan']

# lang: (index pairs, decode pairs, brand pair template)
MAP = {
    'en': ([('Vin AI — Free VIN Decoder &amp; AI Used Car VIN Check', 'VIN Decoder &amp; Used Car VIN Check | Vin AI'),
            ('Vin AI — Free VIN Decoder & AI Used Car VIN Check', 'VIN Decoder & Used Car VIN Check | Vin AI')],
           [('Free VIN Decoder | Vin AI', 'VIN Decoder: Make, Model, Engine by VIN | Vin AI')],
           ('Free {B} VIN decoder', '{B} VIN Decoder: Specs by VIN')),
    'ru': ([('Vin AI — бесплатная расшифровка VIN и проверка авто перед покупкой', 'Расшифровка VIN и проверка авто по VIN | Vin AI')],
           [('Бесплатная расшифровка VIN | Vin AI', 'Расшифровка VIN: марка, модель, двигатель | Vin AI')],
           ('Расшифровка VIN {B} бесплатно', 'Расшифровка VIN {B}: данные по VIN')),
    'de': ([('Vin AI – Kostenloser VIN-Decoder und KI-Gebrauchtwagen-VIN-Check', 'VIN-Decoder &amp; Gebrauchtwagen-VIN-Check | Vin AI')],
           [('Kostenloser VIN-Decoder | Vin AI', 'VIN-Decoder: Marke, Modell, Motor | Vin AI')],
           ('{B} FIN Decoder kostenlos', '{B} FIN Decoder: Daten per FIN')),
    'es': ([('Vin AI — Decodificador VIN y coche usado con IA VIN Check gratuito', 'Decodificador VIN y VIN check de coches usados | Vin AI')],
           [('Decodificador VIN gratuito | Vin AI', 'Decodificador VIN: marca, modelo y motor | Vin AI')],
           ('Decodificador VIN {B} gratis', 'Decodificador VIN {B}: datos por VIN')),
    'fr': ([("Vin AI — Décodeur VIN gratuit et vérification AI VIN des voitures d'occasion", "Décodeur VIN et vérification VIN d'occasion | Vin AI"),
            ('Vin AI — Décodeur VIN gratuit et vérification AI VIN des voitures d&#x27;occasion', 'Décodeur VIN et vérification VIN d&#x27;occasion | Vin AI')],
           [('Décodeur VIN gratuit | Vin AI', 'Décodeur VIN : marque, modèle, moteur | Vin AI')],
           ('Décodeur VIN {B} gratuit', 'Décodeur VIN {B} : données par VIN')),
    'it': ([('Vin AI: decodificatore VIN gratuito e controllo AI per auto usate VIN', 'Decoder VIN e controllo VIN auto usate | Vin AI')],
           [('Decoder VIN gratuito | Vin AI', 'Decoder VIN: marca, modello e motore | Vin AI')],
           ('Decodifica VIN {B} gratis', 'Decodifica VIN {B}: dati dal VIN')),
    'pt': ([('Vin AI — Decodificador VIN gratuito e verificação AI de carro usado VIN', 'Decodificador VIN e consulta de carro usado | Vin AI')],
           [('Decodificador VIN gratuito | Vin AI', 'Decodificador VIN: marca, modelo e motor | Vin AI')],
           None),
    'tr': ([('Vin AI — Ücretsiz VIN Dekoder ve Yapay Zeka Kullanılmış Araba VIN Kontrolü', 'VIN Çözücü ve İkinci El Araç VIN Kontrolü | Vin AI')],
           [('Ücretsiz VIN Çözücü | Vin AI', 'VIN Çözücü: Marka, Model, Motor | Vin AI')],
           ('{B} VIN sorgulama ücretsiz', '{B} VIN sorgulama: VIN ile bilgiler')),
    'ko': ([('Vin AI — 무료 VIN 해독 및 AI 중고차 조회', 'VIN 해독 및 AI 중고차 조회 | Vin AI')],
           [('무료 VIN 해독기 | Vin AI', 'VIN 해독기: 제조사·모델·엔진 | Vin AI')],
           ('{B} 차대번호 조회 · VIN 조회 무료', '{B} 차대번호 조회 · VIN 조회')),
    'zh': ([('Vin AI — 免费 VIN 解码与 AI 二手车查询', 'VIN 解码与 AI 二手车查询 | Vin AI')],
           [('免费VIN解码器 | Vin AI', 'VIN解码器：品牌、车型、发动机 | Vin AI')],
           ('{B} VIN码查询 免费', '{B} VIN码查询')),
}


def main():
    changed = 0
    for lang, (index, decode, brand) in MAP.items():
        pairs = index + decode
        if brand:
            pairs += [(brand[0].format(B=b), brand[1].format(B=b)) for b in BRANDS]
        folder = ROOT if lang == 'en' else ROOT / lang
        for path in folder.glob('*.html'):
            text = path.read_text(encoding='utf-8')
            new = text
            for old, rep in pairs:
                new = new.replace(old, rep)
            if new != text:
                path.write_text(new, encoding='utf-8')
                changed += 1
    print('pages updated:', changed)


if __name__ == '__main__':
    main()
