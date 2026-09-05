import sys
sys.stdout.reconfigure(encoding='utf-8')
import openpyxl

path = r"D:\_Development\Projects\UYSM_Project_2\uysm_flash_bellek_degistirilmemis\hansay 2016 verim\Verim 8\4.KOORDİNATLAR LİSTESİ\koordinat bitkis işlevsel son2.xlsx"
wb = openpyxl.load_workbook(path, data_only=True)
ws = wb.active
rows = list(ws.iter_rows(values_only=True))

# Sutun 2 (rapor no) gercek degerler - ilk 20 ve son 20
print("Sutun 2 (rapor no) - ilk 20:")
for r in rows[:20]:
    print(f"  ist={r[0]}  rno={r[1]}  enlem={r[2]}  boylam={r[3]}  mesafe={r[6]}  aci={r[7]}")

print("\nSutun 2 (rapor no) - son 10:")
for r in rows[-10:]:
    print(f"  ist={r[0]}  rno={r[1]}  enlem={r[2]}  boylam={r[3]}  mesafe={r[6]}  aci={r[7]}")

# Rapor no gercekte ne icerikli?
rno_vals = [r[1] for r in rows if r[1] is not None]
print(f"\nRapor no sutunu: min={min(rno_vals, key=lambda x: int(x) if str(x).isdigit() else 9999)}  max={max(rno_vals, key=lambda x: int(x) if str(x).isdigit() else 0)}")
non_digit = [v for v in rno_vals if not str(v).isdigit()]
print(f"Sayisal olmayan degerler ({len(non_digit)}): {non_digit[:10]}")

# Sutun 5 ve 6 - sadece 1 dolu satiri bul
print("\nSutun 5 ve 6 (nadiren dolu):")
for r in rows:
    if r[4] is not None or r[5] is not None:
        print(f"  {r}")
