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
        themes = [t.strip() for t in r["themes"].split(",") if t.strip()]
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

    # -- Partners (seed) --
    for p in partners:
        for dist in p["districts"]:
            if p["name"] not in districts[dist]["partners"]:
                districts[dist]["partners"].append(p["name"])

    model = {
        "canon": CANON,
        "themes": THEMES,
        "years": sorted(dmf_raw.keys(), reverse=True),
        "partners": partners,
        "anchors": [],
        "districts": districts,
    }
    json.dump(model, open("../model.json", "w"), ensure_ascii=False, indent=1)

    tot_shg = sum(d["shg"]["total"] for d in districts.values())
    tot_fpo = sum(d["fpo"]["fpos"] for d in districts.values())
    tot_blocks = sum(len(d["blockcov"]) for d in districts.values())
    print(f"model.json written: {len(CANON)} districts, {tot_shg} SHGs, {tot_fpo} FPOs, "
          f"{len(partners)} seed partners, {tot_blocks} blocks with known coverage across "
          f"{len(blockcov_by_district)} districts")


if __name__ == "__main__":
    build()
