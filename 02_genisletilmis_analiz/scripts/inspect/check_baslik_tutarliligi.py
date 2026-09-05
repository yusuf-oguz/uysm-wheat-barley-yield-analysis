"""
Hansay xlsx — A ve diğer etiket sütunlarının tutarlılık kontrolü
-----------------------------------------------------------------
A3:A26 arası (A11 hariç) etiket hücrelerini tüm dosyalarda okur,
birden fazla farklı değer içeren hücreleri raporlar.

Ek olarak kontrol edilen etiket konumları:
  - E3 (enlem etiketi), D3 (boylam etiketi?)
  - E4 (boylam etiketi), D4
  - E5, E6, E7, E8, E9, E10 (sağ taraf etiketleri)

Çıktı: data/processed/baslik_tutarliligi.csv (sadece farklılık olanlar)
Ekrana: tüm kontrol edilen hücreler özet olarak
"""

import os
import csv
import collections
import openpyxl

KAYNAK = (
    r"D:\_Development\Projects\UYSM_Project_2"
    r"\uysm_flash_bellek_degistirilmemis"
    r"\hansay 2016 verim\Verim 8"
    r"\1.EXEL HESAPLAR TABLOLARI (7 CİLT)"
)

CIKTI = (
    r"D:\_Development\Projects\UYSM_Project_2"
    r"\yusuf_oguz_calismalari\data\processed\tmp\baslik_tutarliligi.csv"
)

# Kontrol edilecek hücreler: (satir_1bazli, col_0bazli, etiket)
# Sadece sabit etiket (başlık) içermesi beklenen hücreler.
# Veri hücreleri (koordinat, tarih, isim vb.) dahil edilmez.
# A sütunu = col 0, D=3, E=4 (sadece etiket olan satırlar)
KONTROL_NOKTALARI = []

# A sütunu: A3:A26, A11 hariç (tüm A sütunu etiket içerir)
for satir in range(3, 27):
    if satir == 11:
        continue
    KONTROL_NOKTALARI.append((satir, 0, f"A{satir}"))

# Sağ taraf etiket hücreleri (veri değil, sabit başlık içermeli)
# D3=enlem etiketi, D4=boylam etiketi, E5=şehir etiketi,
# E6=sulama etiketi, E7=sulama sayısı etiketi, E8=kamera yönü etiketi,
# E9=fenolojik evre etiketi, E10=ürünü alan etiketi, E11=ürünü sayan etiketi
SABIT_ETIKET_NOKTALARI = [
    (3,  3, "D3"),   # enlem etiketi
    (4,  3, "D4"),   # boylam etiketi
    (5,  4, "E5"),   # şehir etiketi
    (6,  4, "E6"),   # sulama tipi etiketi
    (7,  4, "E7"),   # sulama sayısı etiketi
    (8,  4, "E8"),   # kamera yönü etiketi
    (9,  4, "E9"),   # fenolojik evre etiketi
    (10, 4, "E10"),  # ürünü alan etiketi
    (11, 4, "E11"),  # ürünü sayan etiketi
]
KONTROL_NOKTALARI += SABIT_ETIKET_NOKTALARI


def main():
    dosyalar = sorted([
        f for f in os.listdir(KAYNAK)
        if f.lower().endswith(".xlsx") and not f.startswith("~")
    ])
    print(f"Toplam {len(dosyalar)} dosya kontrol ediliyor...")

    # Her nokta için değer sayacı
    sayaclar = {etiket: collections.Counter() for _, _, etiket in KONTROL_NOKTALARI}

    for dosya in dosyalar:
        yol = os.path.join(KAYNAK, dosya)
        try:
            wb = openpyxl.load_workbook(yol, read_only=True, data_only=True)
            ws = wb.active
            rows = list(ws.iter_rows(min_row=1, max_row=26, values_only=True))
            wb.close()

            for satir, col, etiket in KONTROL_NOKTALARI:
                row = rows[satir - 1] if satir - 1 < len(rows) else None
                val = row[col] if row and len(row) > col else None
                sayaclar[etiket][str(val)] += 1

        except Exception as e:
            print(f"  HATA {dosya}: {e}")

    # Rapor
    tutarsiz = []
    print()
    print("=== TUTARSIZ HÜCRELER ===")
    for _, _, etiket in KONTROL_NOKTALARI:
        sayac = sayaclar[etiket]
        # None tek başına farklılık sayılmasın — anlamlı değerlere bak
        anlamli = {k: v for k, v in sayac.items() if k != "None"}
        if len(anlamli) > 1:
            print(f"\n  {etiket} — {len(anlamli)} farklı değer:")
            for k, v in sorted(sayac.items(), key=lambda x: -x[1]):
                print(f"    {v:4d}x  {repr(k[:60]) if len(k) > 60 else repr(k)}")
            tutarsiz.append(etiket)

    if not tutarsiz:
        print("  Hiç tutarsızlık yok.")

    print(f"\nToplam kontrol edilen hücre konumu: {len(KONTROL_NOKTALARI)}")
    print(f"Tutarsız olanlar: {len(tutarsiz)}")

    # CSV çıktısı
    os.makedirs(os.path.dirname(CIKTI), exist_ok=True)
    satirlar = []
    for _, _, etiket in KONTROL_NOKTALARI:
        sayac = sayaclar[etiket]
        anlamli = {k: v for k, v in sayac.items() if k != "None"}
        if len(anlamli) > 1:
            for deger, sayi in sorted(sayac.items(), key=lambda x: -x[1]):
                satirlar.append({
                    "hucre": etiket,
                    "deger": deger,
                    "dosya_sayisi": sayi,
                })

    if satirlar:
        with open(CIKTI, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=["hucre", "deger", "dosya_sayisi"])
            writer.writeheader()
            writer.writerows(satirlar)
        print(f"Çıktı: {CIKTI}")
    else:
        print("Tutarsızlık olmadığı için CSV oluşturulmadı.")


if __name__ == "__main__":
    main()
