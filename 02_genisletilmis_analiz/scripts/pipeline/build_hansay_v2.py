"""
Hansay processed v2 — bugday/arpa filtresi
--------------------------------------------
hansay_processed_v1.csv -> hansay_processed_v2.csv

Yapılan değişiklik:
  Sadece bitki_adi__C9 == 'bugday' veya 'arpa' olan satırlar tutuldu.
"""

import pandas as pd

GIRDI = (
    r"D:\_Development\Projects\UYSM_Project_2"
    r"\yusuf_oguz_calismalari\data\processed\active\hansay_processed_v1.csv"
)

CIKTI = (
    r"D:\_Development\Projects\UYSM_Project_2"
    r"\yusuf_oguz_calismalari\data\processed\active\hansay_processed_v2.csv"
)

df = pd.read_csv(GIRDI, encoding="utf-8-sig")

onceki = len(df)
df = df[df["bitki_adi__C9"].isin(["bugday", "arpa"])].reset_index(drop=True)
sonraki = len(df)

df.to_csv(CIKTI, index=False, encoding="utf-8-sig")

print(f"Filtre öncesi : {onceki} satır")
print(f"Filtre sonrası: {sonraki} satır ({onceki - sonraki} satır çıkarıldı)")
print(f"\nBitki dağılımı:\n{df['bitki_adi__C9'].value_counts().to_string()}")
print(f"\nÇıktı: {CIKTI}")
