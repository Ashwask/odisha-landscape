#!/usr/bin/env python3
"""Fetch district-level FPO (Farmer Producer Organisation) counts for Odisha.

Source: fpoplatform.com's public dashboard asset (https://www.fpoplatform.com/dashboard),
backed by Cornell TCI's FPO API (fpo.tci.cornell.edu). The dashboard ships a static JSON
asset with state/district-wise FPO counts and farmer numbers for all of India; this script
downloads it and slices out Odisha.

Note: unlike Jharkhand's jh_fpo_data.json (which also has shareholders + complete-financials
counts per district), this public asset only exposes fpo_count and number_of_farmers per
district. The Jharkhand file's shareholders/financials columns were compiled by hand from the
dashboard UI (see that repo's build_fpo.py comment) -- no API exposes that breakdown, so the
same manual step would be needed here to match it exactly.
"""
import json, subprocess, sys

URL = "https://www.fpoplatform.com/assets/data/summary.json"

def fetch():
    out = subprocess.run(["curl", "-s", "-f", "--max-time", "30", URL],
                          capture_output=True, timeout=35)
    if out.returncode != 0:
        print(f"FAILED: {URL} -> curl exit {out.returncode}", file=sys.stderr)
        sys.exit(1)
    return json.loads(out.stdout)

if __name__ == "__main__":
    d = fetch()
    lwd = d["data"]["location_wise_data"]
    odisha = next((s for s in lwd if s["state_name"] == "ODISHA"), None)
    if odisha is None:
        print("FAILED: ODISHA not found in location_wise_data", file=sys.stderr)
        sys.exit(1)
    print(f"Odisha: {odisha['fpo_count']} FPOs, {odisha['number_of_farmers']} farmers, "
          f"{len(odisha['district_wise'])} districts", file=sys.stderr)
    json.dump(odisha, open("../data/odisha_fpo_data.json", "w"), indent=1)
    print("done")
