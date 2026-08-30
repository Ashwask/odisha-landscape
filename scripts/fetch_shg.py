import re, json, time, sys, subprocess, urllib.parse

BASE = "https://preprodmis.lokos.in/shgOuterReports.do"

def fetch(params, retries=4):
    qs = "&".join(f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items())
    url = f"{BASE}?{qs}"
    for attempt in range(retries):
        try:
            result = subprocess.run(["curl", "-s", "-f", "--max-time", "30", url],
                                     capture_output=True, timeout=35)
            if result.returncode == 0:
                return result.stdout.decode("utf-8", errors="replace")
            raise RuntimeError(f"curl exit {result.returncode}")
        except Exception as e:
            if attempt == retries - 1:
                print(f"FAILED: {url} -> {e}", file=sys.stderr)
                return None
            time.sleep(2 * (attempt + 1))

DIST_CODES = {
    "Angul": "2421", "Baleshwar": "2405", "Bargarh": "2414", "Bhadrak": "2417",
    "Bolangir": "2409", "Boudh": "2426", "Cuttack": "2406", "Deogarh": "2416",
    "Dhenkanal": "2407", "Gajapati": "2424", "Ganjam": "2412", "Jagatsinghapur": "2419",
    "Jajpur": "2420", "Jharsuguda": "2415", "Kalahandi": "2410", "Kandhamal": "2408",
    "Kendrapara": "2418", "Kendujhar": "2403", "Khordha": "2423", "Koraput": "2411",
    "Malkangiri": "2431", "Mayurbhanj": "2404", "Nabarangapur": "2430", "Nayagarh": "2422",
    "Nuapada": "2428", "Puri": "2413", "Rayagada": "2429", "Sambalpur": "2401",
    "Sonepur": "2427", "Sundargarh": "2402",
}

def get_blocks(dist_code):
    html = fetch({"methodName": "showBlockPage", "encd": dist_code,
                  "stateName": "ODISHA", "districtName": "X"})
    if not html:
        return None
    tbody_match = re.search(r"<tbody>(.*?)</tbody>", html, re.S)
    if not tbody_match:
        return []
    rows = []
    trs = re.findall(r"<tr>(.*?)</tr>", tbody_match.group(1), re.S)
    for tr in trs:
        tds = re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)
        if len(tds) < 6:
            continue
        clean = lambda x: re.sub(r"<[^>]+>", "", x).strip().replace(",", "")
        vals = [clean(td) for td in tds]
        if not vals[0].isdigit():
            continue
        name = clean(re.sub(r"<a[^>]*>|</a>", "", tds[1]))
        try:
            new_, revived, prenrlm, total, members = (int(v) if v else 0 for v in vals[2:7])
        except ValueError:
            continue
        rows.append({"name": name, "new": new_, "revived": revived, "prenrlm": prenrlm,
                      "total": total, "members": members})
    return rows

if __name__ == "__main__":
    result = {}
    errors = []
    for dist, code in DIST_CODES.items():
        blocks = get_blocks(code)
        if blocks is None:
            errors.append(dist)
            result[dist] = []
            print(f"{dist}: FETCH ERROR", file=sys.stderr)
        else:
            result[dist] = blocks
            tot = sum(b["total"] for b in blocks)
            mem = sum(b["members"] for b in blocks)
            print(f"{dist}: {len(blocks)} blocks, {tot} SHGs, {mem} members", file=sys.stderr)
        time.sleep(0.3)
    json.dump(result, open("../data/odisha_shg_data.json", "w"), indent=1)
    if errors:
        print("ERRORS on:", errors, file=sys.stderr)
    print("done")
