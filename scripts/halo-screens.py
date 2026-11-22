"""Halo redesign (2026-11-22): real app captures (black/white UI) -> site screens.
scan/specs/flags come from emulator captures of the live app; compare is the
Halo-styled mock from render-phone-screens.mjs (guest mode cannot open compare)."""
from pathlib import Path
from PIL import Image, ImageDraw
ROOT = Path(__file__).resolve().parent.parent
CAP = Path('C:/dev/projects/vin_ai_redesign/cap2')
PICK = {'scan': 'dec1.png', 'specs': 'r00.png', 'flags': 'r15.png'}
def save(image, path):
    for q in (85, 80, 75, 70, 65, 60):
        image.save(path, quality=q, method=6)
        if path.stat().st_size < 120_000: return
    raise ValueError(f'over budget {path}')
def fit(img):
    img = img.convert('RGB')
    w, h = img.size
    if (w, h) != (1080, 2340):
        img = img.resize((1080, round(h * 1080 / w)), Image.Resampling.LANCZOS)
        top = (img.height - 2340) // 2
        img = img.crop((0, top, 1080, top + 2340))
    return img
for lang_dir in sorted(CAP.iterdir()):
    lang = lang_dir.name
    target = ROOT / 'assets/web/screens' / lang; target.mkdir(parents=True, exist_ok=True)
    src = {k: lang_dir / v for k, v in PICK.items()}
    src['compare'] = ROOT / 'qa/phone-screens' / f'{lang}-compare.png'
    for name, path in src.items():
        screen = fit(Image.open(path))
        save(screen, target / f'{name}.webp')
        phone = Image.new('RGBA', (600, 1240))
        d = ImageDraw.Draw(phone)
        for box, r, c in [((0,0,599,1239),86,'#b9b9bd'),((4,4,592,1234),82,'#1a1a1c'),((14,14,580,1224),74,'#000000')]:
            d.rounded_rectangle(box, radius=r, fill=c)
        mask = Image.new('L', (540,1170)); ImageDraw.Draw(mask).rounded_rectangle((0,0,539,1169), radius=58, fill=255)
        phone.paste(screen.resize((540,1170), Image.Resampling.LANCZOS), (28,36), mask)
        ImageDraw.Draw(phone).rounded_rectangle((218,40,380,68), radius=14, fill='#000000')
        save(phone, target / ('phone.webp' if name == 'scan' else f'phone-{name}.webp'))
    print(lang, 'ok')
