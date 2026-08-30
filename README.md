# Odisha Landscape — Who Does What Where

The same "who does what where" exercise as
[jharkhand-landscape](https://github.com/sidd-1995/jharkhand-landscape) — a
development-partner ecosystem map (partners × districts) — for **Odisha**.
`index.html` is a self-contained, offline, single-file interactive map (choropleth lenses,
Ecosystem/Place Health scorecards, partner × theme matrix, DMF spend table) — open it
directly in a browser.

**Read it as a data foundation with a working viewer, not a finished partner survey.**
SHG, DMF and FPO layers are complete, live-fetched data across all 30 districts. The
**partner layer is a seed of 11 organisations**, not a systematic canvass — see "What's
not automated" below before treating the health scores as a verdict on Odisha's ecosystem.

## What's in `model.json`

30 Odisha districts (`canon`), each with:

| Field | Status | Source |
|---|---|---|
| `shg` (Self Help Groups: total, members, new/revived/pre-NRLM, block breakdown) | ✅ Complete — all 30 districts | DAY-NRLM public MIS (`preprodmis.lokos.in`), live fetch |
| `dmf` (District Mineral Fund collection, **year-wise**, FY2015-16 → FY2025-26) | ✅ Complete — all 30 districts × 11 years | Odisha's own DMF portal (`dmf.odisha.gov.in`), live fetch |
| `fpo` (Farmer Producer Orgs: count + farmer count) | ✅ Complete — all 30 districts | FPO Platform's public dashboard data (backed by Cornell TCI's FPO API) |
| `aspirational` | ✅ Real — 10 districts | NITI Aayog's Aspirational Districts Programme (official list), *not* inferred from a proxy like Jharkhand's TRI-presence heuristic |
| `partners` / `blockcov` (org names, themes, block-level presence) | ⚠️ Seed only — 11 orgs, 9 districts / 30 blocks with detail | See "What's not automated" below |
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

**Partner geography & thematic focus — genuinely manual, always will be.** There's no
public dataset of "which development-sector org works in which Odisha district on which
theme" the way there's a public MIS for SHGs or a government portal for DMF. Jharkhand's
own `Partners data - Geography & Thematic focus.xlsx`, `Common Ground - List of blocks
(1).xlsx`, and `SOTH places list.xlsx` are hand-compiled research by that project's author.

`data/odisha_partners_seed.csv` is **not** that research redone for Odisha — it's what
those three Jharkhand files *already contained* incidentally, because a few of the orgs
they tracked also operate in Odisha (multi-state orgs, or an "Odisha" tab someone had
already started in the Common Ground workbook). 11 orgs, mostly concentrated in the
southern/western tribal-belt districts (Kalahandi, Kandhamal, Koraput, Rayagada, Mayurbhanj,
Sundargarh, Kendujhar). Real coverage of Odisha's partner ecosystem needs the same kind of
research pass Jharkhand's author did — surveying org websites, annual reports, CSR
disclosures, and known networks (e.g. PRADAN, Gram Vikas, Vikas Bharti-style orgs) district
by district. `data/odisha_partners_seed.csv` is the starting point, not the answer;
several rows are flagged `verify` where a district was inferred from a block name rather
than stated directly in the source.

**TRI-equivalent geographic presence** — Jharkhand's `TRI Geographical Presence` source
has zero Odisha rows (that org doesn't appear to operate there per that file). No
substitute source was found; if the goal is to track TRI or an equivalent block-level
anchor org in Odisha, that's original research too.

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
│   └── odisha_partners_seed.csv      # seed partner data (see "What's not automated")
└── scripts/
    ├── fetch_boundaries.py           # bharatlas.com -> data/odisha_districts.geojson
    ├── fetch_shg.py                  # DAY-NRLM MIS -> data/odisha_shg_data.json
    ├── fetch_dmf.py                  # dmf.odisha.gov.in -> data/odisha_dmf_data.json
    ├── fetch_fpo.py                  # fpoplatform.com -> data/odisha_fpo_data.json
    ├── enrich_geojson.py             # data/odisha_districts.geojson -> ../odisha_enriched.geojson
    └── build_model.py                # merges all fetches -> ../model.json
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
  Odisha's 11 seed partners already *are* that kind of incidental/indicative data (see
  below) — there's no second, cleaner tier to toggle against, so the toggle, `EXT_IMPL`,
  `EXT_FUND`, and the Funders & Philanthropies table are gone entirely.
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
Platform](https://www.fpoplatform.com) / Cornell TCI FPO API (FPO counts) ·
[jharkhand-landscape](https://github.com/sidd-1995/jharkhand-landscape)'s own source
spreadsheets (incidental Odisha partner mentions, see "What's not automated").

CSR data would come from [MCA's National CSR Portal](https://www.csr.gov.in) once someone
manually clears its CAPTCHA.

## License

MIT (see [LICENSE](LICENSE)). Underlying source data remains under the terms of the
respective providers linked above.
