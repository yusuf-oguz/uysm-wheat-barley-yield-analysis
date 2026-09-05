"""
merged2.csv'ye düzeltilmiş dane ağırlığı sütunlarını ekler.
Ham değerler korunur, düzeltilmiş değerler eklenir, uyuşum bool olarak işaretlenir.
"""
import pandas as pd

MERGED2      = r"D:\_Development\Projects\UYSM_Projects\data\processed\UYSM_merged_v2.csv"
KONTROL_CSV  = r"D:\_Development\Projects\UYSM_Projects\data\processed\UYSM_hesap_kontrol.csv"
ESIK         = 0.01  # %1 tolerans

df      = pd.read_csv(MERGED2)
kontrol = pd.read_csv(KONTROL_CSV)

# Kontrol CSV'den sadece ihtiyacımız olan sütunları al
kontrol = kontrol[["dosya_adi", "bizim_hesap", "bizim_gercek"]].copy()

# Birleştir
df = df.merge(kontrol, on="dosya_adi", how="left")

# Sütunları yeniden adlandır — neyin ne olduğu açık olsun
df.rename(columns={
    "dane_m2_hesap_gram" : "xls_hesap_gram",
    "dane_m2_gercek_gram": "xls_gercek_gram",
    "bizim_hesap"        : "duzeltilmis_hesap_gram",
    "bizim_gercek"       : "duzeltilmis_gercek_gram",
}, inplace=True)

# Uyuşum: |xls - duzeltilmis| / duzeltilmis < %1
def uyusum(xls, duz):
    if pd.isna(xls) or pd.isna(duz) or duz == 0:
        return False
    return abs(xls - duz) / abs(duz) < ESIK

df["hesap_uyusum"] = df.apply(
    lambda r: uyusum(r["xls_hesap_gram"], r["duzeltilmis_hesap_gram"]), axis=1
)

# Kaydet
df.to_csv(MERGED2, index=False, encoding="utf-8-sig")

# Özet
print("=== ÖZET ===")
print(f"Toplam satır          : {len(df)}")
print(f"hesap_uyusum True     : {df['hesap_uyusum'].sum()}")
print(f"hesap_uyusum False    : {(~df['hesap_uyusum']).sum()}")

print("\n=== UYUŞMAYAN DOSYALAR ===")
uyusmayanlar = df[~df["hesap_uyusum"]][[
    "dosya_adi", "xls_hesap_gram", "duzeltilmis_hesap_gram"
]]
print(uyusmayanlar.to_string(index=False))

print(f"\nmerged2.csv güncellendi: {MERGED2}")
print(f"Yeni sütunlar: xls_hesap_gram, duzeltilmis_hesap_gram, xls_gercek_gram, duzeltilmis_gercek_gram, hesap_uyusum")
