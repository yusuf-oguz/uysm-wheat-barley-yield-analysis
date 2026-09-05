"""
Satır 35-50 arasını inceler — gerçek değerin kaynağı E42'yi anlamak için.
"""
import openpyxl
import os

KLASOR = r"D:\_Development\Projects\UYSM_Projects\data\source\UYSM-EXECELL HESAPLAMALARI 0-300 DOSYA"
DOSYALAR = ["0101 2km 143.xlsx", "0103 291.xlsx"]

for dosya in DOSYALAR:
    yol = os.path.join(KLASOR, dosya)
    wb_f = openpyxl.load_workbook(yol, data_only=False)
    wb_v = openpyxl.load_workbook(yol, data_only=True)
    ws_f = wb_f.active
    ws_v = wb_v.active

    print(f"\n{'='*75}")
    print(f"DOSYA: {dosya}  |  Sayfa: {wb_f.sheetnames}")
    print(f"{'='*75}")
    print(f"{'Hücre':<6} {'Etiket (A)':<38} {'Formül':<38} {'Sonuç'}")
    print("-" * 100)

    for row_idx in range(35, 52):
        row_f = ws_f[row_idx]
        row_v = ws_v[row_idx]
        etiket = str(row_f[0].value or "")[:36]

        for col_idx, col_harf in [(1,"B"),(2,"C"),(3,"D"),(4,"E"),(5,"F"),(9,"J")]:
            hucre_f = row_f[col_idx]
            hucre_v = row_v[col_idx]
            formul = str(hucre_f.value or "")
            sonuc  = str(hucre_v.value or "")
            if formul or (sonuc and sonuc != "None"):
                print(f"{col_harf}{row_idx:<4}  {etiket:<38} {formul:<38} {sonuc}")
                etiket = ""

    wb_f.close()
    wb_v.close()
