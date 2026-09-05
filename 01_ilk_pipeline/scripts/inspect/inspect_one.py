"""
Tek bir xlsx dosyasının tüm hücrelerini satır satır yazdırır.
"""
import openpyxl

DOSYA = r"D:\_Development\Projects\UYSM_Projects\data\source\UYSM-EXECELL HESAPLAMALARI 0-300 DOSYA\0103 291.xlsx"

wb = openpyxl.load_workbook(DOSYA, read_only=True, data_only=True)

# Tüm sheet isimlerini göster
print("Sheet'ler:", wb.sheetnames)
print()

ws = wb.active
for i, row in enumerate(ws.iter_rows(max_row=25, values_only=True), start=1):
    # None olmayan değerleri göster
    degerler = {j+1: v for j, v in enumerate(row) if v is not None}
    if degerler:
        print(f"Satır {i:2d}: {degerler}")

wb.close()
