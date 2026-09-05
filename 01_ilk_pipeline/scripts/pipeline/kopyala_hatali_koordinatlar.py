import pandas as pd
import shutil
import os

KAYNAK_KLASOR = r"D:\_Development\Projects\UYSM_Projects\data\source\UYSM-EXECELL HESAPLAMALARI 0-300 DOSYA"
HEDEF_KLASOR  = r"D:\_Development\Projects\UYSM_Projects\data\processed\Koordinati Hatali Veriler"
MERGED        = r"D:\_Development\Projects\UYSM_Projects\data\processed\UYSM_merged.csv"

df = pd.read_csv(MERGED)
hatali = df[df["analiz_durumu"].isin(["koordinat_disi", "koordinat_yok"])]

os.makedirs(HEDEF_KLASOR, exist_ok=True)

kopyalandi, bulunamadi = 0, []

for dosya_adi in hatali["dosya_adi"]:
    kaynak = os.path.join(KAYNAK_KLASOR, dosya_adi)
    hedef  = os.path.join(HEDEF_KLASOR, dosya_adi)
    if os.path.exists(kaynak):
        shutil.copy2(kaynak, hedef)
        kopyalandi += 1
    else:
        bulunamadi.append(dosya_adi)

print(f"Kopyalanan : {kopyalandi} dosya")
print(f"Hedef      : {HEDEF_KLASOR}")
if bulunamadi:
    print(f"Bulunamadi : {bulunamadi}")
