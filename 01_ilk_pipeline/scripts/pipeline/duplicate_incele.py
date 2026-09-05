"""
hansay_ilk.xls — Duplicate GercekVerim satırlarını incele
Aynı değere sahip satırların DosyaAdi, koordinat ve diğer alanlarını karşılaştırır.
"""
import pandas as pd, re
import numpy as np

with open(r"D:\_Development\Projects\UYSM_Projects\data\source\hansay_ilk.xls", "r", encoding="utf-8-sig") as f:
    hl = f.readline().rstrip("\n")
    sl = f.readline().rstrip("\n")

colspecs = [(m.start(), m.end()) for m in re.finditer(r"-+", sl)]
cols = [hl[s:e].strip() or f"col_{i}" for i, (s, e) in enumerate(colspecs)]
df = pd.read_fwf(r"D:\_Development\Projects\UYSM_Projects\data\source\hansay_ilk.xls",
                 colspecs=colspecs, names=cols, skiprows=2, encoding="utf-8-sig")
df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
df["GercekVerim"] = pd.to_numeric(df["GercekVerim"], errors="coerce")
df["lat"] = pd.to_numeric(df["Enlem_O"], errors="coerce")
df["lon"] = pd.to_numeric(df["Boylam_O"], errors="coerce")

# Duplicate değerler
dup_values = df[df["GercekVerim"].notna()]["GercekVerim"].value_counts()
dup_values = dup_values[dup_values > 1]

print(f"Tekrar eden değer sayısı: {len(dup_values)}")
print("=" * 80)

for val in dup_values.index:
    grup = df[df["GercekVerim"] == val].copy()
    print(f"\nGercekVerim = {val:.6f}  ({len(grup)} satır)")
    print("-" * 80)

    cols_goster = ["DosyaAdi", "Istasyon", "Tarih", "Bitki", "Enlem_O", "Boylam_O", "lat", "lon"]
    mevcut = [c for c in cols_goster if c in grup.columns]
    print(grup[mevcut].to_string(index=True))

    # Koordinat farkı (varsa)
    if len(grup) == 2 and grup["lat"].notna().all() and grup["lon"].notna().all():
        lats = grup["lat"].values
        lons = grup["lon"].values
        # Basit Öklid mesafesi (km yaklaşık)
        dlat = (lats[1] - lats[0]) * 111.0
        dlon = (lons[1] - lons[0]) * 111.0 * np.cos(np.radians(np.mean(lats)))
        dist = np.sqrt(dlat**2 + dlon**2)
        print(f"  Koordinat farki: {dist:.2f} km")

    # Tüm sütunlar birebir aynı mı?
    if len(grup) == 2:
        check_cols = [c for c in df.columns if c not in ("lat", "lon")]
        row0 = grup.iloc[0][check_cols]
        row1 = grup.iloc[1][check_cols]
        farklar = row0.index[(row0.values != row1.values)]
        if len(farklar) == 0:
            print("  *** TUM SUTUNLAR BIREBIR AYNI -- kesin duplicate ***")
        else:
            print(f"  Farklı sütunlar: {list(farklar)}")
