"""
UYSM_merged_v2.csv
------------------
Koordinatlar yeniden hesaplanmis:
  - Oncelik 1: hansay.xlsx Enlem_O / Boylam_O (dogrulanmis degerler)
  - Oncelik 2: DDMM.MMM formuluyle orijinal raw deger
  - Oncelik 3: Eski yanlis deger (koordinat_kaynagi = 'eski_yanlis')
Orjinal UYSM_merged.csv dokunulmadan korunur.
"""

import pandas as pd
import numpy as np
import re

MERGED  = r"D:\_Development\Projects\UYSM_Projects\data\processed\UYSM_merged.csv"
HANSAY  = r"D:\_Development\Projects\UYSM_Projects\data\source\hansay.xlsx"
CIKTI   = r"D:\_Development\Projects\UYSM\UYSM_merged_v2.csv"


def normalize_ad(s):
    if not isinstance(s, str): return ""
    tr = {"\u00e7":"c","\u011f":"g","\u0131":"i","\u0130":"i",
          "\u00f6":"o","\u015f":"s","\u00fc":"u",
          "\u00c7":"c","\u011e":"g","\u00d6":"o","\u015e":"s","\u00dc":"u"}
    return re.sub(r"\s+", " ", "".join(tr.get(c,c) for c in s.strip().lower())).strip()


def ddmm_to_decimal(raw):
    """DDMM.MMM formatini ondalik dereceye cevirir. Gecersizse None."""
    if raw is None or pd.isna(raw): return None
    try:
        v = int(float(str(raw)))
        if v <= 0: return None
        s = str(v)
        if len(s) < 4: return float(v)
        dd  = int(s[:2])
        mm_str = s[2:]
        mm  = float(mm_str[:2] + "." + mm_str[2:]) if len(mm_str) > 2 else float(mm_str)
        if mm >= 60: return None   # gecersiz dakika
        return round(dd + mm / 60, 7)
    except:
        return None


# ── Verileri yukle ────────────────────────────────────────────────────────────
merged = pd.read_csv(MERGED)

hansay_raw = pd.read_excel(HANSAY, header=1, sheet_name="hansay1")
hansay_raw.columns = [c.strip() for c in hansay_raw.columns]
hansay_raw = hansay_raw.map(lambda x: x.strip() if isinstance(x, str) else x)
hansay_raw["lat_h"] = pd.to_numeric(hansay_raw["Enlem_O"],  errors="coerce")
hansay_raw["lon_h"] = pd.to_numeric(hansay_raw["Boylam_O"], errors="coerce")
hansay_raw["key"]   = hansay_raw["DosyaAdi"].apply(normalize_ad)
hansay_lookup = hansay_raw[hansay_raw["lat_h"].notna()].set_index("key")[["lat_h","lon_h"]]

merged["key"] = merged["dosya_adi"].apply(normalize_ad)

# ── Koordinat guncelleme ──────────────────────────────────────────────────────
v2 = merged.copy()
v2["koordinat_kaynagi"] = ""

for idx, row in v2.iterrows():
    key = row["key"]

    # Oncelik 1: hansay
    if key in hansay_lookup.index:
        h = hansay_lookup.loc[key]
        v2.at[idx, "enlem"]  = h["lat_h"]
        v2.at[idx, "boylam"] = h["lon_h"]
        v2.at[idx, "koordinat_kaynagi"] = "hansay"
        continue

    # Oncelik 2: DDMM formulu
    lat_ddmm = ddmm_to_decimal(row["enlem_raw"])
    lon_ddmm = ddmm_to_decimal(row["boylam_raw"])
    if lat_ddmm and lon_ddmm:
        v2.at[idx, "enlem"]  = lat_ddmm
        v2.at[idx, "boylam"] = lon_ddmm
        v2.at[idx, "koordinat_kaynagi"] = "ddmm_hesap"
    else:
        v2.at[idx, "koordinat_kaynagi"] = "eski_yanlis"

v2.drop(columns=["key"], inplace=True)

# ── Sonuc ─────────────────────────────────────────────────────────────────────
print("=== Koordinat kaynagi dagilimi ===")
print(v2["koordinat_kaynagi"].value_counts().to_string())

v2.to_csv(CIKTI, index=False, encoding="utf-8-sig")
print(f"\nOlusturuldu: {CIKTI}")
print(f"Toplam satir: {len(v2)}")
