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
</style></head>
<body><div class="wrap">
<h1>Odisha Landscape — Who Does What Where</h1>
<p class="sub">Partners × districts, SHG density, FPO density and DMF mining-fund flow. A sense-making view for partnership &amp; ecosystem decisions — data foundation, not a finished partner survey.</p>

<div class="intro card cardpad">
 <p class="intro-lead">A first pass at mapping the development-partner ecosystem in Odisha — <b>who's known to work where</b>, alongside the public infrastructure (SHGs, FPOs) and public money (DMF) already on the ground.</p>
 <p class="intro-body"><b>Read this as a data foundation, not a survey.</b> SHG, DMF and FPO layers are complete, live-fetched government/platform data across all 30 districts. The <b>partner layer is a seed of 11 organisations</b> — pulled from incidental Odisha mentions inside a Jharkhand-focused research project's own source files, not a systematic canvass of who works in Odisha. Treat partner density, theme breadth and the health scores below as illustrative of the method, not as a claim about the real state of the ecosystem, until that research gets done properly.</p>
 <p class="intro-src">Sources: Bharatlas (district boundaries, LGD 2024) · DAY-NRLM public MIS (SHG) · Odisha's own DMF portal (dmf.odisha.gov.in) · FPO Platform / Cornell TCI (FPO) · NITI Aayog Aspirational Districts Programme · seed partner data via jharkhand-landscape's source spreadsheets. CSR data is blocked by a captcha on the national CSR portal — see Sources below. Fully offline &amp; self-contained.</p>
</div>

<div class="grid hero">
 <div class="card">
   <h2>District map</h2>
   <div class="lens" id="lens"></div>
   <div id="mapbox"></div>
   <div class="legend" id="legend"></div>
 </div>
 <div class="card" id="detail"><h2>District detail</h2>
   <div class="empty" id="detEmpty">Click a district on the map to see partners, block coverage, SHGs, FPOs and DMF trend.</div>
   <div class="cardpad" id="detBody" style="display:none"></div>
 </div>
</div>

<div class="strip" id="strip"></div>

<div class="section-title">Ecosystem health</div>
<p class="section-sub">A funder-facing read on the state of the (seed) partner ecosystem — coverage, reach into aspirational districts, resilience, thematic balance, network depth and SHG co-location. Built on 11 seed partner orgs — read the bands as illustrative, not definitive, until the partner layer is properly researched.</p>
<div class="card cardpad"><div class="health"><div class="hindex" id="hindex"></div><div class="hcards" id="hcards"></div></div></div>

<div class="section-title">Partner × Theme matrix</div>
<p class="section-sub">Where thematic energy concentrates among the 11 seed partners. Several block-level orgs (NIRMAN, SEWAK, SEBAJAGAT, WOSCA &amp; WASSAN, WASSAN &amp; its partners, PRADAN) have no theme data in the source and show no cells — that's a gap in the source, not a claim they cover no themes.</p>
<div class="card cardpad mtx" id="matrix"></div>

<div class="section-title">Government spend — DMF (District Mineral Foundation)</div>
<p class="section-sub">Odisha is India's top DMF-collecting state. Figures below are <b>live from Odisha's own DMF portal</b> (dmf.odisha.gov.in), district-wise, FY2015-16 through FY2025-26 — not a static cumulative-to-a-past-year snapshot. See the <b>"DMF mining fund"</b> map lens.</p>
<div class="card"><h2>DMF collection by district (cumulative, FY2015-16 → FY2025-26)</h2><div class="tbl" id="govtdmf"></div></div>

<div class="section-title collapser closed" id="dirToggle" data-wrap="dirwrap">Partner directory <span class="caret">▾</span> <span class="mini" style="font-weight:400" id="dircount"></span></div>
<div id="dirwrap" class="collapsed">
<p class="section-sub">All 11 seed partner organisations. Click a column header to sort; click a district tag to focus the map. See the Sources section for exactly where each row came from.</p>
<div class="card tbl" id="dirtbl"></div>
</div>

<div class="section-title collapser closed" data-wrap="phwrap">Place health — where attention is needed <span class="caret">▾</span></div>
<div id="phwrap" class="collapsed">
<p class="section-sub">Each district scored 0–100 on how well it is served (partner presence 45% · thematic breadth 30% · resilience/no single-point-of-failure 25%), ranked neediest-first, using the 11-org seed dataset. Priority = aspirational (NITI Aayog) &amp; weakly served.</p>
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
 <div class="warnbox">CSR data is not included: every export path on the national CSR portal (csr.gov.in) is gated behind a CAPTCHA, and this project doesn't attempt to bypass CAPTCHAs. District-level CSR would need someone to manually solve it and export the report.</div>
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
  <div><div class="srch">Seed partner data</div>
   <ul><li><a href="https://github.com/sidd-1995/jharkhand-landscape" target="_blank" rel="noopener">jharkhand-landscape</a> — incidental Odisha rows in its own multi-state source files</li></ul></div>
 </div>
</div>
</div>

<div class="foot" id="foot"></div>
</div>

<script>
const MODEL=__MODEL__;
const GEO=__GEO__;
const D=MODEL.districts, CANON=MODEL.canon, THEMES=MODEL.themes, YEARS=MODEL.years, PARTNERS=MODEL.partners;
const NDIST=CANON.length;
const el=(t,c,h)=>{const e=document.createElement(t); if(c)e.className=c; if(h!=null)e.innerHTML=h; return e;};

/* ---------- effective data (no indicative-org toggle here -- the seed *is* the partner set) ---------- */
function effPList(d){return D[d].partners.slice();}
function effP(d){return effPList(d).length;}
function effTList(d){return D[d].themes.slice();}
function effT(d){return effTList(d).length;}
const coveredList=()=>CANON.filter(d=>effP(d)>0);
const whiteList=()=>CANON.filter(d=>effP(d)===0);

/* ---------- DMF (real, year-wise) ---------- */
const DMF_TOTAL={}; CANON.forEach(d=>{DMF_TOTAL[d]=YEARS.reduce((s,y)=>s+(D[d].dmf[y]||0),0);});
const maxDMF=Math.max(1,...Object.values(DMF_TOTAL));
const stateDMF=Object.values(DMF_TOTAL).reduce((a,b)=>a+b,0);
const fmtDmf=v=>'₹'+v.toLocaleString('en-IN',{maximumFractionDigits:0})+' Cr'; // values already in ₹ Cr

/* ---------- theme frequency (for matrix shading + dominant) ---------- */
const themeFreq={}; THEMES.forEach(t=>themeFreq[t]=0);
PARTNERS.forEach(p=>p.themes.forEach(t=>{if(t in themeFreq)themeFreq[t]++;}));
const maxTF=Math.max(...Object.values(themeFreq),1);

/* ---------- summary strip ---------- */
function renderStrip(){const strip=document.getElementById('strip'); strip.innerHTML='';
 const covered=coveredList().length, white=whiteList().length;
 const stats=[
  [NDIST,'Districts'],
  [PARTNERS.length,'Partners mapped (seed)'],
  [covered,'Districts covered'],
  [white,'Whitespace (0 orgs)','warn'],
  [CANON.filter(d=>D[d].aspirational).length,'Aspirational (NITI Aayog)'],
  [fmtDmf(Math.round(stateDMF)),'DMF collected, FY16→FY26']
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
 partners:{label:'Partner density (seed)',fill:d=>seqColor(effP(d),maxP),
   legend:()=>gradLegend('# seed partners',maxP)},
 themes:{label:'Theme breadth',fill:d=>seqColor(effT(d),maxT),
   legend:()=>gradLegend('# themes',maxT)},
 dom:{label:'Dominant theme',fill:d=>{const t=domTheme(d);return t?themePalette[t]:'#f1f5fa';},
   legend:()=>themeLegend()},
 gap:{label:'Coverage gap',fill:d=>{const n=effP(d),a=D[d].aspirational;if(n===0&&a)return '#c2410c';
     if(n===0)return '#e79a6a'; if(a&&n<=1)return '#f0c088'; return '#cfe0d8';},
   legend:()=>gapLegend()},
 blockcov:{label:'Block presence (beta)',fill:d=>{const n=blockN(d);if(!n)return '#f1f5fa';const p=['#dcefe6','#a6ddc4','#6ec6a4','#3aa987','#1f7d63'];return p[Math.min(p.length-1,Math.ceil(n/Math.max(maxBlk,1)*(p.length-1)))];},
   legend:()=>gradLegendC('Known block-level presence — seed data only',['#f1f5fa','#a6ddc4','#6ec6a4','#3aa987','#1f7d63'],'0 → '+maxBlk+' blocks')},
 shg:{label:'SHG density',fill:d=>{const n=shgN(d);if(!n)return '#faf3e8';const p=['#faf3e8','#f0dcae','#e0b968','#c98e2e','#9c6512'];return p[Math.min(p.length-1,Math.ceil(n/Math.max(maxSHG,1)*(p.length-1)))];},
   legend:()=>gradLegendC('Self Help Groups (DAY-NRLM MIS)',['#faf3e8','#f0dcae','#e0b968','#c98e2e','#9c6512'],'0 → '+maxSHG.toLocaleString()+' SHGs')},
 fpo:{label:'FPO density',fill:d=>{const n=fpoN(d);if(!n)return '#eef3ea';const p=['#eef3ea','#c9dfba','#9ec98a','#6fae5c','#3d8730'];return p[Math.min(p.length-1,Math.ceil(n/Math.max(maxFPO,1)*(p.length-1)))];},
   legend:()=>gradLegendC('FPOs (FPO Platform)',['#eef3ea','#c9dfba','#9ec98a','#6fae5c','#3d8730'],'0 → '+maxFPO.toLocaleString()+' FPOs')},
 dmf:{label:'DMF mining fund',fill:d=>{const v=DMF_TOTAL[d]||0;if(!v)return '#f2eef6';const t=v/maxDMF;const p=['#e7dcf0','#c9b0e0','#a97fce','#8a4fbf','#6b2fa0'];return p[Math.min(p.length-1,Math.floor(t*(p.length-1)+0.001))];},
   legend:()=>gradLegendC('DMF collected, FY16→FY26 (₹ Cr)',['#e7dcf0','#c9b0e0','#a97fce','#8a4fbf','#6b2fa0'],'0 → '+fmtDmf(Math.round(maxDMF)))}
};
const blockN=d=>(D[d].blockcov||[]).length;
const maxBlk=Math.max(1,...CANON.map(blockN));
const shgN=d=>(D[d].shg||{}).total||0;
const maxSHG=Math.max(1,...CANON.map(shgN));
const fpoN=d=>(D[d].fpo||{}).fpos||0;
const maxFPO=Math.max(1,...CANON.map(fpoN));
function domTheme(d){const f={};PARTNERS.forEach(p=>{if(p.districts.includes(d))p.themes.forEach(t=>f[t]=(f[t]||0)+1);});
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

/* build map */
const mapbox=document.getElementById('mapbox');
const svgNS='http://www.w3.org/2000/svg';
const svg=document.createElementNS(svgNS,'svg');
svg.setAttribute('viewBox','0 0 '+W+' '+H); svg.setAttribute('class','map');
const paths={},labels={};
GEO.features.forEach(f=>{const name=f.properties.district;
 const p=document.createElementNS(svgNS,'path');
 p.setAttribute('d',pathFor(f.geometry)); p.setAttribute('class','dist'); p.dataset.d=name;
 p.addEventListener('click',()=>selectDist(name));
 p.addEventListener('mousemove',ev=>showTip(ev,name));
 p.addEventListener('mouseleave',hideTip);
 svg.appendChild(p); paths[name]=p;
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
Object.entries(lenses).forEach(([k,v])=>{const b=el('button',k===curLens?'on':'',v.label);b.onclick=()=>{curLens=k;paint();};lensBox.appendChild(b);});
function paint(){
 [...lensBox.children].forEach(b=>b.classList.toggle('on',b.textContent===lenses[curLens].label));
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
 let h='<div class="dh"><span class="name">'+name+'</span><span>';
 if(v.aspirational)h+='<span class="badge asp">Aspirational</span>';
 h+='</span></div>';
 h+='<div class="kv"><div><div class="k">Partners (seed)</div><div class="v">'+effP(name)+'</div></div>'
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
 h+='<div class="sec"><div class="t">Partners here (seed)</div>';
 if(dp.length){h+='<ul class="plist">';dp.forEach(p=>{h+='<li><b>'+p.name+'</b><br><span class="mini">'+(p.themes.length?p.themes.join(' · '):'no theme data in source')+'</span></li>';});h+='</ul>';}
 else h+='<div class="mini">No mapped partner in the seed data. '+(v.aspirational?'Aspirational district — whitespace.':'')+'</div>';
 h+='</div>';
 if(v.themes.length){h+='<div class="sec"><div class="t">Themes active</div><div class="chips">'+v.themes.map(t=>'<span class="chip" style="border-left:3px solid '+(themePalette[t]||'#ccc')+'">'+t+'</span>').join('')+'</div></div>';}
 // block coverage (beta) — seed data only
 const bc=v.blockcov||[];
 if(bc.length){
  const srcs=[...new Set(bc.flatMap(b=>b.by))].sort();
  h+='<div class="sec"><details class="bcov"><summary><b>Block coverage</b> <span class="beta">beta</span> · <b>'+bc.length+'</b> block(s) with known partner presence</summary>';
  h+='<div class="mini" style="margin:5px 0 8px">Block-level presence known for <b>'+srcs.join(', ')+'</b> only, from the seed dataset — this is <b>known presence, not total coverage</b>.</div>';
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
 const rows=PARTNERS.map(p=>({name:p.name,themes:p.themes})).sort((a,b)=>b.themes.length-a.themes.length);
 let h='<table><thead><tr><th>Partner</th>';
 THEMES.forEach(t=>h+='<th class="rot" title="'+t+'"><div>'+shortT(t)+'</div></th>');
 h+='</tr></thead><tbody>';
 rows.forEach(p=>{h+='<tr><td class="name">'+p.name+'</td>';
   THEMES.forEach(t=>{const on=p.themes.includes(t);
     let bg='#fff',dot='';
     if(on){const shade=0.35+0.65*(themeFreq[t]/maxTF);bg='rgba(13,110,140,'+shade.toFixed(2)+')';dot='●';}
     h+='<td><div class="cell" style="background:'+bg+'">'+dot+'</div></td>';});
   h+='</tr>';});
 h+='<tr><td class="name" style="font-weight:700">Orgs / theme</td>';
 THEMES.forEach(t=>h+='<td class="tot">'+themeFreq[t]+'</td>');
 h+='</tbody></table>';
 document.getElementById('matrix').innerHTML=h;
}

/* ---------- partner directory ---------- */
let dirSort={k:'nd',asc:false};
function buildDir(){
 const box=document.getElementById('dirtbl');
 const cols=[['name','Partner'],['districts','Districts'],['themes','Themes / focus'],['nd','#Dist']];
 let rows=PARTNERS.map(p=>({name:p.name,districts:p.districts,themes:p.themes,themesN:p.themes.length,nd:p.districts.length}));
 rows.sort((a,b)=>{let k=dirSort.k,x,y;
   if(k==='themes'){x=a.themesN;y=b.themesN;} else if(k==='districts'){x=a.nd;y=b.nd;} else {x=a[k];y=b[k];}
   if(typeof x==='string')return dirSort.asc?x.localeCompare(y):y.localeCompare(x);return dirSort.asc?x-y:y-x;});
 let h='<table><thead><tr>';cols.forEach(c=>h+='<th data-k="'+c[0]+'">'+c[1]+(dirSort.k===c[0]?(dirSort.asc?' ▲':' ▼'):'')+'</th>');h+='</tr></thead><tbody>';
 rows.forEach(p=>{
   const dcell=p.districts.length?p.districts.map(d=>'<span class="tag pill" data-d="'+d+'">'+d+'</span>').join(''):'<span class="tag">Statewide</span>';
   const tcell=p.themes.length?p.themes.map(t=>'<span class="tag" style="border-left:3px solid '+(themePalette[t]||'#ccc')+'">'+t+'</span>').join(''):'<span class="mini">no theme data in source</span>';
   h+='<tr><td><b>'+p.name+'</b></td><td>'+dcell+'</td><td>'+tcell+'</td><td class="num">'+p.nd+'</td></tr>';});
 h+='</tbody></table>'; box.innerHTML=h;
 box.querySelectorAll('th').forEach(th=>th.onclick=()=>{const k=th.dataset.k;dirSort.asc=dirSort.k===k?!dirSort.asc:false;dirSort.k=k;buildDir();});
 box.querySelectorAll('.pill').forEach(s=>s.onclick=()=>{selectDist(s.dataset.d);document.getElementById('mapbox').scrollIntoView({behavior:'smooth',block:'center'});});
}

/* ---------- district table ---------- */
let disSort={k:'partners',asc:false};
function buildDisTbl(){
 const box=document.getElementById('distbl');
 let rows=CANON.map(d=>({d,partners:effP(d),themes:effT(d),
   asp:D[d].aspirational?1:0,shg:shgN(d),fpo:fpoN(d),plist:effPList(d)}));
 rows.sort((a,b)=>{let x=a[disSort.k],y=b[disSort.k];if(typeof x==='string')return disSort.asc?x.localeCompare(y):y.localeCompare(x);return disSort.asc?x-y:y-x;});
 const cols=[['d','District'],['partners','Partners'],['themes','Themes'],['asp','Asp.'],['shg','SHGs'],['fpo','FPOs']];
 let h='<table><thead><tr>';cols.forEach(c=>h+='<th data-k="'+c[0]+'"'+(c[0]!=='d'?' class="num"':'')+'>'+c[1]+(disSort.k===c[0]?(disSort.asc?' ▲':' ▼'):'')+'</th>');h+='<th>Who</th></tr></thead><tbody>';
 rows.forEach(r=>{const bg=r.partners===0?'background:#fdf3ee':'';
   h+='<tr style="'+bg+'"><td><span class="dot" style="background:'+seqColor(r.partners,maxP)+'"></span><b class="pill" data-d="'+r.d+'">'+r.d+'</b></td>'
    +'<td class="num">'+r.partners+'</td><td class="num">'+r.themes+'</td>'
    +'<td class="num">'+(r.asp?'<span style="color:#c2410c">●</span>':'–')+'</td>'
    +'<td class="num">'+r.shg.toLocaleString()+'</td>'
    +'<td class="num">'+r.fpo.toLocaleString()+'</td>'
    +'<td class="mini">'+(r.plist.join(', ')||'—')+'</td></tr>';});
 h+='</tbody></table>'; box.innerHTML=h;
 box.querySelectorAll('th').forEach(th=>th.onclick=()=>{const k=th.dataset.k;disSort.asc=disSort.k===k?!disSort.asc:(k==='d');disSort.k=k;buildDisTbl();});
 box.querySelectorAll('.pill').forEach(s=>s.onclick=()=>{selectDist(s.dataset.d);document.getElementById('mapbox').scrollIntoView({behavior:'smooth',block:'center'});});
}

function updateFoot(){const wl=whiteList();document.getElementById('foot').innerHTML='Fully self-contained (offline) · '+PARTNERS.length+' seed partners across '+coveredList().length+'/'+NDIST+' districts · Whitespace: <b>'+(wl.length?wl.join(', '):'none')+'</b>.<br>MIT licensed · source &amp; issues: <a href="https://github.com/sidd-1995/odisha-landscape" target="_blank" rel="noopener">github.com/sidd-1995/odisha-landscape</a>';}

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
 const fragile=THEMES.filter(t=>tf[t]>0&&tf[t]<=2);
 const hubs=CANON.filter(d=>effP(d)>=3);
 const avgP=cov.length?cov.reduce((s,d)=>s+effP(d),0)/cov.length:0;
 const lbl='partner';
 // SHG (DAY-NRLM) reach — share of the state's SHG member base sitting in partner-covered districts
 const shgTot=CANON.reduce((s,d)=>s+((D[d].shg||{}).members||0),0);
 const shgMemCov=CANON.reduce((s,d)=>s+(effP(d)?((D[d].shg||{}).members||0):0),0);
 const shgCov=shgTot?shgMemCov/shgTot*100:0;
 const dims=[
  {n:'Geographic coverage',v:cov.length+'/'+NDIST,s:cov.length/NDIST*100,d:Math.round(cov.length/NDIST*100)+'% of districts have ≥1 '+lbl+' (seed data).'},
  {n:'Aspirational reach',v:aspCov.length+'/'+asp.length,s:asp.length?aspCov.length/asp.length*100:0,d:(asp.length-aspCov.length)+' NITI Aayog aspirational districts still unserved in the seed: '+(asp.filter(d=>!effP(d)).join(', ')||'none')+'.'},
  {n:'Resilience',v:(NDIST-wht.length-single.length)+'/'+NDIST,s:(NDIST-wht.length-single.length)/NDIST*100,d:single.length+' single-'+lbl+' + '+wht.length+' zero-'+lbl+' districts = key-person risk.'},
  {n:'Thematic balance',v:(THEMES.length-fragile.length)+'/'+THEMES.length,s:(THEMES.length-fragile.length)/THEMES.length*100,d:'Thin themes (≤2 '+lbl+'s): '+(fragile.join(', ')||'none')+'.'},
  {n:'Network depth',v:hubs.length+' hubs',s:hubs.length/NDIST*100,d:hubs.length+' districts with ≥3 '+lbl+'s; avg '+avgP.toFixed(1)+' where present.'},
  {n:'SHG reach',v:Math.round(shgCov)+'% of SHG base',s:shgCov,d:Math.round(shgCov)+'% of the '+(shgTot/1e6).toFixed(1)+'M SHG members statewide (DAY-NRLM) sit in districts with a mapped '+lbl+' — how much existing grassroots infrastructure the seed ecosystem already touches.'}
 ];
 // weights renormalised from jharkhand-landscape's 7-dimension set after dropping
 // "Resource alignment" (needs CSR, which is blocked for Odisha -- see Sources)
 const W=[0.1413,0.2283,0.1848,0.1413,0.1413,0.1630];
 const idx=Math.round(dims.reduce((s,dm,i)=>s+dm.s*W[i],0));
 const b=BAND[band(idx)];
 document.getElementById('hindex').innerHTML=
  '<div class="big">'+idx+'<small>/100</small></div><div class="lbl">Ecosystem Health Index (seed data)</div>'
  +'<span class="band" style="background:'+b[1]+';color:'+b[0]+'">'+b[2]+'</span>'
  +'<div class="desc">'+cov.length+'/'+NDIST+' districts covered, '+aspCov.length+'/'+asp.length+' aspirational districts reached, '+hubs.length+' hubs — all against an 11-org seed set. This score will move a lot once the partner layer is properly researched; read it as a placeholder for the method, not a verdict on Odisha\'s ecosystem.</div>';
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

/* initial render */
refreshScales(); renderStrip(); paint(); buildHealth(); buildMatrix(); buildPlaceHealth(); buildDir(); buildDisTbl(); updateFoot(); buildGovt();
document.getElementById('dircount').textContent='('+PARTNERS.length+' organisations)';
document.querySelectorAll('.collapser[data-wrap]').forEach(tg=>{const wrap=document.getElementById(tg.dataset.wrap);
 tg.addEventListener('click',()=>{const hidden=wrap.classList.toggle('collapsed'); tg.classList.toggle('closed',hidden);});});

/* deep-link: #lens=<key> selects a map lens */
const hl=location.hash.match(/lens=(\w+)/); if(hl&&lenses[hl[1]]){curLens=hl[1];paint();}
</script></body></html>'''

HTML = HTML.replace('__MODEL__', MODEL).replace('__GEO__', GEO)
open("index.html","w").write(HTML)
print("wrote index.html", len(HTML), "bytes")
