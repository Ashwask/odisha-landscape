#!/usr/bin/env python3
"""Assemble odisha-landscape/model.json from the fetched data files.

Mirrors the schema of jharkhand-landscape's model.json (canon / themes / years / partners /
anchors / districts), with two intentional differences documented in the README:
  - each district also carries a "dmf" block (year-wise DMF collection, live from Odisha's
    own DMF portal) -- Jharkhand's build hardcodes DMF as a small static JS object in build.py
    instead of putting it in model.json; Odisha's dataset is richer (30 districts x 11 years)
    so it gets a proper field here.
  - "fpo" only has {fpos, farmers} (no shareholders / complete_financials -- see fetch_fpo.py
    docstring for why).
  - "partners" / per-district "partners" and "blockcov" are seeded (not empty) from
    data/odisha_partners_seed.csv -- a small set of organisations incidentally named as
    active in Odisha inside jharkhand-landscape's own (multi-state) source spreadsheets.
    This is NOT a systematic Odisha partner survey -- see README "What's not automated".
  - "aspirational" is real, not a stub: it's Odisha's 10 districts under NITI Aayog's
    Aspirational Districts Programme (official list, verified against niti.gov.in's
    List-of-112-Aspirational-Districts PDF), unlike Jharkhand's build which infers
    "aspirational" from whether TRI is present in a district (a proxy, not the actual
    government designation).
  - "themes" (per-district), "tri", "csr", "cg" are left EMPTY -- there is no public
    source for these (csr is blocked by a captcha, see README). They're present so the
    schema matches Jharkhand's and downstream tooling has somewhere to read from once
    filled in.

Run from the scripts/ directory: python3 build_model.py
"""
import csv
import json

CANON = [
    "Anugul", "Balangir", "Baleshwar", "Bargarh", "Bhadrak", "Boudh", "Cuttack",
    "Deogarh", "Dhenkanal", "Gajapati", "Ganjam", "Jagatsinghapur", "Jajapur",
    "Jharsuguda", "Kalahandi", "Kandhamal", "Kendrapara", "Kendujhar", "Khordha",
    "Koraput", "Malkangiri", "Mayurbhanj", "Nabarangpur", "Nayagarh", "Nuapada",
    "Puri", "Rayagada", "Sambalpur", "Sonepur", "Sundargarh",
]

# Reused verbatim from jharkhand-landscape/model.json -- a generic development-sector
# theme taxonomy, not Jharkhand-specific. Adjust once real partner data is compiled.
THEMES = [
    "Education", "Health & Nutrition", "Women & Gender", "Climate Action",
    "Livelihoods & Rural Dev", "Agriculture", "Natural Resource Mgmt",
    "Water & Sanitation", "Governance", "Skill Development", "Clean Energy",
    "Child Protection",
]

# DMF portal's own (inconsistently spelled) district names -> CANON
DMF_MAP = {
    "Anugola": "Anugul", "Balangir": "Balangir", "Baleshwar": "Baleshwar",
    "Baragada": "Bargarh", "Bhadrak": "Bhadrak", "Boudh": "Boudh",
    "Kataka": "Cuttack", "Debagada": "Deogarh", "Dhenkanal": "Dhenkanal",
    "Gajapati": "Gajapati", "Ganjam": "Ganjam", "Jagatsinghapur": "Jagatsinghapur",
    "Jajpur": "Jajapur", "Jharsuguda": "Jharsuguda", "Kalahandi": "Kalahandi",
    "Kandhamala": "Kandhamal", "Kendrapada": "Kendrapara", "Kendujhar": "Kendujhar",
    "Khordha": "Khordha", "Koraput": "Koraput", "Malkangiri": "Malkangiri",
    "Mayurbhanj": "Mayurbhanj", "Nabarangpur": "Nabarangpur", "Nayagada": "Nayagarh",
    "Nuapada": "Nuapada", "Puri": "Puri", "Rayagada": "Rayagada",
    "Sambalpur": "Sambalpur", "Subarnapur": "Sonepur", "Sundaragada": "Sundargarh",
}

# SHG MIS district names -> CANON
SHG_MAP = {
    "Angul": "Anugul", "Baleshwar": "Baleshwar", "Bargarh": "Bargarh",
    "Bhadrak": "Bhadrak", "Bolangir": "Balangir", "Boudh": "Boudh",
    "Cuttack": "Cuttack", "Deogarh": "Deogarh", "Dhenkanal": "Dhenkanal",
    "Gajapati": "Gajapati", "Ganjam": "Ganjam", "Jagatsinghapur": "Jagatsinghapur",
    "Jajpur": "Jajapur", "Jharsuguda": "Jharsuguda", "Kalahandi": "Kalahandi",
    "Kandhamal": "Kandhamal", "Kendrapara": "Kendrapara", "Kendujhar": "Kendujhar",
    "Khordha": "Khordha", "Koraput": "Koraput", "Malkangiri": "Malkangiri",
    "Mayurbhanj": "Mayurbhanj", "Nabarangapur": "Nabarangpur", "Nayagarh": "Nayagarh",
    "Nuapada": "Nuapada", "Puri": "Puri", "Rayagada": "Rayagada",
    "Sambalpur": "Sambalpur", "Sonepur": "Sonepur", "Sundargarh": "Sundargarh",
}

# FPO Platform district names (upper-case) -> CANON
FPO_MAP = {
    "KALAHANDI": "Kalahandi", "MAYURBHANJ": "Mayurbhanj", "KENDUJHAR": "Kendujhar",
    "BARGARH": "Bargarh", "KORAPUT": "Koraput", "SUNDARGARH": "Sundargarh",
    "GANJAM": "Ganjam", "BALANGIR": "Balangir", "PURI": "Puri", "KHORDHA": "Khordha",
    "CUTTACK": "Cuttack", "DHENKANAL": "Dhenkanal", "KENDRAPARA": "Kendrapara",
    "RAYAGARHA": "Rayagada", "KANDHAMAL": "Kandhamal", "NABARANGAPUR": "Nabarangpur",
    "JAJAPUR": "Jajapur", "SAMBALPUR": "Sambalpur", "NAYAGARH": "Nayagarh",
    "GAJAPATI": "Gajapati", "ANUGUL": "Anugul", "JAGATSINGHPUR": "Jagatsinghapur",
    "NUAPARHA": "Nuapada", "BALASORE": "Baleshwar", "MALKANGIRI": "Malkangiri",
    "BHADRAK": "Bhadrak", "JHARSUGUDA": "Jharsuguda", "DEOGARH": "Deogarh",
    "SUBARNAPUR": "Sonepur", "BOUDH": "Boudh",
}

# NITI Aayog Aspirational Districts Programme, Odisha's 10 districts, verified against
# niti.gov.in/sites/default/files/2023-07/List-of-112-Aspirational-Districts%20(1).pdf
ASPIRATIONAL_DISTRICTS = [
    "Balangir", "Dhenkanal", "Gajapati", "Kalahandi", "Kandhamal",
    "Koraput", "Malkangiri", "Nabarangpur", "Nuapada", "Rayagada",
]

# Partner-seed CSV uses a few near-duplicate theme labels; fold them into the THEMES
# taxonomy so per-district theme sets stay clean.
THEME_NORM = {
    "Women Empowerment": "Women & Gender",
    "Gender Integration": "Women & Gender",
    "Livelihoods and Rural Development": "Livelihoods & Rural Dev",
}

# GO CARE portal (csr.odisha.gov.in) district spellings -> CANON. Covers the flagship
# CSR project rows in data/odisha_csr_data.json.
CSR_DIST_MAP = {
    "Angul": "Anugul", "Balangir": "Balangir", "Bolangir": "Balangir",
    "Balasore": "Baleshwar", "Bargarh": "Bargarh", "Bhadrak": "Bhadrak",
    "Boudh": "Boudh", "Cuttack": "Cuttack", "Deogarh": "Deogarh",
    "Dhenkanal": "Dhenkanal", "Gajapati": "Gajapati", "Ganjam": "Ganjam",
    "Jagatsinghpur": "Jagatsinghapur", "Jajpur": "Jajapur", "Jharsuguda": "Jharsuguda",
    "Kalahandi": "Kalahandi", "Kandhamal": "Kandhamal", "Kondhamal": "Kandhamal",
    "Kendrapara": "Kendrapara", "Keonjhar": "Kendujhar", "Khordha": "Khordha",
    "Koraput": "Koraput", "Malkangiri": "Malkangiri", "Mayurbhanj": "Mayurbhanj",
    "Nabarangpur": "Nabarangpur", "Nawarangpur": "Nabarangpur", "Nayagarh": "Nayagarh",
    "Nuapada": "Nuapada", "Puri": "Puri", "Rayagada": "Rayagada",
    "Sambalpur": "Sambalpur", "Sonepur": "Sonepur", "Subarnapur": "Sonepur",
    "Sundergarh": "Sundargarh", "Sundargarh": "Sundargarh",
}

# Keyword -> theme, for mapping an indicative org's free-text "focus" to THEMES
# (mirrors jharkhand-landscape's build.py extThemesOf()).
FOCUS_KEYWORDS = [
    (("education", "school", "learning"), "Education"),
    (("health", "nutrition", "arogya", "maternal", "creche"), "Health & Nutrition"),
    (("women", "gender", "shg", "self-help"), "Women & Gender"),
    (("climate", "disaster", "resilience"), "Climate Action"),
    (("livelihood", "income", "household"), "Livelihoods & Rural Dev"),
    (("agri", "farm", "ntfp", "crop"), "Agriculture"),
    (("nrm", "natural resource", "commons", "watershed", "forest", "ecolog", "biosphere"), "Natural Resource Mgmt"),
    (("wash", "water", "sanitation", "piped"), "Water & Sanitation"),
    (("governance", "rights", "coordination", "land"), "Governance"),
    (("skill", "vocational"), "Skill Development"),
    (("energy", "solar"), "Clean Energy"),
    (("child", "creche"), "Child Protection"),
]


def themes_from_focus(focus):
    f = (focus or "").lower()
    out = []
    for kws, theme in FOCUS_KEYWORDS:
        if any(k in f for k in kws) and theme not in out:
            out.append(theme)
    return out


def money_to_float(s):
    return float(s.replace(",", ""))


def load_partners_seed():
    """Read data/odisha_partners_seed.csv -> (partners list, {district: [blockcov entries]}).

    blockcov entries match jharkhand-landscape's shape: {name, by: [orgs], villages: []}.
    One entry per individual block; if two seed rows name the same block string in the
    same district (exact match only -- no fuzzy spelling merge), their "by" lists combine.
    """
    rows = list(csv.DictReader(open("../data/odisha_partners_seed.csv")))
    partners_by_name = {}
    blocks_by_district = {}  # dist -> {block_name: {orgs...}}
    for r in rows:
        name, dist = r["name"], r["district"]
        if dist not in CANON:
            print(f"WARNING: unmapped partner district {dist!r} for {name!r}")
            continue
        p = partners_by_name.setdefault(name, {"name": name, "districts": [], "themes": []})
        if dist not in p["districts"]:
            p["districts"].append(dist)
        themes = [THEME_NORM.get(t.strip(), t.strip()) for t in r["themes"].split(",") if t.strip()]
        for t in themes:
            if t not in p["themes"]:
                p["themes"].append(t)
        if r["block"]:
            bmap = blocks_by_district.setdefault(dist, {})
            for b in r["block"].split(","):
                b = b.strip()
                if not b:
                    continue
                bmap.setdefault(b, set()).add(name)

    blockcov_by_district = {
        dist: [{"name": b, "by": sorted(orgs), "villages": []} for b, orgs in sorted(bmap.items())]
        for dist, bmap in blocks_by_district.items()
    }
    return list(partners_by_name.values()), blockcov_by_district


def _csr_canon(name):
    """CSR_DIST_MAP lookup with an identity fallback for names already spelled like CANON
    (the district x sector export below uses a few spellings -- e.g. "Sonepur",
    "Jagatsinghapur" -- that CSR_DIST_MAP doesn't need an entry for since they already
    match CANON)."""
    if name in CSR_DIST_MAP:
        return CSR_DIST_MAP[name]
    if name in CANON:
        return name
    return None


def load_csr_district_domain():
    """Read data/odisha_csr_district_domain.csv -- Odisha GO CARE's "Dynamic CSR Report"
    (district x development-sector export), FY2014-15->FY2024-25, real spend in Rupees
    Crore -- not project counts. This is the cut that unblocks the district CSR choropleth
    and a domain/sector split: csr.gov.in's national portal and GO CARE's own district page
    are both gated (see README's "District-total CSR" note), but this district x sector
    cut was obtained as a manual export and has no fetch script.

    It supersedes the FY21->FY25, no-domain-split `Odisha_DistrictwiseCSR.xlsx` cut also in
    this repo (see parse_csr_district.py): more years, a domain breakdown, and its FY21-25
    totals cross-validate closely against that file's (e.g. Anugul ~₹666.5 Cr both ways).

    Returns per-district totals (folded into districts[d]["csr"]) plus a statewide
    domain rollup (the new top-level "csrDomain" model key) for the "by domain" CSR view
    and the CSR-spend map lens's domain filter.
    """
    rows = list(csv.DictReader(open("../data/odisha_csr_district_domain.csv")))
    years = [k for k in rows[0].keys() if k not in ("district", "district_type", "domain", "all")]

    per_district = {d: {"total": 0.0, "byDomain": {}, "byYear": {y: 0.0 for y in years}} for d in CANON}
    unclassified = {"total": 0.0, "byDomain": {}, "byYear": {y: 0.0 for y in years}}
    domain_state = {}  # domain -> {"total": .., "byYear": {y: amt}}

    for r in rows:
        canon = _csr_canon(r["district"])
        domain = r["domain"]
        total_all = float(r["all"])
        by_year = {y: float(r[y]) for y in years}

        ds = domain_state.setdefault(domain, {"total": 0.0, "byYear": {y: 0.0 for y in years}})
        ds["total"] += total_all
        for y in years:
            ds["byYear"][y] += by_year[y]

        if canon is None:
            unclassified["total"] += total_all
            unclassified["byDomain"][domain] = unclassified["byDomain"].get(domain, 0.0) + total_all
            for y in years:
                unclassified["byYear"][y] += by_year[y]
            continue

        pd = per_district[canon]
        pd["total"] += total_all
        pd["byDomain"][domain] = pd["byDomain"].get(domain, 0.0) + total_all
        for y in years:
            pd["byYear"][y] += by_year[y]

    domains_ordered = sorted(domain_state.keys(), key=lambda k: -domain_state[k]["total"])
    state_total = sum(v["total"] for v in domain_state.values())

    return {
        "per_district": per_district,
        "domains": domains_ordered,
        "byDomain": {k: round(v["total"], 2) for k, v in domain_state.items()},
        "byYear": {
            y: {k: round(domain_state[k]["byYear"][y], 2) for k in domains_ordered}
            for y in years
        },
        "total": round(state_total, 2),
        "unclassified": {
            "total": round(unclassified["total"], 2),
            "byDomain": {k: round(v, 2) for k, v in unclassified["byDomain"].items()},
            "byYear": {y: round(v, 2) for y, v in unclassified["byYear"].items()},
        },
        "years": years,
    }


def build():
    shg_raw = json.load(open("../data/odisha_shg_data.json"))
    dmf_raw = json.load(open("../data/odisha_dmf_data.json"))
    fpo_raw = json.load(open("../data/odisha_fpo_data.json"))
    partners, blockcov_by_district = load_partners_seed()

    districts = {}
    for d in CANON:
        districts[d] = {
            "partners": [],
            "themes": [],
            "tri": {"blocks": "", "aspirational": False},
            "cg": None,
            "csr": {},
            "aspirational": d in ASPIRATIONAL_DISTRICTS,
            "blockcov": blockcov_by_district.get(d, []),
            "shg": {"total": 0, "members": 0, "new": 0, "revived": 0, "prenrlm": 0, "blocks": []},
            "fpo": {"fpos": 0, "farmers": 0},
            "dmf": {},
        }

    # -- SHG --
    for src_name, blocks in shg_raw.items():
        canon = SHG_MAP.get(src_name)
        if canon is None:
            print(f"WARNING: unmapped SHG district {src_name!r}")
            continue
        tot = sum(b["total"] for b in blocks)
        mem = sum(b["members"] for b in blocks)
        new_ = sum(b["new"] for b in blocks)
        rev = sum(b["revived"] for b in blocks)
        pre = sum(b["prenrlm"] for b in blocks)
        districts[canon]["shg"] = {
            "total": tot, "members": mem, "new": new_, "revived": rev,
            "prenrlm": pre, "blocks": blocks,
        }

    # -- DMF (year-wise) --
    for fy, payload in dmf_raw.items():
        for src_name, amount_str in payload["districts"].items():
            canon = DMF_MAP.get(src_name)
            if canon is None:
                print(f"WARNING: unmapped DMF district {src_name!r}")
                continue
            districts[canon]["dmf"][fy] = money_to_float(amount_str)

    # -- FPO --
    for row in fpo_raw["district_wise"]:
        canon = FPO_MAP.get(row["district_name"])
        if canon is None:
            print(f"WARNING: unmapped FPO district {row['district_name']!r}")
            continue
        districts[canon]["fpo"] = {
            "fpos": row["fpo_count"], "farmers": row["number_of_farmers"],
        }

    # -- Partners (seed) + per-district theme aggregation --
    partner_by_name = {p["name"]: p for p in partners}
    for p in partners:
        for dist in p["districts"]:
            if p["name"] not in districts[dist]["partners"]:
                districts[dist]["partners"].append(p["name"])
            for t in p["themes"]:
                if t not in districts[dist]["themes"]:
                    districts[dist]["themes"].append(t)

    # -- CSR (GO CARE flagship projects, per district) --
    csr_raw = json.load(open("../data/odisha_csr_data.json"))
    for row in csr_raw.get("flagship", []):
        canon = CSR_DIST_MAP.get(row["district"])
        if canon is None:
            print(f"WARNING: unmapped CSR district {row['district']!r}")
            continue
        cf = districts[canon].setdefault(
            "csrFlagship", {"count": 0, "amountLakh": 0.0, "projects": []})
        cf["count"] += 1
        cf["amountLakh"] += row.get("amountLakh", 0) or 0
        cf["projects"].append({
            "company": row["company"], "project": row["project"],
            "amountLakh": row.get("amountLakh", 0), "status": row["status"],
            "location": row["location"], "agencyType": row["agencyType"],
        })
    for d in districts.values():
        d.setdefault("csrFlagship", {"count": 0, "amountLakh": 0.0, "projects": []})

    csr_state = {
        "yearTotals": csr_raw.get("yearTotals", {}),
        "sectorCounts": csr_raw.get("sectorCounts", {}),
        "companies": len(csr_raw.get("companies", [])),
        "totalCr": round(sum(v["amountCr"] for v in csr_raw.get("yearTotals", {}).values()), 1),
        "source": csr_raw.get("meta", {}).get("source", ""),
        "note": csr_raw.get("meta", {}).get("note", ""),
    }

    # -- CSR (real district x sector spend, GO CARE "Dynamic CSR Report") --
    # Supersedes the older parse_csr_district.py cut (FY21->FY25, no domain split, still in
    # the repo as Odisha_DistrictwiseCSR.xlsx / data/odisha_csr_district.json but no longer
    # wired in): this is a strict superset -- more years, plus a domain breakdown -- and its
    # FY21-25 totals cross-validate closely against that file's. Feeds districts[d]["csr"]
    # (total/byDomain/byYear) and Catalytic Unlock's money-pool leverage calc (see build.py).
    csr_dd = load_csr_district_domain()
    for d in CANON:
        pd = csr_dd["per_district"][d]
        districts[d]["csr"] = {
            "total": round(pd["total"], 2),
            "byDomain": {k: round(v, 2) for k, v in pd["byDomain"].items()},
            "byYear": {y: round(v, 2) for y, v in pd["byYear"].items()},
        }
    csr_domain = {
        "domains": csr_dd["domains"],
        "byDomain": csr_dd["byDomain"],
        "byYear": csr_dd["byYear"],
        "total": csr_dd["total"],
        "years": csr_dd["years"],
        "unclassified": csr_dd["unclassified"],
        "source": "csr.odisha.gov.in (GO CARE, Govt of Odisha CSR portal) — \"Dynamic CSR Report\", district x development-sector export",
        "note": ("Real district-level CSR spend by development sector, FY2014-15→FY2024-25, "
                 "₹ Cr — unlike csrState above (statewide-only, project counts by sector), "
                 "this is the real per-district total, finally unblocking the CSR choropleth. "
                 "Manually exported (no scriptable API for this cut); see "
                 "data/odisha_csr_district_domain.csv. Rows GO CARE files under \"District Not "
                 "Classified Elsewhere\" are excluded from the district map/table and rolled into "
                 "the statewide domain totals here only, under unclassified."),
    }

    # -- Catalytic Unlock layer (editorial nature/commons landscape strategy) --
    # Groups districts into nature/commons landscapes + a catalytic tier; the leverage
    # read itself is computed front-end from the real DMF/CSR/partner fields (see build.py).
    # Everything here is indicative strategy built ON TOP of the real data, not fetched.
    cat = json.load(open("../data/odisha_catalytic.json"))
    land_of = {}
    for ls in cat["landscapes"]:
        for d in ls["districts"]:
            land_of[d] = {"key": ls["key"], "name": ls["name"], "color": ls["color"]}
    for d, meta in cat["districtMeta"].items():
        if d not in districts:
            print(f"WARNING: unmapped catalytic district {d!r}")
            continue
        ls = land_of.get(d, {})
        districts[d]["catalytic"] = {
            "landscape": ls.get("key", ""), "landscapeName": ls.get("name", ""),
            "tier": meta["tier"], "nature": meta["nature"], "note": meta.get("note", ""),
        }
    for d in districts.values():
        d.setdefault("catalytic", {"landscape": "", "landscapeName": "", "tier": "", "nature": 0.0, "note": ""})
    catalytic = {
        "meta": cat.get("meta", {}), "tiers": cat.get("tiers", {}),
        "landscapes": cat.get("landscapes", []), "projects": cat.get("projects", []),
    }

    # -- Ecosystem layers: anchors (TRI-equivalent), funders, schemes, indicative orgs --
    layers = json.load(open("../data/odisha_ecosystem_layers.json"))
    anchor_orgs = layers["anchors"]["orgs"]
    primary_anchor = layers["anchors"]["primary"]
    # paint the primary anchor's districts as the anchor-presence layer
    for a in anchor_orgs:
        for dist in a.get("districts", []):
            if dist in districts:
                districts[dist].setdefault("anchor", {"present": False, "orgs": []})
                districts[dist]["anchor"]["orgs"].append(a["name"])
                if a["name"].startswith(primary_anchor) or primary_anchor in a["name"]:
                    districts[dist]["anchor"]["present"] = True
    for d in districts.values():
        d.setdefault("anchor", {"present": False, "orgs": []})

    # indicative ✳ orgs: keyword-map focus -> themes (kept out of health scores by default)
    indicative = []
    for o in layers.get("indicative", []):
        indicative.append({
            "name": o["name"], "districts": o.get("districts", []),
            "themes": themes_from_focus(o.get("focus", "")),
            "focus": o.get("focus", ""), "source": o.get("source", ""),
            "note": o.get("note", ""),
        })

    model = {
        "canon": CANON,
        "themes": THEMES,
        "years": sorted(dmf_raw.keys(), reverse=True),
        "partners": partners,
        "anchors": anchor_orgs,
        "indicative": indicative,
        "funders": layers.get("funders", []),
        "schemes": layers.get("schemes", {}),
        "vision2036": layers.get("vision2036", {}),
        "csrState": csr_state,
        "csrDomain": csr_domain,
        "catalytic": catalytic,
        "districts": districts,
    }
    json.dump(model, open("../model.json", "w"), ensure_ascii=False, indent=1)

    tot_shg = sum(d["shg"]["total"] for d in districts.values())
    tot_fpo = sum(d["fpo"]["fpos"] for d in districts.values())
    tot_blocks = sum(len(d["blockcov"]) for d in districts.values())
    tot_csr = sum(d["csrFlagship"]["count"] for d in districts.values())
    anchor_n = sum(1 for d in districts.values() if d["anchor"]["present"])
    with_themes = sum(1 for d in districts.values() if d["themes"])
    print(f"model.json written: {len(CANON)} districts, {tot_shg} SHGs, {tot_fpo} FPOs, "
          f"{len(partners)} seed partners, {tot_blocks} blocks with known coverage across "
          f"{len(blockcov_by_district)} districts")
    print(f"  themes populated for {with_themes} districts; {tot_csr} flagship CSR projects; "
          f"anchor ({primary_anchor}) in {anchor_n} districts; "
          f"{len(indicative)} indicative orgs; {len(model['funders'])} funders; "
          f"{len(model['schemes'].get('items', []))} schemes; "
          f"CSR state total ~₹{csr_state['totalCr']} Cr, {csr_state['companies']} companies")
    tot_csr_real = sum(d["csr"]["total"] for d in districts.values())
    print(f"  CSR district x domain: ₹{round(tot_csr_real)} Cr mapped across {len(CANON)} districts "
          f"x {len(csr_domain['domains'])} domains (+ ₹{round(csr_dd['unclassified']['total'])} Cr unclassified)")


if __name__ == "__main__":
    build()
