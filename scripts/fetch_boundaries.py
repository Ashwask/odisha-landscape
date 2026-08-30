#!/usr/bin/env python3
"""Fetch Odisha's 30 district boundaries from Bharatlas (bharatlas.com).

Bharatlas hosts India's LGD (Local Government Directory) district layer, 2024 edition,
785 districts, CC0-1.0 / CC-BY-4.0. This downloads the full-India geojson (~90 MB) and
filters to stname == "ODISHA", writing a standalone ~4 MB file.

Re-run only if boundaries need refreshing (LGD updates, new districts carved out, etc).
"""
import json, subprocess, sys

URL = "https://bharatlas.com/api/dl/admin/districts/LGD_Districts.geojson"

def fetch():
    tmp = "/tmp/LGD_Districts_full.geojson"
    r = subprocess.run(["curl", "-sL", "--max-time", "120", URL, "-o", tmp], timeout=130)
    if r.returncode != 0:
        print(f"FAILED: {URL} -> curl exit {r.returncode}", file=sys.stderr)
        sys.exit(1)
    return tmp

if __name__ == "__main__":
    path = fetch()
    d = json.load(open(path))
    odisha = [f for f in d["features"] if f["properties"]["stname"] == "ODISHA"]
    if len(odisha) != 30:
        print(f"WARNING: expected 30 Odisha districts, got {len(odisha)}", file=sys.stderr)
    out = {"type": "FeatureCollection", "name": "Odisha_Districts", "features": odisha}
    json.dump(out, open("../data/odisha_districts.geojson", "w"))
    print(f"done: {len(odisha)} districts", file=sys.stderr)
