"""
Hansay processed v1 — bitki adı normalizasyonu
------------------------------------------------
hansay_ham_full.csv -> hansay_processed_v1.csv

Yapılan değişiklik:
  bitki_adi__C9: büyük/küçük harf ve Türkçe karakter varyantları normalize edildi.
    'buğday', 'Buğday', 'bugday', ' buğday' -> 'bugday'
    'Arpa'                                   -> 'arpa'
"""

import pandas as pd

GIRDI = (
    r"D:\_Development\Projects\UYSM_Project_2"
    r"\yusuf_oguz_calismalari\data\processed\active\hansay_ham_full.csv"
)

CIKTI = (
    r"D:\_Development\Projects\UYSM_Project_2"
    r"\yusuf_oguz_calismalari\data\processed\active\hansay_processed_v1.csv"
)

BUGDAY_VARYANTLARI = {'buğday', 'Buğday', 'bugday', ' buğday'}

df = pd.read_csv(GIRDI, encoding="utf-8-sig")

onceki = df["bitki_adi__C9"].value_counts(dropna=False).to_dict()

df["bitki_adi__C9"] = df["bitki_adi__C9"].apply(
    lambda x: "bugday" if x in BUGDAY_VARYANTLARI
    else ("arpa" if x == "Arpa" else x)
)

sonraki = df["bitki_adi__C9"].value_counts(dropna=False).to_dict()

df.to_csv(CIKTI, index=False, encoding="utf-8-sig")

print("Değişiklik özeti (bitki_adi__C9):")
print(f"  bugday : {onceki.get('buğday',0) + onceki.get('Buğday',0) + onceki.get('bugday',0) + onceki.get(' buğday',0)} -> {sonraki.get('bugday',0)}")
print(f"  arpa   : {onceki.get('arpa',0) + onceki.get('Arpa',0)} -> {sonraki.get('arpa',0)}")
print(f"\nToplam satır: {len(df)}")
print(f"Çıktı: {CIKTI}")
