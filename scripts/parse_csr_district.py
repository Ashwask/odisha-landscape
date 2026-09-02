#!/usr/bin/env python3
"""Parse Odisha_DistrictwiseCSR.xlsx -> data/odisha_csr_district.json.

This is the one open source of *district-level* CSR spend for Odisha (₹ crore,
FY2020-21 -> FY2024-25). It is a DIFFERENT source/methodology from the GO CARE
statewide series already in the model (data/odisha_csr_data.json -> csrState):
the two do NOT reconcile (the district series is roughly 1.5-3x higher in the
later years). So it is kept as its own layer, clearly labelled, never merged
into the GO CARE trend. See README + the reconciliation note in build.py.

All 30 district labels in the sheet already match CANON exactly; the two
non-district rows ("NEC/ Not Mentioned" and "Grand Total") are handled
separately. Run from the scripts/ directory: python3 parse_csr_district.py
"""
import json
import openpyxl

SRC_XLSX = "../Odisha_DistrictwiseCSR.xlsx"
OUT_JSON = "../data/odisha_csr_district.json"

# CANON, duplicated here so this script has no import dependency on build_model.
CANON = {
    "Anugul", "Balangir", "Baleshwar", "Bargarh", "Bhadrak", "Boudh", "Cuttack",
    "Deogarh", "Dhenkanal", "Gajapati", "Ganjam", "Jagatsinghapur", "Jajapur",
    "Jharsuguda", "Kalahandi", "Kandhamal", "Kendrapara", "Kendujhar", "Khordha",
    "Koraput", "Malkangiri", "Mayurbhanj", "Nabarangpur", "Nayagarh", "Nuapada",
    "Puri", "Rayagada", "Sambalpur", "Sonepur", "Sundargarh",
}


def r2(x):
    return round(float(x), 2) if x is not None else 0.0


def main():
    wb = openpyxl.load_workbook(SRC_XLSX, data_only=True)
    ws = wb["Sheet1"]
    rows = list(ws.iter_rows(values_only=True))
    header = list(rows[0])
    years = [str(y) for y in header[1:-1]]  # drop DISTRICT and Grand Total

    districts, nec, grand = {}, None, None
    for row in rows[1:]:
        name = (row[0] or "").strip()
        year_vals = {y: r2(v) for y, v in zip(years, row[1:-1])}
        total = r2(row[-1])
        if name == "Grand Total":
            grand = {"years": year_vals, "total": total}
        elif name in ("NEC/ Not Mentioned", "NEC/Not Mentioned"):
            nec = {"years": year_vals, "total": total}
        elif name in CANON:
            entry = dict(year_vals)
            entry["total"] = total
            districts[name] = entry
        else:
            print(f"WARNING: unmapped CSR-district row {name!r}")

    missing = CANON - set(districts)
    if missing:
        print(f"WARNING: CANON districts absent from sheet: {sorted(missing)}")

    district_total = round(sum(d["total"] for d in districts.values()), 2)
    out = {
        "meta": {
            "source": "csr.gov.in district-wise CSR export (Odisha_DistrictwiseCSR.xlsx)",
            "unit": "INR crore",
            "span": "FY2020-21 to FY2024-25",
            "note": (
                "District-level CSR spend. DIFFERENT source/methodology from the "
                "GO CARE statewide series (csrState); the two do not reconcile "
                "(this series runs ~1.5-3x higher in later years). Kept as its own "
                "layer, not merged into the GO CARE trend."
            ),
        },
        "years": years,
        "districts": districts,
        "nec": nec,                    # CSR not tagged to any district (~25% of spend)
        "grandTotal": grand["total"] if grand else None,
        "districtTotal": district_total,  # sum of the 30 districts only (excludes NEC)
    }
    json.dump(out, open(OUT_JSON, "w"), ensure_ascii=False, indent=1)
    print(f"wrote {OUT_JSON}: {len(districts)} districts, "
          f"district total ~INR {district_total} Cr, NEC ~INR {nec['total'] if nec else 0} Cr, "
          f"grand total ~INR {grand['total'] if grand else 0} Cr over {len(years)} FYs")


if __name__ == "__main__":
    main()
