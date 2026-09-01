#!/usr/bin/env python3
"""Add a "district" property (= canon name) to each feature, matching
jharkhand-landscape's jh_enriched.geojson shape, which the map renderer in build.py
expects (f.properties.district). Bharatlas's own property is "dtname", which already
matches CANON exactly for all 30 districts, so this is a straight rename.

Also simplifies ring geometry (Douglas-Peucker, ~150k points total in the raw Bharatlas
LGD file -- far more detail than a 760x560px inline SVG map needs or can render smoothly)
and rounds coordinates to 3 decimal places (~110m, still sub-pixel at this map size)
with consecutive-duplicate removal, to keep the inlined GeoJSON small.

Run from scripts/: python3 enrich_geojson.py
"""
import json

TOLERANCE_DEG = 0.003  # ~300m at this latitude; tune down if districts look too blocky


def dp_simplify(points, tol):
    """Classic Douglas-Peucker on a list of [x,y] points."""
    if len(points) < 3:
        return points

    def perp_dist(pt, a, b):
        (x, y), (ax, ay), (bx, by) = pt, a, b
        dx, dy = bx - ax, by - ay
        if dx == 0 and dy == 0:
            return ((x - ax) ** 2 + (y - ay) ** 2) ** 0.5
        t = ((x - ax) * dx + (y - ay) * dy) / (dx * dx + dy * dy)
        t = max(0, min(1, t))
        px, py = ax + t * dx, ay + t * dy
        return ((x - px) ** 2 + (y - py) ** 2) ** 0.5

    def rdp(pts):
        if len(pts) < 3:
            return pts
        a, b = pts[0], pts[-1]
        idx, maxd = -1, 0.0
        for i in range(1, len(pts) - 1):
            d = perp_dist(pts[i], a, b)
            if d > maxd:
                idx, maxd = i, d
        if maxd > tol:
            left = rdp(pts[: idx + 1])
            right = rdp(pts[idx:])
            return left[:-1] + right
        return [a, b]

    return rdp(points)


def simplify_ring(ring, tol):
    pts = dp_simplify(ring, tol)
    if len(pts) < 4:  # not a valid closed ring anymore -> keep original
        return ring
    return pts


DECIMALS = 3  # ~110m; sub-pixel at 760x560 over Odisha's extent


def finish_ring(ring, tol):
    """Simplify, round to DECIMALS, and drop consecutive duplicate points."""
    pts = simplify_ring(ring, tol)
    out, last = [], None
    for p in pts:
        r = [round(p[0], DECIMALS), round(p[1], DECIMALS)]
        if r != last:
            out.append(r)
            last = r
    if len(out) >= 4 and out[0] != out[-1]:
        out.append(out[0])
    return out if len(out) >= 4 else [[round(p[0], DECIMALS), round(p[1], DECIMALS)] for p in ring]


def simplify_geometry(geom, tol):
    if geom["type"] == "Polygon":
        geom["coordinates"] = [finish_ring(ring, tol) for ring in geom["coordinates"]]
    elif geom["type"] == "MultiPolygon":
        geom["coordinates"] = [
            [finish_ring(ring, tol) for ring in poly] for poly in geom["coordinates"]
        ]
    return geom


def count_points(geom):
    n = 0

    def walk(a):
        nonlocal n
        if isinstance(a[0], (int, float)):
            n += 1
        else:
            for x in a:
                walk(x)

    walk(geom["coordinates"])
    return n


if __name__ == "__main__":
    d = json.load(open("../data/odisha_districts.geojson"))
    before = sum(count_points(f["geometry"]) for f in d["features"])
    for f in d["features"]:
        f["properties"] = {"district": f["properties"]["dtname"]}
        simplify_geometry(f["geometry"], TOLERANCE_DEG)
    after = sum(count_points(f["geometry"]) for f in d["features"])
    d.pop("name", None)  # drop unused top-level label to trim the inlined payload
    json.dump(d, open("../odisha_enriched.geojson", "w"), separators=(",", ":"))
    print(f"wrote odisha_enriched.geojson: {len(d['features'])} features, "
          f"{before} -> {after} coordinate points")
