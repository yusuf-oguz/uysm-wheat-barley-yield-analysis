"""
Oluşan CSV'deki anomalileri rapor eder.
"""
import pandas as pd

df = pd.read_csv(r"D:\_Development\Projects\UYSM_Projects\data\processed\UYSM_merged.csv")

print("=== GENEL ÖZET ===")
print(f"Toplam satır: {len(df)}")
print(f"Koordinat geçerli: {df['koordinat_gecerli'].sum()}")
print(f"Dane m2 hesap - dolu: {df['dane_m2_hesap_gram'].notna().sum()}")
print(f"Dane m2 gerçek - dolu: {df['dane_m2_gercek_gram'].notna().sum()}")

print("\n=== GEÇERSİZ KOORDİNATLI DOSYALAR ===")
gecersiz = df[df['koordinat_gecerli'] == False][['dosya_adi','enlem_raw','boylam_raw','enlem','boylam']]
print(gecersiz.to_string(index=False))

print("\n=== DANE AĞIRLIĞI EKSİK DOSYA ===")
eksik = df[df['dane_m2_hesap_gram'].isna()][['dosya_adi','enlem','boylam']]
print(eksik.to_string(index=False))

print("\n=== DANE AĞIRLIĞI İSTATİSTİKLERİ (hesap) ===")
print(df['dane_m2_hesap_gram'].describe().round(2))

print("\n=== DANE AĞIRLIĞI İSTATİSTİKLERİ (gerçek) ===")
print(df['dane_m2_gercek_gram'].describe().round(2))

print("\n=== ŞÜPHELI DEĞERLER (10 g/m2 altı veya 5000 üstü) ===")
supheli = df[
    (df['dane_m2_hesap_gram'] < 10) | (df['dane_m2_hesap_gram'] > 5000)
][['dosya_adi', 'dane_m2_hesap_gram', 'dane_m2_gercek_gram', 'enlem', 'boylam']]
print(supheli.to_string(index=False))

print("\n=== BİTKİ TÜRÜ DAĞILIMI ===")
print(df['bitki_adi'].value_counts())
