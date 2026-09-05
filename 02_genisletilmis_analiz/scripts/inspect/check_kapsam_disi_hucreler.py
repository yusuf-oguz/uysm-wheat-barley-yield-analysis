"""
Kapsam dışı hücre kontrolü
---------------------------
A1:M45 aralığındaki hücrelerden hansay_ham_full.csv'de kullanılmayanları
tüm 769 dosya için okur ve geniş formatta CSV'ye yazar.

Sütunlar: dosya_adi + her kapsam dışı hücre (ör. F3, K7 ...)
Satırlar : her xlsx dosyası için bir satır
Değer    : hücrenin ham içeriği (boşsa None)

Sadece en az bir dosyada dolu olan hücreler sütun olarak eklenir.

Çıktı: data/processed/kapsam_disi_kontrol.csv
"""

import os
import re
import csv
import openpyxl
from openpyxl.utils import column_index_from_string, get_column_letter

KAYNAK = (
    r"D:\_Development\Projects\UYSM_Project_2"
    r"\uysm_flash_bellek_degistirilmemis"
    r"\hansay 2016 verim\Verim 8"
    r"\1.EXEL HESAPLAR TABLOLARI (7 CİLT)"
)

FULL_CSV = (
    r"D:\_Development\Projects\UYSM_Project_2"
    r"\yusuf_oguz_calismalari\data\processed\active\hansay_ham_full.csv"
)

CIKTI = (
    r"D:\_Development\Projects\UYSM_Project_2"
    r"\yusuf_oguz_calismalari\data\processed\tmp\kapsam_disi_kontrol.csv"
)

SATIR_MAX = 45
SUTUN_MAX = 13  # M sütunu


def kullanilan_hucreleri_bul():
    with open(FULL_CSV, encoding="utf-8-sig") as f:
        fieldnames = f.readline().strip().split(",")
    kullanilan = set()
    for ad in fieldnames:
        m = re.search(r"__([A-Z]+\d+)$", ad)
        if m:
            kullanilan.add(m.group(1).upper())
    return kullanilan


def main():
    kullanilan = kullanilan_hucreleri_bul()

    # Kontrol edilecek hücre listesi: A1:M45, kullanılanlar çıkarıldı
    kontrol = []
    for satir in range(1, SATIR_MAX + 1):
        for col_idx in range(1, SUTUN_MAX + 1):
            adres = f"{get_column_letter(col_idx)}{satir}"
            if adres not in kullanilan:
                kontrol.append((adres, satir - 1, col_idx - 1))

    print(f"Toplam hücre (A1:M45)  : {SATIR_MAX * SUTUN_MAX}")
    print(f"Zaten kullanılan       : {len(kullanilan)}")
    print(f"Kontrol edilecek       : {len(kontrol)}")

    dosyalar = sorted([
        f for f in os.listdir(KAYNAK)
        if f.lower().endswith(".xlsx") and not f.startswith("~")
    ])

    # Tüm dosyaları oku
    satirlar = []
    for i, dosya in enumerate(dosyalar, 1):
        yol = os.path.join(KAYNAK, dosya)
        kayit = {"dosya_adi": dosya}
        try:
            wb = openpyxl.load_workbook(yol, read_only=True, data_only=True)
            ws = wb.active
            rows = list(ws.iter_rows(
                min_row=1, max_row=SATIR_MAX,
                max_col=SUTUN_MAX, values_only=True
            ))
            wb.close()
            for adres, r_idx, c_idx in kontrol:
                try:
                    val = rows[r_idx][c_idx] if r_idx < len(rows) and rows[r_idx] and c_idx < len(rows[r_idx]) else None
                except Exception:
                    val = None
                kayit[adres] = val
        except Exception as e:
            for adres, _, _ in kontrol:
                kayit[adres] = None
            kayit["okuma_notu"] = f"HATA: {e}"

        satirlar.append(kayit)
        if i % 100 == 0:
            print(f"  {i}/{len(dosyalar)} işlendi...")

    # Sadece en az bir dosyada dolu olan sütunları tut
    dolu_adresler = []
    for adres, _, _ in kontrol:
        if any(s.get(adres) is not None for s in satirlar):
            dolu_adresler.append(adres)

    bos_adresler = [a for a, _, _ in kontrol if a not in dolu_adresler]
    print(f"\nTüm dosyalarda boş (atlandı): {len(bos_adresler)}")
    print(f"En az bir dosyada dolu      : {len(dolu_adresler)}")

    alan = ["dosya_adi"] + dolu_adresler
    if any("okuma_notu" in s for s in satirlar):
        alan.append("okuma_notu")

    for kayit in satirlar:
        for k in alan:
            kayit.setdefault(k, None)

    os.makedirs(os.path.dirname(CIKTI), exist_ok=True)
    with open(CIKTI, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=alan, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(satirlar)

    print(f"Çıktı: {CIKTI}")
    print(f"Boyut: {os.path.getsize(CIKTI) / 1024:.1f} KB")
    print(f"Sütun sayısı: {len(alan)}")


if __name__ == "__main__":
    main()
