# Odisha Landscape — data foundation

A data foundation for doing the same "who does what where" exercise as
[jharkhand-landscape](https://github.com/sidd-1995/jharkhand-landscape) — a
development-partner ecosystem map (partners × districts × themes) — for **Odisha**.

This repo is **not yet the interactive map**. It's the data-gathering stage: everything
that could be pulled from public sources has been fetched, normalised to a single
`model.json`, and organised for reuse. What jharkhand-landscape's `build.py` does with
`model.json` (turn it into a self-contained `index.html` with a choropleth map,
Ecosystem/Place Health scorecards, and tables) is the natural next step here, once the
manual partner-research gap below is closed enough to be worth visualising.

## What's in `model.json`

30 Odisha districts (`canon`), each with:

| Field | Status | Source |
|---|---|---|
| `shg` (Self Help Groups: total, members, new/revived/pre-NRLM, block breakdown) | ✅ Complete — all 30 districts | DAY-NRLM public MIS (`preprodmis.lokos.in`), live fetch |
| `dmf` (District Mineral Fund collection, **year-wise**, FY2015-16 → FY2025-26) | ✅ Complete — all 30 districts × 11 years | Odisha's own DMF portal (`dmf.odisha.gov.in`), live fetch |
| `fpo` (Farmer Producer Orgs: count + farmer count) | ✅ Complete — all 30 districts | FPO Platform's public dashboard data (backed by Cornell TCI's FPO API) |
| `partners` / `cg` (org names, themes, block-level presence) | ⚠️ Seed only — 11 orgs, 9 districts with block detail | See "What's not automated" below |
| `themes` (per-district), `tri`, `csr`, `blockcov` | ❌ Empty | No public source found / blocked — see below |

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
├── model.json                        # assembled output — the one file downstream tooling reads
├── data/
│   ├── odisha_districts.geojson      # 30 district boundaries (Bharatlas / LGD 2024)
│   ├── odisha_shg_data.json          # raw SHG fetch, block-level, all 30 districts
│   ├── odisha_dmf_data.json          # raw DMF fetch, district × FY, 2015-16 to 2025-26
│   ├── odisha_fpo_data.json          # raw FPO fetch, district-level count + farmers
│   └── odisha_partners_seed.csv      # seed partner data (see "What's not automated")
└── scripts/
    ├── fetch_boundaries.py           # bharatlas.com -> data/odisha_districts.geojson
    ├── fetch_shg.py                  # DAY-NRLM MIS -> data/odisha_shg_data.json
    ├── fetch_dmf.py                  # dmf.odisha.gov.in -> data/odisha_dmf_data.json
    ├── fetch_fpo.py                  # fpoplatform.com -> data/odisha_fpo_data.json
    └── build_model.py                # merges all of the above -> ../model.json
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
```

Only Python 3 stdlib + `curl` on PATH are needed — no dependencies to install.

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
