import pandas as pd

CSV = r"D:\_Development\Projects\UYSM_Projects\data\processed\UYSM_merged_v2.csv"

df = pd.read_csv(CSV)

# Ornek dosyayi cikar
ornek_mask = df["dosya_adi"].str.contains("rnek", case=False, na=False)
df = df[~ornek_mask]
df.to_csv(CSV, index=False, encoding="utf-8-sig")
print(f"Ornek dosya cikarildi. Kalan: {len(df)} satir\n")

# --- Genel tablo ---
hesap = df["dane_m2_hesap_gram"]
gercek = df["dane_m2_gercek_gram"]

print("=== DANE AGIRLIĞI GENEL ISTATISTIK ===")
print(f"{'':30} {'HESAP':>12} {'GERCEK':>12}")
print("-" * 56)
print(f"{'Dolu kayit':30} {hesap.notna().sum():>12} {gercek.notna().sum():>12}")
print(f"{'Eksik kayit':30} {hesap.isna().sum():>12} {gercek.isna().sum():>12}")
print(f"{'Ortalama (g/m2)':30} {hesap.mean():>12.1f} {gercek.mean():>12.1f}")
print(f"{'Medyan (g/m2)':30} {hesap.median():>12.1f} {gercek.median():>12.1f}")
print(f"{'Std sapma':30} {hesap.std():>12.1f} {gercek.std():>12.1f}")
print(f"{'Min (g/m2)':30} {hesap.min():>12.2f} {gercek.min():>12.2f}")
print(f"{'%25 (g/m2)':30} {hesap.quantile(0.25):>12.1f} {gercek.quantile(0.25):>12.1f}")
print(f"{'%75 (g/m2)':30} {hesap.quantile(0.75):>12.1f} {gercek.quantile(0.75):>12.1f}")
print(f"{'Max (g/m2)':30} {hesap.max():>12.1f} {gercek.max():>12.1f}")

# --- Bitki türü dağılımı ---
print("\n=== BITKI TURU DAGILIMI ===")
df["bitki_norm"] = df["bitki_adi"].str.lower().str.strip()
print(df["bitki_norm"].value_counts().to_string())

# --- Bitki türüne göre dane ağırlığı ---
print("\n=== BITKI TURUNE GORE HESAP DANE AGIRLIĞI (g/m2) ===")
print(f"{'Bitki':15} {'n':>5} {'Ort':>8} {'Medyan':>8} {'Min':>8} {'Max':>8}")
print("-" * 55)
for bitki, grup in df.groupby("bitki_norm")["dane_m2_hesap_gram"]:
    print(f"{bitki:<15} {grup.count():>5} {grup.mean():>8.1f} {grup.median():>8.1f} {grup.min():>8.1f} {grup.max():>8.1f}")

# --- Hesap vs Gercek farkı ---
df["fark_yuzde"] = ((df["dane_m2_hesap_gram"] - df["dane_m2_gercek_gram"]) / df["dane_m2_hesap_gram"] * 100)
print("\n=== HESAP vs GERCEK FARKI ===")
print(f"Ortalama fark: %{df['fark_yuzde'].mean():.1f}")
print(f"Medyan fark  : %{df['fark_yuzde'].median():.1f}")
print(f"Fark > %50 olan kayit sayisi: {(df['fark_yuzde'].abs() > 50).sum()}")
print(f"Fark > %100 olan kayit sayisi: {(df['fark_yuzde'].abs() > 100).sum()}")

# --- Uç değerler ---
print("\n=== UC DEGERLER (hesap >3000 veya <20 g/m2) ===")
uc = df[(hesap > 3000) | (hesap < 20)][["dosya_adi", "dane_m2_hesap_gram", "dane_m2_gercek_gram", "bitki_adi"]]
print(uc.to_string(index=False))
