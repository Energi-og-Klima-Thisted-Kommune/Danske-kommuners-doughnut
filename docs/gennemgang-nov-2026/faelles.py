"""Fælles indlæsning til analyserne bag docs/akademisk-gennemgang-nov-2026.md.

Replikerer shared.ts' beregning af kategoriscorer og kommunegruppe-visningen
(samme kode som docs/artikler/analyse_artikler.py).
"""
import json
import os

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def sti(*dele):
    return os.path.join(ROOT, *dele)


reg = json.load(open(sti("data", "indikatorer.json")))
kom = json.load(open(sti("data", "kommuner.json")))
m = pd.read_csv(sti("data", "master_indicators.csv"), dtype={"kommune_kode": str})

IND = {i["id"]: i for i in reg["indikatorer"]}
CATS = reg["sociale_kategorier"]
DIMS = reg["oekologiske_dimensioner"]
CATNAVN = {c["id"]: c["name"] for c in CATS}
DIMNAVN = {d["id"]: d["name"] for d in DIMS}
SOC = [i for c in CATS for i in c["indicators"]]
ECO = [i for d in DIMS for i in d["indicators"]]
KAT_AF = {i: c["id"] for c in CATS for i in c["indicators"]}

R = m.pivot(index="kommune_kode", columns="indicator_id", values="ratio")
RAW = m.pivot(index="kommune_kode", columns="indicator_id", values="raw_value")
REF = m.pivot(index="kommune_kode", columns="indicator_id", values="reference")
NAVN = m.drop_duplicates("kommune_kode").set_index("kommune_kode")["kommune_navn"]
GRP = pd.Series({k["kode"]: k["gruppe"] for k in kom["kommuner"]}).loc[R.index]
GRPNAVN = {int(k): v for k, v in kom["grupper"].items()}
FOLK = pd.read_csv(sti("data", "folketal.csv"), dtype={"kommune_kode": str}).set_index("kommune_kode")["folketal"].loc[R.index]
D = pd.DataFrame({d["id"]: R["_dim_" + d["id"]] for d in DIMS})


def inv(i):
    return bool(IND[i].get("inverse"))


def absolut(i):
    return bool(IND[i].get("absolute_score"))


def loft(i):
    return min(IND[i].get("cap", 150), 150)


def socfarve(s):
    s = s.round(1)
    return pd.Series(np.where(s.isna(), "na", np.where(s >= 100, "g", np.where(s >= 85, "a", "r"))), index=s.index)


def ecofarve(s):
    s = s.round(1)
    return pd.Series(np.where(s.isna(), "na", np.where(s <= 85, "g", np.where(s <= 100, "a", "r"))), index=s.index)


def gar(f):
    return f"{(f == 'g').sum()}/{(f == 'a').sum()}/{(f == 'r').sum()}"


def gruppevisning(Rs=None, udelad_selv=False):
    """computeGroupRatios() fra shared.ts. udelad_selv: gruppesnit uden kommunen selv."""
    Rs = R[SOC] if Rs is None else Rs
    out = Rs.copy()
    for i in SOC:
        if absolut(i):
            continue
        col = Rs[i]
        if udelad_selv:
            s = col.groupby(GRP).transform("sum")
            n = col.groupby(GRP).transform("count")
            base = (s - col.fillna(0)) / (n - col.notna().astype(int))
        else:
            base = GRP.map(col.groupby(GRP).mean())
        out[i] = np.minimum((col / base * 100).round(2), loft(i))
    return out


def kategorier(Rs):
    return pd.DataFrame({c["id"]: Rs[c["indicators"]].mean(axis=1) for c in CATS})


def farver(CSx):
    return CSx.apply(socfarve)


def overskrift(t):
    print("\n" + "=" * 78 + "\n" + t + "\n" + "=" * 78)


pd.set_option("display.width", 220)
pd.set_option("display.max_rows", 300)
pd.set_option("display.float_format", lambda x: f"{x:.2f}")
