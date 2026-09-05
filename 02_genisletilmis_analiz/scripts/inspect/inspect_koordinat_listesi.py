import sys
sys.stdout.reconfigure(encoding='utf-8')
import openpyxl
import re
from collections import defaultdict

path = r"D:\_Development\Projects\UYSM_Project_2\uysm_flash_bellek_degistirilmemis\hansay 2016 verim\Verim 8\4.KOORDİNATLAR LİSTESİ\koordinat bitkis işlevsel son2.xlsx"

wb = openpyxl.load_workbook(path, data_only=True)
ws = wb.active

rows = list(ws.iter_rows(values_only=True))
print(f"Toplam satir: {len(rows)}")

# Sutun yapisi
print("\nSutun analizi (tum satirlardaki deger turleri):")
col_samples = defaultdict(set)
col_none = defaultdict(int)
for row in rows:
    for i, val in enumerate(row):
        if val is None:
            col_none[i] += 1
        else:
            col_samples[i].add(type(val).__name__)

for i in range(8):
    sample_vals = []
    for row in rows[:10]:
        if len(row) > i and row[i] is not None:
            sample_vals.append(str(row[i]))
    print(f"  Sutun {i+1}: tipler={col_samples[i]}  bos={col_none[i]}/{len(rows)}  ornekler={sample_vals[:4]}")

# Sutun 7 (index 6) - mesafe/istasyon degerleri
print("\nSutun 7 (mesafe/yer) unique degerler ornegi:")
col7_vals = [str(r[6]) for r in rows if r[6] is not None]
istasyon_count = sum(1 for v in col7_vals if v.lower() == 'istasyon')
sayi_count = sum(1 for v in col7_vals if v.isdigit())
print(f"  'istasyon' yazanlar: {istasyon_count}")
print(f"  Sayisal mesafe yazanlar: {sayi_count}")
print(f"  Diger: {len(col7_vals) - istasyon_count - sayi_count}")
print(f"  Diger ornekler: {[v for v in col7_vals if not v.lower()=='istasyon' and not v.isdigit()][:10]}")

# Sutun 8 (index 7) - aci
print("\nSutun 8 (aci) dolu olan: ", sum(1 for r in rows if r[7] is not None))
print("  Ornekler:", [str(r[7]) for r in rows if r[7] is not None][:8])

# Istasyon kodu (sutun 1) analizi
print("\nIstasyon kodu (Sutun 1) analizi:")
il_counts = defaultdict(int)
for row in rows:
    kod = str(row[0]) if row[0] else ''
    il = kod[:2] if len(kod) >= 2 else kod
    il_counts[il] += 1
print(f"  Toplam unique il kodu: {len(il_counts)}")
print("  Il bazinda satir sayisi (en cok 15):")
for il, cnt in sorted(il_counts.items(), key=lambda x: -x[1])[:15]:
    print(f"    Il {il}: {cnt}")

# Rapor no (sutun 2) aralik
rapor_nos = [r[1] for r in rows if r[1] is not None]
print(f"\nRapor no (Sutun 2) aralik: {min(rapor_nos)} -- {max(rapor_nos)}")
print(f"  Unique rapor no sayisi: {len(set(rapor_nos))}")

# KMZ ile karsilastirma: kac rapor no ortusüyor
# KMZ'den bildigimiz: 2109 nokta, burada 814 satir
print(f"\nBu liste: 814 satir / KMZ: 2109 nokta")
print("Fark: KMZ daha kapsamli (tum GPS pinleri), bu liste secilmis/ozet koordinat tablosu olabilir")
