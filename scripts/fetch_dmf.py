import json, subprocess, sys

YEARS = ["2015-2016","2016-2017","2017-2018","2018-2019","2019-2020","2020-2021",
         "2021-2022","2022-2023","2023-2024","2024-2025","2025-2026"]

def fetch(fy):
    cmd = ["curl", "-sk", "-X", "POST", "https://dmf.odisha.gov.in/report/fund_collection_list",
           "-H", "X-Requested-With: XMLHttpRequest",
           "--data-urlencode", "draw=1", "--data-urlencode", "start=0",
           "--data-urlencode", "length=100", "--data-urlencode", "search[value]=",
           "--data-urlencode", "csrf_test_name=",
           "--data-urlencode", f"finacial_year={fy}",
           "--data-urlencode", "mineral_type="]
    out = subprocess.run(cmd, capture_output=True, timeout=30).stdout
    return json.loads(out)

result = {}
errors = []
for fy in YEARS:
    try:
        d = fetch(fy)
        result[fy] = {"total": d.get("total_collection"), "districts": {row[1]: row[2] for row in d.get("data", [])}}
        print(f"{fy}: total {d.get('total_collection')} Cr, {len(d.get('data',[]))} districts", file=sys.stderr)
    except Exception as e:
        errors.append((fy, str(e)))
        print(f"{fy}: ERROR {e}", file=sys.stderr)

json.dump(result, open("../data/odisha_dmf_data.json","w"), indent=1)
if errors:
    print("ERRORS:", errors, file=sys.stderr)
print("done")
