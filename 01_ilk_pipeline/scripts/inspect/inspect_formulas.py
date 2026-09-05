"""
Bir xlsx dosyasındaki tüm formülleri ve değerleri yan yana gösterir.
Hem formüllü hem de değer olarak açıp karşılaştırır.
"""
import openpyxl
import os

KLASOR = r"D:\_Development\Projects\UYSM_Projects\data\source\UYSM-EXECELL HESAPLAMALARI 0-300 DOSYA"

# İki farklı dosyayı karşılaştır: biri 4x, diğeri 16x kullanan
DOSYALAR = [
    "0101 2km 143.xlsx",   # 16x kullanan
    "0103 291.xlsx",        # 4x kullanan
]

for dosya in DOSYALAR:
    yol = os.path.join(KLASOR, dosya)

    # Formüllü versiyon
    wb_f = openpyxl.load_workbook(yol, read_only=False, data_only=False)
    # Hesaplanmış versiyon
    wb_v = openpyxl.load_workbook(yol, read_only=False, data_only=True)

    ws_f = wb_f.active
    ws_v = wb_v.active

    print(f"\n{'='*70}")
    print(f"DOSYA: {dosya}")
    print(f"{'='*70}")
    print(f"{'Hücre':<6} {'Etiket (A sütunu)':<40} {'Formül/Değer':<35} {'Sonuç'}")
    print("-" * 110)

    for row_idx in range(1, 28):
        row_f = ws_f[row_idx]
        row_v = ws_v[row_idx]

        # A sütunu (etiket)
        etiket = str(row_f[0].value or "")[:38]

        # C, D, E sütunlarını göster (index 2, 3, 4)
        for col_idx, col_harf in [(2, "C"), (3, "D"), (4, "E")]:
            hucre_f = row_f[col_idx]
            hucre_v = row_v[col_idx]

            formul = str(hucre_f.value or "")
            sonuc  = str(hucre_v.value or "")

            if formul.startswith("=") or (sonuc and sonuc not in ["None", ""]):
                print(f"{col_harf}{row_idx:<4}  {etiket:<40} {formul:<35} {sonuc}")
                etiket = ""  # Aynı satırın devamında etiketi tekrar yazma

    wb_f.close()
    wb_v.close()
