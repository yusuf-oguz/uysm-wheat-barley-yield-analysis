"""
Birden fazla xlsx dosyasında hangi satırda ne olduğunu karşılaştırır.
Satır etiketlerini ve 3. sütundaki değerleri gösterir.
"""
import os
import openpyxl

KLASOR = r"D:\_Development\Projects\UYSM_Projects\data\source\UYSM-EXECELL HESAPLAMALARI 0-300 DOSYA"

# Farklı istasyonlardan örnekler
ORNEKLER = [
    "0101 2km 143.xlsx",
    "0103 291.xlsx",
    "0201 3.xlsx",
    "0202 2KM 8 .xlsx",
    "0301 5.xlsx",
]

HEDEF_SATIRLAR = [
    "TTR",         # enlem satırı
    "Rapor no",    # boylam satırı
    "1 m2 de toplanan",  # dane ağırlığı
]

for dosya in ORNEKLER:
    yol = os.path.join(KLASOR, dosya)
    if not os.path.exists(yol):
        print(f"{dosya}: DOSYA YOK\n")
        continue

    print(f"\n=== {dosya} ===")
    try:
        wb = openpyxl.load_workbook(yol, read_only=True, data_only=True)
        ws = wb.active

        for i, row in enumerate(ws.iter_rows(max_row=30, values_only=True), start=1):
            col1 = str(row[0]) if row[0] is not None else ""
            col3 = row[2] if len(row) > 2 else None
            col4 = row[3] if len(row) > 3 else None
            col5 = row[4] if len(row) > 4 else None

            # Sadece ilgili satırları göster
            if any(h.lower() in col1.lower() for h in HEDEF_SATIRLAR):
                print(f"  Satır {i:2d}: [{col1[:40]}] | C3={col3} | C4={col4} | C5={col5}")
            elif i <= 5:  # ilk 5 satırı her zaman göster
                print(f"  Satır {i:2d}: [{col1[:40]}] | C3={col3} | C5={col5}")

        wb.close()
    except Exception as e:
        print(f"  HATA: {e}")
