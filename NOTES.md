# Revision 5 - current behavior (supersedes earlier revision notes)

- Removed the limitations FAQ from all ten languages and FAQPage JSON-LD (four questions remain). Removed the old history-limitations copy from generated pages and translation dictionaries. All pages have one small translated footer notice: "Vin AI provides informational insights to help you decide. Always inspect a car before you buy." The sample introduction and bottom caption now say only "Sample report for illustration." No new history or accuracy claims were added.
- Full motion: desktop pinned hero rotates the real Three.js phone through four app screens. Its headline scales and blurs away in the same scrubbed timeline. A second desktop pinned section moves the five feature cards horizontally; the AI assistant card stays below the track. Mobile uses a native vertical stack. The localized oversized "Check the VIN. Then decide." heading lights up word by word with scroll. Automotive backgrounds reveal with a clip-path wipe. Existing report score, ring, counters, bars and card staggers remain.
- Reduced motion: a lightweight, deferred `gentle-motion.js` module uses IntersectionObserver and native Web Animations for opacity fades, rises of at most 10px, report counters and score-ring fill; report bars fade in. A small eyebrow glow animates in colour/opacity. No Lenis, GSAP, pinning, scrub, parallax or WebGL is loaded in this mode. Content is visible without JavaScript, and changing the OS preference cleans up and switches effects live.
- Dependencies unchanged: GSAP/ScrollTrigger 3.15.1, Lenis 1.3.27, Three.js 0.170.0; all served locally. The Three.js phone still loads after first paint, uses DPR <=2 and pauses off-screen; weak devices and unavailable WebGL retain the static phone.
- Build: `python scripts/build.py`; base templates -> `scripts/revision.py` -> `scripts/revision5.py` -> offline localization. New translations live in all ten `i18n/*.json` dictionaries. `scripts/task5-copy.py` records the offline translations added for this revision. Include **gentle-motion.js** with the existing runtime files when preparing a future upload.
- New browser regression suite: `npm.cmd run check:revision5`. It passed en/ru/zh in both motion modes at 360px and 1440px: actual gentle animation <=12px, full five-card horizontal travel, native mobile flow, final report counters/ring, four-question FAQ/schema, neutral footer/captions, no horizontal overflow and no console/page errors. Screenshots: ignored `qa/r5-*`. Visually inspected the hero, Russian horizontal track and Chinese mobile reduced-motion layout.
- Existing regression suites also passed: `npm.cmd run check:i18n` (all 20 localized pages at both widths), `npm.cmd run check:motion` (four rendered phone textures, anchors, WebGL hover, live preference changes and responsive cleanup), and `npm.cmd run check` (including 404, full report text and unavailable WebGL). The general mobile test now scrolls to the phone before expecting 3D, matching its existing 70%-visible lazy-loading condition.
- Local Lighthouse 12.8.2 mobile: landing **Performance 96 / Accessibility 100 / Best Practices 100 / SEO 100**; sample **Performance 99 / Accessibility 100 / Best Practices 100 / SEO 100**. Both exceed the requested 85. Reports: `qa/lighthouse-r5-index.json`, `qa/lighthouse-r5-sample.json`. These are local simulated results; physical Android and production hosting were not tested.
- No commit, push, deployment, publication, payment or secret access was performed.

---

# Vin AI website

## Revision 3 — ten static languages

- English remains at `/` and `/sample.html`. Russian, German, Spanish, French, Italian, Portuguese, Turkish, Korean and Simplified Chinese have `/<lang>/` and `/<lang>/sample.html`. All twenty pages contain their complete text at build time; JavaScript and translation services are not needed to read them. The English 404 page is retained.
- `scripts/build.py` generates the original presentation, applies Revision 2, then runs `scripts/localize.py`. All language copy is stored in UTF-8 `i18n/{en,ru,de,es,fr,it,pt,tr,ko,zh}.json`. The keys are English source strings; values are the language's copy. This covers headings, navigation, FAQ, metadata, accessibility labels, vehicle values and every supplied AI report sentence/list item. Report facts, VIN, score 55, prices and source data stay unchanged. Original app screenshots remain the supplied English screenshots.
- The native disclosure language selector uses a globe and all ten native language names, supports keyboard/touch, and retains the current page type. The active language is marked with `aria-current`. There are no automatic redirects, browser-language requests, cookies or browser storage.
- Each localized page has its own canonical, HTML language, translated title/description and OG/Twitter text. Each has reciprocal hreflang links to all ten languages and English `x-default`. The sitemap contains 20 URLs with 220 alternate links. Landing-page SoftwareApplication includes `inLanguage` and localized copy; FAQPage uses the exact visible FAQ questions and answers.
- Every localized download link includes `hl`, with `zh-CN` and `pt-BR` for Chinese and Portuguese. Assets are shared, using correct relative URLs. The Three.js phone texture now resolves relative to its module, including in nested language routes.
- NHTSA recall components and summaries remain verbatim official English with an explicitly translated note. The introduction, counts, source links, disclosure labels and explanation of model-year coverage are translated. AI recommendations and official-history limitations are translated in every language.
- Responsive wrapping supports long text without overflow at 360px. Korean and Chinese use system font fallbacks, without external font requests. Automatic dictionary hyphenation was removed after it caused slow mobile layout in Chrome; long text still wraps with CSS.
- Translation copy was checked for product terminology, pricing, report facts and limitations. Some language drafts used machine translation and were edited; no external native-speaker review was performed. The build itself is fully offline and has no translation API dependency.

### Editing a translation

1. Edit **values** in `i18n/<lang>.json`; keep the English keys, JSON syntax and UTF-8 encoding. For example, change the value of `"Sample report"` in `i18n/de.json`. English wording can also be edited in `i18n/en.json` and is preserved on rebuild.
2. Keep `Vin AI`, `VIN`, model names, numeric facts and `$3.99` intact. Preserve the meaning of all official-history limitations. NHTSA source text stays unchanged.
3. Run `python scripts/build.py`. Do not edit generated `index.html` or language HTML files directly. For new content/markup, edit the base templates or `scripts/revision.py`, then add translations of the new source keys to each JSON file. The build fails on a missing or empty non-English translation instead of quietly falling back to English.
4. Start `python -m http.server 4173 --bind 127.0.0.1`, then run `npm.cmd run check:i18n` and `npm.cmd run check`.

### Revision 3 validation

- Browser checks cover all 20 pages at **360px and 1440px**, translated report completeness, FAQ/schema agreement, canonical/hreflang links, Play language parameters, language switching, images, reduced motion and console/page errors. A separate normal-motion check verifies the actual Three.js scene at `/de/`. Desktop/mobile screenshots for German, Russian and Chinese are saved in ignored `qa/`.
- Existing English checks also cover the English 404, actual 3D initialization, disabled-WebGL fallback, reduced-motion fallback, report disclosures, source report text and NHTSA counts.
- Final local Lighthouse mobile result for `/ru/`: **Performance 96 / Accessibility 100 / Best Practices 100 / SEO 100**. Report: `qa/lighthouse-r3-ru-final.json`. This is a simulated local result; physical Android hardware and production hosting were not tested.
- No required Revision 3 feature remains unfinished. The optional browser-language suggestion banner was omitted. No commit, push, deployment, publication, payment or secret access was performed.

For a future static upload, include the original runtime files/assets **and all nine language folders** (`ru`, `de`, `es`, `fr`, `it`, `pt`, `tr`, `ko`, `zh`). `i18n/`, `scripts/`, and `data/` are build inputs; development dependencies, QA files and logs are not runtime files.

Built locally from TASK.md. No commit, push, publication, payment or deployment was performed.

## Delivered

- English static landing page with neon violet/pink styling, chrome-style headings, glowing orb, rings and particles.
- Lazy-loaded Three.js phone with the real supplied app screen, metallic body, pointer tilt and scroll movement. Rendering pauses outside the viewport or when the tab is hidden. Pixel ratio is capped at 2.
- Static phone fallback for reduced motion, unavailable WebGL2, low device memory / CPU count, data saver and failed scene loading. A change to reduced motion also disposes the running scene.
- Feature descriptions, two-car comparison with real screens, three steps, $3.99 one-time report pricing, free basic decode, native HTML FAQ and download links.
- Complete sample report generated from `data/sample_report_ford_escape_2018.json`. All original AI fields and vehicle specifications are preserved, including caution / score 55. The supplied screenshots illustrate the app; they are not represented as screenshots of this Ford report.
- 404 page, robots.txt, sitemap.xml, CNAME, icon-derived favicon, 1200×630 og.png, canonical URLs, unique page metadata, Open Graph / Twitter cards, SoftwareApplication and FAQPage JSON-LD.
- Explicit limitations: no official title / accident / salvage / lien history. No invented ratings, reviews or usage claims.

## Run locally

The checked-in HTML and runtime assets work as-is, with no build step or network dependencies:

```text
python -m http.server 4173 --bind 127.0.0.1
```

Open http://127.0.0.1:4173/ . Use a static server rather than opening HTML with `file://` (the 3D module needs HTTP).

For future content or asset regeneration:

```text
npm.cmd ci --cache .npm-cache
python -m pip install -r requirements.txt
python scripts/build.py
```

Edit landing-page and report templates in `scripts/build.py`; edit visual styling in `styles.css` and scene behavior in `app.js`. Rebuild after changing the report JSON. No browser-side report fetch is required; the full report is real HTML, including without JavaScript.

## Libraries / tools

- Three.js 0.170.0, vendored locally in `assets/vendor/three.module.min.js`; license included. No GSAP or external fonts.
- Pillow 13.0.0 for deterministic image optimization, icon sizes, phone frame and social-card layout. Original screenshots remain untouched.
- Playwright 1.56.1 with installed Google Chrome for browser verification.
- Lighthouse 12.8.2 for mobile lab measurements.
- Python 3.12.9 / Node.js 24.19.0 used for build and checks. Neither is needed on production hosting.

## Verification

`node scripts/check.mjs` (while the local server is running) verifies all three pages at desktop 1440px, mobile 360px and reduced motion; a separate context disables WebGL. Checks include no horizontal overflow, image loading and proportions, local links, FAQ interaction, JSON-LD parsing, all supplied AI report text and no JavaScript / console errors. Normal desktop and mobile contexts also verify that the 3D scene becomes active. Screenshots are saved in ignored `qa/`.

Original revision Lighthouse mobile lab result for the local landing page (superseded by Revision 2 below): **Performance 99 / Accessibility 100 / Best Practices 100 / SEO 100**. LCP 1.4 s, CLS 0, total blocking time 100 ms. Report: ignored `qa/lighthouse.json`. These are local simulated results, not a guarantee for every device or hosting provider. Real physical Android hardware was not available for testing.

## Remaining / optional

No required site feature is intentionally left unfinished. Revision 2 adds a saved NHTSA model-year snapshot, rendered as static HTML; see below. No runtime requests go to NHTSA or an AI service. Hosting must supply HTTPS and its normal compression / caching policy. Production deployment and domain configuration were not performed.

For a static upload, use `index.html`, `sample.html`, `404.html`, `styles.css`, `app.js`, `og.png`, `robots.txt`, `sitemap.xml`, `CNAME` `motion.js`, `report.js` and `assets/`. Do not upload development dependencies, QA output or local logs. The `data/` and `scripts/` folders are build inputs and are not required at runtime.


## Revision 2 ? cinematic automotive design

- Four AI-generated illustrations created with the built-in imagegen tool: hero SUV on wet night street, headlight/wheel detail, showroom compact SUV and night road with light trails. These are generic illustrations, not photographs of the sample VIN. No people, branding, readable plates or image text were requested.
- Final assets: `assets/backgrounds/{hero,details,sample,road}.webp` (1920?1080, 108?188 KB each) and corresponding `-mobile.webp` crops (900?1200, 73?103 KB). All eight files are below 250 KB. Originals remain at the generator's default location; production uses only workspace assets.
- Photos sit behind violet overlays, subtle SVG turbulence grain, glow and real HTML content. Below-fold images are native lazy-loaded. Small scroll parallax stops with reduced motion. The Three.js phone stays in front of the hero car.
- Layered glass cards, inner highlights, desktop hover tilt, shimmering border highlight, section light lines, chrome headings with serif italic accents and consistent inline SVG icons.
- Sample header now identifies the vehicle, VIN scan line and key specifications. A dimensional animated 55/100 score ring, sticky eight-section navigation, coloured report cards, numbered lists, mobile disclosures and sticky Google Play link complete the report presentation. Without JavaScript, all original report content stays expanded and readable.
- `data/nhtsa_ford_escape_2018.json` contains the actual complete NHTSA responses and retrieval timestamp. This fetch returned **4 recall campaigns and 1,825 complaints**. Static HTML shows each recall component and expandable summary, plus the six most reported complaint components. Each complaint counts once per named component; a complaint can name multiple components. All model-year data is explicitly separate from the sample VIN and AI report. Source URLs are shown in the report; no runtime API requests are needed.
- `scripts/revision.py` composes the revision after base templates inside `python scripts/build.py`. Rebuild with that command; do not run the composition function on already revised HTML. New runtime modules: `motion.js` and `report.js`.
- The GPU scene is initialized when at least 70% of the phone stage is visible, after load and idle time. This avoids compiling a scene for a mostly off-screen phone on small screens. The static phone is immediately available. Existing weak-device, reduced-motion and no-WebGL fallbacks remain.

### Revision 2 validation

Playwright passed all three pages at 1440px and 360px, reduced motion and disabled WebGL. Checks include image loading/proportions (intentional cover crops exempt), no horizontal page overflow, working disclosures and nav opening a collapsed section, all original AI report text, NHTSA campaign/complaint counts, links, structured metadata and no console or JavaScript errors. Screenshots are in ignored `qa/`.

Mobile Lighthouse local lab results: **landing Performance 89 / Accessibility 100 / Best Practices 100 / SEO 100**; **sample Performance 99 / Accessibility 100 / Best Practices 100 / SEO 100**. Landing LCP 2.6 s, TBT 350 ms, CLS 0. Reports: `qa/lighthouse-r2-index.json`, `qa/lighthouse-r2-sample.json`. Physical Android hardware was not available; hosting performance may differ. No commit, push, payment, deployment or publication was performed.

### Image generation prompt set

Tool: built-in `image_gen.imagegen`, opaque backgrounds, one generation per asset. Prompts:

1. Hero: Wide cinematic premium automotive website background, photorealistic generic modern compact SUV on wet dark city studio street at night, three-quarter front view occupying right center, violet and neon pink rim lighting, bright subtle silver body reflections, shallow depth of field, luxurious editorial car photography, wide 16:9, negative space at left for white headline. No logos badges license plate lettering text people or watermark.
2. Details: Wide cinematic macro automotive detail photography for premium website background, close up generic compact SUV headlight and front wheel, violet luminous reflections and silver metallic textures, dark luxury studio, sharp sophisticated materials, wide 16:9. No logos badges readable plates text people or watermark.
3. Sample: Wide cinematic luxury showroom photography of a generic 2018 era compact SUV similar proportions to 2018 Ford Escape, silver metallic paint, three quarter front view right of frame, dramatic violet spotlights neon pink rim light and polished reflecting floor, rich premium product photography, dark negative space on left, wide 16:9. No logos badges readable plates text people or watermark.
4. Road: Wide cinematic premium night road background, sweeping empty mountain road disappearing into violet dusk, delicate neon pink and violet long exposure light trails, glossy asphalt reflecting lights, atmospheric rich dark blue purple sky, luxurious automotive campaign photography, wide 16:9. No vehicles logos text people or watermark.

## Revision 4 — Lenis + GSAP premium motion

- Local runtime dependencies: **Lenis 1.3.27**, **GSAP 3.15.1 + ScrollTrigger 3.15.1**, existing **Three.js 0.170.0**. Exact npm names, versions and upstream repository URLs were verified using `npm view` before installation. No React or other new dependencies. `package-lock.json` pins the installation. Runtime copies are in `assets/vendor/`; `LENIS-LICENSE.txt` and `GSAP-LICENSE.txt` accompany them, alongside the original Three.js license. GSAP's license text was retrieved from https://gsap.com/community/standard-license/; npm does not include a separate license file. Package sources: https://www.npmjs.com/package/lenis and https://www.npmjs.com/package/gsap.
- `motion.js` waits for load and idle time before importing `motion-engine.js`, which loads the local libraries. Lenis emits `scroll` to `ScrollTrigger.update`; the GSAP ticker calls `lenis.raf(time * 1000)`, with lag smoothing disabled. Touch scrolling stays native (`syncTouch:false`). Same-page anchors retain hashes and keyboard focus; report links expand their disclosure before scrolling. The anchor calculation accounts for reveal transforms and avoids double CSS scroll offsets.
- Hero intro: actual HTML words rise with a small desktop blur, italic accent follows with a glow, then CTA and phone. The car pushes in slowly. Heading splitting preserves inline emphasis, line breaks and each language's text; Chinese/Korean use `Intl.Segmenter` where available.
- On capable desktop viewports (at least 1100px wide and 760px tall, fine pointer), hero pins for 1100px of scroll. ScrollTrigger drives the Three.js phone's position/rotation and scan → specs → red flags → compare screens, with translated chapter labels. Additional framed textures are generated from the supplied real screenshots by `scripts/build.py`. Textures load on demand; the fallback image changes too, so the same chapters work without WebGL. The labels describe app screens, not data for the sample Ford VIN.
- Cards reveal with stagger and one gradient-border sweep; heading words reveal on entry. The sample report animates 55/100 and its ring, 4 recalls, 1,825 complaints and component bars. Final numbers and all source facts remain unchanged in static HTML. Counters restore the original formatted text after animation.
- Desktop primary buttons respond magnetically. Car-photo hover uses `photo-effect.js` and the existing Three.js module for a small ripple/RGB shift. This module loads on first eligible hover; one transient canvas is active at a time, rendered only while hovered and visible. Pointer leave, tab hiding, viewport exit and reduced motion dispose the resources. Images stay underneath as fallback. No distortion on touch/weak devices. Photo parallax is bounded to ±12px.
- Reduced motion on first visit loads neither Lenis/GSAP nor the photo effect; no pin, scrub or WebGL phone. Changing the preference at runtime destroys Lenis, reverts GSAP effects/pin, restores heading HTML/counter values/static phone and disposes distortion. Responsive media changes rebuild effects without retaining desktop pinning on a narrow viewport.
- All 20 pages remain static and localized, with the original language switcher, canonical/hreflang, SEO/schema and official-history limitations. New chapter copy reuses existing translation keys; no new translation service is involved.

### Motion tuning

- `motion-engine.js`: Lenis `duration:.95`; hero intro durations/stagger; desktop media query; pin `end:'+=1100'`; scrub `.65` desktop / `.3` mobile; chapter index `Math.floor(progress.value*4)`; card rise `38` desktop / `18` touch; counter duration `1.3`; photo parallax `±12px`; magnetic strength `.13`/`.2`.
- `app.js`: Three.js phone rotation/position equations use `stage.motion.progress`. DPR remains capped at 2; off-screen/tab-hidden scene rendering still pauses. GPU/device fallbacks remain in place.
- `photo-effect.js`: ripple amplitude maximum `.006`, RGB separation `.28`, hover DPR cap 1.5. This is an optional hover layer and never replaces the underlying image asset.
- `styles.css`: chapter transitions, `border-sweep`, split-word styling and reduced-motion overrides. All content starts visible; a missing library leaves a usable static site.
- To regenerate HTML and all framed phone screens: `python scripts/build.py`. Runtime upload now also needs `motion-engine.js`, `photo-effect.js`, the new `assets/web/phone-*.webp`, and the added vendor files. Do not upload node_modules, QA artifacts or task logs.

### Revision 4 validation

- `npm.cmd run check:i18n` passed: all 20 pages at 360px and 1440px, full translated report text, reciprocal hreflang/canonical/sitemap, FAQ/schema consistency, language switching, Play locale parameters, reduced-motion fallback and nested-route 3D, with no browser errors.
- `npm.cmd run check` passed: desktop/mobile/reduced-motion pages, disabled WebGL, complete report facts, sources, images, links, disclosures and no console/page errors. The existing check now waits for the complaint counter to finish before checking its final value.
- `node scripts/check-motion.mjs` exercises en/ru/zh normal motion at desktop/mobile widths: four actual rendered phone textures, translated chapter changes, desktop pin/mobile no pin, WebGL hover appearance/disposal, anchors and direct hashes, sticky report links opening disclosures, final counters/ring/bar values, live reduced-motion teardown/restoration and responsive pin cleanup. Screenshots are saved under ignored `qa/r4-*`.
- Local Lighthouse 12.8.2 mobile results: **`/`: Performance 91 / Accessibility 100 / Best Practices 100 / SEO 100** (LCP 2.7s, TBT 250ms, CLS 0); **`/sample.html`: Performance 99 / Accessibility 100 / Best Practices 100 / SEO 100** (LCP 1.8s, TBT 30ms, CLS 0). Reports: `qa/lighthouse-r4-index.json`, `qa/lighthouse-r4-sample.json`. Both meet the requested mobile Performance ≥85. These are simulated local results; physical Android hardware and production hosting were not tested.
- No required Revision 4 feature is intentionally unfinished. No commit, push, publication, deployment, payment or secret access was performed.
- Revision 6: Removed the travelling neon-pink orb, its glow, CSS and scroll JavaScript from all languages and the build template; everything else is unchanged.
