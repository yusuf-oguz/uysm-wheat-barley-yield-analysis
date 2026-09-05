"""
Hesap ve gerçek dane ağırlığının nasıl hesaplandığını görmek için
birkaç dosyanın ilgili satırlarını yanyana koyar.
"""
import os
import openpyxl

KLASOR = r"D:\_Development\Projects\UYSM_Projects\data\source\UYSM-EXECELL HESAPLAMALARI 0-300 DOSYA"
DOSYALAR = ["0101 2km 143.xlsx", "0103 291.xlsx", "0201 3.xlsx", "0202 2KM 8 .xlsx"]

for dosya in DOSYALAR:
    yol = os.path.join(KLASOR, dosya)
    wb = openpyxl.load_workbook(yol, read_only=True, data_only=True)
    ws = wb.active
    satirlar = list(ws.iter_rows(min_row=1, max_row=27, values_only=True))

    def c(row_idx, col_idx):
        row = satirlar[row_idx]
        return row[col_idx] if row and len(row) > col_idx else None

    print(f"\n{'='*60}")
    print(f"DOSYA: {dosya}")
    print(f"{'='*60}")

    # İlgili satırlar (0-indexed)
    satirlar_ilgili = {
        "1/4 m2 basak sayisi  (row11,C3)": (10, 2),
        "1 m2 basak sayisi    (row12,C3)": (11, 2),
        "10 bitki dane sayisi (row13,C3)": (12, 2),  # aslında başaksız bitki?
        "1 m2 basaksiz bitki  (row14,C3)": (13, 2),
        "1 m2 toplam bitki    (row15,C3)": (14, 2),
        "10 bitki sap agirlik (row16,C3)": (15, 2),
        "1 m2 sap agirlik     (row17,C3)": (16, 2),
        "1 basak kilic.agirlik(row18,C3)": (17, 2),
        "1 basak dane sayisi  (row19,C3)": (18, 2),
        "1 basak dane agirlik (row20,C3)": (19, 2),
        "1 m2 dane agirlik    (row21,C3)": (20, 2),
        "1 m2 dane agirlik GRC(row21,C4)": (20, 3),
        "1000 dane agirlik    (row22,C3)": (21, 2),
    }

    for aciklama, (r, col) in satirlar_ilgili.items():
        deger = c(r, col)
        print(f"  {aciklama}: {deger}")

    # Doğrulama
    basak_m2  = c(11, 2)
    dane_agir = c(19, 2)
    hesap_val = c(20, 2)
    gercek_val = c(20, 3)

    if basak_m2 and dane_agir:
        carpim = round(basak_m2 * dane_agir, 4)
        print(f"\n  KONTROL: {basak_m2} basak x {dane_agir} g/basak = {carpim} g/m2")
        print(f"  Dosyadaki hesap degeri: {hesap_val}")
        print(f"  Dosyadaki gercek degeri: {gercek_val}")

    wb.close()
