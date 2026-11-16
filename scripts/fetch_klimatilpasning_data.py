#!/usr/bin/env python3
"""
fetch_klimatilpasning_data.py

Henter F&P's (Forsikring & Pension) vejrrelaterede skadestatistik for alle 98
kommuner og regner den om fra skader pr. 1.000 indbyggere til skader pr. 1.000
boliger og fritidshuse.

Datakilde: Datawrapper-kort publiceret af F&P i november 2025.
Analyse: "Sådan er Danmark blevet ramt af vejrrelaterede skader de seneste år"
URL: https://fogp.dk/tal-og-analyser/saadan-er-danmark-blevet-ramt-af-vejrrelaterede-skader-de-seneste-aar/

Tidsperiode: Q1 2023 - Q4 2025 (2,5 år akkumuleret)
Dækning: ~90% af forsikringsmarkedet

OBS: Indikatoren er en PROXY for vejrrelateret sårbarhed, ikke en direkte
målestok for klimatilpasningskapacitet. Se data/klimatilpasning.md for fuld
metodediskussion og fremtidige forbedringer.

Output: data/klimatilpasning_scores.csv
Kolonner: kommune_kode, kommune_navn, vejr_skader_raw, vejr_skader_ratio, vejr_skader_ref, vejr_skader_pr_indb

Kilden har kun kommunenavne. Koden slås op i data/kommuner.json, og et navn
der ikke kan slås op, stopper scriptet (build_master_csv.py nøgler på kode).

Nævner (fra nov. 2026): boliger og fritidshuse (DST BOL105, alle anvendelser,
beboede og ubeboede). Skaderne sker på bygninger, også fritidshuse, og F&P's
tal pr. 1.000 indbyggere fulgte andelen af fritidshuse (rangkorrelation 0,59):
Fanø og Odsherred, hvor over halvdelen af boligenhederne er fritidshuse, stod
med to til tre gange landstallet, fordi skaderne blev delt med de fastboende
alene. Antallet af skader regnes tilbage af F&P's rate og folketallet 1. januar
2025 og deles med boligenhederne samme år. F&P's rate er afrundet til hele
tal, så antallet er et skøn (docs/akademisk-gennemgang-nov-2026.md, afsnit 2.4).
Erhvervsbygninger er ikke i nævneren.

Ratio-konvention: INVERS social indikator.
  ratio = (landstal / kommune_val) * 100
  100 = på landstallet, >100 = bedre (færre skader), <100 = værre

Landstallet er Danmark som helhed: kommunernes skader samlet delt med deres
boliger og fritidshuse samlet. Skrives i vejr_skader_ref. F&P's oprindelige
tal står i vejr_skader_pr_indb.

Kør fra projektets rodmappe:
  python3 scripts/fetch_klimatilpasning_data.py
"""

import csv
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from kommuner import kode_for_navn  # noqa: E402  (de 98 kommuner, data/kommuner.json)
from dst import api_post, folketal, pr_kommune_aar  # noqa: E402  (fælles DST-kald)

BEFOLKNINGSAAR = "2025"   # slutåret for skadesperioden 2023-2025; også året for boligtallet

DATA_URL = "https://datawrapper.dwcdn.net/NDLlA/4/dataset.csv"
OUTPUT_FILE = Path(__file__).parent.parent / "data" / "klimatilpasning_scores.csv"

# Navne-mapping: Datawrapper-navne → kanoniske kommunenavne i projektet
# Kun nødvendig hvis der er uoverensstemmelser. Her er navnene direkte brugbare.
NAME_CORRECTIONS = {
    # "Datawrapper-navn": "Projektnavn",
    # Ingen korrektioner nødvendige per maj 2026
}


def fetch_data() -> list[dict]:
    """Henter CSV fra Datawrapper og returnerer liste af dicts."""
    print(f"Henter vejrskadedata fra F&P (Datawrapper)...")
    request = urllib.request.Request(
        DATA_URL,
        headers={"User-Agent": "Mozilla/5.0 (compatible; doughnut-data-fetcher/1.0)"},
    )
    req = urllib.request.urlopen(request, timeout=20)
    content = req.read().decode("utf-8")
    reader = csv.DictReader(content.splitlines())
    rows = list(reader)
    print(f"  Modtaget {len(rows)} kommuner")
    return rows


def boligenheder(aar: str) -> dict[str, float]:
    """Boliger og fritidshuse pr. kommune (DST BOL105): alle anvendelser, både
    beboede boliger, ubeboede boliger og ubeboede fritidshuse."""
    rows = api_post("BOL105", [
        {"code": "AMT", "values": ["*"]},
        {"code": "BEBO", "values": ["1000", "2000", "5000"]},
        {"code": "Tid", "values": [aar]},
    ])
    return {k: v for (k, a), v in pr_kommune_aar(rows, "AMT").items() if k != "000"}


def compute_scores(rows: list[dict]) -> tuple[list[dict], float]:
    """
    Regner F&P's skader pr. 1.000 indb. om til skader pr. 1.000 boliger og
    fritidshuse og beregner den inverse ratio (landstal / kommune_val) * 100.
    Færre skader = højere score. Landstallet er Danmark som helhed, se
    modulets docstring.
    """
    results = []
    for row in rows:
        navn = row["kom"].strip()
        navn = NAME_CORRECTIONS.get(navn, navn)
        try:
            pr_indb = float(row["antal skader pr 1000"])
        except (ValueError, KeyError):
            pr_indb = None
        results.append({"kommune_kode": kode_for_navn(navn), "kommune_navn": navn,
                        "vejr_skader_pr_indb": pr_indb})

    ukendte = [r["kommune_navn"] for r in results if r["kommune_kode"] is None]
    if ukendte:
        print(f"FEJL: kommunenavne der ikke findes i data/kommuner.json: {ukendte}\n"
              "  Tilføj en rettelse i NAME_CORRECTIONS.", file=sys.stderr)
        sys.exit(1)

    folk = {k: v for (k, a), v in folketal([BEFOLKNINGSAAR]).items() if k != "000"}
    enheder = boligenheder(BEFOLKNINGSAAR)
    print(f"  Boliger og fritidshuse (BOL105, {BEFOLKNINGSAAR}): {sum(enheder.values()):,.0f} i {len(enheder)} kommuner")
    for r in results:
        k, pr_indb = r["kommune_kode"], r["vejr_skader_pr_indb"]
        ok = pr_indb is not None and folk.get(k) and enheder.get(k)
        r["_skader"] = pr_indb * folk[k] / 1000 if ok else None
        r["vejr_skader_raw"] = round(r["_skader"] / enheder[k] * 1000, 2) if ok else None
    med = [r for r in results if r["_skader"] is not None]
    if not med:
        print("FEJL: Ingen gyldige værdier fundet", file=sys.stderr)
        sys.exit(1)
    national_avg = round(sum(r["_skader"] for r in med)
                         / sum(enheder[r["kommune_kode"]] for r in med) * 1000, 4)
    print(f"  Landstal: {national_avg:.2f} skader pr. 1.000 boliger og fritidshuse")

    for r in results:
        raw = r["vejr_skader_raw"]
        r["vejr_skader_ratio"] = round((national_avg / raw) * 100, 2) if raw else None
        r["vejr_skader_ref"] = national_avg
    return results, national_avg


def write_csv(results: list[dict]) -> None:
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["kommune_kode", "kommune_navn", "vejr_skader_raw", "vejr_skader_ratio",
                                               "vejr_skader_ref", "vejr_skader_pr_indb"],
                                extrasaction="ignore")
        writer.writeheader()
        writer.writerows(results)
    print(f"  Gemt: {OUTPUT_FILE}")
    print(f"  Rækker: {len(results)}")


def main():
    rows = fetch_data()
    results, national_avg = compute_scores(rows)

    # Vis top 5 hårdest og mindst ramt
    sorted_by_raw = sorted(results, key=lambda x: x["vejr_skader_raw"] or 0)
    print("\nMindst ramt (lavest råværdi → højest score):")
    for r in sorted_by_raw[:5]:
        print(f"  {r['kommune_navn']}: {r['vejr_skader_raw']} skader/1.000 enheder → score {r['vejr_skader_ratio']}")
    print("Hårdest ramt (højest råværdi → lavest score):")
    for r in sorted_by_raw[-5:]:
        print(f"  {r['kommune_navn']}: {r['vejr_skader_raw']} skader/1.000 enheder → score {r['vejr_skader_ratio']}")

    write_csv(results)
    print("\nFærdigt.")


if __name__ == "__main__":
    main()

    # ───────────────────────────────────────────────────────────
    # AUTO-REBUILD af master_indicators.csv
    # ───────────────────────────────────────────────────────────
    try:
        import sys as _sys
        from pathlib import Path as _Path
        _sys.path.insert(0, str(_Path(__file__).resolve().parent))
        from build_master_csv import auto_build_master
        auto_build_master()
    except Exception as _e:
        print(f"\n⚠ Kunne ikke auto-rebuild master-CSV: {_e}")
        print("  Rådata er gemt. Kør manuelt: python3 scripts/build_master_csv.py")
