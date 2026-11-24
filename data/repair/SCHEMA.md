# Repair-cost pages: data format

One file per language: `data/repair/<lang>.json` (en, ru, de, es, fr, it, pt, tr, ko, zh).
`scripts/repair_pages.py` turns them into `<lang>/<slug>.html` pages plus a hub page `repair-costs.html`.

## Rules (all languages)

- NEVER invent a price. Every range must come from the sources listed for that topic (repair-cost
  guides, shop price lists, insurer or consumer sites of THAT country, 2025-2026). If sources disagree,
  give a wide honest range. If nothing reliable is found for a topic in that country, set
  `"skip": true` for that topic (the page is then not built for that language).
- Prices are for the page's country (see table below), in its currency, whole numbers.
- Plain, calm language. No hype, no exclamation marks, no em dashes.
- The app: "Vin AI" on Google Play. Photo check: the user photographs a dent, scratch, rust, tyre, light,
  leak or warning light and gets what is likely wrong and a fair repair price. The FIRST photo check is
  free. Do not claim anything else is free. Do not promise exact prices; the app gives an estimate too.
- title <= 60 characters, description <= 155 characters. Put the main search phrase people type in
  that language first in the title (e.g. "Brake pad replacement cost 2026" / "Замена тормозных колодок: цена 2026").
- `answer` = 2-3 sentences that directly answer "how much does it cost" with the total range, the
  country and what is included. This is what Google AI Overview / ChatGPT quote, so make it self-contained.

| lang | country | currency | price_format | thousands |
|---|---|---|---|---|
| en | United States | USD | `${n}` | `,` |
| ru | Россия | RUB | `{n} ₽` | ` ` (narrow nbsp U+202F) |
| de | Deutschland | EUR | `{n} €` | `.` |
| es | España | EUR | `{n} €` | `.` |
| fr | France | EUR | `{n} €` | ` ` (U+202F) |
| it | Italia | EUR | `{n} €` | `.` |
| pt | Brasil | BRL | `R$ {n}` | `.` |
| tr | Türkiye | TRY | `{n} TL` | `.` |
| ko | 대한민국 | KRW | `{n}원` | `,` |
| zh | 中国 | CNY | `{n} 元` | `,` |

## Shape

```json
{
  "lang": "en",
  "country": "United States",
  "price_format": "${n}",
  "thousands": ",",
  "ui": {
    "hub_title": "Car repair costs 2026: what a fair price looks like",
    "hub_description": "...<=155",
    "hub_h1": "Car repair costs",
    "hub_intro": "1-2 sentences",
    "table_item": "Part of the job",
    "table_low": "Low",
    "table_high": "High",
    "factors_title": "What changes the price",
    "tips_title": "How not to overpay",
    "cta_title": "Not sure your quote is fair?",
    "cta_text": "Take a photo of the problem in Vin AI. It tells you what is likely wrong and what a fair repair costs. Your first photo check is free.",
    "cta_button": "Get Vin AI on Google Play",
    "faq_title": "FAQ",
    "sources_label": "Price sources",
    "disclaimer": "Estimates for {country}, November 2026. Real prices depend on the car, the region and the shop.",
    "related_title": "Other repair costs",
    "footer_link": "Car repair costs",
    "home": "Home"
  },
  "topics": [
    {
      "slug": "brake-pad-replacement-cost",
      "skip": false,
      "title": "...",
      "description": "...",
      "h1": "...",
      "answer": "...",
      "rows": [["Brake pads (one axle)", 40, 150], ["Labor", 80, 150], ["Total, one axle", 120, 300]],
      "factors": ["4-6 short points"],
      "tips": ["3-5 short points"],
      "faq": [["question", "answer"], ["...", "..."], ["...", "..."], ["...", "..."]],
      "sources": [{"name": "Site name", "url": "https://..."}]
    }
  ]
}
```

The last row of `rows` is always the total. Keep the topic order and slugs exactly as below.

## The 15 slugs (same in every language)

1. brake-pad-replacement-cost
2. car-battery-replacement-cost
3. clutch-replacement-cost
4. shock-absorber-replacement-cost
5. water-pump-replacement-cost
6. car-dent-repair-cost
7. car-scratch-repair-cost
8. bumper-repair-cost
9. windshield-replacement-cost
10. headlight-replacement-cost
11. toyota-camry-water-pump-replacement-cost
12. toyota-corolla-brake-pad-replacement-cost
13. honda-civic-clutch-replacement-cost
14. hyundai-elantra-battery-replacement-cost (in ru the car is sold as Hyundai Elantra / Avante in ko: use the local name in text)
15. volkswagen-golf-timing-belt-replacement-cost
