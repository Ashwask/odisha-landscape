# Odisha Landscape — Who Does What Where

A "who does what where" view of Odisha's development-partner ecosystem
(partners × districts × themes), with an **Odisha Vision 2036** tab and a **2036 Alignment**
tab. `index.html` is a self-contained, offline, single-file interactive dashboard
(choropleth lenses, Ecosystem/Place Health scorecards, partner × theme matrix, funders,
government schemes, DMF spend, CSR context, a Vision 2036 view and an alignment read) —
open it directly in a browser. One request, no external dependencies, ~83 KB gzipped.

**Live:** https://ashwask.github.io/odisha-landscape/

**Read it as a research pass with a working viewer, not a verified census.** SHG, DMF and
FPO layers are complete, live-fetched government data across all 30 districts. The partner
layer is a **46-organisation research pass** reaching all 30 districts, plus a **14-org
indicative ✳ tier** (large multi-district anchors, networks and BCKIC) kept out of the
health scores unless you toggle it on. Funders, CSR, anchors and schemes are sourced but
not independently field-verified — see the honesty notes below.

## Three tabs

- **Ecosystem landscape** — the district map is the hero (11 lenses), then Ecosystem &
  Place Health scorecards, partner × theme matrix, government spend (DMF + 25 schemes),
  CSR & funders, and the partner / district tables. Major sections are collapsible.
- **Odisha Vision 2036** — the state government's official centenary vision (with a 2047
  horizon), as seven pillar cards (economy, skills, urban/infra, agriculture, education &
  health, women, governance) with stated targets and flagship programmes, each mapped to
  the themes this dashboard tracks. These are **government targets, not audited outcomes**.
- **2036 Alignment** — cross-reads the mapped ecosystem against the Vision pillars:
  a pillar alignment scorecard (banded, with **trajectory** badges), the human-development-
  vs-economic-transformation structural gap, a **velocity** table (pace 2036 demands vs
  current drift), headline target-vs-today, geographic priority gaps, and an **unlocks**
  table (lever → what it unblocks → who holds the key).

## Map lenses (11)

Place health · Partner density · Theme breadth · Dominant theme · Coverage gap ·
Block presence (beta) · SHG density · FPO density · DMF mining fund ·
**CSR flagship ✳** · **Anchor org ✳**. Click a district for partners, themes, block
coverage, anchor orgs, CSR flagship projects, SHG/FPO and a DMF trend; hover for a readout.
Deep-links: `#vision`, `#align`, `#ext` (indicative scoring on), `#lens=<key>`.

## What's in `model.json`

30 Odisha districts (`canon`), each with:

| Field | Status | Source |
|---|---|---|
| `shg` (Self Help Groups: total, members, block breakdown) | ✅ Complete — all 30 districts | DAY-NRLM public MIS, live fetch |
| `dmf` (District Mineral Fund, **year-wise**, FY2015-16 → FY2025-26) | ✅ Complete — all 30 × 11 years | Odisha's DMF portal (`dmf.odisha.gov.in`), live fetch |
| `fpo` (Farmer Producer Orgs: count + farmers) | ✅ Complete — all 30 districts | FPO Platform / Cornell TCI |
| `aspirational` | ✅ Real — 10 districts | NITI Aayog Aspirational Districts Programme (official list) |
| `themes` (per-district) | ✅ Derived — 29/30 districts | Aggregated from the partner research pass, vocabulary normalised |
| `partners` / `blockcov` | ⚠️ Research pass — 46 orgs, all 30 districts; 49 blocks / 14 districts | See "Partner research pass" |
| `anchor` (multi-district anchor presence) | ⚠️ Sourced leads | CYSD's named field-office districts paint the anchor layer; Gram Vikas / Harsha Trust / Niyatee listed without per-district paint |
| `csrFlagship` (per-district flagship CSR projects) | ⚠️ Subset, not total | GO CARE portal geocoded projects (company → amount → sector) |
| top-level `csrState`, `funders`, `schemes`, `indicative`, `vision2036` | ⚠️ Sourced | see below |

## CSR & funders — what's open, what's gated

**District-total CSR spend is not openly available.** The national MCA portal
([csr.gov.in](https://www.csr.gov.in)) gates every export behind a CAPTCHA, and Odisha's
own [GO CARE portal](https://csr.odisha.gov.in)'s district page requires a login (HTTP
401). So **there is no CSR choropleth**. What `scripts/fetch_csr.py` *does* pull from GO
CARE's open endpoints (it is MCA-fed) and what the dashboard shows:

- **Statewide CSR by year** (FY2014-15 → FY2026-27) — ~₹5,333 Cr cumulative — as a trend.
- **Sector mix** (project counts across 13 CSR sectors).
- The **300-company funder universe** filing CSR in Odisha.
- **Geocoded flagship projects** (company → district → amount → sector), shown in district
  detail and the "CSR flagship ✳" lens — a **curated subset, not total spend**.

**Funders & Philanthropies** (`data/odisha_ecosystem_layers.json` → rendered as a table):
27 funders with **domain-wise and district-wise** focus and a confidence flag, linking each
to the org(s) it backs in Odisha where public — e.g. Gates Foundation (ADAPT agriculture,
BONI nutrition), Piramal Foundation (Aspirational Districts Collaborative), Tata Steel
Foundation (MANSI, Samvaad), Rainmatter Foundation (→ Gram Vikas, Socratus, Goonj, Nature's
Club, WellLabs, NCF), HDFC Parivartan (→ PARFI/Pratham/Antarang), Axis Bank Foundation (→
Harsha Trust), Vedanta (→ AFPRO), IMFA, SAIL, JSPL, NALCO, UNICEF, WFP, UNDP, CIFF, Shakti,
EdelGive, Rohini Nilekani, ITC Sunehra Kal, Adani, JSW and more. Amounts are org-wide unless
noted, and district attributions are approximate — **treat as leads, not audited flows**.

## Indicative ✳ tier + scoring toggle

A second tier of **14 large multi-district orgs/networks** (CYSD, Gram Vikas, Harsha Trust,
Niyatee, PRADAN, FES, Landesa, SPREAD, Lokadrusti, Socratus, SELCO, Bakul, NCF, WellLabs and
**BCKIC**) sits alongside the 46 source-file partners. It is **kept out of the health
scores** unless you tick *"Include ✳ indicative orgs in scoring"* (or open with `#ext`),
which recomputes the strip, health index, place health, map lenses and tables on the wider
set. In the matrix and directory these orgs are gold-flagged with keyword-mapped themes.
**BCKIC** (Bhubaneswar City Knowledge Innovation Cluster, PSA/PM-STIAC) is the one growth/
innovation-pillar actor — flagged in the Alignment tab as the bridge to the vision's
economic engine.

## Anchor layer

**CYSD** (Centre for Youth & Social Development) — with named field offices in 10 districts —
is used as the concrete multi-district anchor-presence layer ("Anchor org ✳" lens + district
badge/column). Gram Vikas (27 districts), Harsha Trust (17 districts) and Niyatee (14-16
districts) are large anchors too, but their per-district lists aren't cleanly published, so
they're listed without per-district paint.

## Government spend & schemes

- **DMF** — real, district-wise, year-wise (FY2015-16 → FY2025-26), live from Odisha's
  portal. Odisha is India's top DMF-collecting state.
- **Major schemes & allocations** — **25 schemes across centrally-sponsored + state**
  (level-tagged) from the Odisha 2025-26 budget: state (Subhadra ₹10,145 Cr, Antyodaya
  Gruha ₹2,603 Cr, CM-KISAN ₹2,020 Cr, Mission Shakti ₹1,107 Cr, Shree Anna ₹600 Cr, BSKY,
  Adarsha Vidyalaya…) and central-sponsored (MGNREGS ₹1,450 Cr, AB-PMJAY ₹711 Cr, PM POSHAN
  ₹392 Cr, Samagra Shiksha ₹307 Cr, Jal Jeevan Mission, PMAY-G, PM-KISAN…), each mapped to a
  theme. "–" where the Odisha-specific amount isn't separately published.

## Ecosystem Health

A 7-dimension composite: coverage, aspirational reach,
resilience, thematic balance, network depth, SHG reach and **resource alignment**. Because
Odisha has no open district CSR, the resource-alignment dimension uses **DMF** (share of
the state's place-based public money sitting in partner-covered districts) instead of CSR.

## Partner research pass

There's no public dataset of "which org works in which Odisha district on which theme," so
this was researched: **46 organisations, 132 org-district rows, all 30 districts**, each
row backed by a source URL in `data/odisha_partners_seed.csv` (with a `notes` column). It is
**not** an independently field-verified survey; a handful of rows are flagged low-confidence
there (AIIDA/Kandhamal, SAMBHAV/Nayagarh, VORSA/OVARR/VARD, some Atmashakti rows) and worth
a second look. Thinnest coverage: Boudh, Sonepur.

## Odisha Vision 2036 — sources

Odisha turns 100 as a state in 2036. The government's official Vision 2036 (with a 2047
horizon) was unveiled by the PM on 12 Jun 2025 alongside 105 projects (~₹18,600 Cr) and 36
flagship programmes; it is the first AI-assisted state vision (3.2 lakh+ citizen inputs).
Headline: a **$500B economy by 2036, $1.5T by 2047**. Pillars/targets — plus the
per-pillar **trajectory**, **velocity** (required pace) and **unlocks** used by the 2036
Alignment tab — live in `data/odisha_ecosystem_layers.json → vision2036`, sourced to the
vision document and press
([Tribune](https://www.tribuneindia.com/news/india/pm-modi-launches-105-projects-worth-over-rs-18600-crore-unveils-odisha-vision-document),
[Sambad](https://sambadenglish.com/latest-news/bjp-govts-first-anniv-pm-unveils-odisha-vision-2036-launches-projects-worth-over-18000-crore-9381580),
[Odisha Plus](https://odisha.plus/2025/05/odisha-government-launching-36-initiatives-to-achieve-a-developed-odisha-by-2036/)).

## 2036 Alignment tab

Connects the two: for each Vision pillar it reads the ecosystem behind it (orgs + funders +
scheme ₹) into a **Strong/Emerging/Thin/Gap** band, flags growth pillars where the theme is
a rural proxy, and calls out the **structural gap** (a human-development ecosystem vs the
vision's economic-transformation ambition), **velocity** (e.g. urbanisation needs ~+2.3 pp/yr
vs ~0.3 historically), **trajectory** per pillar, **geographic priority gaps** (weakest 8
districts — Boudh & Sonepur lead), and **unlocks** (levers → what they unblock → who).

## LoTF workshop board

`lotf-workshop/gap-board.html` is a separate standalone tool for the Convening on Landscape
of the Future — a live "Landscape Confluence Board" where attendees add their org under an
archetype × outcome lens so empty cells surface as gaps. Not pre-populated; the file here is
the empty seed.

## Files

```
odisha-landscape/
├── index.html                          # the dashboard — open this in a browser
├── build.py                            # model.json + odisha_enriched.geojson -> index.html
├── model.json                          # assembled data — what build.py reads
├── odisha_enriched.geojson             # simplified boundaries with {district: <canon name>}
├── data/
│   ├── odisha_districts.geojson        # 30 district boundaries, raw (Bharatlas / LGD 2024)
│   ├── odisha_shg_data.json            # raw SHG fetch, block-level, all 30 districts
│   ├── odisha_dmf_data.json            # raw DMF fetch, district × FY, 2015-16 to 2025-26
│   ├── odisha_fpo_data.json            # raw FPO fetch, district-level count + farmers
│   ├── odisha_csr_data.json            # GO CARE CSR: year totals, sectors, 300 companies, flagship projects
│   ├── odisha_partners_seed.csv        # 46-org partner research pass
│   ├── odisha_ecosystem_layers.json    # 27 funders, anchors, 25 schemes, 14 indicative orgs, Vision 2036 (pillars/trajectory/velocity/unlocks)
│   └── odisha_research_funders.csv     # earlier 5-lead funders list (superseded by ecosystem_layers)
├── scripts/
│   ├── fetch_boundaries.py             # bharatlas.com -> data/odisha_districts.geojson
│   ├── fetch_shg.py                    # DAY-NRLM MIS -> data/odisha_shg_data.json
│   ├── fetch_dmf.py                    # dmf.odisha.gov.in -> data/odisha_dmf_data.json
│   ├── fetch_fpo.py                    # fpoplatform.com -> data/odisha_fpo_data.json
│   ├── fetch_csr.py                    # csr.odisha.gov.in (GO CARE) -> data/odisha_csr_data.json
│   ├── enrich_geojson.py               # data/odisha_districts.geojson -> ../odisha_enriched.geojson
│   └── build_model.py                  # merges all fetches + layers -> ../model.json
└── lotf-workshop/
    └── gap-board.html                  # standalone live workshop tool
```

## Rebuilding

```bash
cd scripts
python3 fetch_boundaries.py   # boundaries (~90 MB download, filtered)
python3 fetch_shg.py          # SHG, all districts
python3 fetch_dmf.py          # DMF, 11 financial years
python3 fetch_fpo.py          # FPO, all-India asset filtered to Odisha
python3 fetch_csr.py          # GO CARE CSR: totals, sectors, companies, flagship projects
python3 build_model.py        # merges fetches + data/odisha_ecosystem_layers.json -> ../model.json
python3 enrich_geojson.py     # simplifies + relabels boundaries
cd .. && python3 build.py     # model.json + odisha_enriched.geojson -> index.html
```

Only Python 3 stdlib + `curl` on PATH are needed. `data/odisha_ecosystem_layers.json`
(funders, anchors, schemes, Vision 2036) is hand-compiled from public sources and edited
directly, not fetched.

## District name normalisation

The sources spell district names inconsistently. `build_model.py` carries an explicit
mapping table per source (SHG, DMF, FPO, CSR/GO CARE), keyed to a `canon` list of 30 names
from the Bharatlas/LGD boundary file. A `WARNING: unmapped district` during a rebuild means
a source renamed a district and the map needs a new entry.

## Data sources

[Bharatlas](https://bharatlas.com) (boundaries, LGD 2024) · [DAY-NRLM MIS](https://nrlm.gov.in/)
(SHG) · [Odisha DMF portal](https://dmf.odisha.gov.in) (DMF) · [FPO Platform](https://www.fpoplatform.com) /
Cornell TCI (FPO) · [NITI Aayog](https://www.niti.gov.in/) (aspirational districts) ·
[GO CARE — Odisha CSR portal](https://csr.odisha.gov.in) (statewide CSR, sectors, companies,
flagship projects; MCA-fed) · [Odisha Finance Dept](https://finance.odisha.gov.in/) (budget
schemes) · org sites for funders & anchors (CYSD, Gram Vikas, Harsha Trust, Socratus,
Rainmatter, Gates, Piramal, Tata Steel, HDFC, Axis, UNICEF, WFP, …) · Odisha Vision 2036
document & press · 46 org websites/reports/directories for the partner pass.

CSR **district totals** would come from [MCA's National CSR Portal](https://www.csr.gov.in)
once someone manually clears its CAPTCHA, or from a GO CARE login export.

## License

MIT (see [LICENSE](LICENSE)) © 2026 Ashwin Kulkarni. Underlying source data remains under
the terms of the respective providers linked above.
