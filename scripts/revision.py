"""Revision 2 HTML composition; all report facts stay in the source JSON files."""
import html,json,re
from collections import Counter
from pathlib import Path
E=lambda x:html.escape(str(x),quote=True)

def icon(n=0):
 paths=['M4 7h16v14H4z M8 3h8v4 M8 12h8 M8 16h5','M12 3 3 7v6c0 5 9 9 9 9s9-4 9-9V7z M8 12l3 3 5-6','M5 19 19 5 M5 5h14v14','M3 12h18 M12 3v18']
 return f'<svg class="line-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="{paths[n%4]}"/></svg>'

def photo(name,eager=False):
 return f'<picture class="cinema" aria-hidden="true"><source media="(max-width:700px)" srcset="assets/backgrounds/{name}-mobile.webp"><img src="assets/backgrounds/{name}.webp" width="1920" height="1080" alt="" loading="{"eager" if eager else "lazy"}" {"fetchpriority=high" if eager else ""}></picture><div class="cinema-shade" aria-hidden="true"></div>'

def revise(root):
 play='https://play.google.com/store/apps/details?id=com.vinai.app'
 p=root/'index.html';s=p.read_text(encoding='utf-8')
 s=s.replace('<section class="hero" aria-labelledby="hero-title">','<section class="hero cinematic" aria-labelledby="hero-title">'+photo('hero',True))
 s=s.replace('Before you pay.</span>','Before you <em>pay.</em></span>')
 s=s.replace('<canvas class="scene" aria-hidden="true"></canvas>', '<canvas class="scene" aria-hidden="true"></canvas><div class="phone-chapters" aria-hidden="true">'+''.join(f'<span class="phone-chapter{ " active" if i == 0 else ""}"><small>0{i+1} / VIN AI</small>{title}</span>' for i,title in enumerate(['Scan The VIN','See The Specs','Spot The Red Flags','Side-by-side comparison']))+'</div>')
 s=s.replace('<section class="section wrap" id="features">','<section class="section wrap cinematic features-stage" id="features">'+photo('details'))
 i=iter(range(6))
 s=re.sub(r'<span class="feature-icon" aria-hidden="true">.*?</span>',lambda _:f'<span class="feature-icon">{icon(next(i))}</span>',s)
 s=s.replace('class="final-cta"','class="final-cta cinematic"').replace('<section class="final-cta cinematic">','<section class="final-cta cinematic">'+photo('road'))
 p.write_text(s,encoding='utf-8')
 p=root/'sample.html';s=p.read_text(encoding='utf-8')
 s=s.replace('<section class="report-head">','<section class="report-head cinematic">'+photo('sample',True))
 s=s.replace('Before the test drive,<br><span class="chrome">read between the lines.</span>','2018 Ford Escape <em class="chrome">SEL.</em>')
 vin=json.loads((root/'data/sample_report_ford_escape_2018.json').read_text(encoding='utf-8'))['vin']
 chips=['1.5L 4-cyl turbo gasoline','Automatic','4WD','SUV','Built in USA']
 s=s.replace('<p>Sample report for illustration.',f'<div class="vin-scan"><span>VIN /</span> {E(vin)}</div><div class="spec-chips">'+''.join(f'<span>{x}</span>' for x in chips)+'</div><p>Sample report for illustration.')
 s=s.replace('<div class="report-grid">','<nav class="report-nav" aria-label="Report sections">'+''.join(f'<a href="#{key}">{title}</a>' for key,title in [('overview','Overview'),('specs','Specs'),('verdict','Verdict'),('red-flags','Red flags'),('nhtsa','Recalls & complaints'),('check','What to check'),('seller','Ask the seller'),('negotiate','Negotiate')])+'</nav><div class="report-grid">')
 s=s.replace('<section class="report-card wide verdict">','<section id="verdict" class="report-card wide verdict">')
 s=s.replace('<div class="score"><b>55</b><small>INSPECTION / 100</small></div>','<div class="score" aria-label="Inspection score 55 out of 100"><svg viewBox="0 0 160 160" aria-hidden="true"><circle class="score-track" cx="80" cy="80" r="68"/><circle class="score-fill" cx="80" cy="80" r="68" pathLength="100"/></svg><div><b data-count="55">55</b><small>/ 100</small><span>INSPECTION SCORE</span></div></div>')
 # Turn every report content card into an accessible disclosure, expanded on desktop.
 ids={'Vehicle specifications':'specs','The overview':'overview','Red flags':'red-flags','What to check':'check','Questions to ask the seller':'seller','Negotiation tips':'negotiate'}
 counter=iter(range(1,30))
 def card(m):
  classes,title,content=m.groups();classes=classes or "";num=next(counter);key=ids.get(title,'report-'+str(num))
  tint=' danger' if title in ['Red flags','Weak points','Risk'] else ' positive' if title in ['What to check','Negotiation tips','Your next steps'] else ''
  content=content.replace('<ul>','<ol>').replace('</ul>','</ol>')
  return f'<details open id="{key}" class="report-card disclosure{classes}{tint}"><summary>{icon(num)}<span><small>REPORT / {num:02}</small>{title}</span></summary><div class="report-content">{content}</div></details>'
 s=re.sub(r'<section class="report-card( wide)?"><h2>(.*?)</h2>(.*?)</section>',card,s)
 n=json.loads((root/'data/nhtsa_ford_escape_2018.json').read_text(encoding='utf-8'))
 recalls=n['recalls']['results'];complaints=n['complaints']['results']
 components=Counter()
 for row in complaints:
  for component in set(x.strip() for x in row.get('components','').split(',') if x.strip()):components[component]+=1
 top=components.most_common(6);maximum=top[0][1] if top else 1
 nh=f'<section id="nhtsa" class="report-card wide nhtsa"><div class="eyebrow">Public safety data</div><h2>{icon(1)} Recalls & owner complaints</h2><p class="source-note">Source: NHTSA, public data for all 2018 Ford Escape vehicles, not this specific VIN. Retrieved {E(n["fetched_at"][:10])}. A recall listed here does not establish whether this car is affected or repaired. Verify open recalls using your VIN with NHTSA or a Ford dealer.</p><div class="safety-counts"><div><b data-count="{len(recalls)}">{len(recalls)}</b><span>Recall campaigns</span></div><div><b data-count="{len(complaints)}">{len(complaints):,}</b><span>Owner complaints</span></div></div><div class="safety-grid"><div><h3>Recall campaigns</h3>'
 for row in recalls:
  nh+=f'<details class="recall"><summary><span><small>{E(row.get("NHTSACampaignNumber",""))}</small>{E(row.get("Component",""))}</span></summary><p>{E(row.get("Summary",""))}</p></details>'
 nh+='</div><div><h3>Most reported components</h3><p class="micro">Complaint reports may name multiple components. Counts are reports, not verified defects.</p><ol class="bar-chart">'
 for label,count in top:
  nh+=f'<li><div><span>{E(label.title())}</span><b>{count:,}</b></div><div class="bar-track"><span style="width:{count/maximum*100:.2f}%"></span></div></li>'
 nh+=f'</ol><div class="source-links"><a href="{E(n["sources"]["recalls"])}">NHTSA recall source ↗</a><a href="{E(n["sources"]["complaints"])}">NHTSA complaint source ↗</a></div></div></div></section>'
 s=s.replace('</div><aside class="report-note">',nh+'</div><aside class="report-note">')
 s=s.replace('Market value, mileage and live NHTSA / EPA results are not included in this snapshot.','Market value, mileage and EPA results are not included in this snapshot. NHTSA model-year data above is separate from the AI snapshot.')
 s=s.replace('<section class="final-cta">','<section class="final-cta cinematic">'+photo('road'))
 s=s.replace('</body>',f'<a class="mobile-download" href="{play}">Check YOUR car <span>Get Vin AI ↗</span></a><script type="module" src="report.js"></script></body>')
 p.write_text(s,encoding='utf-8')

# Invoked once by build.py after generating the base HTML templates.
