import json
model=json.load(open("model.json"))
geo=json.load(open("odisha_enriched.geojson"))
MODEL=json.dumps(model, separators=(',',':'))
GEO=json.dumps(geo, separators=(',',':'))

HTML = r'''<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Odisha Landscape — Who Does What Where</title>
<style>
:root{
 --ink:#0f2440; --ink2:#31456a; --mut:#6b7a93; --line:#dce3ee; --line2:#eef2f8;
 --bg:#f6f8fc; --card:#ffffff; --accent:#0d6e8c; --accent2:#c2410c; --gold:#b45309;
 --c0:#eef2f8; --hl:#0d6e8c;
 --shadow:0 1px 2px rgba(15,36,64,.04),0 6px 24px rgba(15,36,64,.06);
}
*{box-sizing:border-box}
html,body{margin:0}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,Helvetica,Arial,sans-serif;
 background:var(--bg); color:var(--ink); font-size:14px; line-height:1.45; -webkit-font-smoothing:antialiased;}
.wrap{max-width:1320px; margin:0 auto; padding:28px 22px 80px}
h1{font-size:23px; margin:0 0 3px; letter-spacing:-.02em; font-weight:700}
.sub{color:var(--mut); font-size:13px; margin:0 0 2px}
.prov{color:var(--mut); font-size:11.5px; margin:6px 0 0}
a{color:var(--accent)}
.strip{display:flex; gap:12px; flex-wrap:wrap; margin:20px 0 22px}
.stat{background:var(--card); border:1px solid var(--line); border-radius:12px; padding:12px 15px; min-width:120px; box-shadow:var(--shadow)}
.stat .n{font-size:22px; font-weight:700; letter-spacing:-.02em; line-height:1}
.stat .l{color:var(--mut); font-size:11px; margin-top:5px; text-transform:uppercase; letter-spacing:.04em}
.stat.warn .n{color:var(--accent2)}
.grid{display:grid; grid-template-columns:1.35fr 1fr; gap:18px; align-items:start}
.intro{margin-top:16px; border-left:3px solid var(--accent)}
.intro p{margin:0 0 9px}
.intro p:last-child{margin:0}
.intro-lead{font-size:15px; line-height:1.5; color:var(--ink)}
.intro-body{font-size:13px; line-height:1.55; color:var(--ink2)}
.intro-src{font-size:11.5px; line-height:1.45; color:var(--mut)}
.grid.hero{margin-top:20px}
.grid.hero .card h2{font-size:14px}
@media(max-width:960px){.grid{grid-template-columns:1fr}}
.card{background:var(--card); border:1px solid var(--line); border-radius:14px; box-shadow:var(--shadow)}
.card h2{font-size:13px; text-transform:uppercase; letter-spacing:.05em; color:var(--ink2); margin:0; padding:14px 16px; border-bottom:1px solid var(--line2)}
.cardpad{padding:14px 16px}
.lens{display:flex; gap:6px; flex-wrap:wrap; padding:12px 16px 0}
.lens button{font:inherit; font-size:12px; border:1px solid var(--line); background:#fff; color:var(--ink2);
 padding:6px 11px; border-radius:8px; cursor:pointer; transition:.12s}
.lens button:hover{border-color:var(--accent)}
.lens button.on{background:var(--ink); color:#fff; border-color:var(--ink)}
.dsel{font:inherit; font-size:12px; border:1px solid var(--line); background:#fff; color:var(--ink2);
 padding:6px 11px; border-radius:8px; cursor:pointer; max-width:100%}
svg.map{width:100%; height:auto; display:block}
.dist{stroke:#fff; stroke-width:.8; cursor:pointer; transition:fill .2s}
.dist:hover{stroke:var(--ink); stroke-width:1.6}
.dist.sel{stroke:var(--ink); stroke-width:2}
.dlabel{font-size:8.5px; fill:#25324a; pointer-events:none; text-anchor:middle; font-weight:500}
.dlabel.lite{fill:#eaf0f8}
.legend{display:flex; align-items:center; gap:10px; flex-wrap:wrap; padding:8px 16px 16px; font-size:11.5px; color:var(--mut)}
.legend .sw{display:inline-flex; align-items:center; gap:5px}
.legend .box{width:14px; height:12px; border-radius:3px; border:1px solid rgba(0,0,0,.05)}
.legtitle{font-size:11px; text-transform:uppercase; letter-spacing:.04em; color:var(--ink2); font-weight:600}
/* detail */
#detail .empty{color:var(--mut); font-size:13px; padding:26px 16px; text-align:center}
.dh{display:flex; align-items:baseline; justify-content:space-between; gap:8px; margin-bottom:2px}
.dh .name{font-size:17px; font-weight:700}
.badge{font-size:10.5px; padding:2px 8px; border-radius:20px; font-weight:600; white-space:nowrap}
.badge.asp{background:#fdece3; color:var(--accent2)}
.kv{display:flex; gap:18px; margin:10px 0 4px; flex-wrap:wrap}
.kv .k{color:var(--mut); font-size:11px; text-transform:uppercase; letter-spacing:.03em}
.kv .v{font-size:16px; font-weight:700}
.sec{margin-top:14px}
.sec .t{font-size:11px; text-transform:uppercase; letter-spacing:.04em; color:var(--ink2); font-weight:600; margin-bottom:6px}
.chips{display:flex; gap:5px; flex-wrap:wrap}
.chip{font-size:11.5px; padding:3px 9px; border-radius:7px; background:var(--c0); color:var(--ink2); border:1px solid var(--line)}
.plist{list-style:none; margin:0; padding:0}
.plist li{padding:6px 0; border-bottom:1px solid var(--line2); font-size:13px}
.plist li:last-child{border:0}
.blk{font-size:12px; color:var(--ink2); background:var(--c0); border-radius:8px; padding:8px 10px; margin-top:4px}
.bcov summary{cursor:pointer; font-size:13px; color:var(--ink2); list-style:none; padding:2px 0}
.bcov summary::-webkit-details-marker{display:none}
.bcov summary::before{content:'▸'; display:inline-block; margin-right:6px; color:var(--mut); transition:transform .15s}
.bcov[open] summary::before{transform:rotate(90deg)}
.beta{font-size:9.5px; text-transform:uppercase; letter-spacing:.05em; background:#1f7d63; color:#fff; padding:1px 5px; border-radius:4px; vertical-align:1px}
.blist{list-style:none; margin:4px 0 0; padding:0}
.blist li{padding:5px 0; border-bottom:1px solid var(--line2); font-size:13px}
.blist li:last-child{border:0}
.spark{display:flex; align-items:flex-end; gap:3px; height:44px; margin-top:6px}
.spark .bar{flex:1; background:var(--accent); border-radius:2px 2px 0 0; min-height:2px; opacity:.85}
.spark .bar:hover{opacity:1}
.sparkx{display:flex; justify-content:space-between; font-size:9px; color:var(--mut); margin-top:3px}
/* matrix */
.mtx{overflow-x:auto}
table{border-collapse:collapse; width:100%; font-size:12.5px}
.mtx th{font-weight:600; color:var(--ink2); text-align:left; padding:7px 8px; position:sticky; top:0; background:#fff}
.mtx{padding-top:6px}
.mtx th.rot{vertical-align:bottom; padding:0; text-align:center}
.mtx th.rot > div{writing-mode:vertical-rl; transform:rotate(180deg); white-space:nowrap; font-size:11px; line-height:1; font-weight:600; margin:0 auto; padding:8px 0 6px; color:var(--ink2)}
.mtx thead th{border-bottom:2px solid var(--line); vertical-align:bottom}
.mtx thead th.tot{padding-bottom:8px; font-size:12px; text-align:center}
.mtx thead th:first-child{padding-bottom:8px}
.mtx td{text-align:center; padding:0; border:1px solid var(--line2)}
.mtx td.name{text-align:left; padding:6px 8px; white-space:nowrap; font-weight:500; color:var(--ink)}
.cell{width:26px; height:26px; display:flex; align-items:center; justify-content:center; color:#fff; font-size:10px; font-weight:700}
.mtx td.tot{font-weight:700; color:var(--ink2); background:#f8fafd}
/* directory + table */
.tbl{overflow-x:auto}
.tbl table{font-size:12.5px}
.tbl th{text-align:left; padding:9px 10px; border-bottom:2px solid var(--line); color:var(--ink2); cursor:pointer; user-select:none; white-space:nowrap}
.tbl th:hover{color:var(--accent)}
.tbl td{padding:8px 10px; border-bottom:1px solid var(--line2); vertical-align:top}
.tbl tr:hover td{background:#f8fafd}
.tbl .num{text-align:right; font-variant-numeric:tabular-nums}
.tag{font-size:10.5px; padding:1px 6px; border-radius:5px; background:var(--c0); color:var(--ink2); margin:1px 2px 1px 0; display:inline-block; border:1px solid var(--line)}
.mini{color:var(--mut); font-size:11px}
.dot{width:8px; height:8px; border-radius:50%; display:inline-block; margin-right:4px}
.section-title{font-size:15px; font-weight:700; margin:30px 0 4px; letter-spacing:-.01em}
.section-sub{color:var(--mut); font-size:12px; margin:0 0 12px}
.foot{color:var(--mut); font-size:11px; margin-top:34px; border-top:1px solid var(--line); padding-top:14px}
.pill{cursor:pointer}
.collapser{cursor:pointer; user-select:none; display:block}
.collapser .caret{display:inline-block; font-size:12px; color:var(--mut); margin-left:7px; transition:transform .15s}
.collapser.closed .caret{transform:rotate(-90deg)}
.collapsed{display:none}
.srcgrid{display:grid; grid-template-columns:repeat(3,1fr); gap:18px 22px}
@media(max-width:760px){.srcgrid{grid-template-columns:1fr 1fr}}
.srch{font-size:11px; text-transform:uppercase; letter-spacing:.05em; color:var(--ink2); font-weight:700; margin-bottom:6px}
.srcs ul{margin:0; padding:0; list-style:none}
.srcs li{font-size:12px; color:var(--mut); padding:3px 0; line-height:1.35}
.srcs a{color:var(--accent); text-decoration:none}
.srcs a:hover{text-decoration:underline}
.warnbox{background:#fdf0e2; border:1px solid #f0d5a8; color:#7a4a06; border-radius:10px; padding:10px 13px; font-size:12.5px; margin:0 0 14px}
/* ecosystem health */
.health{display:grid; grid-template-columns:1.1fr 2fr; gap:14px}
@media(max-width:760px){.health{grid-template-columns:1fr}}
.hindex{background:linear-gradient(155deg,#0f2440,#22406e); color:#fff; border-radius:14px; padding:20px 22px; display:flex; flex-direction:column; justify-content:center}
.hindex .big{font-size:48px; font-weight:800; letter-spacing:-.03em; line-height:.95}
.hindex .big small{font-size:19px; opacity:.65; font-weight:600}
.hindex .lbl{font-size:11.5px; text-transform:uppercase; letter-spacing:.06em; opacity:.8; margin-top:4px}
.hindex .band{align-self:flex-start; margin-top:13px; font-size:12px; font-weight:700; padding:4px 13px; border-radius:20px}
.hindex .desc{font-size:12.5px; opacity:.9; margin-top:12px; line-height:1.45}
.hcards{display:grid; grid-template-columns:repeat(3,1fr); gap:12px}
@media(max-width:960px){.hcards{grid-template-columns:1fr 1fr}}
@media(max-width:760px){.hcards{grid-template-columns:1fr}}
.hc{border:1px solid var(--line); border-radius:12px; padding:12px 13px; background:#fff}
.hc .band{font-size:9.5px; font-weight:700; text-transform:uppercase; letter-spacing:.04em; padding:2px 8px; border-radius:20px}
.hc .m{font-size:21px; font-weight:700; letter-spacing:-.02em; margin:9px 0 1px}
.hc .nm{font-size:11px; color:var(--ink2); font-weight:600}
.hc .bar{height:5px; background:var(--line2); border-radius:3px; margin:9px 0 7px; overflow:hidden}
.hc .bar > i{display:block; height:100%; border-radius:3px}
.hc .d{font-size:10.5px; color:var(--mut); line-height:1.38}
/* place health */
.ph{padding:4px 16px 14px}
.phrow{display:grid; grid-template-columns:158px 1fr 82px; gap:12px; align-items:center; padding:7px 0; border-bottom:1px solid var(--line2)}
.phrow:last-child{border-bottom:0}
.phrow .pn{font-weight:600; font-size:13px; display:flex; align-items:center; gap:6px; cursor:pointer}
.phrow .pn:hover{color:var(--accent)}
.phrow .track{height:9px; background:var(--line2); border-radius:5px; overflow:hidden}
.phrow .track > i{display:block; height:100%; border-radius:5px}
.phrow .right{display:flex; align-items:center; justify-content:flex-end; gap:8px}
.phrow .sc{font-weight:700; font-variant-numeric:tabular-nums; font-size:13px; min-width:26px; text-align:right}
.tagp{font-size:9px; font-weight:700; padding:2px 7px; border-radius:20px; white-space:nowrap}
.phhead{display:grid; grid-template-columns:158px 1fr 82px; gap:12px; padding:2px 16px 0; font-size:10px; text-transform:uppercase; letter-spacing:.04em; color:var(--mut)}
/* tabs */
.tabbar{display:flex; gap:8px; margin:16px 0 4px; border-bottom:1px solid var(--line)}
.tabbar button{font:inherit; font-size:13.5px; font-weight:600; border:0; background:none; color:var(--mut); padding:9px 14px; cursor:pointer; border-bottom:2.5px solid transparent; margin-bottom:-1px}
.tabbar button:hover{color:var(--ink2)}
.tabbar button.on{color:var(--accent); border-bottom-color:var(--accent)}
/* vision 2036 */
.vhero{background:linear-gradient(155deg,#0f2440,#1c5a5a); color:#fff; border-radius:16px; padding:26px 26px 24px; margin-top:6px}
.vhero .big{font-size:30px; font-weight:800; letter-spacing:-.02em; line-height:1.08; max-width:760px}
.vhero .meta{font-size:12.5px; opacity:.85; margin-top:12px}
.vhero .meta a{color:#bfe3dd}
.vgrid{display:grid; grid-template-columns:repeat(3,1fr); gap:14px; margin-top:16px}
@media(max-width:960px){.vgrid{grid-template-columns:1fr 1fr}}
@media(max-width:640px){.vgrid{grid-template-columns:1fr}}
.vcard{border:1px solid var(--line); border-radius:14px; background:#fff; padding:15px 16px; box-shadow:var(--shadow)}
.vcard .vh{display:flex; align-items:center; gap:8px; font-size:14px; font-weight:700; color:var(--ink)}
.vcard .vth{width:9px; height:9px; border-radius:50%; flex:none}
.vcard .vt{list-style:none; margin:10px 0 0; padding:0}
.vcard .vt li{font-size:12.5px; color:var(--ink2); padding:4px 0 4px 16px; position:relative; line-height:1.4}
.vcard .vt li::before{content:'▸'; position:absolute; left:0; color:var(--accent)}
.vcard .vp{margin-top:9px; display:flex; gap:5px; flex-wrap:wrap}
.vcard .vp .tag{background:var(--c0)}
.vnote{font-size:11.5px; color:var(--mut); margin:14px 0 0; line-height:1.5}
</style></head>
<body><div class="wrap">
<h1>Odisha Landscape — Who Does What Where</h1>
<p class="sub">Partners × districts × themes, with anchor orgs, SHG/FPO density, DMF mining-fund flow, CSR &amp; funders and government schemes. A sense-making view for partnership &amp; ecosystem decisions — data foundation, not a finished partner survey.</p>

<div class="tabbar" id="tabbar">
 <button class="on" data-view="main">Ecosystem landscape</button>
 <button data-view="vision">Odisha Vision 2036</button>
 <button data-view="align">2036 Alignment</button>
</div>

<div id="viewMain">
<!-- HERO: district map + detail -->
<div class="grid hero">
 <div class="card">
   <h2>District map</h2>
   <div class="lens" id="lens"></div>
   <div id="csrDomainRow" style="display:none;padding:8px 16px 0">
    <select id="csrDomainSel" class="dsel"></select>
   </div>
   <div id="mapbox"></div>
   <div class="legend" id="legend"></div>
 </div>
 <div class="card" id="detail"><h2>District detail</h2>
   <div class="empty" id="detEmpty">Click a district on the map to see partners, block coverage, SHGs, FPOs and DMF trend.</div>
   <div class="cardpad" id="detBody" style="display:none"></div>
 </div>
</div>

<div style="margin:18px 0 -4px;display:flex;align-items:center;gap:10px;flex-wrap:wrap">
 <label style="display:flex;align-items:center;gap:7px;cursor:pointer;font-size:12.5px;color:var(--ink2)">
  <input type="checkbox" id="extToggle"> Include <span style="color:#b45309;font-weight:600">✳ indicative</span> multi-district orgs (CYSD, Gram Vikas, Harsha Trust, PRADAN, FES…) in scoring &amp; map
 </label>
 <span class="mini">recomputes the strip, health index, place health, map lenses &amp; tables · deep-link <code>#ext</code></span>
</div>

<div class="strip" id="strip"></div>

<div class="section-title collapser closed" data-wrap="aboutwrap">About this dashboard &amp; how to read it <span class="caret">▾</span></div>
<div id="aboutwrap" class="collapsed">
<div class="intro card cardpad">
 <p class="intro-lead">A first pass at mapping the development-partner ecosystem in Odisha — <b>who's known to work where</b>, alongside the public infrastructure (SHGs, FPOs) and public money (DMF) already on the ground.</p>
 <p class="intro-body"><b>Read this as a research pass, not a verified census.</b> SHG, DMF and FPO layers are complete, live-fetched government/platform data across all 30 districts. The <b>partner layer is a 46-organisation research pass reaching all 30 districts</b> — compiled via targeted searches across livelihoods/agriculture/NRM, health/nutrition/women/child, education/WASH/governance, and coastal &amp; northern Odisha, with every row backed by a source link (an org's own site, an annual report, a CSR filing, or a directory listing). It is still mostly self-reported and has <b>not been independently field-verified</b> — a handful of rows are explicitly flagged low-confidence in the underlying data (see the Partner directory's source column). Treat it as a strong first pass, not a finished partner survey.</p>
 <p class="intro-src">Sources: Bharatlas (district boundaries, LGD 2024) · DAY-NRLM public MIS (SHG) · Odisha's own DMF portal (dmf.odisha.gov.in) · FPO Platform / Cornell TCI (FPO) · NITI Aayog Aspirational Districts Programme · GO CARE (statewide CSR) · Odisha budget (schemes) · org sites for funders &amp; anchors, one source URL per row. Fully offline &amp; self-contained.</p>
</div>
<p style="margin:14px 0 0;font-size:12.5px;color:var(--mut)">Attending the <b>Landscape of the Future convening</b>? Add your organisation to the <a href="https://claude.ai/code/artifact/23ca2417-b0a9-43dd-8b2d-dfc0d1aac9d9" target="_blank" rel="noopener">Landscape Confluence Board</a> — a live board mapping who's in the room against archetype and outcome lens, so the empty cells are visible to everyone.</p>
</div>

<div class="section-title collapser" data-wrap="healthwrap">Ecosystem health <span class="caret">▾</span></div>
<div id="healthwrap">
<p class="section-sub">A funder-facing read on the state of the partner ecosystem — coverage, reach into aspirational districts, resilience, thematic balance, network depth and SHG co-location. Built on the 46-org research pass — still not independently field-verified, so read the bands as a strong first read, not a definitive verdict.</p>
<div class="card cardpad"><div class="health"><div class="hindex" id="hindex"></div><div class="hcards" id="hcards"></div></div></div>
</div>

<div class="section-title collapser" data-wrap="mtxwrap">Partner × Theme matrix <span class="caret">▾</span></div>
<div id="mtxwrap">
<p class="section-sub">Where thematic energy concentrates among the 46 researched partners. 8 orgs (Goonj, Gram Vikas, NIRMAN, PRADAN, SEBAJAGAT, SEWAK, WASSAN &amp; its partners, WOSCA &amp; WASSAN) have no theme data in the source and show no cells — that's a gap in the source, not a claim they cover no themes.</p>
<div class="card cardpad mtx" id="matrix"></div>
</div>

<div class="section-title collapser" data-wrap="govtwrap">Government spend &amp; allocation <span class="caret">▾</span></div>
<div id="govtwrap">
<p class="section-sub">The largest place-based public money in Odisha. <b>DMF (District Mineral Foundation)</b> is district-specific and live from Odisha's own portal (dmf.odisha.gov.in), FY2015-16 → FY2025-26 — see the <b>"DMF mining fund"</b> map lens. Major state/central schemes are largely state-wide; figures are from the Odisha 2025-26 budget (finance.odisha.gov.in &amp; press).</p>
<div class="grid" style="grid-template-columns:1fr 1fr;align-items:start">
 <div class="card"><h2>DMF collection by district (cumulative, FY16 → FY26)</h2><div class="tbl" id="govtdmf"></div></div>
 <div class="card"><h2>Major schemes &amp; allocations (Odisha budget FY2025-26)</h2><div class="tbl" id="schemes"></div></div>
</div>
</div>

<div class="section-title collapser" data-wrap="csrwrap">CSR &amp; funders <span class="caret">▾</span></div>
<div id="csrwrap">
<p class="section-sub">Who funds development work in Odisha. <b>District-level CSR, real ₹ by development domain,</b> comes from GO CARE's "Dynamic CSR Report" export (see the <b>"CSR spend" map lens</b> + its domain filter) — the older "CSR flagship ✳" lens still shows only the portal's geocoded flagship projects, a curated subset. The Funders table links each funder to the org(s) it backs in Odisha where public; amounts are org-wide unless noted, and rows carry a confidence flag.</p>
<div class="grid" style="grid-template-columns:1fr 1fr;align-items:start">
 <div class="card"><h2>CSR filed in Odisha</h2><div class="lens" id="csrTabs"></div>
  <div id="csrFyRow" style="display:none;padding:8px 16px 0"><select id="csrFySel" class="dsel"></select></div>
  <div id="csrstate"></div></div>
 <div class="card"><h2>Funders &amp; philanthropies → who they back in Odisha</h2><div class="tbl" id="funders"></div></div>
</div>
</div>

<div class="section-title collapser closed" id="dirToggle" data-wrap="dirwrap">Partner directory <span class="caret">▾</span> <span class="mini" style="font-weight:400" id="dircount"></span></div>
<div id="dirwrap" class="collapsed">
<p class="section-sub">All 46 researched partner organisations. Click a column header to sort; click a district tag to focus the map. Each row's source URL and confidence notes live in <code>data/odisha_partners_seed.csv</code> in the repo — a few rows are flagged low-confidence there and worth independent verification before relying on them.</p>
<div class="card tbl" id="dirtbl"></div>
</div>

<div class="section-title collapser closed" data-wrap="phwrap">Place health — where attention is needed <span class="caret">▾</span></div>
<div id="phwrap" class="collapsed">
<p class="section-sub">Each district scored 0–100 on how well it is served (partner presence 45% · thematic breadth 30% · resilience/no single-point-of-failure 25%), ranked neediest-first, using the 46-org research pass. Priority = aspirational (NITI Aayog) &amp; weakly served.</p>
<div class="card">
 <div class="phhead"><span>District</span><span>Coverage strength</span><span style="text-align:right">Score</span></div>
 <div class="ph" id="placehealth"></div>
</div>
</div>

<div class="section-title collapser closed" data-wrap="dcwrap">District coverage table <span class="caret">▾</span></div>
<div id="dcwrap" class="collapsed">
<p class="section-sub">The full grid: partners, themes, aspirational status (NITI Aayog), SHGs and FPOs.</p>
<div class="card tbl" id="distbl"></div>
</div>

<div class="section-title collapser closed" data-wrap="srcwrap">Sources <span class="caret">▾</span></div>
<div id="srcwrap" class="collapsed">
<p class="section-sub">Everything above is traceable. See the repo README for the full provenance note per field.</p>
<div class="card cardpad srcs">
 <div class="warnbox"><b>District-total CSR was gated — now included via a different GO CARE export.</b> The national CSR portal (csr.gov.in) still gates every district export behind a CAPTCHA, and GO CARE's own district-total page still needs a login (HTTP 401). But GO CARE's "Dynamic CSR Report" tool (district × development-sector cut) is open and was manually exported — see the <b>"CSR spend" map lens</b> and the CSR &amp; funders section's "By district" / "By domain" tabs. ~46% of statewide CSR (FY15→FY25) is filed by companies under "District Not Classified Elsewhere" (typically statewide/multi-district projects) — that slice is in the statewide domain totals but excluded from the district map/table since it isn't attributable to one. The "CSR flagship ✳" lens is unrelated — it's still only the portal's geocoded flagship projects, a curated subset. (An earlier, narrower FY21→FY25 total-only cut from <code>Odisha_DistrictwiseCSR.xlsx</code> — same underlying csr.gov.in data, no domain split — is superseded by the export above; its numbers cross-validate to the nearest ₹0.1 Cr.)</div>
 <div class="srcgrid">
  <div><div class="srch">Boundaries</div>
   <ul><li><a href="https://bharatlas.com" target="_blank" rel="noopener">Bharatlas</a> — district boundaries, LGD 2024 (CC0-1.0 / CC-BY-4.0)</li></ul></div>
  <div><div class="srch">SHG (Self Help Groups)</div>
   <ul><li><a href="https://nrlm.gov.in/" target="_blank" rel="noopener">DAY-NRLM public MIS</a> — block-wise SHG counts, all 30 districts</li></ul></div>
  <div><div class="srch">DMF (mining fund)</div>
   <ul><li><a href="https://dmf.odisha.gov.in" target="_blank" rel="noopener">Odisha DMF portal</a> — district × FY collection, live</li></ul></div>
  <div><div class="srch">FPOs (Farmer Producer Orgs)</div>
   <ul><li><a href="https://www.fpoplatform.com/dashboard" target="_blank" rel="noopener">FPO Platform</a> (backed by Cornell TCI's FPO API) — district count &amp; farmers</li></ul></div>
  <div><div class="srch">Aspirational districts</div>
   <ul><li><a href="https://www.niti.gov.in/" target="_blank" rel="noopener">NITI Aayog</a> — Aspirational Districts Programme, official list</li></ul></div>
  <div><div class="srch">CSR &amp; funders</div>
   <ul><li><a href="https://csr.odisha.gov.in/" target="_blank" rel="noopener">GO CARE — Odisha CSR portal</a> (MCA-fed) — statewide CSR-by-year, sectors, 300 companies, flagship projects, and a district × development-sector "Dynamic CSR Report" export (manual, no scriptable API — see <code>data/odisha_csr_district_domain.csv</code>) · funder→org links from org sites &amp; CSR filings (see the Funders table)</li></ul></div>
  <div><div class="srch">Government schemes</div>
   <ul><li><a href="https://finance.odisha.gov.in/" target="_blank" rel="noopener">Odisha Finance Dept</a> — Budget 2025-26 (People Budget / Highlights) &amp; press</li></ul></div>
  <div><div class="srch">Anchor / indicative orgs</div>
   <ul><li>Multi-district anchors from org sites: <a href="https://www.cysd.org/about-us/where-we-work" target="_blank" rel="noopener">CYSD</a>, <a href="https://www.gramvikas.org/" target="_blank" rel="noopener">Gram Vikas</a>, <a href="https://harshatrust.org/" target="_blank" rel="noopener">Harsha Trust</a>, Niyatee, PRADAN, FES — indicative district sets, kept out of scoring unless toggled</li></ul></div>
  <div><div class="srch">Partner research pass</div>
   <ul><li>Org websites, annual reports, CSR filings &amp; NGO directories, one source URL per row — see the Partner directory</li></ul></div>
 </div>
</div>
</div>

<div class="foot" id="foot"></div>
</div><!-- /viewMain -->

<div id="viewVision" style="display:none"></div>
<div id="viewAlign" style="display:none"></div>
</div>

<script>
const MODEL=__MODEL__;
const GEO=__GEO__;
const D=MODEL.districts, CANON=MODEL.canon, THEMES=MODEL.themes, YEARS=MODEL.years, PARTNERS=MODEL.partners;
const NDIST=CANON.length;
const el=(t,c,h)=>{const e=document.createElement(t); if(c)e.className=c; if(h!=null)e.innerHTML=h; return e;};

/* ---------- indicative ✳ orgs, funders, schemes, CSR state ---------- */
const INDICATIVE=MODEL.indicative||[], FUNDERS=MODEL.funders||[];
const SCHEMES=MODEL.schemes||{items:[],stateBudgetCr:0,fy:''};
const CSR=MODEL.csrState||{yearTotals:{},sectorCounts:{},companies:0,totalCr:0};
const ANCHORS=MODEL.anchors||[];
const VISION=MODEL.vision2036||{pillars:[]};
let INCLUDE_EXT=false;                       // "include indicative orgs in scoring" toggle
const indBy=d=>INDICATIVE.filter(o=>(o.districts||[]).includes(d));

/* ---------- effective data (folds in indicative orgs when the toggle is on) ---------- */
function effPList(d){const base=D[d].partners.slice();
 if(INCLUDE_EXT)indBy(d).forEach(o=>{if(!base.includes(o.name))base.push(o.name);});
 return base;}
function effP(d){return effPList(d).length;}
function effTList(d){const s=new Set(D[d].themes);
 if(INCLUDE_EXT)indBy(d).forEach(o=>(o.themes||[]).forEach(t=>s.add(t)));
 return [...s];}
function effT(d){return effTList(d).length;}
const coveredList=()=>CANON.filter(d=>effP(d)>0);
const whiteList=()=>CANON.filter(d=>effP(d)===0);

/* ---------- DMF (real, year-wise) ---------- */
const DMF_TOTAL={}; CANON.forEach(d=>{DMF_TOTAL[d]=YEARS.reduce((s,y)=>s+(D[d].dmf[y]||0),0);});
const maxDMF=Math.max(1,...Object.values(DMF_TOTAL));
const stateDMF=Object.values(DMF_TOTAL).reduce((a,b)=>a+b,0);
const fmtDmf=v=>'₹'+v.toLocaleString('en-IN',{maximumFractionDigits:0})+' Cr'; // values already in ₹ Cr

/* ---------- CSR (real district x sector spend, GO CARE "Dynamic CSR Report") ---------- */
const CSRD=MODEL.csrDomain||{domains:[],byDomain:{},byYear:{},total:0,years:[],unclassified:{total:0,byDomain:{},byYear:{}}};
const fmtCr=v=>'₹'+(+v).toLocaleString('en-IN',{maximumFractionDigits:v>=100?0:1})+' Cr';
const CSRSHORT={
 'Education, Differently Abled, livelihood':'Education & Livelihood',
 'Encouraging Sports':'Sports',
 'Environment, Animal Welfare, Conservation of Resources':'Environment',
 'Gender Equality, Women Empowerment, Old Age Homes, Reducing Inequalities':'Gender Equality',
 'Health, Eradicating Hunger, Poverty and Malnutrition, Safe Drinking water, Sanitation':'Health & Sanitation',
 'Heritage Art And Culture':'Heritage, Art & Culture',
 'Other Sectors (Technology Incubator And benefits To Armed Forces And Admin Overheads)':'Other (Tech / Armed Forces)',
 'Others':'Others', 'Rural Development':'Rural Development', 'Slum Area Development':'Slum Area Development',
};
const shortCsr=d=>CSRSHORT[d]||d;
const csrTotalN=d=>((D[d].csr||{}).total)||0;
const maxCsrTotal=Math.max(1,...CANON.map(csrTotalN));

/* ---------- Catalytic Unlock (nature/commons landscape strategy, indicative) ---------- */
const CAT=MODEL.catalytic||{tiers:{},landscapes:[],projects:[],meta:{}};
const CAT_TIERS=CAT.tiers||{}, CAT_LAND=CAT.landscapes||[], CAT_PROJ=CAT.projects||[];
const landById={}; CAT_LAND.forEach(l=>landById[l.key]=l);
const catOf=d=>D[d].catalytic||{landscape:'',tier:'',nature:0,note:''};
// Leverage read = where small catalytic ₹ unblocks the most: committed money (pool) x
// capacity gap x nature/commons stake (nature carries the highest weight, by design).
const maxPart=Math.max(1,...CANON.map(d=>(D[d].partners||[]).length));
function catLeverage(d){
 const pool=(( (DMF_TOTAL[d]||0)/maxDMF )+( csrTotalN(d)/maxCsrTotal ))/2;   // committed money to steer/crowd-in
 const gap=1-((D[d].partners||[]).length/maxPart);                       // capacity bottleneck
 const nature=catOf(d).nature||0;                                        // nature/commons stake
 return Math.round(100*(0.35*pool+0.25*gap+0.40*nature));
}
const maxLev=Math.max(1,...CANON.map(catLeverage));

/* ---------- theme frequency (for matrix shading + dominant) ---------- */
const themeFreq={}; THEMES.forEach(t=>themeFreq[t]=0);
PARTNERS.forEach(p=>p.themes.forEach(t=>{if(t in themeFreq)themeFreq[t]++;}));
const maxTF=Math.max(...Object.values(themeFreq),1);

/* ---------- summary strip ---------- */
function renderStrip(){const strip=document.getElementById('strip'); strip.innerHTML='';
 const covered=coveredList().length, white=whiteList().length;
 const orgN=INCLUDE_EXT?(PARTNERS.length+INDICATIVE.length):PARTNERS.length;
 const stats=[
  [NDIST,'Districts'],
  [orgN,INCLUDE_EXT?'Orgs (incl. ✳ indicative)':'Partners mapped (researched)'],
  [covered,'Districts covered'],
  [white,'Whitespace (0 orgs)','warn'],
  [CANON.filter(d=>D[d].aspirational).length,'Aspirational (NITI Aayog)'],
  [fmtDmf(Math.round(stateDMF)),'DMF collected, FY16→FY26'],
  ['₹'+CSR.totalCr.toLocaleString('en-IN',{maximumFractionDigits:0})+' Cr','CSR filed, FY15→FY27 (statewide)'],
  [CSR.companies,'CSR-filing companies (funders)']
 ];
 stats.forEach(s=>{const c=el('div','stat'+(s[2]?' '+s[2]:'')); c.appendChild(el('div','n',s[0])); c.appendChild(el('div','l',s[1])); strip.appendChild(c);});
}

/* ---------- projection (equirectangular fit) ---------- */
function bounds(){let mnx=1e9,mny=1e9,mxx=-1e9,mxy=-1e9;
 GEO.features.forEach(f=>eachCoord(f.geometry,(x,y)=>{if(x<mnx)mnx=x;if(x>mxx)mxx=x;if(y<mny)mny=y;if(y>mxy)mxy=y;}));
 return [mnx,mny,mxx,mxy];}
function eachCoord(g,cb){const c=g.coordinates;
 const walk=a=>{if(typeof a[0]==='number'){cb(a[0],a[1]);}else a.forEach(walk);}; walk(c);}
const W=760,H=560,PAD=26;
const [mnx,mny,mxx,mxy]=bounds();
const midLat=(mny+mxy)/2, kx=Math.cos(midLat*Math.PI/180);
const bw=(mxx-mnx)*kx, bh=(mxy-mny);
const sc=Math.min((W-2*PAD)/bw,(H-2*PAD)/bh);
const ox=(W-bw*sc)/2, oy=(H-bh*sc)/2;
const px=x=>ox+((x-mnx)*kx)*sc;
const py=y=>oy+(mxy-y)*sc;
function pathFor(g){let d='';
 const ring=r=>{r.forEach((pt,i)=>{d+=(i?'L':'M')+px(pt[0]).toFixed(1)+' '+py(pt[1]).toFixed(1);});d+='Z';};
 if(g.type==='Polygon')g.coordinates.forEach(ring);
 else g.coordinates.forEach(poly=>poly.forEach(ring));
 return d;}
function centroid(g){let sx=0,sy=0,n=0;eachCoord(g,(x,y)=>{sx+=x;sy+=y;n++;});return [px(sx/n),py(sy/n)];}

/* ---------- color scales ---------- */
const seq=['#eaf1f7','#cfe0ee','#a7c7e0','#6fa3cc','#3f7cb0','#1f5a8f','#0d3c6b']; // blue seq
function seqColor(v,max){if(!max||v<=0)return '#f1f5fa'; const t=v/max; const i=Math.min(seq.length-1,Math.floor(t*(seq.length-1)+0.001)); return seq[Math.max(1,i)];}
const themePalette={}; const TP=['#0d6e8c','#c2410c','#4d7c2f','#7c3a86','#b45309','#1f5a8f','#0e8074','#a1344b','#5b6bbf','#8a6d1a','#2b8a3e','#9a3412'];
THEMES.forEach((t,i)=>themePalette[t]=TP[i%TP.length]);

/* ---------- lenses ---------- */
let maxP,maxT;
function refreshScales(){maxP=Math.max(1,...CANON.map(effP));maxT=Math.max(1,...CANON.map(effT));}
refreshScales();
const lenses={
 placehealth:{label:'Place health score',fill:d=>{const pal=['#c2410c','#e0762f','#e6b84d','#8bbf5a','#2b8a3e'];return pal[Math.min(4,Math.floor(placeScore(d)/20.0001))];},
   legend:()=>gradLegendC('Place health 0 → 100',['#c2410c','#e0762f','#e6b84d','#8bbf5a','#2b8a3e'],'weak → strong')},
 partners:{label:'Partner density',fill:d=>seqColor(effP(d),maxP),
   legend:()=>gradLegend('# partners',maxP)},
 themes:{label:'Theme breadth',fill:d=>seqColor(effT(d),maxT),
   legend:()=>gradLegend('# themes',maxT)},
 dom:{label:'Dominant theme',fill:d=>{const t=domTheme(d);return t?themePalette[t]:'#f1f5fa';},
   legend:()=>themeLegend()},
 gap:{label:'Coverage gap',fill:d=>{const n=effP(d),a=D[d].aspirational;if(n===0&&a)return '#c2410c';
     if(n===0)return '#e79a6a'; if(a&&n<=1)return '#f0c088'; return '#cfe0d8';},
   legend:()=>gapLegend()},
 blockcov:{label:'Block presence (beta)',fill:d=>{const n=blockN(d);if(!n)return '#f1f5fa';const p=['#dcefe6','#a6ddc4','#6ec6a4','#3aa987','#1f7d63'];return p[Math.min(p.length-1,Math.ceil(n/Math.max(maxBlk,1)*(p.length-1)))];},
   legend:()=>gradLegendC('Known block-level presence — from the research pass only',['#f1f5fa','#a6ddc4','#6ec6a4','#3aa987','#1f7d63'],'0 → '+maxBlk+' blocks')},
 shg:{label:'SHG density',fill:d=>{const n=shgN(d);if(!n)return '#faf3e8';const p=['#faf3e8','#f0dcae','#e0b968','#c98e2e','#9c6512'];return p[Math.min(p.length-1,Math.ceil(n/Math.max(maxSHG,1)*(p.length-1)))];},
   legend:()=>gradLegendC('Self Help Groups (DAY-NRLM MIS)',['#faf3e8','#f0dcae','#e0b968','#c98e2e','#9c6512'],'0 → '+maxSHG.toLocaleString()+' SHGs')},
 fpo:{label:'FPO density',fill:d=>{const n=fpoN(d);if(!n)return '#eef3ea';const p=['#eef3ea','#c9dfba','#9ec98a','#6fae5c','#3d8730'];return p[Math.min(p.length-1,Math.ceil(n/Math.max(maxFPO,1)*(p.length-1)))];},
   legend:()=>gradLegendC('FPOs (FPO Platform)',['#eef3ea','#c9dfba','#9ec98a','#6fae5c','#3d8730'],'0 → '+maxFPO.toLocaleString()+' FPOs')},
 dmf:{label:'DMF mining fund',fill:d=>{const v=DMF_TOTAL[d]||0;if(!v)return '#f2eef6';const t=v/maxDMF;const p=['#e7dcf0','#c9b0e0','#a97fce','#8a4fbf','#6b2fa0'];return p[Math.min(p.length-1,Math.floor(t*(p.length-1)+0.001))];},
   legend:()=>gradLegendC('DMF collected, FY16→FY26 (₹ Cr)',['#e7dcf0','#c9b0e0','#a97fce','#8a4fbf','#6b2fa0'],'0 → '+fmtDmf(Math.round(maxDMF)))},
 csr:{label:'CSR flagship ✳',fill:d=>{const n=csrN(d);if(!n)return '#f1f5fa';const p=['#fbeee6','#f4c9a8','#e89b63','#d1702f','#a8500f'];return p[Math.min(p.length-1,Math.ceil(n/Math.max(maxCSR,1)*(p.length-1)))];},
   legend:()=>gradLegendC('Mapped flagship CSR projects (GO CARE) — count, not total spend',['#f1f5fa','#f4c9a8','#e89b63','#d1702f','#a8500f'],'0 → '+maxCSR)},
 csrspend:{label:'CSR spend (real ₹)',fill:d=>{const v=csrLensN(d),mx=csrLensMax();if(!v)return '#fff8ef';
     const p=['#fff1de','#fbd6a3','#f2ac5c','#dd7f21','#b25a04'];return p[Math.min(p.length-1,Math.ceil(v/Math.max(mx,1)*(p.length-1)))];},
   legend:()=>gradLegendC('District CSR spend'+(curCsrDomain==='__all__'?', all domains':' — '+shortCsr(curCsrDomain))+' (₹ Cr, FY15→FY25)',
     ['#fff1de','#fbd6a3','#f2ac5c','#dd7f21','#b25a04'],'0 → '+fmtCr(Math.round(csrLensMax())))},
 catalytic:{label:'Catalytic Unlock ✳',fill:d=>{const l=catOf(d).landscape;return (landById[l]||{}).color||'#f1f5fa';},
   legend:()=>catLandLegend()},
 anchor:{label:'Anchor org ✳',fill:d=>{const a=D[d].anchor||{};return a.present?'#0e8074':((a.orgs&&a.orgs.length)?'#a6ddc4':'#f1f5fa');},
   legend:()=>anchorLegend()}
};
const blockN=d=>(D[d].blockcov||[]).length;
const maxBlk=Math.max(1,...CANON.map(blockN));
const shgN=d=>(D[d].shg||{}).total||0;
const maxSHG=Math.max(1,...CANON.map(shgN));
const fpoN=d=>(D[d].fpo||{}).fpos||0;
const maxFPO=Math.max(1,...CANON.map(fpoN));
const csrN=d=>((D[d].csrFlagship||{}).count)||0;
const maxCSR=Math.max(1,...CANON.map(csrN));
const csrDomainN=(d,dom)=>(((D[d].csr||{}).byDomain||{})[dom])||0;
const maxCsrDomainCache={};
function maxCsrDomainN(dom){if(!(dom in maxCsrDomainCache))maxCsrDomainCache[dom]=Math.max(1,...CANON.map(d=>csrDomainN(d,dom)));return maxCsrDomainCache[dom];}
let curCsrDomain='__all__';
const csrLensN=d=>curCsrDomain==='__all__'?csrTotalN(d):csrDomainN(d,curCsrDomain);
const csrLensMax=()=>curCsrDomain==='__all__'?maxCsrTotal:maxCsrDomainN(curCsrDomain);
function domTheme(d){const f={};PARTNERS.forEach(p=>{if(p.districts.includes(d))p.themes.forEach(t=>f[t]=(f[t]||0)+1);});
 if(INCLUDE_EXT)indBy(d).forEach(o=>(o.themes||[]).forEach(t=>f[t]=(f[t]||0)+1));
 let best=null,bv=0;for(const k in f)if(f[k]>bv){bv=f[k];best=k;}return best;}
let curLens='placehealth', selD=null;

/* legends */
function gradLegend(title,max){const w=el('div');w.appendChild(el('span','legtitle',title));
 const grad=el('div'); grad.style.cssText='display:flex;gap:0;border-radius:4px;overflow:hidden';
 seq.forEach(c=>{const b=el('div');b.style.cssText='width:24px;height:12px;background:'+c;grad.appendChild(b);});
 w.appendChild(grad);
 w.appendChild(el('span','','0 → '+max));
 w.style.cssText='display:flex;align-items:center;gap:8px;flex-wrap:wrap';return w;}
function gradLegendC(title,cols,rng){const w=el('div');w.style.cssText='display:flex;align-items:center;gap:8px;flex-wrap:wrap';
 w.appendChild(el('span','legtitle',title));
 const grad=el('div'); grad.style.cssText='display:flex;gap:0;border-radius:4px;overflow:hidden';
 cols.forEach(c=>{const b=el('div');b.style.cssText='width:24px;height:12px;background:'+c;grad.appendChild(b);});
 w.appendChild(grad); w.appendChild(el('span','',rng)); return w;}
function themeLegend(){const w=el('div');w.style.cssText='display:flex;gap:10px;flex-wrap:wrap';
 const used=[...new Set(CANON.map(domTheme).filter(Boolean))];
 used.forEach(t=>{const s=el('span','sw');const b=el('span','box');b.style.background=themePalette[t];s.appendChild(b);s.appendChild(el('span','',t));w.appendChild(s);});return w;}
function gapLegend(){const items=[['#c2410c','Whitespace + aspirational'],['#e79a6a','Whitespace'],['#f0c088','Aspirational, thin (≤1)'],['#cfe0d8','Covered']];
 const w=el('div');w.style.cssText='display:flex;gap:12px;flex-wrap:wrap';
 items.forEach(i=>{const s=el('span','sw');const b=el('span','box');b.style.background=i[0];s.appendChild(b);s.appendChild(el('span','',i[1]));w.appendChild(s);});return w;}
function anchorLegend(){const items=[['#0e8074','CYSD (primary anchor) present'],['#a6ddc4','Other anchor org (indicative)'],['#f1f5fa','No mapped anchor']];
 const w=el('div');w.style.cssText='display:flex;gap:12px;flex-wrap:wrap';
 w.appendChild(el('span','legtitle','Multi-district anchor orgs'));
 items.forEach(i=>{const s=el('span','sw');const b=el('span','box');b.style.background=i[0];s.appendChild(b);s.appendChild(el('span','',i[1]));w.appendChild(s);});return w;}
function catLandLegend(){const w=el('div');w.style.cssText='display:flex;gap:12px;flex-wrap:wrap;align-items:center';
 w.appendChild(el('span','legtitle','Nature/commons landscapes ✳ (indicative)'));
 CAT_LAND.forEach(l=>{const s=el('span','sw');const b=el('span','box');b.style.background=l.color;s.appendChild(b);s.appendChild(el('span','',l.name));w.appendChild(s);});return w;}

/* build map */
const mapbox=document.getElementById('mapbox');
const svgNS='http://www.w3.org/2000/svg';
const svg=document.createElementNS(svgNS,'svg');
svg.setAttribute('viewBox','0 0 '+W+' '+H); svg.setAttribute('class','map');
const paths={},labels={};
/* two passes: all fills first, then all labels on top -- otherwise a later district's
   fill (appended after an earlier district's label, in the same single-pass loop) paints
   over that label whenever their bounding boxes overlap near a shared border. */
GEO.features.forEach(f=>{const name=f.properties.district;
 const p=document.createElementNS(svgNS,'path');
 p.setAttribute('d',pathFor(f.geometry)); p.setAttribute('class','dist'); p.dataset.d=name;
 p.addEventListener('click',()=>selectDist(name));
 p.addEventListener('mousemove',ev=>showTip(ev,name));
 p.addEventListener('mouseleave',hideTip);
 svg.appendChild(p); paths[name]=p;
});
GEO.features.forEach(f=>{const name=f.properties.district;
 const [cx,cy]=centroid(f.geometry);
 const tx=document.createElementNS(svgNS,'text'); tx.setAttribute('x',cx); tx.setAttribute('y',cy);
 tx.setAttribute('class','dlabel'); tx.dataset.base=name; tx.textContent=name;
 svg.appendChild(tx); labels[name]=tx;
});
mapbox.appendChild(svg);

/* tooltip */
const tip=el('div'); tip.style.cssText='position:fixed;pointer-events:none;background:#0f2440;color:#fff;padding:7px 10px;border-radius:8px;font-size:12px;box-shadow:0 6px 20px rgba(0,0,0,.25);z-index:99;display:none;max-width:230px';
document.body.appendChild(tip);
function showTip(ev,name){
 tip.innerHTML='<b>'+name+'</b> · health '+placeScore(name)+'/100<br>'+effP(name)+' org'+(effP(name)!=1?'s':'')+' · '+effT(name)+' themes<br>DMF: '+fmtDmf(Math.round(DMF_TOTAL[name]||0))+(D[name].aspirational?' · <span style="color:#f0a878">Aspirational</span>':'');
 tip.style.display='block'; tip.style.left=Math.min(ev.clientX+14,innerWidth-240)+'px'; tip.style.top=(ev.clientY+14)+'px';}
function hideTip(){tip.style.display='none';}

/* lens buttons */
const lensBox=document.getElementById('lens');
/* Partial-coverage / beta lenses: shown only when the ✳ indicative toggle is on, so their
   many blank districts aren't misread as "no activity" by default. */
const GATED_LENSES=['blockcov'];
function buildLensButtons(){
 if(GATED_LENSES.includes(curLens)&&!INCLUDE_EXT)curLens='placehealth';
 lensBox.innerHTML='';
 Object.entries(lenses).forEach(([k,v])=>{
  if(GATED_LENSES.includes(k)&&!INCLUDE_EXT)return;
  const b=el('button',k===curLens?'on':'',v.label);b.onclick=()=>{curLens=k;paint();};lensBox.appendChild(b);});
}
buildLensButtons();
/* CSR domain filter -- only shown while the "CSR spend (real ₹)" lens is active */
const csrDomainSel=document.getElementById('csrDomainSel');
csrDomainSel.innerHTML='<option value="__all__">All domains (total)</option>'
 +CSRD.domains.map(dm=>'<option value="'+dm.replace(/"/g,'&quot;')+'">'+shortCsr(dm)+'</option>').join('');
csrDomainSel.onchange=()=>{curCsrDomain=csrDomainSel.value;paint();};
function paint(){
 [...lensBox.children].forEach(b=>b.classList.toggle('on',b.textContent===lenses[curLens].label));
 document.getElementById('csrDomainRow').style.display=curLens==='csrspend'?'':'none';
 CANON.forEach(d=>{const f=lenses[curLens].fill(d); paths[d].setAttribute('fill',f);
   const dark=isDark(f); labels[d].classList.toggle('lite',dark);
   labels[d].textContent = curLens==='placehealth' ? labels[d].dataset.base+' · '+placeScore(d) : labels[d].dataset.base;});
 const lg=document.getElementById('legend'); lg.innerHTML=''; lg.appendChild(lenses[curLens].legend());
}
function isDark(hex){if(!hex||hex[0]!=='#'||hex.length<7)return false;const r=parseInt(hex.slice(1,3),16),g=parseInt(hex.slice(3,5),16),b=parseInt(hex.slice(5,7),16);return (0.299*r+0.587*g+0.114*b)<140;}

/* detail */
function selectDist(name){selD=name;
 Object.values(paths).forEach(p=>p.classList.remove('sel')); paths[name].classList.add('sel');
 const v=D[name]; document.getElementById('detEmpty').style.display='none';
 const body=document.getElementById('detBody'); body.style.display='block';
 const dp=PARTNERS.filter(p=>p.districts.includes(name));
 const anc=v.anchor||{present:false,orgs:[]};
 let h='<div class="dh"><span class="name">'+name+'</span><span>';
 if(v.aspirational)h+='<span class="badge asp">Aspirational</span>';
 if(anc.present)h+=' <span class="badge" style="background:#dcf1ec;color:#0e8074">Anchor: CYSD</span>';
 h+='</span></div>';
 h+='<div class="kv"><div><div class="k">Partners</div><div class="v">'+effP(name)+'</div></div>'
   +'<div><div class="k">Themes</div><div class="v">'+effT(name)+'</div></div>'
   +'<div><div class="k">DMF (FY16→FY26)</div><div class="v">'+fmtDmf(Math.round(DMF_TOTAL[name]||0))+'</div></div></div>';
 // place health readout
 const ps=placeScore(name), pb=BAND[band(ps)], pt=placeTag(name);
 h+='<div class="sec"><div class="t">Place health score</div>'
  +'<div style="display:flex;align-items:center;gap:11px">'
  +'<div style="font-size:28px;font-weight:800;color:'+pb[0]+';line-height:1">'+ps+'<span style="font-size:13px;opacity:.55;font-weight:600">/100</span></div>'
  +'<span class="tagp" style="background:'+pt.tb+';color:'+pt.tc+'">'+pt.tag+'</span>'
  +'<span class="mini">'+pb[2]+'</span></div>'
  +'<div class="track" style="height:8px;background:var(--line2);border-radius:5px;overflow:hidden;margin-top:7px"><i style="display:block;height:100%;width:'+Math.max(ps,2)+'%;background:'+pb[0]+'"></i></div>'
  +'<div class="mini" style="margin-top:5px">'+effP(name)+' org'+(effP(name)!=1?'s':'')+' (45%) · '+effT(name)+' themes (30%) · resilience (25%)</div></div>';
 h+='<div class="sec"><div class="t">Partners here</div>';
 if(dp.length){h+='<ul class="plist">';dp.forEach(p=>{h+='<li><b>'+p.name+'</b><br><span class="mini">'+(p.themes.length?p.themes.join(' · '):'no theme data in source')+'</span></li>';});h+='</ul>';}
 else h+='<div class="mini">No mapped partner found in this research pass. '+(v.aspirational?'Aspirational district — whitespace.':'')+'</div>';
 h+='</div>';
 if(v.themes.length){h+='<div class="sec"><div class="t">Themes active</div><div class="chips">'+v.themes.map(t=>'<span class="chip" style="border-left:3px solid '+(themePalette[t]||'#ccc')+'">'+t+'</span>').join('')+'</div></div>';}
 // block coverage (beta) — from the research pass only
 const bc=v.blockcov||[];
 if(bc.length){
  const srcs=[...new Set(bc.flatMap(b=>b.by))].sort();
  h+='<div class="sec"><details class="bcov"><summary><b>Block coverage</b> <span class="beta">beta</span> · <b>'+bc.length+'</b> block(s) with known partner presence</summary>';
  h+='<div class="mini" style="margin:5px 0 8px">Block-level presence known for <b>'+srcs.join(', ')+'</b> only, from the research pass — this is <b>known presence, not total coverage</b>.</div>';
  h+='<ul class="blist">';
  bc.forEach(b=>{h+='<li><b>'+b.name+'</b> '+b.by.map(s=>'<span class="tag">'+s+'</span>').join('')
    +(b.villages&&b.villages.length?'<br><span class="mini">villages: '+b.villages.join(', ')+'</span>':'')+'</li>';});
  h+='</ul></details></div>';
 }
 // SHG (Self Help Group) counts — district total + block-wise breakdown, DAY-NRLM MIS
 const shg=v.shg;
 if(shg&&shg.total){
  h+='<div class="sec"><details class="bcov"><summary><b>Self Help Groups (SHG)</b> · <b>'+shg.total.toLocaleString()+'</b> SHGs · '+shg.members.toLocaleString()+' members</summary>';
  h+='<div class="mini" style="margin:5px 0 8px">Source: DAY-NRLM public MIS (block-wise rollup) — New '+shg.new.toLocaleString()+' · Revived '+shg.revived.toLocaleString()+' · Pre-NRLM '+shg.prenrlm.toLocaleString()+'.</div>';
  h+='<ul class="blist">';
  shg.blocks.forEach(b=>{h+='<li><b>'+b.name+'</b> <span class="mini">'+b.total.toLocaleString()+' SHGs · '+b.members.toLocaleString()+' members</span></li>';});
  h+='</ul></details></div>';
 }
 // FPO (Farmer Producer Organisation) counts — district-level only, FPO Platform
 const fpo=v.fpo;
 if(fpo&&fpo.fpos){
  h+='<div class="sec"><div class="t">FPOs (Farmer Producer Organisations)</div><div class="blk">'
   +'<b>'+fpo.fpos.toLocaleString()+'</b> FPOs · '+fpo.farmers.toLocaleString()+' farmers <span class="mini">(FPO Platform)</span></div></div>';
 }
 // Anchor / multi-district orgs present here
 if(anc.orgs&&anc.orgs.length){
  h+='<div class="sec"><div class="t">Anchor orgs (multi-district ✳)</div><div class="chips">'
   +anc.orgs.map(o=>'<span class="chip" style="border-left:3px solid #0e8074">'+o+'</span>').join('')+'</div></div>';
 }
 // CSR flagship projects (GO CARE) — mapped subset, not total district spend
 const cf=v.csrFlagship||{count:0,projects:[]};
 if(cf.count){
  h+='<div class="sec"><details class="bcov"><summary><b>CSR flagship projects</b> ✳ · <b>'+cf.count+'</b> mapped project(s)'+(cf.amountLakh?' · ₹'+Math.round(cf.amountLakh).toLocaleString('en-IN')+' L':'')+'</summary>';
  h+='<div class="mini" style="margin:5px 0 8px">Geocoded flagship CSR projects on Odisha’s GO CARE portal — a curated subset, <b>not total district CSR</b> (district totals are login/captcha-gated).</div>';
  h+='<ul class="blist">';
  cf.projects.forEach(pr=>{h+='<li><b>'+pr.company+'</b>'+(pr.amountLakh?' <span class="mini">₹'+pr.amountLakh+' L</span>':'')+'<br><span class="mini">'+pr.project+(pr.location?' · '+pr.location:'')+'</span></li>';});
  h+='</ul></details></div>';
 }
 // Real CSR spend, by development domain (GO CARE "Dynamic CSR Report", district total)
 const csr=v.csr||{total:0,byDomain:{}};
 if(csr.total){
  const doms=Object.entries(csr.byDomain).sort((a,b)=>b[1]-a[1]);
  const dmx=Math.max(...doms.map(e=>e[1]),1);
  h+='<div class="sec"><div class="t">CSR spend by domain (real ₹, FY15→FY25)</div>'
   +'<div class="kv" style="margin:0 0 8px"><div><div class="k">District total</div><div class="v">'+fmtCr(csr.total)+'</div></div>'
   +'<div><div class="k">Share of state</div><div class="v">'+(maxCsrTotal?(csr.total/CANON.reduce((s,d)=>s+csrTotalN(d),0)*100).toFixed(1):'0')+'%</div></div></div>';
  doms.forEach(([dm,amt])=>{h+='<div style="display:grid;grid-template-columns:1fr 60px;gap:8px;align-items:center;padding:2px 0" title="'+dm+'">'
   +'<span class="mini">'+shortCsr(dm)+'</span>'
   +'<span class="num mini">'+fmtCr(amt)+'</span></div>'
   +'<span class="track" style="display:block;height:6px;background:var(--line2);border-radius:4px;overflow:hidden;margin-bottom:4px"><i style="display:block;height:100%;width:'+(amt/dmx*100)+'%;background:#dd7f21"></i></span>';});
  h+='</div>';
 }
 // Funders / philanthropies mapped to this district + CSR companies seen here
 const dFund=FUNDERS.filter(f=>(f.districts||[]).includes(name));
 const dComp=[...new Set((cf.projects||[]).map(p=>p.company))];
 if(dFund.length||dComp.length){
  h+='<div class="sec"><div class="t">Funders &amp; CSR active here</div>';
  if(dFund.length){
   h+='<div class="mini" style="margin-bottom:4px">Funders / philanthropies with a mapped presence in '+name+':</div><ul class="blist">';
   dFund.forEach(f=>{h+='<li><b>'+f.name+'</b>'+(f.confidence?' <span class="mini">('+f.confidence+' conf.)</span>':'')+(f.source?' <a href="'+f.source+'" target="_blank" rel="noopener" class="mini">src</a>':'')+'<br><span class="mini">'+(f.supports||'')+'</span></li>';});
   h+='</ul>';
  }
  if(dComp.length){
   h+='<div class="mini" style="margin:6px 0 4px">CSR companies with flagship projects here ✳ <span class="mini">(GO CARE geocoded subset, not all CSR)</span>:</div><div class="chips">'
    +dComp.map(c=>'<span class="chip" style="border-left:3px solid #d1702f">'+c+'</span>').join('')+'</div>';
  }
  h+='</div>';
 }
 // Catalytic Unlock: nature/commons landscape read (indicative strategy)
 const ct=catOf(name), ls=landById[ct.landscape]||{}, ti=CAT_TIERS[ct.tier]||{};
 if(ct.landscape){
  h+='<div class="sec"><div class="t">Catalytic Unlock ✳ <span class="mini" style="font-weight:400">(indicative)</span></div>'
   +'<div class="blk" style="border-left:3px solid '+(ls.color||'#ccc')+';padding-left:8px">'
   +'<b>'+(ls.name||'')+'</b><br>'
   +'<span class="chip" style="background:'+(ti.color||'#666')+';color:#fff;border:0">'+(ti.label||'')+'</span> '
   +'<span class="mini">leverage read '+catLeverage(name)+'/100</span>'
   +(ti.strategy?'<div class="mini" style="margin-top:5px">'+ti.strategy+'</div>':'')
   +(ct.note?'<div class="mini" style="margin-top:4px"><b>Here:</b> '+ct.note+'</div>':'')
   +'</div></div>';
 }
 // DMF trend sparkline (year-wise, real data)
 const yr=[...YEARS].reverse(); const vals=yr.map(y=>v.dmf[y]||0); const mx=Math.max(...vals,1);
 h+='<div class="sec"><div class="t">DMF collection trend (₹ Cr / FY)</div><div class="spark">';
 vals.forEach(val=>{h+='<div class="bar" style="height:'+(val/mx*100)+'%" title="'+fmtDmf(Math.round(val))+'"></div>';});
 h+='</div><div class="sparkx"><span>'+yr[0].slice(2,4)+'</span><span>'+yr[yr.length-1].slice(2,4)+'</span></div></div>';
 body.innerHTML=h;
 body.scrollIntoView&&window.matchMedia('(max-width:960px)').matches&&body.scrollIntoView({behavior:'smooth',block:'nearest'});
}

/* ---------- matrix ---------- */
const THSHORT={'Health & Nutrition':'Health','Women & Gender':'Women','Climate Action':'Climate','Livelihoods & Rural Dev':'Livelihoods','Natural Resource Mgmt':'NRM','Water & Sanitation':'WASH','Skill Development':'Skills','Clean Energy':'Energy','Child Protection':'Child Ptn'};
const shortT=t=>THSHORT[t]||t;
function buildMatrix(){
 const src=PARTNERS.map(p=>({name:p.name,themes:p.themes,ind:false}));
 const ind=INDICATIVE.map(o=>({name:o.name,themes:o.themes||[],ind:true}));
 const rows=src.concat(ind).sort((a,b)=>b.themes.length-a.themes.length);
 let h='<table><thead><tr><th>Organisation</th>';
 THEMES.forEach(t=>h+='<th class="rot" title="'+t+'"><div>'+shortT(t)+'</div></th>');
 h+='</tr></thead><tbody>';
 rows.forEach(p=>{h+='<tr><td class="name"'+(p.ind?' style="color:#b45309"':'')+'>'+p.name+(p.ind?' <span style="color:#b45309" title="indicative org, keyword-mapped themes">✳</span>':'')+'</td>';
   THEMES.forEach(t=>{const on=p.themes.includes(t);
     let bg='#fff',dot='';
     if(on){if(p.ind){bg='rgba(180,83,9,0.55)';}else{const shade=0.35+0.65*(themeFreq[t]/maxTF);bg='rgba(13,110,140,'+shade.toFixed(2)+')';}dot='●';}
     h+='<td><div class="cell" style="background:'+bg+'">'+dot+'</div></td>';});
   h+='</tr>';});
 h+='<tr><td class="name" style="font-weight:700">Source orgs / theme</td>';
 THEMES.forEach(t=>h+='<td class="tot">'+themeFreq[t]+'</td>');
 h+='</tbody></table>';
 document.getElementById('matrix').innerHTML=h;
}

/* ---------- partner directory ---------- */
let dirSort={k:'nd',asc:false};
function buildDir(){
 const box=document.getElementById('dirtbl');
 const cols=[['name','Organisation'],['districts','Districts'],['themes','Themes / focus'],['nd','#Dist']];
 let rows=PARTNERS.map(p=>({name:p.name,districts:p.districts,themes:p.themes,themesN:p.themes.length,nd:p.districts.length,ind:false,src:''}));
 INDICATIVE.forEach(o=>rows.push({name:o.name,districts:o.districts||[],themes:o.themes||[],themesN:(o.themes||[]).length,nd:(o.districts||[]).length,ind:true,src:o.source||'',focus:o.focus||''}));
 rows.sort((a,b)=>{let k=dirSort.k,x,y;
   if(k==='themes'){x=a.themesN;y=b.themesN;} else if(k==='districts'){x=a.nd;y=b.nd;} else {x=a[k];y=b[k];}
   if(typeof x==='string')return dirSort.asc?x.localeCompare(y):y.localeCompare(x);return dirSort.asc?x-y:y-x;});
 let h='<table><thead><tr>';cols.forEach(c=>h+='<th data-k="'+c[0]+'">'+c[1]+(dirSort.k===c[0]?(dirSort.asc?' ▲':' ▼'):'')+'</th>');h+='</tr></thead><tbody>';
 rows.forEach(p=>{
   const dcell=p.districts.length?p.districts.map(d=>'<span class="tag pill" data-d="'+d+'">'+d+'</span>').join(''):'<span class="tag">Statewide</span>';
   const tcell=p.themes.length?p.themes.map(t=>'<span class="tag" style="border-left:3px solid '+(themePalette[t]||'#ccc')+'">'+t+'</span>').join(''):'<span class="mini">'+(p.ind&&p.focus?p.focus:'no theme data in source')+'</span>';
   const nm='<b'+(p.ind?' style="color:#b45309"':'')+'>'+p.name+'</b>'+(p.ind?' <span style="color:#b45309" title="indicative org">✳</span>'+(p.src?' <a href="'+p.src+'" target="_blank" rel="noopener" class="mini">src</a>':''):'');
   h+='<tr><td>'+nm+'</td><td>'+dcell+'</td><td>'+tcell+'</td><td class="num">'+p.nd+'</td></tr>';});
 h+='</tbody></table>'; box.innerHTML=h;
 box.querySelectorAll('th').forEach(th=>th.onclick=()=>{const k=th.dataset.k;dirSort.asc=dirSort.k===k?!dirSort.asc:false;dirSort.k=k;buildDir();});
 box.querySelectorAll('.pill').forEach(s=>s.onclick=()=>{selectDist(s.dataset.d);document.getElementById('mapbox').scrollIntoView({behavior:'smooth',block:'center'});});
}

/* ---------- district table ---------- */
let disSort={k:'partners',asc:false};
function buildDisTbl(){
 const box=document.getElementById('distbl');
 let rows=CANON.map(d=>({d,partners:effP(d),themes:effT(d),
   asp:D[d].aspirational?1:0,anchor:(D[d].anchor||{}).present?1:0,csr:csrN(d),csrcr:csrTotalN(d),
   shg:shgN(d),fpo:fpoN(d),plist:effPList(d)}));
 rows.sort((a,b)=>{let x=a[disSort.k],y=b[disSort.k];if(typeof x==='string')return disSort.asc?x.localeCompare(y):y.localeCompare(x);return disSort.asc?x-y:y-x;});
 const cols=[['d','District'],['partners','Partners'],['themes','Themes'],['asp','Asp.'],['anchor','Anchor'],['csr','CSR ✳'],['csrcr','CSR ₹Cr'],['shg','SHGs'],['fpo','FPOs']];
 let h='<table><thead><tr>';cols.forEach(c=>h+='<th data-k="'+c[0]+'"'+(c[0]!=='d'?' class="num"':'')+'>'+c[1]+(disSort.k===c[0]?(disSort.asc?' ▲':' ▼'):'')+'</th>');h+='<th>Who</th></tr></thead><tbody>';
 rows.forEach(r=>{const bg=r.partners===0?'background:#fdf3ee':'';
   h+='<tr style="'+bg+'"><td><span class="dot" style="background:'+seqColor(r.partners,maxP)+'"></span><b class="pill" data-d="'+r.d+'">'+r.d+'</b></td>'
    +'<td class="num">'+r.partners+'</td><td class="num">'+r.themes+'</td>'
    +'<td class="num">'+(r.asp?'<span style="color:#c2410c">●</span>':'–')+'</td>'
    +'<td class="num">'+(r.anchor?'<span style="color:#0e8074" title="CYSD present">●</span>':'–')+'</td>'
    +'<td class="num">'+(r.csr||'–')+'</td>'
    +'<td class="num">'+(r.csrcr?r.csrcr.toLocaleString('en-IN',{maximumFractionDigits:0}):'–')+'</td>'
    +'<td class="num">'+r.shg.toLocaleString()+'</td>'
    +'<td class="num">'+r.fpo.toLocaleString()+'</td>'
    +'<td class="mini">'+(r.plist.join(', ')||'—')+'</td></tr>';});
 h+='</tbody></table>'; box.innerHTML=h;
 box.querySelectorAll('th').forEach(th=>th.onclick=()=>{const k=th.dataset.k;disSort.asc=disSort.k===k?!disSort.asc:(k==='d');disSort.k=k;buildDisTbl();});
 box.querySelectorAll('.pill').forEach(s=>s.onclick=()=>{selectDist(s.dataset.d);document.getElementById('mapbox').scrollIntoView({behavior:'smooth',block:'center'});});
}

function updateFoot(){const wl=whiteList();document.getElementById('foot').innerHTML='Fully self-contained (offline) · '+PARTNERS.length+' researched partners across '+coveredList().length+'/'+NDIST+' districts · Whitespace: <b>'+(wl.length?wl.join(', '):'none')+'</b>.<br>MIT licensed · source &amp; issues: <a href="https://github.com/Ashwask/odisha-landscape" target="_blank" rel="noopener">github.com/Ashwask/odisha-landscape</a>';}

/* ---------- ecosystem + place health ---------- */
const BAND={strong:['#2b8a3e','#e7f3ea','Strong'],mod:['#b45309','#fdf0e2','Moderate'],weak:['#c2410c','#fdece3','Weak']};
function band(s){return s>=75?'strong':s>=50?'mod':'weak';}

function buildHealth(){
 const cov=coveredList();
 const asp=CANON.filter(d=>D[d].aspirational);
 const aspCov=asp.filter(d=>effP(d)>0);
 const single=CANON.filter(d=>effP(d)===1);
 const wht=whiteList();
 const tf={};THEMES.forEach(t=>tf[t]=0);PARTNERS.forEach(p=>p.themes.forEach(t=>{if(t in tf)tf[t]++;}));
 if(INCLUDE_EXT)INDICATIVE.forEach(o=>(o.themes||[]).forEach(t=>{if(t in tf)tf[t]++;}));
 const fragile=THEMES.filter(t=>tf[t]>0&&tf[t]<=2);
 const hubs=CANON.filter(d=>effP(d)>=3);
 const avgP=cov.length?cov.reduce((s,d)=>s+effP(d),0)/cov.length:0;
 const lbl='partner';
 // SHG (DAY-NRLM) reach — share of the state's SHG member base sitting in partner-covered districts
 const shgTot=CANON.reduce((s,d)=>s+((D[d].shg||{}).members||0),0);
 const shgMemCov=CANON.reduce((s,d)=>s+(effP(d)?((D[d].shg||{}).members||0):0),0);
 const shgCov=shgTot?shgMemCov/shgTot*100:0;
 // Resource alignment — share of the state's place-based public money (DMF) sitting in
 // partner-covered districts. Odisha lacks district-level CSR (blocked), so DMF stands in
 // for the "do resources track effort?" resource-alignment dimension.
 const dmfCov=CANON.reduce((s,d)=>s+(effP(d)?(DMF_TOTAL[d]||0):0),0);
 const resAlign=stateDMF?dmfCov/stateDMF*100:0;
 const dims=[
  {n:'Geographic coverage',v:cov.length+'/'+NDIST,s:cov.length/NDIST*100,d:Math.round(cov.length/NDIST*100)+'% of districts have ≥1 '+lbl+(INCLUDE_EXT?' (incl. ✳)':' (research pass)')+'.'},
  {n:'Aspirational reach',v:aspCov.length+'/'+asp.length,s:asp.length?aspCov.length/asp.length*100:0,d:(asp.length-aspCov.length)+' NITI Aayog aspirational districts still unserved: '+(asp.filter(d=>!effP(d)).join(', ')||'none')+'.'},
  {n:'Resilience',v:(NDIST-wht.length-single.length)+'/'+NDIST,s:(NDIST-wht.length-single.length)/NDIST*100,d:single.length+' single-'+lbl+' + '+wht.length+' zero-'+lbl+' districts = key-person risk.'},
  {n:'Thematic balance',v:(THEMES.length-fragile.length)+'/'+THEMES.length,s:(THEMES.length-fragile.length)/THEMES.length*100,d:'Thin themes (≤2 '+lbl+'s): '+(fragile.join(', ')||'none')+'.'},
  {n:'Network depth',v:hubs.length+' hubs',s:hubs.length/NDIST*100,d:hubs.length+' districts with ≥3 '+lbl+'s; avg '+avgP.toFixed(1)+' where present.'},
  {n:'SHG reach',v:Math.round(shgCov)+'% of SHG base',s:shgCov,d:Math.round(shgCov)+'% of the '+(shgTot/1e6).toFixed(1)+'M SHG members statewide (DAY-NRLM) sit in districts with a mapped '+lbl+' — how much existing grassroots infrastructure the mapped ecosystem already touches.'},
  {n:'Resource alignment',v:Math.round(resAlign)+'% of DMF',s:resAlign,d:Math.round(resAlign)+'% of the state’s '+fmtDmf(Math.round(stateDMF))+' DMF pool sits in districts with a mapped '+lbl+' — how well place-based public money and partner effort co-locate (Odisha has no open district CSR).'}
 ];
 // 7 dimensions (weights sum to 1). Resource alignment uses DMF, not CSR, since district
 // CSR is login/captcha-gated for Odisha (see Sources) — the statewide CSR trend is shown separately.
 const W=[0.14,0.20,0.17,0.13,0.12,0.12,0.12];
 const idx=Math.round(dims.reduce((s,dm,i)=>s+dm.s*W[i],0));
 const b=BAND[band(idx)];
 document.getElementById('hindex').innerHTML=
  '<div class="big">'+idx+'<small>/100</small></div><div class="lbl">Ecosystem Health Index (research pass)</div>'
  +'<span class="band" style="background:'+b[1]+';color:'+b[0]+'">'+b[2]+'</span>'
  +'<div class="desc">'+cov.length+'/'+NDIST+' districts covered, '+aspCov.length+'/'+asp.length+' aspirational districts reached, '+hubs.length+' hubs — against a 46-org research pass that is sourced but not independently field-verified. Read it as a strong first read, not a verdict on Odisha\'s ecosystem.</div>';
 document.getElementById('hcards').innerHTML=dims.map(dm=>{const bb=BAND[band(dm.s)];
  return '<div class="hc"><span class="band" style="background:'+bb[1]+';color:'+bb[0]+'">'+bb[2]+'</span>'
   +'<div class="m">'+dm.v+'</div><div class="nm">'+dm.n+'</div>'
   +'<div class="bar"><i style="width:'+Math.round(dm.s)+'%;background:'+bb[0]+'"></i></div>'
   +'<div class="d">'+dm.d+'</div></div>';}).join('');
}

function placeScore(d){const p=effP(d),t=effT(d);
 const sp=Math.min(p/3,1)*45, st=Math.min(t/10,1)*30, sr=(p>=2?1:p===1?.4:0)*25;
 return Math.round(sp+st+sr);}
function placeTag(d){const p=effP(d),s=placeScore(d),asp=D[d].aspirational;
 if(p===0&&asp)return{tag:'Whitespace',tc:'#c2410c',tb:'#fdece3',need:0};
 if(p===0)return{tag:'Uncovered',tc:'#b45309',tb:'#fdf0e2',need:1};
 if(asp&&s<55)return{tag:'Priority',tc:'#b45309',tb:'#fdf0e2',need:2};
 if(p===1)return{tag:'Fragile',tc:'#b45309',tb:'#fdf0e2',need:3};
 return{tag:'Served',tc:'#2b8a3e',tb:'#e7f3ea',need:4};}
function buildPlaceHealth(){
 const rows=CANON.map(d=>{const s=placeScore(d),asp=D[d].aspirational,pt=placeTag(d);
  return {d,s,asp,tag:pt.tag,tc:pt.tc,tb:pt.tb,need:pt.need};});
 rows.sort((a,b)=>a.need-b.need||a.s-b.s);
 document.getElementById('placehealth').innerHTML=rows.map(r=>{const bc=BAND[band(r.s)][0];
  return '<div class="phrow"><span class="pn" data-d="'+r.d+'">'
   +(r.asp?'<span class="dot" style="background:#c2410c" title="Aspirational"></span>':'<span class="dot" style="background:#cdd7e6"></span>')+r.d+'</span>'
   +'<span class="track"><i style="width:'+Math.max(r.s,2)+'%;background:'+bc+'"></i></span>'
   +'<span class="right"><span class="tagp" style="background:'+r.tb+';color:'+r.tc+'">'+r.tag+'</span><span class="sc">'+r.s+'</span></span></div>';}).join('');
 document.querySelectorAll('#placehealth .pn').forEach(s=>s.onclick=()=>{selectDist(s.dataset.d);document.getElementById('mapbox').scrollIntoView({behavior:'smooth',block:'center'});});
}

function buildGovt(){
 const dmf=Object.entries(DMF_TOTAL).sort((a,b)=>b[1]-a[1]);
 let h='<table><thead><tr><th>District</th><th class="num">DMF ₹Cr (FY16→FY26)</th><th>Share of state DMF</th></tr></thead><tbody>';
 dmf.forEach(([d,v])=>{h+='<tr><td><span class="dot" style="background:#8a4fbf"></span><b class="pill" data-d="'+d+'">'+d+'</b></td><td class="num">'+fmtDmf(Math.round(v))+'</td><td><span class="track" style="display:inline-block;width:60%;height:8px;background:#efe8f6;border-radius:5px;overflow:hidden;vertical-align:middle"><i style="display:block;height:100%;width:'+(v/maxDMF*100)+'%;background:#8a4fbf"></i></span> <span class="mini">'+(stateDMF?(v/stateDMF*100).toFixed(1):'0')+'%</span></td></tr>';});
 h+='</tbody></table>'; const box=document.getElementById('govtdmf'); box.innerHTML=h;
 box.querySelectorAll('.pill').forEach(s=>s.onclick=()=>{selectDist(s.dataset.d);document.getElementById('mapbox').scrollIntoView({behavior:'smooth',block:'center'});});
}

/* ---------- CSR state panel: trend & sectors / by district / by domain ---------- */
let csrTab='trend';
const CSR_TABS=[['trend','Trend (₹/yr)'],['district','By district'],['domain','By domain']];
const csrTabsBox=document.getElementById('csrTabs');
CSR_TABS.forEach(([k,label])=>{const b=el('button',k===csrTab?'on':'',label);b.onclick=()=>{csrTab=k;buildCsrTabs();buildCsrState();};csrTabsBox.appendChild(b);});
function buildCsrTabs(){[...csrTabsBox.children].forEach((b,i)=>b.classList.toggle('on',CSR_TABS[i][0]===csrTab));
 document.getElementById('csrFyRow').style.display=(csrTab==='district'||csrTab==='domain')?'':'none';}

/* FY filter for the "By district" / "By domain" tabs (real ₹ data only -- CSRD.years) */
let curCsrFy='__all__';
const csrFySel=document.getElementById('csrFySel');
csrFySel.innerHTML='<option value="__all__">All years (FY'+CSRD.years[0].slice(2)+'→FY'+CSRD.years[CSRD.years.length-1].slice(2)+')</option>'
 +CSRD.years.map(y=>'<option value="'+y+'">FY'+y+'</option>').join('');
csrFySel.onchange=()=>{curCsrFy=csrFySel.value;buildCsrState();};
const fyLabel=()=>curCsrFy==='__all__'?'FY2014-15→FY2024-25':'FY'+curCsrFy;

function renderCsrTrend(){
 const yt=CSR.yearTotals||{}; let yrs=Object.keys(yt).sort();
 // CSR filings lag ~6-18 months, so the most recent FY(s) are still coming in. Trim any
 // trailing year whose spend cliffs to <50% of the prior year, so a partial year doesn't
 // read as a real collapse. (Was showing FY25-26 ₹78 Cr / FY26-27 ₹2 Cr next to ~₹450 Cr years.)
 while(yrs.length>2){const n=yrs.length,last=yt[yrs[n-1]].amountCr||0,prev=yt[yrs[n-2]].amountCr||0;if(prev>0&&last<prev*0.5)yrs.pop();else break;}
 const vals=yrs.map(y=>yt[y].amountCr||0); const mx=Math.max(...vals,1);
 const lastY=yrs[yrs.length-1]||'';
 let h='<div class="cardpad"><div class="mini" style="margin-bottom:6px">Statewide CSR filed on Odisha’s GO CARE portal (MCA-fed), ₹ crore per FY, shown through FY'+lastY.slice(2)+' (later years omitted while filings are still coming in). For the real spend split by development sector, see the <b>By domain</b> tab; for per-district ₹, see <b>By district</b>.</div>';
 h+='<div class="spark" style="height:70px">';
 yrs.forEach((y,i)=>{h+='<div class="bar" style="height:'+(vals[i]/mx*100)+'%;background:#d1702f" title="'+y+': ₹'+vals[i]+' Cr"></div>';});
 h+='</div><div class="sparkx"><span>'+(yrs[0]||'')+'</span><span>'+lastY+'</span></div>';
 h+='</div>';
 return h;
}
function renderCsrByDistrict(){
 const amt=d=>curCsrFy==='__all__'?csrTotalN(d):((D[d].csr.byYear||{})[curCsrFy]||0);
 const rows=CANON.map(d=>[d,amt(d)]).sort((a,b)=>b[1]-a[1]);
 const stateTot=rows.reduce((s,r)=>s+r[1],0);
 const uncl=curCsrFy==='__all__'?CSRD.unclassified.total:(CSRD.unclassified.byYear[curCsrFy]||0);
 let h='<div class="cardpad"><div class="mini" style="margin-bottom:8px">Real CSR spend per district (GO CARE "Dynamic CSR Report"), all domains, '+fyLabel()+'. Click a district to open its detail panel; use the map\'s "CSR spend" lens to see this geographically.</div>';
 h+='<div class="tbl"><table><thead><tr><th>District</th><th class="num">CSR ₹Cr ('+fyLabel()+')</th><th>Share of mapped state total</th></tr></thead><tbody>';
 rows.forEach(([d,v])=>{h+='<tr><td><span class="dot" style="background:#dd7f21"></span><b class="pill" data-d="'+d+'">'+d+'</b></td><td class="num">'+fmtCr(v)+'</td>'
  +'<td><span class="track" style="display:inline-block;width:60%;height:8px;background:#fbead6;border-radius:5px;overflow:hidden;vertical-align:middle"><i style="display:block;height:100%;width:'+(stateTot?v/stateTot*100:0)+'%;background:#dd7f21"></i></span> <span class="mini">'+(stateTot?(v/stateTot*100).toFixed(1):'0')+'%</span></td></tr>';});
 h+='</tbody></table></div>';
 h+='<div class="mini" style="margin-top:8px">+ '+fmtCr(uncl)+' filed statewide under "District Not Classified Elsewhere" for '+fyLabel()+' — not attributable to one district, so excluded here (included in the "By domain" tab\'s totals).</div></div>';
 return h;
}
function renderCsrByDomain(){
 const amt=dm=>curCsrFy==='__all__'?(CSRD.byDomain[dm]||0):((CSRD.byYear[curCsrFy]||{})[dm]||0);
 const ent=CSRD.domains.map(dm=>[dm,amt(dm)]).sort((a,b)=>b[1]-a[1]);
 const dmx=Math.max(...ent.map(e=>e[1]),1);
 const mappedTot=ent.reduce((s,e)=>s+e[1],0);
 const uncl=curCsrFy==='__all__'?CSRD.unclassified.total:(CSRD.unclassified.byYear[curCsrFy]||0);
 let h='<div class="cardpad"><div class="mini" style="margin-bottom:8px">Real CSR spend by development domain, statewide, '+fyLabel()+' — includes the "District Not Classified Elsewhere" slice (mostly statewide/multi-district projects), so totals here run higher than summing the "By district" tab.</div>';
 ent.forEach(([dm,v])=>{h+='<div style="display:grid;grid-template-columns:190px 1fr 72px;gap:8px;align-items:center;padding:4px 0" title="'+dm+'"><span class="mini">'+shortCsr(dm)+'</span><span class="track" style="height:9px;background:var(--line2);border-radius:5px;overflow:hidden"><i style="display:block;height:100%;width:'+(v/dmx*100)+'%;background:#dd7f21"></i></span><span class="num mini">'+fmtCr(v)+'</span></div>';});
 h+='<div class="mini" style="margin-top:10px">Total mapped ('+fyLabel()+'): '+fmtCr(mappedTot)+' · of which '+fmtCr(uncl)+' (~'+(mappedTot?(uncl/mappedTot*100).toFixed(0):'0')+'%) is statewide/unclassified. Use the map\'s "CSR spend" lens + domain filter to see any one domain by district (all-years only).</div></div>';
 return h;
}
function buildCsrState(){
 const box=document.getElementById('csrstate');
 box.innerHTML = csrTab==='district' ? renderCsrByDistrict() : csrTab==='domain' ? renderCsrByDomain() : renderCsrTrend();
 box.querySelectorAll('.pill').forEach(s=>s.onclick=()=>{selectDist(s.dataset.d);document.getElementById('mapbox').scrollIntoView({behavior:'smooth',block:'center'});});
}
/* ---------- funders table ---------- */
const CONFDOT={high:'#2b8a3e',med:'#b45309',low:'#c2410c'};
function buildFunders(){
 let h='<table><thead><tr><th>Funder</th><th>Supports in Odisha · domains · districts</th><th>Implementing org(s)</th><th>Conf.</th></tr></thead><tbody>';
 FUNDERS.forEach(f=>{
  const orgs=(f.orgs&&f.orgs.length)?f.orgs.map(o=>'<span class="tag" style="border-left:3px solid #b45309">'+o+'</span>').join(''):'<span class="mini">direct implementer / not public</span>';
  const doms=(f.domains&&f.domains.length)?'<div style="margin-top:4px">'+f.domains.map(t=>'<span class="tag" style="border-left:3px solid '+(themePalette[t]||'#ccc')+'">'+(THSHORT[t]||t)+'</span>').join('')+'</div>':'';
  const dists=(f.districts&&f.districts.length)?'<div style="margin-top:3px">'+f.districts.map(d=>'<span class="tag pill" data-d="'+d+'">'+d+'</span>').join('')+'</div>':'<div class="mini" style="margin-top:3px">statewide / district not specified</div>';
  const amt=(f.amt||f.amtNote)?'<div class="mini">'+[f.amt,f.amtNote].filter(Boolean).join(' · ')+'</div>':'';
  const cd=CONFDOT[f.confidence]||'#888';
  h+='<tr><td><b>'+(f.source?'<a href="'+f.source+'" target="_blank" rel="noopener">'+f.name+'</a>':f.name)+'</b></td><td>'+f.supports+doms+dists+amt+'</td><td>'+orgs+'</td><td class="mini"><span class="dot" style="background:'+cd+'"></span>'+(f.confidence||'')+'</td></tr>';
 });
 h+='</tbody></table>';
 document.getElementById('funders').innerHTML=h;
 document.querySelectorAll('#funders .pill').forEach(s=>s.onclick=()=>{const b=document.querySelector('#tabbar button[data-view=main]');if(b)b.click();selectDist(s.dataset.d);document.getElementById('mapbox').scrollIntoView({behavior:'smooth',block:'center'});});
}
/* ---------- Catalytic Unlock: nature/commons landscapes + top 10 projects ---------- */
function buildCatalytic(){
 const intro=document.getElementById('catintro');
 if(intro)intro.innerHTML=(CAT.meta&&CAT.meta.framing?CAT.meta.framing+' ':'')
  +'<b>Indicative strategy ✳</b>, not fetched data: this is the project-level subset of the unlocks above. Districts are grouped into six nature/commons landscapes, each with a catalytic tier; the leverage read per district is computed from the real DMF, CSR and partner-capacity fields (nature/commons carries the highest weight). On the Ecosystem landscape tab, the "Catalytic Unlock ✳" map lens paints these landscapes; click a district chip to jump there.';
 // landscape cards: money + capacity readout per landscape, from the real data
 let h='';
 CAT_LAND.forEach(l=>{
  let dmf=0,csr=0,pn=0; l.districts.forEach(d=>{dmf+=DMF_TOTAL[d]||0;csr+=csrTotalN(d);pn+=(D[d].partners||[]).length;});
  const tiers=[...new Set(l.districts.map(d=>catOf(d).tier))].map(t=>(CAT_TIERS[t]||{}).label).filter(Boolean);
  h+='<div style="border-left:4px solid '+l.color+';padding:8px 0 10px 12px;margin-bottom:10px">'
   +'<div style="font-weight:700;color:var(--ink)">'+l.name+' <span class="mini" style="font-weight:400">'+l.districts.length+' districts · '+tiers.join(' / ')+'</span></div>'
   +'<div class="mini" style="margin:3px 0 5px">'+l.thesis+'</div>'
   +'<div class="mini"><b>Money in place:</b> '+fmtDmf(Math.round(dmf))+' DMF · '+fmtCr(csr)+' CSR (FY15→FY25) · <b>capacity:</b> '+pn+' partner-links</div>'
   +'<div style="margin-top:4px">'+l.districts.map(d=>'<span class="tag pill" data-d="'+d+'">'+d+'</span>').join('')+'</div>'
   +'<div class="mini" style="margin-top:4px"><b>Commons at stake:</b> '+(l.commons||[]).join(' · ')+'</div>'
   +'</div>';
 });
 const cl=document.getElementById('catland'); if(cl){cl.innerHTML=h;
  cl.querySelectorAll('.pill').forEach(s=>s.onclick=()=>{const b=document.querySelector('#tabbar button[data-view=main]');if(b)b.click();curLens='catalytic';paint();selectDist(s.dataset.d);document.getElementById('mapbox').scrollIntoView({behavior:'smooth',block:'center'});});}
 // top 10 projects table
 let p='<div class="mini" style="margin-bottom:6px"><b>Top 10 catalytic projects</b> ✳ : a cross-domain, cross-landscape subset of the unlock/unblock. ₹ figures are indicative catalytic sizing (design proposal), not committed pipelines.</div>';
 p+='<table><thead><tr><th>#</th><th>Project · domain</th><th>Landscape / geography</th><th>Subset of unlock</th><th>Catalytic instrument</th><th class="num">₹Cr</th><th>Unblocks</th></tr></thead><tbody>';
 CAT_PROJ.forEach(pr=>{
  const geos=(pr.geographies||[]).map(g=>CANON.includes(g)?'<span class="tag pill" data-d="'+g+'">'+g+'</span>':'<span class="tag">'+g+'</span>').join('');
  const lname=(landById[pr.landscape]||{}).name||(pr.landscape==='all'?'Statewide':pr.landscape);
  p+='<tr><td class="num"><b>'+pr.rank+'</b></td>'
   +'<td><b>'+pr.name+'</b><div class="mini">'+pr.domain+'</div>'+(pr.commons?'<div class="mini"><b>Commons:</b> '+pr.commons.join(' · ')+'</div>':'')+'</td>'
   +'<td class="mini"><b>'+lname+'</b><div style="margin-top:3px">'+geos+'</div></td>'
   +'<td class="mini">'+pr.unlock+'</td>'
   +'<td class="mini">'+pr.instrument+'</td>'
   +'<td class="num">'+(pr.catalyticCr||'–')+'</td>'
   +'<td class="mini">'+(pr.mobilises||'')+'</td></tr>';
 });
 const totCat=CAT_PROJ.reduce((s,pr)=>s+(pr.catalyticCr||0),0);
 p+='<tr><td></td><td class="mini" colspan="4" style="font-weight:700">Total indicative catalytic capital</td><td class="num" style="font-weight:700">'+totCat+'</td><td class="mini">unblocks far larger committed DMF + CSR + scheme pools</td></tr>';
 p+='</tbody></table>';
 const cp=document.getElementById('catproj'); if(cp){cp.innerHTML=p;
  cp.querySelectorAll('.pill').forEach(s=>s.onclick=()=>{const b=document.querySelector('#tabbar button[data-view=main]');if(b)b.click();curLens='catalytic';paint();selectDist(s.dataset.d);document.getElementById('mapbox').scrollIntoView({behavior:'smooth',block:'center'});});}
}
/* ---------- government schemes table ---------- */
function buildSchemes(){
 const items=(SCHEMES.items||[]).slice().sort((a,b)=>b.outlayCr-a.outlayCr);
 let h='<table><thead><tr><th>Scheme</th><th>Theme</th><th class="num">Outlay ₹Cr</th><th>Level</th></tr></thead><tbody>';
 const LVL={'central':'#1f5a8f','state':'#0e8074','central-state':'#7c3a86'};
 items.forEach(s=>{const amt=s.outlayCr?s.outlayCr.toLocaleString('en-IN'):'–';
   h+='<tr><td><b>'+(s.source?'<a href="'+s.source+'" target="_blank" rel="noopener">'+s.name+'</a>':s.name)+'</b>'+(s.note?'<div class="mini">'+s.note+'</div>':'')+'</td><td><span class="tag">'+s.theme+'</span></td><td class="num">'+amt+'</td><td class="mini"><span class="dot" style="background:'+(LVL[s.level]||'#888')+'"></span>'+s.level+'</td></tr>';});
 h+='</tbody></table>';
 document.getElementById('schemes').innerHTML=h;
}

/* ---------- Odisha Vision 2036 tab ---------- */
let visionBuilt=false;
function buildVision(){
 if(visionBuilt)return; visionBuilt=true;
 const srcLinks=(VISION.sources||[]).map(s=>'<a href="'+s.url+'" target="_blank" rel="noopener">'+s.label+'</a>').join(' · ');
 let h='<div class="vhero"><div class="big">'+(VISION.headline||'')+'</div>'
  +'<div class="meta">'+(VISION.launch||'')+'</div>'
  +(srcLinks?'<div class="meta">Sources: '+srcLinks+'</div>':'')+'</div>';
 h+='<p class="section-sub" style="margin-top:16px">Odisha turns 100 as a state in 2036. The government\'s official Vision 2036 (with a 2047 horizon) sets targets across the economy, infrastructure, agriculture, social sectors, women\'s empowerment and governance — shown here as the state\'s stated priorities and commitments, mapped to the same themes this dashboard tracks. These are government targets, not audited outcomes.</p>';
 h+='<div class="vgrid">';
 (VISION.pillars||[]).forEach(p=>{
  const col=themePalette[p.theme]||'#0d6e8c';
  h+='<div class="vcard"><div class="vh"><span class="vth" style="background:'+col+'"></span>'+p.name+'</div>';
  if(p.targets&&p.targets.length){h+='<ul class="vt">'+p.targets.map(t=>'<li>'+t+'</li>').join('')+'</ul>';}
  if(p.programs&&p.programs.length){h+='<div class="vp">'+p.programs.map(pr=>'<span class="tag">'+pr+'</span>').join('')+'</div>';}
  if(p.theme){h+='<div class="mini" style="margin-top:9px">Maps to: <span class="tag" style="border-left:3px solid '+col+'">'+p.theme+'</span></div>';}
  h+='</div>';
 });
 h+='</div>';
 h+='<p class="vnote">'+(VISION._note||'')+'</p>';
 document.getElementById('viewVision').innerHTML=h;
}
/* ---------- 2036 Alignment tab ---------- */
let alignBuilt=false;
const ALIGN_BAND={Strong:['#2b8a3e','#e7f3ea'],Emerging:['#b45309','#fdf0e2'],Thin:['#c2410c','#fdece3'],Gap:['#7a2312','#f6dcd4']};
const TRAJ={Accelerating:['#2b8a3e','#e7f3ea'],Steady:['#1f5a8f','#e7eef7'],Emerging:['#b45309','#fdf0e2'],Lagging:['#c2410c','#fdece3']};
const TRAJ_ARROW={Accelerating:'▲▲',Steady:'▲',Emerging:'◇',Lagging:'▼'};
function pillarSignals(theme){
 const partners=PARTNERS.filter(p=>p.themes.includes(theme)).length;
 const indic=INDICATIVE.filter(o=>(o.themes||[]).includes(theme)).length;
 const funders=FUNDERS.filter(f=>(f.domains||[]).includes(theme));
 const schemeCr=(SCHEMES.items||[]).filter(s=>s.theme===theme).reduce((a,s)=>a+(s.outlayCr||0),0);
 const dists=CANON.filter(d=>D[d].themes.includes(theme)).length;
 return {partners,indic,funders,schemeCr,dists,orgs:partners+indic};
}
function alignBand(s){
 if(s.orgs>=15&&s.funders.length>=3)return 'Strong';
 if(s.orgs>=6||s.funders.length>=2)return 'Emerging';
 if(s.orgs>=1)return 'Thin';
 return 'Gap';
}
function buildAlignment(){
 if(alignBuilt)return; alignBuilt=true;
 const cov=coveredList().length, asp=CANON.filter(d=>D[d].aspirational), aspCov=asp.filter(d=>effP(d)>0).length;
 const shgTot=CANON.reduce((s,d)=>s+((D[d].shg||{}).total||0),0);
 const fpoTot=CANON.reduce((s,d)=>s+((D[d].fpo||{}).fpos||0),0);
 // priority districts: the weakest-served across ALL 30 (the aspirational belt is saturated
 // by the research pass, so the genuine gaps are thin non-aspirational districts).
 const singles=CANON.filter(d=>effP(d)===1), white=whiteList();
 const prio=CANON.map(d=>({d,s:placeScore(d),t:placeTag(d),asp:D[d].aspirational})).sort((a,b)=>a.s-b.s).slice(0,8);

 let h='<div class="vhero" style="background:linear-gradient(155deg,#0f2440,#5b2a86)"><div class="big">How aligned is today’s ecosystem to Vision 2036?</div>'
  +'<div class="meta">Cross-reads the mapped ecosystem (partners, funders, government money, public infrastructure) against the seven Vision 2036 pillars — to surface where effort already lines up with the state’s stated priorities, and where the gaps and missing links are. Alignment is inferred from a sourced research pass, not an audit.</div></div>';

 // --- pillar scorecard ---
 h+='<div class="section-title">Pillar alignment scorecard</div>';
 h+='<p class="section-sub">Each Vision 2036 pillar scored by the ecosystem behind it right now: mapped organisations on that theme (source + ✳ indicative), funders backing that domain, and government scheme money tagged to it. Bands: <b style="color:#2b8a3e">Strong</b> · <b style="color:#b45309">Emerging</b> · <b style="color:#c2410c">Thin</b> · <b style="color:#7a2312">Gap</b>.</p>';
 h+='<div class="vgrid">';
 (VISION.pillars||[]).forEach(p=>{
  const s=pillarSignals(p.theme);
  const band=p.growth?'Gap':alignBand(s), bc=ALIGN_BAND[band];
  const col=themePalette[p.theme]||'#0d6e8c';
  h+='<div class="vcard"><div class="vh"><span class="vth" style="background:'+col+'"></span>'+p.name
    +'<span class="badge" style="margin-left:auto;background:'+bc[1]+';color:'+bc[0]+'">'+band+(p.growth?'*':'')+'</span></div>';
  h+='<div class="kv" style="margin:11px 0 4px;gap:14px">'
    +'<div><div class="k">Orgs</div><div class="v">'+s.orgs+'</div></div>'
    +'<div><div class="k">Funders</div><div class="v">'+s.funders.length+'</div></div>'
    +'<div><div class="k">Govt ₹Cr</div><div class="v">'+(s.schemeCr?s.schemeCr.toLocaleString('en-IN'):'–')+'</div></div>'
    +'<div><div class="k">Districts</div><div class="v">'+s.dists+'</div></div></div>';
  const tj=(VISION.trajectory||{})[p.name];
  if(tj){const tc=TRAJ[tj.dir]||['#6b7a93','#eef2f8'];
    h+='<div class="mini" style="margin-top:8px"><span class="badge" style="background:'+tc[1]+';color:'+tc[0]+'">'+TRAJ_ARROW[tj.dir]+' '+tj.dir+'</span> <span style="color:var(--mut)">'+tj.why+'</span></div>';}
  if(p.growth){h+='<div class="mini" style="margin-top:6px;color:#7a2312">*Growth pillar — the ecosystem theme shown is a <b>rural proxy</b>; the vision’s industry / urban / digital ambition is largely off-map, so the org count overstates true alignment.</div>';}
  h+='<div class="mini" style="margin-top:6px">Theme: <span class="tag" style="border-left:3px solid '+col+'">'+p.theme+'</span>'
    +(s.funders.length?' · funders: '+s.funders.slice(0,3).map(f=>f.name.split(' (')[0].split(' —')[0]).join(', ')+(s.funders.length>3?'…':''):'')+'</div>';
  h+='</div>';
 });
 h+='</div>';

 // --- structural gap callout ---
 const humanThemes=['Women & Gender','Health & Nutrition','Education','Agriculture','Livelihoods & Rural Dev'];
 const humanOrgs=[...new Set(PARTNERS.filter(p=>p.themes.some(t=>humanThemes.includes(t))).map(p=>p.name))].length;
 h+='<div class="section-title">The structural gap: human development vs economic transformation</div>';
 h+='<div class="card cardpad" style="border-left:4px solid #7a2312">'
   +'<p style="margin:0 0 8px">The mapped ecosystem is overwhelmingly a <b>human-development</b> ecosystem — women &amp; SHGs, health, education, agriculture and rural livelihoods (~'+humanOrgs+' of the '+PARTNERS.length+' partners work on at least one of these). That aligns tightly with the vision’s social pillars.</p>'
   +'<p style="margin:0 0 8px">But Vision 2036’s <b>headline ambition is economic transformation</b>: a $500B economy, manufacturing mega-parks, port-based SEZs, digital services, tourism and urbanisation from 17% to 40%. <b>Almost no mapped development partner, and few philanthropies, work on these</b> — the ecosystem has no theme for industry, digital, urban development or tourism at all. The rural "Livelihoods &amp; Rural Dev" theme is the closest proxy, and it is not the same thing.</p>'
   +'<p style="margin:0 0 8px"><b>Implication:</b> the civil-society + philanthropy ecosystem can help the vision deliver <i>inclusion</i> (who benefits), but the <i>growth engine</i> (industry, jobs, cities) currently sits almost entirely with government + corporates, largely outside this map. That is the single biggest alignment gap.</p>'
   +'<p style="margin:0"><b>The green shoot:</b> <a href="https://bckic.in/" target="_blank" rel="noopener">BCKIC</a> (Bhubaneswar City Knowledge Innovation Cluster, PSA/PM-STIAC) is the one mapped actor squarely on the growth side — future/blue-green economy, critical minerals, STEM and startups, with NALCO/JSW/BPCL/IIT-BBSR/KIIT. It is the natural bridge from this ecosystem to the vision’s economic engine, but today it is a single node in Khordha, not a statewide network.</p></div>';

 // --- velocity to 2036 ---
 const V=VISION.velocity||[];
 if(V.length){
  h+='<div class="section-title">Velocity: the pace 2036 demands</div>';
  h+='<p class="section-sub">Odisha is ~10 years from its centenary. For the quantified targets, this is the annual pace required — and how far today’s drift is from it.</p>';
  h+='<div class="card tbl"><table><thead><tr><th>Target</th><th>2036/47 goal</th><th>Required pace</th><th>Where the drift is today</th></tr></thead><tbody>';
  V.forEach(v=>{h+='<tr><td><b>'+v.metric+'</b></td><td>'+v.target+'</td><td><b style="color:#7c3a86">'+v.pace+'</b></td><td class="mini">'+v.now+'</td></tr>';});
  h+='</tbody></table></div>';
 }

 // --- headline target vs today ---
 h+='<div class="section-title">Headline target vs where it stands today</div>';
 h+='<p class="section-sub">Vision 2036 target next to a real current signal from this dashboard. "Distance" is the honest gap to close in ~10 years.</p>';
 const rows=[
  ['Economy','$500B GSDP by 2036 ($1.5T by 2047)','No partner/funder theme for industry or digital in the ecosystem','Growth engine largely off-map — biggest gap'],
  ['Urbanisation','17% → 40% urban; ANKUR resilient cities','Ecosystem is district/rural; ~0 mapped urban-development partners','Missing link'],
  ['Jobs &amp; skills','1.1 cr jobs by 2047; Skilled in Odisha','Skilling partners + HDFC Parivartan (₹24 Cr, Bhubaneswar)','Emerging — narrow'],
  ['Women','Employment, entrepreneurship, leadership','~'+(shgTot/1e5|0)+' lakh SHGs (Mission Shakti ₹1,107 Cr, Subhadra ₹10,145 Cr) + Gates/WFP','Strong alignment'],
  ['Agriculture','All cultivable land irrigated; higher incomes','~'+fpoTot.toLocaleString('en-IN')+' FPOs + Gates ADAPT + many NRM/agri partners','Emerging → strong'],
  ['Inclusion','Equitable growth across all districts','Aspirational districts served: '+aspCov+'/'+asp.length+'; overall coverage '+cov+'/'+NDIST,'Partial — see priority gaps'],
 ];
 h+='<div class="card tbl"><table><thead><tr><th>Pillar</th><th>2036 target</th><th>Where it stands today</th><th>Read</th></tr></thead><tbody>';
 rows.forEach(r=>{h+='<tr><td><b>'+r[0]+'</b></td><td>'+r[1]+'</td><td>'+r[2]+'</td><td class="mini">'+r[3]+'</td></tr>';});
 h+='</tbody></table></div>';

 // --- geographic priority gaps ---
 h+='<div class="section-title">Geographic priority gaps</div>';
 h+='<p class="section-sub">Vision 2036 promises inclusive growth across all districts. The 8 <b>weakest-served</b> districts in the mapped ecosystem (lowest place-health) are the clearest place-based priorities — a ● marks NITI Aayog <b>aspirational</b> districts. Note the twist: the aspirational/KBK belt is actually <b>well covered</b> by the research pass, so the real thin spots are mostly <b>non-aspirational</b> districts.</p>';
 h+='<div class="card"><div class="phhead" style="grid-template-columns:170px 1fr 120px"><span>District</span><span>Coverage strength</span><span style="text-align:right">Score</span></div><div class="ph">';
 prio.forEach(x=>{const bc=BAND[band(x.s)][0];
  h+='<div class="phrow" style="grid-template-columns:170px 1fr 120px"><span class="pn" data-d="'+x.d+'">'
   +(x.asp?'<span class="dot" style="background:#c2410c" title="Aspirational (NITI Aayog)"></span>':'<span class="dot" style="background:#cdd7e6"></span>')+x.d
   +' <span class="mini">'+effP(x.d)+' org'+(effP(x.d)!=1?'s':'')+'</span></span>'
   +'<span class="track"><i style="width:'+Math.max(x.s,3)+'%;background:'+bc+'"></i></span>'
   +'<span class="right"><span class="tagp" style="background:'+x.t.tb+';color:'+x.t.tc+'">'+x.t.tag+'</span><span class="sc">'+x.s+'</span></span></div>';});
 h+='</div></div>';

 // --- missing links + priorities ---
 h+='<div class="grid" style="grid-template-columns:1fr 1fr;align-items:start;margin-top:18px">';
 h+='<div class="card cardpad"><div class="section-title" style="margin-top:0">Missing links</div><ul class="vt" style="margin-top:4px">'
   +'<li>No mapped ecosystem for <b>industry, manufacturing, digital services or tourism</b> — the vision’s growth engine.</li>'
   +'<li><b>Urban development</b> (ANKUR, 40% urbanisation) has virtually no mapped civil-society partner.</li>'
   +'<li><b>Clean energy / just transition</b> rests on a single anchor (SELCO) despite Odisha’s coal-belt exposure.</li>'
   +'<li><b>Skilling for the industrial belt</b> (Jajapur, Anugul, Jharsuguda, Sundargarh) is thin vs the jobs target.</li>'
   +'<li>Thinnest coverage is in <b>non-aspirational</b> districts — '+(singles.join(', ')||'none')+' have a single mapped partner'+(white.length?'; '+white.join(', ')+' have none':' (no zero-partner districts)')+'. The aspirational/KBK belt is comparatively well-served.</li></ul></div>';
 h+='<div class="card cardpad"><div class="section-title" style="margin-top:0">Where to point partnerships &amp; funding</div><ul class="vt" style="margin-top:4px">'
   +'<li><b>Convene the growth pillars:</b> bring industry/skilling/urban actors onto the map so inclusion and growth are planned together.</li>'
   +'<li><b>Back a clean-energy / just-transition anchor</b> in the coal &amp; mining belt (Anugul, Jharsuguda, Sundargarh, Kendujhar).</li>'
   +'<li><b>Fund the weakest aspirational districts</b> first (top of the list at left) to honour the inclusive-growth promise.</li>'
   +'<li><b>Channel DMF + CSR</b> in mining districts toward vision-aligned skilling &amp; urban resilience, not only welfare.</li>'
   +'<li><b>Deepen agriculture-to-market</b> (FPOs + Gates ADAPT + Model Mandi) toward the productivity/income target.</li></ul></div>';
 h+='</div>';

 // --- unlocks: what could shift the alignment ---
 const U=VISION.unlocks||[];
 if(U.length){
  h+='<div class="section-title">Unlocks: what could shift the alignment</div>';
  h+='<p class="section-sub">Concrete levers that would unblock movement — each with what it releases and who holds the key.</p>';
  h+='<div class="card tbl"><table><thead><tr><th>Lever</th><th>What it unblocks</th><th>Who can unlock it</th></tr></thead><tbody>';
  U.forEach((u,i)=>{h+='<tr><td><b>'+(i+1)+'. '+u.lever+'</b></td><td>'+u.unblocks+'</td><td class="mini">'+u.who+'</td></tr>';});
  h+='</tbody></table></div>';
 }

 // --- Catalytic Unlock: nature-first landscapes + top 10 projects (project-level subset of the unlocks) ---
 h+='<div class="section-title">Catalytic Unlock ✳ · nature-first landscapes &amp; top 10 projects</div>';
 h+='<p class="section-sub" id="catintro"></p>';
 h+='<div class="card cardpad"><div id="catland"></div></div>';
 h+='<div class="card tbl" id="catproj" style="margin-top:14px"></div>';

 h+='<p class="vnote">Trajectory, velocity and unlocks are a planning read inferred by cross-referencing the mapped ecosystem with the Vision 2036 pillars; both sides are sourced but not independently audited. Not a scorecard of government performance.</p>';
 const box=document.getElementById('viewAlign'); box.innerHTML=h;
 box.querySelectorAll('.pn[data-d]').forEach(s=>s.onclick=()=>{const b=document.querySelector('#tabbar button[data-view=main]');if(b)b.click();selectDist(s.dataset.d);document.getElementById('mapbox').scrollIntoView({behavior:'smooth',block:'center'});});
 buildCatalytic(); // fills #catintro / #catland / #catproj now that they exist in the alignment view
}

const VIEWS={main:'viewMain',vision:'viewVision',align:'viewAlign'};
const tabbar=document.getElementById('tabbar');
tabbar.addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;
 [...tabbar.children].forEach(x=>x.classList.toggle('on',x===b));
 const v=b.dataset.view;
 Object.entries(VIEWS).forEach(([k,id])=>{document.getElementById(id).style.display=(k===v)?'':'none';});
 if(v==='vision')buildVision();
 if(v==='align')buildAlignment();
 if(v!=='main')window.scrollTo({top:0,behavior:'smooth'});
});

/* ---------- indicative-org toggle: recompute everything on the wider org set ---------- */
function recompute(){refreshScales();buildLensButtons();renderStrip();paint();buildHealth();buildPlaceHealth();buildDir();buildDisTbl();updateFoot();}

/* initial render */
refreshScales(); renderStrip(); paint(); buildHealth(); buildMatrix(); buildPlaceHealth(); buildDir(); buildDisTbl(); updateFoot(); buildGovt(); buildSchemes(); buildCsrState(); buildFunders(); /* buildCatalytic() runs inside buildAlignment (2036 Alignment tab) */
document.getElementById('dircount').textContent='('+PARTNERS.length+' organisations)';
document.querySelectorAll('.collapser[data-wrap]').forEach(tg=>{const wrap=document.getElementById(tg.dataset.wrap);
 tg.addEventListener('click',()=>{const hidden=wrap.classList.toggle('collapsed'); tg.classList.toggle('closed',hidden);});});

/* indicative-org toggle */
const extCb=document.getElementById('extToggle');
if(extCb){extCb.addEventListener('change',()=>{INCLUDE_EXT=extCb.checked;recompute();});}

/* deep-links: #vision opens Vision 2036 · #ext turns on indicative scoring · #lens=<key> selects a map lens */
if(location.hash.includes('ext')&&extCb){extCb.checked=true;INCLUDE_EXT=true;recompute();}
const hl=location.hash.match(/lens=(\w+)/); if(hl&&lenses[hl[1]]){
 // honour a deep-link to a gated lens by turning on the ✳ toggle that reveals it
 if(GATED_LENSES.includes(hl[1])&&!INCLUDE_EXT&&extCb){extCb.checked=true;INCLUDE_EXT=true;recompute();}
 curLens=hl[1];buildLensButtons();paint();}
if(location.hash.includes('vision')){const vb=document.querySelector('#tabbar button[data-view=vision]');if(vb)vb.click();}
if(location.hash.includes('align')){const ab=document.querySelector('#tabbar button[data-view=align]');if(ab)ab.click();}
</script></body></html>'''

HTML = HTML.replace('__MODEL__', MODEL).replace('__GEO__', GEO)
open("index.html","w").write(HTML)
print("wrote index.html", len(HTML), "bytes")
