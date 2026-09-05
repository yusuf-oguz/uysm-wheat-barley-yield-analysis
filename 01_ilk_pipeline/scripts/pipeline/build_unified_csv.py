"""
Tüm verileri tek bir CSV'de toplar.
merged.csv → güncellenir (291 satır, tüm sütunlar + durum sütunları)
merged2.csv → silinmez ama artık kullanılmaz.
"""
import pandas as pd
import os

MERGED  = r"D:\_Development\Projects\UYSM_Projects\data\processed\UYSM_merged.csv"
KONTROL = r"D:\_Development\Projects\UYSM_Projects\data\processed\UYSM_hesap_kontrol.csv"
ESIK    = 0.01  # %1 tolerans

# --- Yükle ---
df      = pd.read_csv(MERGED)
kontrol = pd.read_csv(KONTROL)

# Kontrol'den ihtiyaç duyulan sütunlar
kontrol = kontrol[[
    "dosya_adi", "bizim_hesap", "bizim_gercek",
    "e39_formul_mu", "e39_uyusumu", "e39_fark_pct", "dolu_satir"
]].copy()

df = df.merge(kontrol, on="dosya_adi", how="left")

# --- Sütun isimlendirmesi ---
df.rename(columns={
    "dane_m2_hesap_gram" : "xls_hesap_gram",
    "dane_m2_gercek_gram": "xls_gercek_gram",
    "bizim_hesap"        : "duzeltilmis_hesap_gram",
    "bizim_gercek"       : "duzeltilmis_gercek_gram",
}, inplace=True)

# --- hesap_uyusum ---
def uyusum(xls, duz):
    if pd.isna(xls) or pd.isna(duz) or duz == 0:
        return False
    return abs(xls - duz) / abs(duz) < ESIK

df["hesap_uyusum"] = df.apply(
    lambda r: uyusum(r["xls_hesap_gram"], r["duzeltilmis_hesap_gram"]), axis=1
)

# --- analiz_durumu ve duzeltme_notu ---
def durum_ve_not(row):
    dosya = str(row["dosya_adi"])

    # Şablon/örnek dosyası
    if "rnek" in dosya or "rnek" in dosya.lower():
        return "veri_hatasi", "Ornek/sablon dosyasi, gercek olcum degil"

    vd = row.get("veri_durumu", "")

    # Koordinat sorunları
    if vd == "koordinat_yok":
        return "koordinat_yok", "Koordinat girilmemis"
    if vd == "ulke_disi":
        return "koordinat_disi", "Koordinat Turkiye siniri disinda (buffer ile de yakalanamadi)"

    # Hesap uyuşmazlıkları
    if not row.get("hesap_uyusum", True):
        e39_formul = row.get("e39_formul_mu", True)
        e39_uyum   = row.get("e39_uyusumu", True)
        fark       = row.get("e39_fark_pct", 0)
        dolu       = row.get("dolu_satir", 10)

        if not e39_formul and fark > 50:
            return "duzeltilmis", "E39 sabit 948 (sablon hatasi), ham veriden yeniden hesaplandi"
        elif not e39_uyum:
            return "duzeltilmis", f"E39 formul ama uyumsuz (%{fark:.1f}), ham veriden yeniden hesaplandi"
        elif dolu and int(dolu) < 10:
            return "duzeltilmis", f"Sadece {int(dolu)} basak verisi var (10 yerine), bolme duzeltildi"
        else:
            return "duzeltilmis", "XLS hesap ile ham veri arasindan >%1 fark, ham veriden yeniden hesaplandi"

    return "kullanilabilir", ""

sonuclar = df.apply(durum_ve_not, axis=1, result_type="expand")
df["analiz_durumu"] = sonuclar[0]
df["duzeltme_notu"] = sonuclar[1]

# --- analize_dahil (kolayca filtrelemek için) ---
df["analize_dahil"] = df["analiz_durumu"].isin(["kullanilabilir", "duzeltilmis"])

# --- Sütun sırası: durum sütunları en sona ---
on_sutunlar = [
    "dosya_adi", "rapor_no", "istasyon_no", "tarih", "bitki_adi", "cesit_adi",
    "enlem_raw", "boylam_raw", "enlem", "boylam",
    "il_koordinat_buffersiz", "il_koordinat_bufferli",
    "m2_basak_sayisi",
    "xls_hesap_gram", "xls_gercek_gram",
    "duzeltilmis_hesap_gram", "duzeltilmis_gercek_gram",
    "ortalama_bitki_boyu_cm", "ortalama_basak_boyu_cm",
]
durum_sutunlari = [
    "hesap_uyusum", "analiz_durumu", "duzeltme_notu", "analize_dahil"
]
# Geri kalan sütunlar (kalanları da tut, düzen bozulmasın)
kalan = [c for c in df.columns if c not in on_sutunlar + durum_sutunlari]
df = df[on_sutunlar + kalan + durum_sutunlari]

# --- Kaydet ---
df.to_csv(MERGED, index=False, encoding="utf-8-sig")

# --- Özet ---
print("=== TEK CSV OZETI ===")
print(f"Toplam satir          : {len(df)}")
print(f"\nanaliz_durumu dagilimi:")
print(df["analiz_durumu"].value_counts().to_string())
print(f"\nanalize_dahil True    : {df['analize_dahil'].sum()}")
print(f"analize_dahil False   : {(~df['analize_dahil']).sum()}")
print(f"\nhesap_uyusum False    : {(~df['hesap_uyusum']).sum()}")
print(f"\nDosya: {MERGED}")
