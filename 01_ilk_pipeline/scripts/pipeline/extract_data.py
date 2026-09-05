"""
UYSM Proje - Veri Çıkarma Scripti
-----------------------------------
Tüm xlsx dosyalarından enlem, boylam ve dane ağırlığı verilerini çekerek
tek bir CSV dosyasına toplar.

Çıktı: UYSM_merged.csv
"""

import os
import re
import csv
import openpyxl

KLASOR = r"D:\_Development\Projects\UYSM_Projects\data\source\UYSM-EXECELL HESAPLAMALARI 0-300 DOSYA"
CIKTI = r"D:\_Development\Projects\UYSM_Projects\data\processed\UYSM_merged.csv"


def raw_koordinat_to_decimal(raw):
    """
    Ham tam sayı koordinatı ondalık dereceye çevirir.
    Örnek: 3643467 -> 36.43467, 37435578 -> 37.435578
    """
    if raw is None:
        return None
    try:
        raw_int = int(float(str(raw)))
        if raw_int <= 0:
            return None
        s = str(raw_int)
        if len(s) < 3:
            return float(raw_int)  # Zaten tam derece
        return raw_int / (10 ** (len(s) - 2))
    except (ValueError, TypeError):
        return None


def koordinat_gecerli_mi(enlem, boylam):
    """Türkiye sınırları için basit kontrol (36-42N, 26-45E)."""
    if enlem is None or boylam is None:
        return False
    return 35.0 <= enlem <= 43.0 and 25.0 <= boylam <= 46.0


def satirda_ara(satirlar, anahtar, sutun=0):
    """Satırlar içinde anahtar metni arar, bulunan satırı döner."""
    for i, row in enumerate(satirlar):
        val = row[sutun] if row and len(row) > sutun else None
        if val and anahtar.lower() in str(val).lower():
            return i, row
    return None, None


def dosyayi_isle(yol):
    """
    Tek bir xlsx dosyasından verileri çıkarır.
    Döner: dict veya None (hata durumunda)
    """
    dosya_adi = os.path.basename(yol)

    try:
        wb = openpyxl.load_workbook(yol, read_only=True, data_only=True)
        ws = wb.active

        # İlk 30 satırı oku
        satirlar = list(ws.iter_rows(min_row=1, max_row=30, values_only=True))
        wb.close()

        # Sabit satır konumları (2 boş satır + veri başlangıcı)
        # Satır 3 (index 2): TTR başlığı, enlem col 5 (index 4)
        # Satır 4 (index 3): Rapor no, boylam col 5 (index 4)
        # Satır 5 (index 4): Tarih, şehir
        # Satır 6 (index 5): İstasyon No
        # Satır 9 (index 8): Bitki adı
        # Satır 10 (index 9): Çeşit adı
        # Satır 12 (index 11): 1 M2 Başak sayısı
        # Satır 21 (index 20): 1 m2 dane ağırlığı gram
        # Satır 23 (index 22): Ortalama bitki boyu
        # Satır 24 (index 23): Ortalama başak boyu

        def get(row_idx, col_idx):
            """Güvenli hücre okuma."""
            if row_idx >= len(satirlar):
                return None
            row = satirlar[row_idx]
            if row is None or col_idx >= len(row):
                return None
            return row[col_idx]

        # Önce sabit konumlarla dene, başarısız olursa etiket arama yap
        enlem_raw = get(2, 4)
        boylam_raw = get(3, 4)

        # Etiket tabanlı doğrulama: "enlem" etiketi row 3 col 4'te mi?
        enlem_etiketi = get(2, 3)
        if enlem_etiketi is None or "enlem" not in str(enlem_etiketi).lower():
            # Etiket burada değil, ara
            idx, row = satirda_ara(satirlar, "enlem", sutun=3)
            if idx is not None:
                enlem_raw = satirlar[idx][4] if len(satirlar[idx]) > 4 else None
                boylam_row = satirlar[idx + 1] if idx + 1 < len(satirlar) else None
                boylam_raw = boylam_row[4] if boylam_row and len(boylam_row) > 4 else None

        enlem = raw_koordinat_to_decimal(enlem_raw)
        boylam = raw_koordinat_to_decimal(boylam_raw)

        # Dane ağırlığı - "1 m2 de toplanan" etiketini ara
        dane_m2_hesap = None
        dane_m2_gercek = None

        idx, row = satirda_ara(satirlar, "1 m2 de toplanan", sutun=0)
        if idx is not None:
            dane_m2_hesap = satirlar[idx][2] if len(satirlar[idx]) > 2 else None
            dane_m2_gercek = satirlar[idx][3] if len(satirlar[idx]) > 3 else None

        # Diğer alanlar (sabit konumdan)
        rapor_no = get(3, 9)
        if rapor_no is None:
            rapor_no = get(0, 9)  # Bazı dosyalarda row 1'de olabilir

        istasyon_no = get(5, 2)
        tarih = get(4, 2)
        bitki_adi = get(8, 2)
        cesit_adi = get(9, 2)
        m2_basak_sayisi = get(11, 2)
        ortalama_bitki_boyu = get(22, 2)
        ortalama_basak_boyu = get(23, 2)

        # Koordinat geçerliliği
        koord_gecerli = koordinat_gecerli_mi(enlem, boylam)

        return {
            "dosya_adi": dosya_adi,
            "rapor_no": rapor_no,
            "istasyon_no": istasyon_no,
            "tarih": str(tarih)[:10] if tarih else None,
            "bitki_adi": str(bitki_adi) if bitki_adi else None,
            "cesit_adi": str(cesit_adi) if cesit_adi else None,
            "enlem_raw": enlem_raw,
            "boylam_raw": boylam_raw,
            "enlem": round(enlem, 6) if enlem else None,
            "boylam": round(boylam, 6) if boylam else None,
            "koordinat_gecerli": koord_gecerli,
            "m2_basak_sayisi": m2_basak_sayisi,
            "dane_m2_hesap_gram": round(dane_m2_hesap, 4) if isinstance(dane_m2_hesap, float) else dane_m2_hesap,
            "dane_m2_gercek_gram": round(dane_m2_gercek, 4) if isinstance(dane_m2_gercek, float) else dane_m2_gercek,
            "ortalama_bitki_boyu_cm": ortalama_bitki_boyu,
            "ortalama_basak_boyu_cm": ortalama_basak_boyu,
        }

    except Exception as e:
        return {
            "dosya_adi": dosya_adi,
            "hata": str(e),
        }


def main():
    dosyalar = sorted([f for f in os.listdir(KLASOR) if f.endswith(".xlsx")])
    print(f"Toplam {len(dosyalar)} xlsx dosyası bulundu.")

    sonuclar = []
    hatali = []

    for i, dosya in enumerate(dosyalar, 1):
        yol = os.path.join(KLASOR, dosya)
        veri = dosyayi_isle(yol)

        if "hata" in veri:
            hatali.append(veri)
            print(f"  [HATA] {dosya}: {veri['hata']}")
        else:
            sonuclar.append(veri)

        if i % 50 == 0:
            print(f"  {i}/{len(dosyalar)} işlendi...")

    print(f"\n{len(sonuclar)} dosya başarıyla işlendi, {len(hatali)} hata.")

    # İstatistikler
    koordinat_var = sum(1 for s in sonuclar if s.get("koordinat_gecerli"))
    dane_var = sum(1 for s in sonuclar if s.get("dane_m2_hesap_gram") is not None)
    print(f"Koordinat geçerli: {koordinat_var}/{len(sonuclar)}")
    print(f"Dane ağırlığı var: {dane_var}/{len(sonuclar)}")

    # CSV'ye yaz
    if sonuclar:
        kolonlar = list(sonuclar[0].keys())

        with open(CIKTI, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=kolonlar, extrasaction="ignore")
            writer.writeheader()
            for s in sonuclar:
                writer.writerow(s)

        print(f"\nÇıktı dosyası: {CIKTI}")

    # Hatalı dosyalar varsa listele
    if hatali:
        print("\nHatalı dosyalar:")
        for h in hatali:
            print(f"  - {h['dosya_adi']}: {h.get('hata', '?')}")


if __name__ == "__main__":
    main()
