import openpyxl

DOSYA = r"D:\_Development\Projects\UYSM_Projects\data\source\UYSM-EXECELL HESAPLAMALARI 0-300 DOSYA\01118 6 .xlsx"

wb_f = openpyxl.load_workbook(DOSYA, data_only=False)
wb_v = openpyxl.load_workbook(DOSYA, data_only=True)
ws_f = wb_f.active
ws_v = wb_v.active

print("=== SATIRLAR 27-42: FORMUL ve DEGER ===")
print(f"{'Hucre':<6} {'A (etiket)':<35} {'B formul':<25} {'C formul':<25} {'D formul':<25} {'E formul':<30} {'E deger'}")
print("-"*170)

for row_idx in range(27, 43):
    row_f = ws_f[row_idx]
    row_v = ws_v[row_idx]

    etiket  = str(row_f[0].value or "")[:33]
    b_f     = str(row_f[1].value or "")
    c_f     = str(row_f[2].value or "")
    d_f     = str(row_f[3].value or "")
    e_f     = str(row_f[4].value or "")
    e_v     = str(row_v[4].value or "")

    if any([b_f, c_f, d_f, e_f, e_v]):
        print(f"{row_idx:<6} {etiket:<35} {b_f:<25} {c_f:<25} {d_f:<25} {e_f:<30} {e_v}")

print("\n=== E29:E38 HAM DEGERLER ===")
bizim_toplam = 0
dolu = 0
for row_idx in range(29, 39):
    e_v = ws_v[row_idx][4].value
    print(f"  E{row_idx}: {e_v}")
    if e_v and str(e_v).replace('.','').replace('-','').isdigit():
        bizim_toplam += float(e_v)
        dolu += 1

print(f"\nBizim toplam (E29:E38): {bizim_toplam}  (dolu satir: {dolu})")
print(f"XLS E39 degeri:        {ws_v[39][4].value}")
print(f"XLS E39 formulu:       {ws_f[39][4].value}")

wb_f.close()
wb_v.close()
