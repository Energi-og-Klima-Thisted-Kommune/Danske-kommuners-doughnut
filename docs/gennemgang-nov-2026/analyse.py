"""Tallene bag docs/akademisk-gennemgang-nov-2026.md.

Ren diagnose: læser de committede datafiler og skriver en tekstrapport til
stdout. Ændrer ingen filer. Køres fra rodmappen:

    python3 docs/gennemgang-nov-2026/analyse.py

Kræver numpy, pandas og scipy. Afsnit 6 og 7 bruger fire små udtræk i
docs/gennemgang-nov-2026/data/ (hentet 15. nov. 2026):

- dst_sbr01_2025.csv, dst_hjemsyg_2025.csv: DST SBR01 og HJEMSYG for 2025,
  opdelt på alder (Statistikbankens API, BULK med koder).
- dst_folk1a_2025k1_aldersbaand.csv: DST FOLK1A 2025K1 lagt sammen i aldersbånd.
- boliger_fritidshuse_2026.csv: boliger (parcel-, række- og etagehuse) og
  ubeboede fritidshuse pr. kommune, DST BOL105, taget fra søsterprojektet
  forbrugsudledninger (web/data/data.json).

Afsnitsnumrene følger notatets fund.
"""
import os
import sys

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from faelles import (CATS, D, DIMS, FOLK, GRP, GRPNAVN, IND, KAT_AF, NAVN, R, RAW, REF, SOC,  # noqa: E402
                     absolut, ecofarve, farver, gar, gruppevisning, inv, kategorier, loft,
                     overskrift, socfarve, sti)

DATA = sti("docs", "gennemgang-nov-2026", "data")
G = gruppevisning()
CSa, CSg = kategorier(R[SOC]), kategorier(G)


def varians_andel(X, ids):
    """Hver indikators andel af variansen i kategoriens gennemsnit (summerer til 100)."""
    S = X[ids].mean(axis=1)
    ud = {}
    for i in ids:
        ok = X[i].notna()
        ud[i] = np.cov(X[i][ok], S[ok])[0, 1] / S[ok].var() / len(ids) * 100
    return ud


# ------------------------------------------------------------------ 1
def implicitte_vaegte():
    overskrift("1. Implicitte vægte: andel af kategoriens varians (nominel vægt er 100/n)")
    rows = []
    for c in CATS:
        ids = c["indicators"]
        if len(ids) < 2:
            continue
        va, vg = varians_andel(R[SOC], ids), varians_andel(G, ids)
        for i in ids:
            rows.append((c["name"], i, "ja" if inv(i) else "", RAW[i].std() / RAW[i].mean() * 100,
                         100 / len(ids), va[i], vg[i]))
    df = pd.DataFrame(rows, columns=["kategori", "indikator", "vendt", "CV% rå", "nominel%", "landsgns%", "gruppe%"])
    print(df.to_string(index=False))
    print("\nKategoriens spredning og farver (grøn/gul/rød), landsgennemsnit og kommunegruppe:")
    for c in CATS:
        k = c["id"]
        print(f"  {c['name']:16s} n={len(c['indicators'])}  sd {CSa[k].std():5.1f} / {CSg[k].std():5.1f}"
              f"   {gar(socfarve(CSa[k])):>9s} / {gar(socfarve(CSg[k])):>9s}")


# ------------------------------------------------------------------ 2
def framing():
    overskrift("2. Samme tal, modsat formulering: andel der har (nu) mod andel der mangler")
    print("ratio som nu: værdi/ref. Som mangel: (100-ref)/(100-værdi), dvs. den vendte brøk på komplementet.")
    for i in ["selvvurderet_helbred", "employment", "youth_education", "education", "voter_turnout_national",
              "income_gender_gap"]:
        x = RAW[i]
        ref = IND[i]["reference"]["value"] if IND[i]["reference"]["type"] == "maal" else REF[i].iloc[0]
        r1 = np.minimum(x / ref * 100, 150)
        r2 = np.minimum((100 - ref) / (100 - x) * 100, 150)
        print(f"  {i:24s} ref {ref:5.1f}  nu: sd {r1.std():4.1f}, under 85: {int((r1.round(1) < 85).sum()):2d}"
              f"   som mangel: sd {r2.std():4.1f}, under 85: {int((r2.round(1) < 85).sum()):2d}")
    x = RAW["education"]
    print("  education efter den økologiske rings komplementformel (100-x)/(100-95)*100:",
          f"median {((100 - x) / 5 * 100).median():.0f}, kommuner inden for målet: {int((x >= 95).sum())}")


# ------------------------------------------------------------------ 3
def uddannelse_overlap():
    overskrift("3. Uddannelse: education (30-34 år) og low_education (25-29 år) er hinandens komplement")
    a, b = RAW["education"], RAW["low_education"]
    print(f"  korrelation rå: {a.corr(b):.2f}   sum af de to andele: gns {(a + b).mean():.1f}, sd {(a + b).std():.1f}")
    print("  HFUDD-koder i education (fetch_doughnut_data.py): H20 gymnasial, H30, H35, H40-H80")
    u = ["education", "low_education", "youth_education", "exam_grade", "neet", "disposable_income"]
    print(RAW[u].corr().round(2).to_string())


# ------------------------------------------------------------------ 4
def stoej():
    """År-til-år-støj: residualer om kommunens egen lineære udvikling, efter at årets
    fælles niveau (medianen over kommunerne) er trukket fra. Seneste 8 år."""
    H = pd.read_csv(sti("data", "trend_history_raw.csv"), dtype={"kommune_kode": str})
    ud = {}
    for i, h in H.groupby("indicator_id"):
        if i not in IND:
            continue
        w = h.pivot(index="kommune_kode", columns="aar", values="vaerdi")
        if w.shape[1] < 6:
            continue
        w = w.iloc[:, -8:]
        wd = w - w.median(axis=0)
        yrs = np.array(w.columns, dtype=float)
        res = {}
        for k, r in wd.iterrows():
            ok = r.notna().values
            if ok.sum() < 5:
                continue
            b = np.polyfit(yrs[ok], r.values[ok], 1)
            e = r.values[ok] - np.polyval(b, yrs[ok])
            res[k] = np.sqrt((e ** 2).sum() / (ok.sum() - 2))
        ud[i] = (pd.Series(res), w.iloc[:, -1].var(), w.shape[1])
    return ud


def reliabilitet(ST):
    overskrift("4. Reliabilitet: forskelle mellem kommuner mod støj fra år til år")
    rows = []
    for i, (s, vb, n) in ST.items():
        x, ref = RAW[i].reindex(s.index), REF[i].reindex(s.index)
        if IND[i]["reference"]["type"] == "maal":
            ref = ref * 0 + IND[i]["reference"]["value"]
        smaa, store = FOLK[FOLK < 25000].index.intersection(s.index), FOLK[FOLK >= 50000].index.intersection(s.index)
        rows.append((i, IND[i]["category"][:3], n, np.sqrt(vb), s.median(), 1 - (s ** 2).mean() / vb,
                     int(((x - ref).abs() < 1.96 * s).sum()), len(s), s[smaa].median() / s[store].median()))
    df = pd.DataFrame(rows, columns=["indikator", "ring", "år", "sd mellem", "støj (median)", "reliabilitet",
                                     "ikke skelnelig fra ref", "n", "støj små/store"]).sort_values("reliabilitet")
    print(df.to_string(index=False))
    print("\nKategoriniveau: standardfejl fra støjen (delta-metoden, uafhængige indikatorer, kun dem med serie)")
    for navn, Rs, CS in [("landsgns", R[SOC], CSa), ("gruppe", G, CSg)]:
        tot = usik = 0
        for c in CATS:
            ids = c["indicators"]
            var = pd.Series(0.0, index=R.index)
            med = 0
            for i in ids:
                if i not in ST:
                    continue
                sr = (Rs[i] / RAW[i]).abs() * ST[i][0].reindex(R.index)
                var = var + sr.where(Rs[i] < loft(i), 0).fillna(0) ** 2
                med += 1
            se = np.sqrt(var) / Rs[ids].notna().sum(axis=1)
            sc = CS[c["id"]]
            u = int((np.minimum((sc - 100).abs(), (sc - 85).abs()) < 1.96 * se).sum())
            tot += sc.notna().sum()
            usik += u
            print(f"  {navn:9s}{c['name']:16s} serier {med}/{len(ids)}  median SE {se.median():4.1f}"
                  f"  farver inden for 1,96 SE af en grænse: {u}")
        print(f"  {navn}: {usik} af {tot}")


# ------------------------------------------------------------------ 5
def pile():
    overskrift("5. Retningspile: er udviklingen en monoton tendens? (Mann-Kendall, p < 0,10, serier på 8+ år)")
    H = pd.read_csv(sti("data", "trend_history_raw.csv"), dtype={"kommune_kode": str})
    T = pd.read_csv(sti("data", "trend_indicators.csv"), dtype={"kommune_kode": str})
    out = []
    for i, h in H.groupby("indicator_id"):
        if i not in IND:
            continue
        w = h.pivot(index="kommune_kode", columns="aar", values="vaerdi")
        if w.shape[1] < 8:
            continue
        t = T[T.indicator_id == i].set_index("kommune_kode")
        for k, r in w.iterrows():
            r = r.dropna()
            if len(r) < 8 or k not in t.index:
                continue
            out.append((i, t.loc[k, "retning"], stats.kendalltau(r.index.values, r.values)[1] < 0.10))
    o = pd.DataFrame(out, columns=["ind", "retning", "signifikant"])
    print(pd.crosstab(o.retning, o.signifikant, margins=True).to_string())
    x = o[o.retning.isin(["rigtig", "tempo", "forkert"])]
    print(f"  pile med vurdering uden signifikant tendens: {(~x.signifikant).sum()} af {len(x)} ({(1 - x.signifikant.mean()) * 100:.0f} %)")
    print("  andel signifikante, laveste indikatorer:")
    print(x.groupby("ind").signifikant.mean().sort_values().head(8).round(2).to_string())


# ------------------------------------------------------------------ 6
def alder():
    overskrift("6. Aldersstruktur: rå rater mod aldersstandardiserede")
    A = pd.read_csv(os.path.join(DATA, "dst_folk1a_2025k1_aldersbaand.csv"), dtype={"kommune_kode": str}).set_index("kommune_kode").loc[R.index]
    tot = A.sum(axis=1)
    baand = list(A.columns)
    idx = {b: n for n, b in enumerate(baand)}
    ALD = pd.DataFrame({"a0_19": A[baand[:idx["15-19"] + 1]].sum(axis=1) / tot * 100,
                        "a65": A[baand[idx["65-69"]:]].sum(axis=1) / tot * 100,
                        "a80": A[baand[idx["80-84"]:]].sum(axis=1) / tot * 100})
    print("  andel 65+ pr. kommune: min %.1f, median %.1f, max %.1f" % (ALD.a65.min(), ALD.a65.median(), ALD.a65.max()))
    rows = []
    for i in SOC:
        y = RAW[i].dropna()
        X = np.column_stack([np.ones(len(y)), ALD.loc[y.index].values])
        b = np.linalg.lstsq(X, y.values, rcond=None)[0]
        rows.append((i, KAT_AF[i], y.corr(ALD.a65.loc[y.index]), 1 - ((y.values - X @ b) ** 2).sum() / ((y - y.mean()) ** 2).sum()))
    df = pd.DataFrame(rows, columns=["indikator", "kategori", "r med 65+", "R2 (0-19, 65+, 80+)"])
    print(df.sort_values("R2 (0-19, 65+, 80+)", ascending=False).head(16).to_string(index=False))

    # hospital_long: direkte standardisering med landets aldersfordeling (SBR01's egne persontal)
    s = pd.read_csv(os.path.join(DATA, "dst_sbr01_2025.csv"), sep=";", dtype=str)
    s = s[s.ALDER != "TOT"]
    s["v"] = pd.to_numeric(s.INDHOLD, errors="coerce")
    pers = s[s["OPHOLD_PÅ_SYGEHUS"] == "200100"].pivot(index="KOMMUNEDK", columns="ALDER", values="v")
    lang = s[s["OPHOLD_PÅ_SYGEHUS"] == "200230"].pivot(index="KOMMUNEDK", columns="ALDER", values="v")
    std = pers.loc["000"] / pers.loc["000"].sum()
    raa = (lang.sum(axis=1) / pers.sum(axis=1) * 100)
    dsr = ((lang / pers) * std).sum(axis=1) * 100
    ref = raa["000"]
    h_raa = np.minimum(ref / raa.loc[R.index] * 100, 150)
    h_std = np.minimum(ref / dsr.loc[R.index] * 100, 150)

    # hjemsyg: indirekte standardisering (observeret mod forventet ved landets aldersrater)
    h = pd.read_csv(os.path.join(DATA, "dst_hjemsyg_2025.csv"), sep=";", dtype=str)
    h = h[h["OMRÅDE"].isin(R.index)]
    h["v"] = pd.to_numeric(h.INDHOLD, errors="coerce")
    hp = h.pivot(index="OMRÅDE", columns="ALDER1", values="v").loc[R.index]
    grupper = {"100": baand[:idx["60-64"] + 1], "375": ["65-69"], "400": ["70-74"], "500": ["75-79"],
               "600": ["80-84"], "700": ["85-89"], "800": ["90-"]}
    N = pd.DataFrame({k: A[v].sum(axis=1) for k, v in grupper.items()})
    forventet = (N * (hp[list(grupper)].sum() / N.sum())).sum(axis=1)
    smr = hp[list(grupper)].sum(axis=1) / forventet * 100
    raa_h = hp["050"] / tot * 1000
    j_raa = np.minimum(hp["050"].sum() / tot.sum() * 1000 / raa_h * 100, 150)
    j_std = np.minimum(100 / smr * 100, 150)

    for navn, a, b in [("hospital_long", h_raa, h_std), ("hjemsyg", j_raa, j_std)]:
        print(f"\n  {navn}: farver {gar(socfarve(a))} -> {gar(socfarve(b))}, skift {(socfarve(a) != socfarve(b)).sum()},"
              f" rangkorrelation {a.corr(b, method='spearman'):.2f}")
        t = pd.DataFrame({"kommune": NAVN, "65+ %": ALD.a65, "rå": a, "standardiseret": b, "ændring": b - a}).sort_values("ændring")
        print(t.iloc[[0, 1, 2, -3, -2, -1]].round(1).to_string(index=False))
    R2 = R[SOC].copy()
    R2["hospital_long"], R2["hjemsyg"] = h_std, j_std
    for navn, a, b in [("landsgns", R[SOC], R2), ("gruppe", G, gruppevisning(R2))]:
        ca, cb = kategorier(a)["sundhed"], kategorier(b)["sundhed"]
        print(f"  Sundhed ({navn}): {gar(socfarve(ca))} -> {gar(socfarve(cb))}, farveskift {(socfarve(ca) != socfarve(cb)).sum()},"
              f" gns. ændring {(cb - ca).abs().mean():.1f}, største {(cb - ca).abs().max():.1f}")
    return ALD


# ------------------------------------------------------------------ 7
def naevnere(ALD):
    overskrift("7. Nævnere: pr. indbygger, hvor de udsatte er noget andet")
    B = pd.read_csv(os.path.join(DATA, "boliger_fritidshuse_2026.csv"), dtype={"kommune_kode": str}).set_index("kommune_kode").loc[R.index]
    enh = B.boliger + B.fritidshuse
    fa = B.fritidshuse / enh * 100
    vs = RAW["vejr_skader"]
    skader = vs * FOLK / 1000
    r1 = np.minimum(skader.sum() / FOLK.sum() * 1000 / vs * 100, 150)
    alt = skader / enh * 1000
    r2 = np.minimum(skader.sum() / enh.sum() * 1000 / alt * 100, 150)
    print(f"  vejr_skader pr. 1.000 indb.: rangkorrelation med fritidshusandel {vs.corr(fa, method='spearman'):.2f};"
          f" pr. 1.000 boliger og fritidshuse: {alt.corr(fa, method='spearman'):.2f}")
    print(f"  farver {gar(socfarve(r1))} -> {gar(socfarve(r2))}, skift {(socfarve(r1) != socfarve(r2)).sum()}")
    t = pd.DataFrame({"kommune": NAVN, "fritidshuse %": fa, "pr. indb.": r1, "pr. enhed": r2, "ændring": r2 - r1}).sort_values("ændring")
    print(t.iloc[[0, 1, -4, -3, -2, -1]].round(1).to_string(index=False))
    for i in ["crime_rate", "traffic_accidents", "kystrisiko"]:
        print(f"  {i}: rangkorrelation med fritidshusandel {RAW[i].corr(fa, method='spearman'):.2f}")
    ms = RAW["music_school"]
    pr_ung = ms / (ALD.a0_19 / 100)
    ref_ung = (ms * FOLK).sum() / (ALD.a0_19 / 100 * FOLK).sum()
    m1 = np.minimum(ms / REF["music_school"] * 100, 150)
    m2 = np.minimum(pr_ung / ref_ung * 100, 150)
    print(f"  music_school pr. 0-19-årig i stedet for pr. indbygger: farveskift {(socfarve(m1) != socfarve(m2)).sum()},"
          f" rangkorrelation {m1.corr(m2, method='spearman'):.2f}")


# ------------------------------------------------------------------ 8
def gruppereference():
    overskrift("8. Kommunegruppen som reference")
    fa = farver(CSg)
    Gl = gruppevisning(udelad_selv=True)
    fl = farver(kategorier(Gl))
    for g in sorted(GRP.unique()):
        idx = GRP.index[GRP == g]
        print(f"  {GRPNAVN[g]:20s} n={len(idx):2d}  gns. afstand til 100: {(G.loc[idx] - 100).abs().mean().mean():4.1f}"
              f" med kommunen selv i snittet, {(Gl.loc[idx] - 100).abs().mean().mean():4.1f} uden;"
              f" farveskift {int((fa.loc[idx] != fl.loc[idx]).sum().sum())} af {len(idx) * len(CATS)}")
    alt = G.copy()
    for i in SOC:
        if absolut(i) or i == "kystrisiko":
            continue
        x = RAW[i]
        gm = GRP.map(x.groupby(GRP).mean())
        alt[i] = np.minimum(((gm / x) if inv(i) else (x / gm)) * 100, loft(i))
    falt = farver(kategorier(alt))
    print(f"  gruppesnit af råværdier i stedet for af scorer: {int((falt != fa).sum().sum())} af {fa.size} farver skifter")
    print("  " + ", ".join(f"{c['name']} {int((falt[c['id']] != fa[c['id']]).sum())}" for c in CATS if (falt[c['id']] != fa[c['id']]).sum()))


# ------------------------------------------------------------------ 9
def standardiseret():
    overskrift("9. Følsomhed: standardiseret afstand (100 + 10 z, klippet ved 3 sd) i stedet for ratio")
    Z = R[SOC].copy()
    for i in SOC:
        if absolut(i):
            continue
        z = (REF[i] - RAW[i]) / RAW[i].std() if inv(i) else (RAW[i] - REF[i]) / RAW[i].std()
        Z[i] = 100 + 10 * z.clip(-3, 3)
        if i == "kystrisiko":
            Z[i] = np.minimum(Z[i], 100)
    CSz = kategorier(Z)
    for c in CATS:
        k, ids = c["id"], c["indicators"]
        if len(ids) < 2:
            continue
        flyt = (CSa[k].rank() - CSz[k].rank()).abs()
        v = varians_andel(Z, ids)
        print(f"  {c['name']:16s} rangkorrelation {CSa[k].corr(CSz[k], method='spearman'):.2f}, median rangflyt {flyt.median():4.1f},"
              f" flytter 20+ pladser: {int((flyt >= 20).sum()):2d}, vægte {min(v.values()):5.1f}-{max(v.values()):4.1f} %")


# ------------------------------------------------------------------ 10
def oekologisk():
    overskrift("10. Den økologiske ring")
    fc = RAW["forbrug_co2"]
    print(f"  forbrug_co2: befolkningsvægtet gennemsnit af kommunerne {(fc * FOLK).sum() / FOLK.sum():.2f} ton,"
          f" spænd {fc.min():.1f}-{fc.max():.1f}; korrelation med median indkomst {fc.corr(RAW['disposable_income']):.2f}")
    for d in DIMS:
        ids = d["indicators"]
        binder = ""
        if len(ids) > 1 and d.get("aggregation") != "gennemsnit":
            binder = ", ".join(f"{i} {int((R[i] == R[ids].max(axis=1)).sum())}" for i in ids)
        print(f"  {d['name']:18s} {gar(ecofarve(D[d['id']])):>9s}  {binder}")
    kem, aff = ["pesticider", "nitrat"], ["cirkularitet_recycling", "cirkularitet_waste"]
    print(f"  Forurening delt: grundvand worst-of {gar(ecofarve(R[kem].max(axis=1)))}, affald worst-of {gar(ecofarve(R[aff].max(axis=1)))}")
    print("  korrelationer mellem Forurenings fire indikatorer:")
    print(R[kem + aff].corr().round(2).to_string())
    pm = RAW["luftkvalitet_pm25"]
    print(f"  PM2.5: {pm.min():.1f}-{pm.max():.1f} µg/m³; over 5: {(pm > 5).sum()}, over 7,5: {(pm > 7.5).sum()}, over 10: {(pm > 10).sum()}")
    for i in ["bio_vasentlig", "bio_uerstattelig"]:
        print(f"  {i}: median {RAW[i].median():.1f} %, kommuner over målet: {(RAW[i] >= IND[i]['reference']['value']).sum()}")


# ------------------------------------------------------------------ 11
def sundhedsprofil():
    overskrift("11. Sundhedsprofilen: stikprøveusikkerhed ved et antaget antal svar (simpel tilfældig udvælgelse)")
    sp = ["selvvurderet_helbred", "mentalt_helbred", "rygning", "alkohol", "kost", "svaer_overvaegt", "ensomhed", "social_stoette"]
    for n in (290, 900, 1380):
        print(f"  n = {n} (290: Læsø, 900: kommune med minimumsstikprøven, 1.380: gennemsnitskommunen)")
        for i in sp:
            p = RAW[i] / 100
            se = np.sqrt(p * (1 - p) / n) * 100
            print(f"    {i:22s} sd mellem {RAW[i].std():4.2f}  SE {se.mean():4.2f} pp  reliabilitet {1 - (se ** 2).mean() / RAW[i].var():5.2f}"
                  f"  ikke skelnelig fra landstallet: {int(((RAW[i] - REF[i]).abs() < 1.96 * se).sum()):2d}"
                  f"  95 %-interval ±{(1.96 * se / RAW[i] * 100).mean():.0f} scorepoint")


if __name__ == "__main__":
    implicitte_vaegte()
    framing()
    uddannelse_overlap()
    ST = stoej()
    reliabilitet(ST)
    pile()
    ALD = alder()
    naevnere(ALD)
    gruppereference()
    standardiseret()
    oekologisk()
    sundhedsprofil()
