"""
1. merged.csv'ye veri_durumu etiketi ekler
2. Geçerli kayıtlardan merged2.csv oluşturur
"""

import pandas as pd

MERGED_CSV  = r"D:\_Development\Projects\UYSM_Projects\data\processed\UYSM_merged.csv"
MERGED2_CSV = r"D:\_Development\Projects\UYSM_Projects\data\processed\UYSM_merged_v2.csv"

df = pd.read_csv(MERGED_CSV)

def veri_durumu(row):
    bs = row["il_koordinat_buffersiz"]
    bl = row["il_koordinat_bufferli"]
    if bs == "Koordinat Yok":
        return "koordinat_yok"
    elif bl == "Turkiye Disi":
        return "ulke_disi"
    else:
        return "gecerli"

df["veri_durumu"] = df.apply(veri_durumu, axis=1)

# Özet
print("=== ETIKET DAGILIMI ===")
print(df["veri_durumu"].value_counts().to_string())

# merged.csv güncelle (etiket eklendi)
df.to_csv(MERGED_CSV, index=False, encoding="utf-8-sig")
print(f"\nmerged.csv guncellendi: {MERGED_CSV}")

# merged2.csv: sadece geçerliler
df2 = df[df["veri_durumu"] == "gecerli"].copy()
df2.to_csv(MERGED2_CSV, index=False, encoding="utf-8-sig")
print(f"merged2.csv olusturuldu: {MERGED2_CSV} ({len(df2)} satir)")
