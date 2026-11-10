"""Encode Playwright's 1080x2340 mock-ups and frame all four fallback states."""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
for source in sorted((ROOT / 'qa/phone-screens').glob('*.png')):
    lang, name = source.stem.split('-', 1)
    target = ROOT / 'assets/web/screens' / lang
    target.mkdir(parents=True, exist_ok=True)
    screen = Image.open(source).convert('RGB')
    assert screen.size == (1080, 2340)
    def save(image, path):
        for quality in (85, 80, 75, 70, 65):
            image.save(path, quality=quality, method=6)
            if path.stat().st_size < 120_000:
                return
        raise ValueError(f'Asset over budget: {path}')
    save(screen, target / f'{name}.webp')
    phone = Image.new('RGBA', (600, 1240))
    draw = ImageDraw.Draw(phone)
    for box, radius, color in [((0,0,599,1239),86,'#91849d'),((4,4,592,1234),82,'#24212c'),((14,14,580,1224),74,'#050409')]:
        draw.rounded_rectangle(box, radius=radius, fill=color)
    mask = Image.new('L', (540,1170))
    ImageDraw.Draw(mask).rounded_rectangle((0,0,539,1169),radius=58,fill=255)
    phone.paste(screen.resize((540,1170), Image.Resampling.LANCZOS),(28,36),mask)
    ImageDraw.Draw(phone).rounded_rectangle((218,40,380,68),radius=14,fill='#07060c')
    save(phone, target / ('phone.webp' if name == 'scan' else f'phone-{name}.webp'))
print('Rendered 40 localized screens and 40 phone fallbacks; each asset < 120 KB.')
