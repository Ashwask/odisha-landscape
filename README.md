# Odisha Landscape — Who Does What Where

The same "who does what where" exercise as
[jharkhand-landscape](https://github.com/sidd-1995/jharkhand-landscape) — a
development-partner ecosystem map (partners × districts) — for **Odisha**.
`index.html` is a self-contained, offline, single-file interactive map (choropleth lenses,
Ecosystem/Place Health scorecards, partner × theme matrix, DMF spend table) — open it
directly in a browser.

**Read it as a research pass with a working viewer, not a verified census.**
SHG, DMF and FPO layers are complete, live-fetched data across all 30 districts. The
**partner layer is a 46-organisation research pass reaching all 30 districts** — see
"Partner research pass" below for methodology and what's still unverified before treating
the health scores as a verdict on Odisha's ecosystem.

## What's in `model.json`

30 Odisha districts (`canon`), each with:

| Field | Status | Source |
|---|---|---|
| `shg` (Self Help Groups: total, members, new/revived/pre-NRLM, block breakdown) | ✅ Complete — all 30 districts | DAY-NRLM public MIS (`preprodmis.lokos.in`), live fetch |
| `dmf` (District Mineral Fund collection, **year-wise**, FY2015-16 → FY2025-26) | ✅ Complete — all 30 districts × 11 years | Odisha's own DMF portal (`dmf.odisha.gov.in`), live fetch |
| `fpo` (Farmer Producer Orgs: count + farmer count) | ✅ Complete — all 30 districts | FPO Platform's public dashboard data (backed by Cornell TCI's FPO API) |
| `aspirational` | ✅ Real — 10 districts | NITI Aayog's Aspirational Districts Programme (official list), *not* inferred from a proxy like Jharkhand's TRI-presence heuristic |
| `partners` / `blockcov` (org names, themes, block-level presence) | ⚠️ Research pass — 46 orgs across all 30 districts, 14 districts / 49 blocks with block-level detail | See "Partner research pass" below — sourced but not independently field-verified |
| `themes` (per-district), `tri`, `csr` | ❌ Empty | No public source found / blocked — see below |

District boundaries: `data/odisha_districts.geojson` — Odisha's 30 districts, filtered out
of [Bharatlas](https://bharatlas.com)'s all-India LGD (Local Government Directory, 2024)
district layer, CC0-1.0/CC-BY-4.0.

## What's not automated

**CSR data — blocked, not missing.** [csr.gov.in](https://www.csr.gov.in)'s "Explore CSR
Data" section (Dynamic CSR Report, State-wise, District-wise, Company-wise) is the only
public source for district-level CSR spend, and **every export on it is gated behind a
CAPTCHA** — there's no way around that without a human solving it. To add CSR data:
go to Explore CSR Data → Dynamic CSR Report, filter State = Odisha, solve the captcha,
download the report, and drop the export into `data/`.

**TRI-equivalent geographic presence** — Jharkhand's `TRI Geographical Presence` source
has zero Odisha rows, and a direct check of TRI's own materials (its `/about` page and a
third-party CSR project profile) confirms TRI's stated operating states are Madhya Pradesh,
Jharkhand and Chhattisgarh — Odisha isn't one of them as of 2026. If the goal is to track
TRI or an equivalent multi-district anchor org in Odisha, the closest lead found is
**Niyatee Foundation**, which self-reports 19+ districts of presence (disaster management,
women's SHGs, WASH, health, early-childhood creches) — see `data/odisha_partners_seed.csv`.
It has not been independently cross-verified per district, so it isn't promoted to
`model.json`'s `anchors` field the way Jharkhand's PHIA Foundation is; do that once a
second source confirms activity in at least a few of its named districts.

## Partner research pass

There's no public dataset of "which development-sector org works in which Odisha district
on which theme" the way there's a public MIS for SHGs or a government portal for DMF — this
had to be researched the same way Jharkhand's author researched Jharkhand's. That research
is now done as a first pass: **46 organisations, 132 org-district rows, reaching all 30
districts**, compiled by four parallel research passes — livelihoods/agriculture/NRM,
health/nutrition/women/child, education/WASH/governance (+ funders), and coastal/northern
Odisha — each org verified against a real, checkable source (the org's own site, an annual
report, a CSR filing, or an NGO directory listing), recorded per row in
`data/odisha_partners_seed.csv` along with a `notes` column.

**What this is not:** an independently field-verified survey. Every row traces to a public
source, but nobody has called these organisations, checked they're still active in the
stated district, or resolved cases where two similarly-named orgs may have been conflated.
A handful of rows are explicitly flagged in `notes` as lower-confidence and worth a second
look before relying on them:
- **Ashakiran Institute for Integrated Developmental Actions (AIIDA)**, Kandhamal — the
  org/URL pairing came from a search-result synthesis, not an independently opened and
  confirmed source; there are multiple similarly-named "Asha Kiran" orgs in Odisha.
- **SAMBHAV**, Nayagarh — single thin directory listing.
- **VORSA** (Kendrapara), **OVARR** (Puri), **VARD** (Baleshwar) — small local NGOs sourced
  only from donation-directory listings, not the orgs' own sites.
- **Atmashakti Trust**, Sambalpur & Sundargarh rows — from a search-engine summary of a
  household-mobilisation project, not independently verified on the org's own site (its
  other 7 district rows are backed by the org's own per-district profile pages and are
  higher-confidence).
- A few rows infer a district from a named block rather than a source stating the district
  directly (flagged per-row) — e.g. CYSD's Surakshya Project rows, PRADAN's original seed
  rows.

**Funders.** A smaller, separate pass on who funds development work in Odisha turned up 5
leads (BRLF, Vedanta Aluminium, NALCO, Azim Premji Foundation, UNICEF) in
`data/odisha_research_funders.csv` — not yet wired into `model.json` or the map, since two
of the five are really direct CSR implementers rather than CSO grant-makers, and none of
the five have Odisha-specific grant totals in their public disclosures. Treat this as a
lead list for the next pass, not a finished Funders table like Jharkhand's.

**Districts with only one mapped partner** (thinnest coverage, worth prioritising in a
follow-up pass): Boudh (Save the Children only) and Sonepur (VJSS only).

## LoTF workshop board

`lotf-workshop/gap-board.html` is a separate, standalone tool for the **Convening on
Landscape of the Future (LoTF)** — a live, shared "Landscape Confluence Board" where
convening attendees add their own organisation under an archetype (Orchestrators,
Influencers, Funders, Government, Eco/Market, Grassroots Orgs) and an outcome lens
(Health, Education, Ecological, or whatever they name), so the empty archetype × lens
cells surface as visible gaps for the room to discuss.

It's deliberately **not pre-populated** — no lens, including the ecological outcomes
(Air/Water/Soil/Energy/Biodiversity/Materials) any one funder in the room cares about
most, is hardcoded or given visual priority. Every column exists only because someone
added it live, as a peer to every other column. This was a specific ask: the board
needed to avoid privileging any single funder's framework over the others attending.

The file in this repo is the **seed** (an empty board) — the live, filled-in version
lives at its published Artifact URL (linked from the main site's intro and from the
board's own back-link) and updates itself via `claude.use('artifact').publish(...)` each
time someone adds an entry; pulling a fresh copy back into this repo after the workshop,
if wanted, is a manual step (open the live URL, save its source).

## Files

```
odisha-landscape/
├── index.html                        # the map — open this in a browser
├── build.py                          # model.json + odisha_enriched.geojson -> index.html
├── model.json                        # assembled data — what build.py reads
├── odisha_enriched.geojson           # simplified boundaries with {district: <canon name>}
├── data/
│   ├── odisha_districts.geojson      # 30 district boundaries, raw (Bharatlas / LGD 2024)
│   ├── odisha_shg_data.json          # raw SHG fetch, block-level, all 30 districts
│   ├── odisha_dmf_data.json          # raw DMF fetch, district × FY, 2015-16 to 2025-26
│   ├── odisha_fpo_data.json          # raw FPO fetch, district-level count + farmers
│   ├── odisha_partners_seed.csv      # 46-org partner research pass (see "Partner research pass")
│   └── odisha_research_funders.csv   # 5-lead funders list, not yet wired into model.json
├── scripts/
│   ├── fetch_boundaries.py           # bharatlas.com -> data/odisha_districts.geojson
│   ├── fetch_shg.py                  # DAY-NRLM MIS -> data/odisha_shg_data.json
│   ├── fetch_dmf.py                  # dmf.odisha.gov.in -> data/odisha_dmf_data.json
│   ├── fetch_fpo.py                  # fpoplatform.com -> data/odisha_fpo_data.json
│   ├── enrich_geojson.py             # data/odisha_districts.geojson -> ../odisha_enriched.geojson
│   └── build_model.py                # merges all fetches -> ../model.json
└── lotf-workshop/
    └── gap-board.html                # standalone live workshop tool (see "LoTF workshop board")
```

## Rebuilding

Each fetch script is independently re-runnable (all read-only public data, no auth) and
writes straight into `data/`. Run from inside `scripts/`:

```bash
python3 fetch_boundaries.py   # ~90 MB download, filtered down to ~4 MB
python3 fetch_shg.py          # ~30 districts, a few seconds each, polite 0.3s delay
python3 fetch_dmf.py          # 11 financial years
python3 fetch_fpo.py          # one request, all-India asset filtered to Odisha
python3 build_model.py        # merges everything into ../model.json
python3 enrich_geojson.py     # simplifies + relabels boundaries for the map
cd .. && python3 build.py     # model.json + odisha_enriched.geojson -> index.html
```

Only Python 3 stdlib + `curl` on PATH are needed — no dependencies to install.

## What build.py deliberately drops or changes vs. jharkhand-landscape's

Rather than transplant Jharkhand's `build.py` wholesale, sections with no real Odisha data
behind them were removed instead of left showing empty/misleading numbers:

- **No ✳ indicative-org toggle.** Jharkhand's build separates "source-file partners" from
  a wider hand-compiled "indicative" layer (PRADAN, CInI, etc.) with a scoring toggle.
  Odisha only has one tier of partner data (see "Partner research pass" above) — there's no
  second, cleaner tier to toggle against, so the toggle, `EXT_IMPL`, `EXT_FUND`, and the
  Funders & Philanthropies table are gone from the map (the funders lead list that does
  exist lives in `data/odisha_research_funders.csv`, unwired — see above).
- **No CSR anywhere** (lens, strip stat, sparkline, "Resource alignment" health dimension) —
  blocked by a captcha, see below. Ecosystem Health's weights are renormalised across the
  remaining 6 dimensions instead of 7.
- **DMF is real and year-wise**, not a 6-district static snapshot cumulative to 2018. It's
  computed at runtime from `model.json`'s per-district, per-FY figures, and the district
  detail panel's CSR sparkline is replaced with a genuine DMF-collection-by-year sparkline.
  No "Major schemes & outlays" table — that was hand-researched for Jharkhand and has no
  Odisha equivalent yet.
- **No TRI badge/column.** Jharkhand's `tri` field is populated for every district (used as
  an aspirational-status proxy); Odisha's `tri` is an unpopulated stub since no TRI-like
  source covers Odisha, so showing the badge would be meaningless. `aspirational` uses the
  real NITI Aayog list instead of a TRI proxy.
- District count is `CANON.length` everywhere instead of a hardcoded `24`.

## District name normalisation

The four sources spell district names inconsistently (e.g. DMF portal: "Anugola",
"Baragada", "Kataka", "Debagada", "Sundaragada"; FPO Platform: "RAYAGARHA", "JAGATSINGHPUR"
missing a letter, "BALASORE" for Baleshwar). `build_model.py` carries an explicit mapping
table per source, keyed to a `canon` list of 30 names taken from the Bharatlas/LGD
boundary file (the presumed source of truth for official spelling). Every mapping resolved
cleanly against all 30 districts on the last build — a `WARNING: unmapped district` printed
during a rebuild means a source added/renamed a district and the map needs a new entry.

## Data sources

[Bharatlas](https://bharatlas.com) (district boundaries, LGD 2024) · [DAY-NRLM public
MIS](https://nrlm.gov.in/) via `preprodmis.lokos.in` (SHG counts) · [Odisha DMF
portal](https://dmf.odisha.gov.in) (District Mineral Fund collection) · [FPO
Platform](https://www.fpoplatform.com) / Cornell TCI FPO API (FPO counts) · 46 individual
org websites, annual reports, CSR filings and NGO directories for the partner layer (one
source URL per row in `data/odisha_partners_seed.csv` — see "Partner research pass"), 11 of
which trace back to incidental Odisha mentions in
[jharkhand-landscape](https://github.com/sidd-1995/jharkhand-landscape)'s own source files.

CSR data would come from [MCA's National CSR Portal](https://www.csr.gov.in) once someone
manually clears its CAPTCHA.

## License

MIT (see [LICENSE](LICENSE)). Underlying source data remains under the terms of the
respective providers linked above.
