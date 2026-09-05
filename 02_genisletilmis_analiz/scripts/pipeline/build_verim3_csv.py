"""
VERİM 3 eski saha verisi — ham CSV çıkarıcı
--------------------------------------------
291 xlsx dosyasını okur, verileri DEĞİŞTİRMEDEN ham haliyle CSV'ye yazar.
Koordinat dönüşümü, normalleştirme vb. YOK — bunlar sonraki aşamada yapılacak.

Hansay'dan tek farkı: koordinatlar DMS string değil, ham tam sayı formatındadır
(ör. enlem=378349, boylam=3540379). enlem_raw / boylam_raw sütunlarına olduğu gibi yazılır.

Ayrıca S3'te mesafe bazen col[6]'da (Hansay gibi) bazen col[7]'de bulunur;
her ikisi de okunarak mesafe_ici sütununa ilki dolu olan yazılır.

Çıktı: yusuf_oguz_calismalari/data/processed/verim3_ham_ozet.csv
"""

import os
import csv
import openpyxl

KAYNAK = (
    r"D:\_Development\Projects\UYSM_Project_2"
    r"\uysm_flash_bellek_degistirilmemis"
    r"\HANSAY ÇALIŞMA(VERİM 3) UFUK DAN ALINAN"
    r"\Z. EXECELL HESAPLAMALARI 0-300 DOSYA"
)

CIKTI = (
    r"D:\_Development\Projects\UYSM_Project_2"
    r"\yusuf_oguz_calismalari\data\processed\verim3_ham_ozet.csv"
)

KOLONLAR = [
    # Dosya kimliği
    "dosya_adi",
    "dosya_il_kodu",
    "dosya_ist_no",
    "dosya_mesafe",
    "dosya_rapor_no",
    # Üst bilgi (S3-S12)
    "ttr_baslik",
    "rapor_no_ici",
    "enlem_raw",       # ham tam sayı (ör. 378349)
    "boylam_raw",      # ham tam sayı (ör. 3540379)
    "mesafe_ici",
    "tarih",
    "sehir_istasyon",
    "istasyon_no",
    "sulama_tipi",
    "ad",
    "sulama_sayisi",
    "rakim",
    "kamera_yonu",
    "bitki_adi",
    "fenolojik_evre",
    "cesit_adi",
    "urunum_alan",
    "urunum_sayan",
    "ceyrek_m2_basak",
    "m2_basak_sayisi",
    # Özet ölçümler (S13-S24)
    "basaksiz_bitki_sayisi",
    "m2_basaksiz_bitki",
    "m2_toplam_bitki",
    "on_bitki_sap_agirlik_mgr",
    "m2_sap_agirlik_kg",
    "basak_kilikli_agirlik_gram",
    "basak_dane_sayisi",
    "basak_dane_agirlik_gram",
    "dane_m2_hesap_gram",
    "dane_m2_gercek_gram",
    "bin_dane_agirlik_gram",
    "ort_bitki_boyu_cm",
    "ort_basak_boyu_cm",
    # Durum
    "okuma_notu",
]


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

    il_kodu = None
    ist_no = None
    mesafe = None
    rapor_no = None

    if parcalar:
        ilk = parcalar[0]
        if len(ilk) >= 4 and ilk[:4].isdigit():
            il_kodu = ilk[:2].zfill(2)
            ist_no = ilk[2:4].zfill(2)
        elif len(ilk) >= 2 and ilk[:2].isdigit():
            il_kodu = ilk[:2].zfill(2)

    if len(parcalar) >= 2:
        try:
            rapor_no = int(parcalar[-1])
        except ValueError:
            rapor_no = None

        if len(parcalar) >= 3:
            mesafe = " ".join(parcalar[1:-1])
        else:
            mesafe = None

    return il_kodu, ist_no, mesafe, rapor_no


def dosyayi_isle(yol):
    dosya_adi = os.path.basename(yol)
    il_kodu, ist_no, mesafe_dosya, rapor_no_dosya = dosya_adini_ayristir(dosya_adi)

    kayit = {k: None for k in KOLONLAR}
    kayit["dosya_adi"] = dosya_adi
    kayit["dosya_il_kodu"] = il_kodu
    kayit["dosya_ist_no"] = ist_no
    kayit["dosya_mesafe"] = mesafe_dosya
    kayit["dosya_rapor_no"] = rapor_no_dosya

    try:
        wb = openpyxl.load_workbook(yol, read_only=True, data_only=True)
        ws = wb.active
        rows = list(ws.iter_rows(min_row=1, max_row=25, values_only=True))
        wb.close()

        # S3 (idx=2)
        kayit["ttr_baslik"] = get(rows, 2, 0)
        kayit["enlem_raw"]  = get(rows, 2, 4)
        # Mesafe: VERİM 3'te col[6] veya col[7]'de olabilir
        mesafe_6 = get(rows, 2, 6)
        mesafe_7 = get(rows, 2, 7)
        kayit["mesafe_ici"] = mesafe_6 if mesafe_6 is not None else mesafe_7

        # S4 (idx=3)
        kayit["rapor_no_ici"] = get(rows, 3, 2)
        kayit["boylam_raw"]   = get(rows, 3, 4)

        # S5 (idx=4)
        tarih_val = get(rows, 4, 2)
        kayit["tarih"] = str(tarih_val)[:10] if tarih_val is not None else None
        kayit["sehir_istasyon"] = get(rows, 4, 8)

        # S6 (idx=5)
        kayit["istasyon_no"] = get(rows, 5, 2)
        kayit["sulama_tipi"] = get(rows, 5, 6)

        # S7 (idx=6)
        kayit["ad"]           = get(rows, 6, 2)
        kayit["sulama_sayisi"]= get(rows, 6, 8)

        # S8 (idx=7)
        kayit["rakim"]       = get(rows, 7, 2)
        kayit["kamera_yonu"] = get(rows, 7, 6)

        # S9 (idx=8)
        kayit["bitki_adi"]      = get(rows, 8, 2)
        kayit["fenolojik_evre"] = get(rows, 8, 6)

        # S10 (idx=9)
        kayit["cesit_adi"]   = get(rows, 9, 2)
        kayit["urunum_alan"] = get(rows, 9, 6)

        # S11 (idx=10)
        kayit["ceyrek_m2_basak"] = get(rows, 10, 2)
        kayit["urunum_sayan"]    = get(rows, 10, 6)

        # S12 (idx=11)
        kayit["m2_basak_sayisi"] = get(rows, 11, 2)

        # S13 (idx=12)
        kayit["basaksiz_bitki_sayisi"] = get(rows, 12, 2)

        # S14 (idx=13)
        kayit["m2_basaksiz_bitki"] = get(rows, 13, 2)

        # S15 (idx=14)
        kayit["m2_toplam_bitki"] = get(rows, 14, 2)

        # S16 (idx=15)
        kayit["on_bitki_sap_agirlik_mgr"] = get(rows, 15, 2)

        # S17 (idx=16)
        kayit["m2_sap_agirlik_kg"] = get(rows, 16, 2)

        # S18 (idx=17)
        kayit["basak_kilikli_agirlik_gram"] = get(rows, 17, 2)

        # S19 (idx=18)
        kayit["basak_dane_sayisi"] = get(rows, 18, 2)

        # S20 (idx=19)
        kayit["basak_dane_agirlik_gram"] = get(rows, 19, 2)

        # S21 (idx=20)
        kayit["dane_m2_hesap_gram"]  = get(rows, 20, 2)
        kayit["dane_m2_gercek_gram"] = get(rows, 20, 3)

        # S22 (idx=21)
        kayit["bin_dane_agirlik_gram"] = get(rows, 21, 2)

        # S23 (idx=22)
        kayit["ort_bitki_boyu_cm"] = get(rows, 22, 2)

        # S24 (idx=23)
        kayit["ort_basak_boyu_cm"] = get(rows, 23, 2)

    except Exception as e:
        kayit["okuma_notu"] = f"HATA: {e}"

    return kayit


def main():
    os.makedirs(os.path.dirname(CIKTI), exist_ok=True)

    dosyalar = sorted([f for f in os.listdir(KAYNAK) if f.lower().endswith(".xlsx")])
    print(f"Toplam {len(dosyalar)} xlsx dosyası bulundu.")

    sonuclar = []
    hatali_sayisi = 0

    for i, dosya in enumerate(dosyalar, 1):
        yol = os.path.join(KAYNAK, dosya)
        kayit = dosyayi_isle(yol)
        sonuclar.append(kayit)

        if kayit.get("okuma_notu") and kayit["okuma_notu"].startswith("HATA"):
            hatali_sayisi += 1
            print(f"  [HATA] {dosya}: {kayit['okuma_notu']}")

        if i % 100 == 0:
            print(f"  {i}/{len(dosyalar)} işlendi...")

    print(f"\n{len(sonuclar)} dosya işlendi, {hatali_sayisi} hata.")

    enlem_dolu  = sum(1 for s in sonuclar if s.get("enlem_raw") is not None)
    verim_dolu  = sum(1 for s in sonuclar if s.get("dane_m2_hesap_gram") is not None)
    sulama_dolu = sum(1 for s in sonuclar if s.get("sulama_tipi") is not None)
    print(f"Enlem dolu        : {enlem_dolu}/{len(sonuclar)}")
    print(f"Verim (hesap) dolu: {verim_dolu}/{len(sonuclar)}")
    print(f"Sulama tipi dolu  : {sulama_dolu}/{len(sonuclar)}")

    with open(CIKTI, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=KOLONLAR)
        writer.writeheader()
        writer.writerows(sonuclar)

    print(f"\nÇıktı: {CIKTI}")
    print(f"Boyut : {os.path.getsize(CIKTI) / 1024:.1f} KB")


if __name__ == "__main__":
    main()
