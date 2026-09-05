"""
Koordinat sistemini anlamak için ilk 20 dosyayı okur,
enlem/boylam değerlerini ve dane ağırlığını yazdırır.
"""
import os
import openpyxl

KLASOR = r"D:\_Development\Projects\UYSM_Projects\data\source\UYSM-EXECELL HESAPLAMALARI 0-300 DOSYA"

dosyalar = sorted([f for f in os.listdir(KLASOR) if f.endswith(".xlsx")])[:25]

print(f"{'Dosya':<35} {'Enlem':>12} {'Boylam':>12} {'Dane_gr_m2':>14} {'E_hane':>7} {'B_hane':>7}")
print("-" * 95)

for dosya in dosyalar:
    yol = os.path.join(KLASOR, dosya)
    try:
        wb = openpyxl.load_workbook(yol, read_only=True, data_only=True)
        ws = wb.active

        satirlar = list(ws.iter_rows(min_row=1, max_row=20, values_only=True))

        # Satır 1 (index 0): enlem satır 2 (index 1): boylam
        enlem = satirlar[0][4] if len(satirlar[0]) > 4 else None
        boylam = satirlar[1][4] if len(satirlar[1]) > 4 else None

        # Satır 19 (index 18): dane ağırlığı
        dane = satirlar[18][2] if len(satirlar) > 18 and len(satirlar[18]) > 2 else None

        e_hane = len(str(int(enlem))) if enlem and str(enlem).replace('.','').isdigit() else "?"
        b_hane = len(str(int(boylam))) if boylam and str(boylam).replace('.','').isdigit() else "?"

        print(f"{dosya:<35} {str(enlem):>12} {str(boylam):>12} {str(dane):>14} {str(e_hane):>7} {str(b_hane):>7}")
        wb.close()
    except Exception as e:
        print(f"{dosya:<35} HATA: {e}")
