"""
Hansay 2016 — TAM ham veri çıkarıcı
-------------------------------------
769 xlsx dosyasının tüm içeriğini çeker:
  - S3–S26: üst bilgi ve özet ölçümler (hansay_ham_ozet.csv ile aynı)
  - S29–S38: 10 başak ham ölçüm satırı (her başak ayrı sütun grubu)
  - S39: 10 başak toplamı
  - S40: 10 başak ortalaması
  - S41: 1/4 başaklı ağırlık ve 10 sap ağırlığı
  - S42: tarih lab ve tarla tartım değeri

Hiçbir değer değiştirilmez, hesaplanmaz, dönüştürülmez.

Çıktı: yusuf_oguz_calismalari/data/processed/hansay_ham_full.csv
"""

import os
import csv
import openpyxl

KAYNAK = (
    r"D:\_Development\Projects\UYSM_Project_2"
    r"\uysm_flash_bellek_degistirilmemis"
    r"\hansay 2016 verim\Verim 8"
    r"\1.EXEL HESAPLAR TABLOLARI (7 CİLT)"
)

CIKTI = (
    r"D:\_Development\Projects\UYSM_Project_2"
    r"\yusuf_oguz_calismalari\data\processed\active\hansay_ham_full.csv"
)

# Başak sütun isimleri (S29–S38, her satır bir başak)
# col[1]=B uzunluk, col[2]=C agirlik_mg, col[3]=D dane_sayisi, col[4]=E dane_agirlik_mg
# col[7]=H sap_basak_boyu, col[8]=I sap_alt, col[9]=J sap_boy
BASAK_SUTUNLAR = []
for b in range(1, 11):
    satir = 28 + b  # b1→29, b10→38
    BASAK_SUTUNLAR += [
        f"b{b}_uzunluk_cm__B{satir}",
        f"b{b}_agirlik_mg__C{satir}",
        f"b{b}_dane_sayisi__D{satir}",
        f"b{b}_dane_agirlik_mg__E{satir}",
        f"b{b}_sap_basak_boyu_cm__H{satir}",
        f"b{b}_sap_alt_cm__I{satir}",
        f"b{b}_sap_boy_cm__J{satir}",
    ]

KOLONLAR = (
    # ── Dosya kimliği (dosya adından ayrıştırılır) ─────────────────────────
    ["dosya_adi__dosyaadi", "dosya_il_kodu__dosyaadi", "dosya_ist_no__dosyaadi",
     "dosya_mesafe__dosyaadi", "dosya_rapor_no__dosyaadi"]
    # ── 3. satır ──────────────────────────────────────────────────────────
    + ["ttr_baslik__A3", "olcum_birimi_etiketi__C3", "enlem_raw__E3", "mesafe_ici__G3", "bilinmeyen__H3", "rapor_no_xlsx__J3"]
    # ── 4. satır ──────────────────────────────────────────────────────────
    + ["rapor_no_ici__C4", "boylam_raw__E4"]
    # ── 5. satır ──────────────────────────────────────────────────────────
    + ["tarih__C5", "sehir_istasyon__I5"]
    # ── 6. satır ──────────────────────────────────────────────────────────
    + ["istasyon_no__C6", "sulama_tipi__G6"]
    # ── 7. satır ──────────────────────────────────────────────────────────
    + ["ad__C7", "bilinmeyen__G7", "sulama_sayisi__I7"]
    # ── 8. satır ──────────────────────────────────────────────────────────
    + ["rakim__C8", "kamera_yonu__G8"]
    # ── 9. satır ──────────────────────────────────────────────────────────
    + ["bitki_adi__C9", "fenolojik_evre__G9"]
    # ── 10. satır ─────────────────────────────────────────────────────────
    + ["cesit_adi__C10", "urunum_alan__G10"]
    # ── 11. satır ─────────────────────────────────────────────────────────
    + ["olcum_alani_etiketi__A11", "olcum_alani_basak__C11", "urunum_sayan__G11"]
    # ── 12. satır ─────────────────────────────────────────────────────────
    + ["m2_basak_sayisi__C12"]
    # ── 13. satır ─────────────────────────────────────────────────────────
    + ["basaksiz_bitki_sayisi__C13", "olcum_alani_carpani__E13"]
    # ── 14. satır ─────────────────────────────────────────────────────────
    + ["m2_basaksiz_bitki__C14", "basaksiz_bitki_carpani__E14"]
    # ── 15. satır ─────────────────────────────────────────────────────────
    + ["m2_toplam_bitki__C15"]
    # ── 16. satır ─────────────────────────────────────────────────────────
    + ["on_bitki_sap_agirlik_mgr__C16"]
    # ── 17. satır ─────────────────────────────────────────────────────────
    + ["m2_sap_agirlik_kg__C17"]
    # ── 18. satır ─────────────────────────────────────────────────────────
    + ["basak_kilcikli_agirlik_gram__C18"]
    # ── 19. satır ─────────────────────────────────────────────────────────
    + ["basak_ort_dane_sayisi__C19"]
    # ── 20. satır ─────────────────────────────────────────────────────────
    + ["basak_ort_dane_agirlik_gram__C20"]
    # ── 21. satır ─────────────────────────────────────────────────────────
    + ["dane_m2_hesap_gram__C21", "dane_m2_gercek_gram__D21"]
    # ── 22. satır ─────────────────────────────────────────────────────────
    + ["bin_dane_agirlik_gram__C22"]
    # ── 23. satır ─────────────────────────────────────────────────────────
    + ["ort_bitki_boyu_cm__C23"]
    # ── 24. satır ─────────────────────────────────────────────────────────
    + ["ort_basak_boyu_cm__C24", "bilinmeyen__J24"]
    # ── 25. satır ─────────────────────────────────────────────────────────
    + ["bitki_alan__C25", "bilinmeyen__J25"]
    # ── 26. satır ─────────────────────────────────────────────────────────
    + ["bitki_sayan__C26"]
    # ── 29–38. satırlar: 10 başak ham ölçümü ─────────────────────────────
    + BASAK_SUTUNLAR
    # ── 39. satır: Toplam (B/C/D/E) + Ortalama (H/I/J) ──────────────────
    + ["toplam_basak_uzunluk__B39", "toplam_basak_agirlik_mg__C39",
       "toplam_dane_sayisi__D39", "toplam_dane_agirlik_mg__E39",
       "ort_sap_basak_boyu__H39", "ort_sap_basak_alti_boyu__I39", "ort_sap_boy__J39"]
    # ── 40. satır: Ortalama ───────────────────────────────────────────────
    + ["ort_basak_uzunluk__B40", "ort_basak_agirlik_mg__C40",
       "ort_dane_sayisi__D40", "ort_dane_agirlik_mg__E40"]
    # ── 41. satır ─────────────────────────────────────────────────────────
    + ["olcum_alani_etiketi__B41",
       "olcum_basak_agirlik_ham__C41", "basak_dane_oran__D41",
       "olcum_basak_dane_agirlik_hesap__E41", "on_sap_agirlik_mg__J41"]
    # ── 42. satır ─────────────────────────────────────────────────────────
    + ["tarih_lab__C42", "bilinmeyen__D42", "dane_m2_tartim_hesap__E42"]
    # ── Durum ─────────────────────────────────────────────────────────────
    + ["okuma_notu"]
)


def get(rows, row_idx, col_idx):
    if row_idx >= len(rows):
        return None
    row = rows[row_idx]
    if row is None or col_idx >= len(row):
        return None
    return row[col_idx]


def dosya_adini_ayristir(dosya_adi):
    ad = os.path.splitext(dosya_adi)[0]
    parcalar = ad.split()
    il_kodu = ist_no = mesafe = rapor_no = None

    if parcalar:
        ilk = parcalar[0]
        if len(ilk) >= 4 and ilk[:4].isdigit():
            il_kodu = ilk[:2].zfill(2)
            ist_no  = ilk[2:4].zfill(2)
        elif len(ilk) >= 2 and ilk[:2].isdigit():
            il_kodu = ilk[:2].zfill(2)

    if len(parcalar) >= 2:
        try:
            rapor_no = int(parcalar[-1])
        except ValueError:
            rapor_no = None
        mesafe = " ".join(parcalar[1:-1]) if len(parcalar) >= 3 else None

    return il_kodu, ist_no, mesafe, rapor_no


def dosyayi_isle(yol):
    dosya_adi = os.path.basename(yol)
    il_kodu, ist_no, mesafe_dosya, rapor_no_dosya = dosya_adini_ayristir(dosya_adi)

    kayit = {k: None for k in KOLONLAR}
    kayit["dosya_adi__dosyaadi"]      = dosya_adi
    kayit["dosya_il_kodu__dosyaadi"]  = il_kodu
    kayit["dosya_ist_no__dosyaadi"]   = ist_no
    kayit["dosya_mesafe__dosyaadi"]   = mesafe_dosya
    kayit["dosya_rapor_no__dosyaadi"] = rapor_no_dosya

    try:
        wb = openpyxl.load_workbook(yol, read_only=True, data_only=True)
        ws = wb.active
        rows = list(ws.iter_rows(min_row=1, max_row=43, max_col=10, values_only=True))
        wb.close()

        # ── 3–12. satırlar: Üst bilgi ─────────────────────────────────────
        kayit["ttr_baslik__A3"]            = get(rows, 2, 0)
        kayit["olcum_birimi_etiketi__C3"]  = get(rows, 2, 2)
        kayit["enlem_raw__E3"]             = get(rows, 2, 4)
        kayit["mesafe_ici__G3"]            = get(rows, 2, 6)
        kayit["bilinmeyen__H3"]             = get(rows, 2, 7)
        kayit["rapor_no_xlsx__J3"]         = get(rows, 2, 9)
        kayit["rapor_no_ici__C4"]          = get(rows, 3, 2)
        kayit["boylam_raw__E4"]            = get(rows, 3, 4)
        tarih_val                          = get(rows, 4, 2)
        kayit["tarih__C5"]                 = str(tarih_val)[:10] if tarih_val is not None else None
        kayit["sehir_istasyon__I5"]        = get(rows, 4, 8)
        kayit["istasyon_no__C6"]           = get(rows, 5, 2)
        kayit["sulama_tipi__G6"]           = get(rows, 5, 6)
        kayit["ad__C7"]                    = get(rows, 6, 2)
        kayit["bilinmeyen__G7"]             = get(rows, 6, 6)
        kayit["sulama_sayisi__I7"]         = get(rows, 6, 8)
        kayit["rakim__C8"]                 = get(rows, 7, 2)
        kayit["kamera_yonu__G8"]           = get(rows, 7, 6)
        kayit["bitki_adi__C9"]             = get(rows, 8, 2)
        kayit["fenolojik_evre__G9"]        = get(rows, 8, 6)
        kayit["cesit_adi__C10"]            = get(rows, 9, 2)
        kayit["urunum_alan__G10"]          = get(rows, 9, 6)
        kayit["olcum_alani_etiketi__A11"]  = get(rows, 10, 0)
        kayit["olcum_alani_basak__C11"]    = get(rows, 10, 2)
        kayit["urunum_sayan__G11"]         = get(rows, 10, 6)
        kayit["m2_basak_sayisi__C12"]      = get(rows, 11, 2)

        # ── 13–26. satırlar: Özet ölçümler ───────────────────────────────
        kayit["basaksiz_bitki_sayisi__C13"]       = get(rows, 12, 2)
        kayit["olcum_alani_carpani__E13"]         = get(rows, 12, 4)
        kayit["m2_basaksiz_bitki__C14"]           = get(rows, 13, 2)
        kayit["basaksiz_bitki_carpani__E14"]      = get(rows, 13, 4)
        kayit["m2_toplam_bitki__C15"]             = get(rows, 14, 2)
        kayit["on_bitki_sap_agirlik_mgr__C16"]    = get(rows, 15, 2)
        kayit["m2_sap_agirlik_kg__C17"]           = get(rows, 16, 2)
        kayit["basak_kilcikli_agirlik_gram__C18"] = get(rows, 17, 2)
        kayit["basak_ort_dane_sayisi__C19"]       = get(rows, 18, 2)
        kayit["basak_ort_dane_agirlik_gram__C20"] = get(rows, 19, 2)
        kayit["dane_m2_hesap_gram__C21"]          = get(rows, 20, 2)
        kayit["dane_m2_gercek_gram__D21"]         = get(rows, 20, 3)
        kayit["bin_dane_agirlik_gram__C22"]       = get(rows, 21, 2)
        kayit["ort_bitki_boyu_cm__C23"]           = get(rows, 22, 2)
        kayit["ort_basak_boyu_cm__C24"]           = get(rows, 23, 2)
        kayit["bilinmeyen__J24"]                  = get(rows, 23, 9)
        kayit["bitki_alan__C25"]                  = get(rows, 24, 2)
        kayit["bilinmeyen__J25"]                  = get(rows, 24, 9)
        kayit["bitki_sayan__C26"]                 = get(rows, 25, 2)

        # ── 29–38. satırlar: 10 başak ham ölçümü ─────────────────────────
        for b in range(10):
            row_idx = 28 + b
            n = b + 1
            satir = 29 + b
            kayit[f"b{n}_uzunluk_cm__B{satir}"]       = get(rows, row_idx, 1)
            kayit[f"b{n}_agirlik_mg__C{satir}"]        = get(rows, row_idx, 2)
            kayit[f"b{n}_dane_sayisi__D{satir}"]       = get(rows, row_idx, 3)
            kayit[f"b{n}_dane_agirlik_mg__E{satir}"]   = get(rows, row_idx, 4)
            kayit[f"b{n}_sap_basak_boyu_cm__H{satir}"] = get(rows, row_idx, 7)
            kayit[f"b{n}_sap_alt_cm__I{satir}"]        = get(rows, row_idx, 8)
            kayit[f"b{n}_sap_boy_cm__J{satir}"]        = get(rows, row_idx, 9)

        # ── 39. satır: Toplam (B-E) + Ortalama (H-J, formül /10 içeriyor) ──
        kayit["toplam_basak_uzunluk__B39"]    = get(rows, 38, 1)
        kayit["toplam_basak_agirlik_mg__C39"] = get(rows, 38, 2)
        kayit["toplam_dane_sayisi__D39"]      = get(rows, 38, 3)
        kayit["toplam_dane_agirlik_mg__E39"]  = get(rows, 38, 4)
        kayit["ort_sap_basak_boyu__H39"]      = get(rows, 38, 7)
        kayit["ort_sap_basak_alti_boyu__I39"]  = get(rows, 38, 8)
        kayit["ort_sap_boy__J39"]             = get(rows, 38, 9)

        # ── 40. satır: Ortalama ───────────────────────────────────────────
        kayit["ort_basak_uzunluk__B40"]    = get(rows, 39, 1)
        kayit["ort_basak_agirlik_mg__C40"] = get(rows, 39, 2)
        kayit["ort_dane_sayisi__D40"]      = get(rows, 39, 3)
        kayit["ort_dane_agirlik_mg__E40"]  = get(rows, 39, 4)

        # ── 41. satır ────────────────────────────────────────────────────
        kayit["olcum_alani_etiketi__B41"]           = get(rows, 40, 1)
        kayit["olcum_basak_agirlik_ham__C41"]        = get(rows, 40, 2)
        kayit["basak_dane_oran__D41"]               = get(rows, 40, 3)
        kayit["olcum_basak_dane_agirlik_hesap__E41"]= get(rows, 40, 4)
        kayit["on_sap_agirlik_mg__J41"]             = get(rows, 40, 9)

        # ── 42. satır ────────────────────────────────────────────────────
        import datetime as _dt
        tarih_lab = get(rows, 41, 2)
        if isinstance(tarih_lab, _dt.datetime):
            kayit["tarih_lab__C42"] = tarih_lab.strftime("%Y-%m-%d")
        elif tarih_lab is not None:
            kayit["tarih_lab__C42"] = str(tarih_lab)[:10]
        else:
            kayit["tarih_lab__C42"] = None
        kayit["bilinmeyen__D42"]           = get(rows, 41, 3)
        kayit["dane_m2_tartim_hesap__E42"] = get(rows, 41, 4)

    except Exception as e:
        kayit["okuma_notu"] = f"HATA: {e}"  # key değişmedi, KOLONLAR'daki son eleman

    return kayit


def main():
    os.makedirs(os.path.dirname(CIKTI), exist_ok=True)

    dosyalar = sorted([f for f in os.listdir(KAYNAK) if f.lower().endswith(".xlsx")])
    print(f"Toplam {len(dosyalar)} xlsx dosyası bulundu.")

    sonuclar = []
    hatali = 0

    for i, dosya in enumerate(dosyalar, 1):
        kayit = dosyayi_isle(os.path.join(KAYNAK, dosya))
        sonuclar.append(kayit)
        if (kayit.get("okuma_notu") or "").startswith("HATA"):
            hatali += 1
            print(f"  [HATA] {dosya}: {kayit['okuma_notu']}")  # okuma_notu key'i değişmedi
        if i % 100 == 0:
            print(f"  {i}/{len(dosyalar)} işlendi...")

    print(f"\n{len(sonuclar)} dosya işlendi, {hatali} hata.")
    print(f"Sütun sayısı: {len(KOLONLAR)}")

    # Doluluk özeti
    enlem_dolu  = sum(1 for s in sonuclar if s.get("enlem_raw__E3") is not None)
    verim_dolu  = sum(1 for s in sonuclar if s.get("dane_m2_hesap_gram__C21") is not None)
    b1_dolu     = sum(1 for s in sonuclar if s.get("b1_agirlik_mg__C29") is not None)  # başak sütun adları değişmedi
    print(f"Enlem dolu          : {enlem_dolu}/{len(sonuclar)}")
    print(f"Verim (hesap) dolu  : {verim_dolu}/{len(sonuclar)}")
    print(f"Başak-1 ağırlık dolu: {b1_dolu}/{len(sonuclar)}")

    with open(CIKTI, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=KOLONLAR)
        writer.writeheader()
        writer.writerows(sonuclar)

    print(f"\nCikti: {CIKTI}")
    print(f"Boyut : {os.path.getsize(CIKTI) / 1024:.1f} KB")


if __name__ == "__main__":
    main()
