"""Revision 5 copy and structure, before offline localization."""
import re

NOTICE = 'Vin AI provides informational insights to help you decide. Always inspect a car before you buy.'

def revise(root):
    for name in ('index.html', 'sample.html', '404.html'):
        path = root / name
        text = path.read_text(encoding='utf-8')
        text = text.replace('<footer class="footer wrap">', '<footer class="footer wrap"><p class="footer-notice">' + NOTICE + '</p>')
        if name == 'index.html':
            # The assistant remains visible outside the five-card scroll track.
            text = text.replace('<article class="feature"><span class="number">A SECOND OPINION', '</div><article class="feature assistant-feature"><span class="number">A SECOND OPINION')
            text = text.replace('10 supported languages.</p></article></div></section>', '10 supported languages.</p></article></section>')
            text = text.replace('<div class="features">', '<div class="feature-window"><div class="features">')
            text = text.replace('</div><article class="feature assistant-feature">', '</div></div><article class="feature assistant-feature">')
            text = text.replace('<section class="showcase wrap">', '<section class="kinetic wrap"><h2>Check the VIN. Then decide.</h2></section><section class="showcase wrap">')
        if name == 'sample.html':
            text = re.sub(r'<aside class="report-note">.*?</aside>', '<aside class="report-note">Sample report for illustration.</aside>', text)
            text = re.sub(r'<p>A real Vin AI sample report\..*?</p>', '<p>Sample report for illustration.</p>', text)
        path.write_text(text, encoding='utf-8')
