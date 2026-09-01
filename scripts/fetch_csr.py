#!/usr/bin/env python3
"""Fetch Odisha CSR data from the state GO CARE portal (csr.odisha.gov.in).

GO CARE is Odisha's own CSR-administration portal, fed from MCA CSR filings.
Its district-total page (districtWise.aspx) is login-gated (HTTP 401), and the
national MCA portal (csr.gov.in) gates every export behind a CAPTCHA, so a full
district-wise *total spend* table is not openly available (see README). What IS
openly served, and what this script captures, is:

  * yearTotals   -- statewide projects + CSR spend per FY (loadTotalProject),
                    FY2014-15 .. FY2026-27. Amounts are reported in Rupees Lakh
                    on the portal; stored here in Lakh, plus a Cr convenience.
  * sectorCounts -- statewide project counts by CSR sector (GetStatusGraph).
  * companies    -- the ~300 companies that have filed CSR projects in Odisha
                    (the "funder" universe), from getMasterData.
  * flagship     -- the geocoded flagship/priority projects shown on the portal
                    map (getTableData): company -> district -> amount -> sector
                    -> agency-type -> location. A curated subset, NOT all spend.

Everything here is read-only public JSON (ASP.NET PageMethods), no auth.
Writes -> data/odisha_csr_data.json
"""
import json, os, time, urllib.request

BASE = "https://csr.odisha.gov.in"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36")
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "odisha_csr_data.json")


def post(path, payload, referer="/"):
    req = urllib.request.Request(
        BASE + path, data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json; charset=utf-8",
                 "X-Requested-With": "XMLHttpRequest",
                 "User-Agent": UA, "Referer": BASE + referer})
    return json.load(urllib.request.urlopen(req, timeout=90))


def unwrap(r):
    d = r.get("d", r)
    return json.loads(d) if isinstance(d, str) else d


def main():
    master = unwrap(post("/projectUndertakenCompany.aspx/getMasterData", {}))
    districts = master["distData"]
    years = [y["year_name"] for y in master["yearData"]]
    cats = {c["cat_id"]: c["cat_name"] for c in master["categoryData"]}
    companies = sorted(c["comp_name"] for c in master["comapanyData"])
    print(f"master: {len(districts)} districts, {len(years)} years, "
          f"{len(cats)} sectors, {len(companies)} companies")

    # statewide totals per FY: "projects,amountLakh"
    year_totals = {}
    for y in years:
        resp = post("/Default.aspx/loadTotalProject", {"pData": y})
        s = resp.get("d", "")
        if s and "," in s:
            proj, amt = s.split(",")[:2]
            year_totals[y] = {"projects": int(float(proj)),
                              "amountLakh": float(amt),
                              "amountCr": round(float(amt) / 100.0, 2)}
        time.sleep(0.1)
    print("year totals:", {k: v["amountCr"] for k, v in year_totals.items()})

    # statewide sector counts (all years). GetStatusGraph returns every category.
    sector_counts = {}
    sr = post("/Default.aspx/GetStatusGraph", {"pData": "1", "dData": "0"})
    for row in unwrap(sr):
        sector_counts[row["CategoryName"]] = row["Count"]
    print("sectors:", sector_counts)

    # flagship geocoded projects (union across districts)
    seen = {}
    for d in districts:
        p = {"type": "D", "distId": str(d["dist_id"]), "catId": "0", "FinYr": "0",
             "companyId": "0", "statusId": "0", "AgencyId": "0",
             "PageNo": 1, "PageSize": 100000, "StartAmnt": "0", "EndAmnt": "0"}
        try:
            rows = post("/projectUndertakenCompany.aspx/getTableData", p,
                        "/projectUndertakenCompany.aspx")["d"][0]["objgetTableData"]
        except Exception as e:
            print("  flagship err", d["dist_name"], e); rows = []
        for row in rows:
            seen[row["projectID"]] = {
                "district": row["dist_name"], "company": row["companyName"],
                "project": row["projectName"].strip(),
                "amountLakh": float(row["ammount_spend"] or 0),
                "status": row["status"], "agencyType": row["Agency"],
                "location": row["Location"],
                "lat": row.get("latitude"), "lng": row.get("longitude")}
        time.sleep(0.1)
    flagship = list(seen.values())
    print(f"flagship projects: {len(flagship)}")

    out = {
        "meta": {
            "source": "csr.odisha.gov.in (GO CARE, Govt of Odisha CSR portal; MCA-fed)",
            "note": ("Statewide totals + sector counts + company (funder) list + "
                     "geocoded flagship projects are openly served. District-wise "
                     "TOTAL spend is login-gated on GO CARE and CAPTCHA-gated on "
                     "csr.gov.in, so it is NOT included. Amounts in Rupees Lakh "
                     "(amountCr = /100)."),
            "unit": "Rupees Lakh"},
        "companies": companies,
        "yearTotals": year_totals,
        "sectorCounts": sector_counts,
        "flagship": flagship,
    }
    with open(OUT, "w") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("wrote", os.path.abspath(OUT))


if __name__ == "__main__":
    main()
