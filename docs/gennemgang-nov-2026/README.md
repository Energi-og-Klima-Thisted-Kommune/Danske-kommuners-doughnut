# Analysen bag den akademiske gennemgang (november 2026)

Tallene i `docs/akademisk-gennemgang-nov-2026.md` kommer fra `analyse.py`. Scriptet læser de committede datafiler, skriver en tekstrapport og ændrer intet. Det er ikke en del af datapipelinen.

```bash
python3 -m pip install numpy pandas scipy
python3 docs/gennemgang-nov-2026/analyse.py
```

- `faelles.py`: indlæsning og en kopi af `shared.ts`' kategoriscorer og kommunegruppe-visning (samme kode som `docs/artikler/analyse_artikler.py`).
- `analyse.py`: elleve afsnit, nummereret som i scriptets docstring. Notatets fund henviser til dem.
- `data/`: fire små udtræk hentet 15. november 2026, så analysen kan køres uden netadgang.
  - `dst_sbr01_2025.csv`, `dst_hjemsyg_2025.csv`: DST SBR01 og HJEMSYG for 2025 opdelt på alder.
  - `dst_folk1a_2025k1_aldersbaand.csv`: DST FOLK1A 2025K1 lagt sammen i aldersbånd.
  - `boliger_fritidshuse_2026.csv`: boliger og ubeboede fritidshuse pr. kommune (DST BOL105), taget fra søsterprojektet forbrugsudledninger.

Tallene er et øjebliksbillede af masterfilen ved commit `7ee9884`. Opdateres data, flytter de sig.
