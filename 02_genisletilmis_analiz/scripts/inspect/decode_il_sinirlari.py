"""
IL_SINIRLARI shapefile'larındaki v0-v47 sütunlarını çözer ve
turkiye_iller_shp_Arpa/Bugday altındaki Il_arpa.csv / Il_bugday.csv'yi
okunabilir formata dönüştürür.

Çıktılar: yusuf_oguz_calismalari/data/il_verim/
  - Il_arpa_temiz.csv
  - Il_bugday_temiz.csv
  - v_kolon_aciklamasi.csv   (v0-v47 → anlamı eşleşme tablosu)
"""

import pandas as pd
import geopandas as gpd
import os, sys

sys.stdout.reconfigure(encoding='utf-8')

BASE_FLASH = r"D:\_Development\Projects\UYSM_Project_2\uysm_flash_bellek_degistirilmemis\Tarbil_Serdar Bağış\Uhuzam\Jpeg\verim tablolari2015"
OUT_DIR = r"D:\_Development\Projects\UYSM_Project_2\yusuf_oguz_calismalari\data\il_verim"
os.makedirs(OUT_DIR, exist_ok=True)

# v0-v47 sütun eşleştirmesi
# Her blok: VERIM(6) + ALAN(4) + URETIM(6) = 16 sütun
# Sıra: Genel → Kuru → Sulu
YILLAR_VERIM  = ['TÜİK_2012', 'TÜİK_2013', 'TÜİK_2014', 'T.Otsu_2015', 'T.Ort_2015', 'T.KLR_2015']
YILLAR_ALAN   = ['TÜİK_2012', 'TÜİK_2013', 'TÜİK_2014', 'Tüml_2015']
YILLAR_URETIM = ['TÜİK_2012', 'TÜİK_2013', 'TÜİK_2014', 'T.Otsu_2015', 'T.Ort_2015', 'T.KLR_2015']

def build_colmap():
    """v0–v47 → (grup, metrik, yıl) üçlüsü"""
    colmap = {}
    idx = 0
    for grup in ['Genel', 'Kuru', 'Sulu']:
        for yil in YILLAR_VERIM:
            colmap[f'v{idx}'] = (grup, 'Verim_kg_da', yil)
            idx += 1
        for yil in YILLAR_ALAN:
            colmap[f'v{idx}'] = (grup, 'Alan_da', yil)
            idx += 1
        for yil in YILLAR_URETIM:
            colmap[f'v{idx}'] = (grup, 'Uretim_ton', yil)
            idx += 1
    return colmap

def decode_shapefile(shp_path, il_csv_path, bitki, colmap):
    shp = gpd.read_file(shp_path)
    vcols = [c for c in shp.columns if c.startswith('v')]

    # CSV'yi oku (sütun 0 = IL kodu 1-based, sütunlar 1-48 = v0-v47)
    csv_df = pd.read_csv(il_csv_path, encoding='utf-8', header=None)

    # Shapefile IL kolonunu bul
    il_col = 'IL' if 'IL' in shp.columns else None
    ad_col = 'AD' if 'AD' in shp.columns else None

    # Long-format tablo oluştur
    records = []
    for _, row in shp.iterrows():
        il_kodu = row.get(il_col) if il_col else None
        il_adi  = row.get(ad_col) if ad_col else None
        for vc in vcols:
            if vc in colmap:
                grup, metrik, yil = colmap[vc]
                records.append({
                    'il_kodu': il_kodu,
                    'il_adi':  il_adi,
                    'bitki':   bitki,
                    'grup':    grup,
                    'metrik':  metrik,
                    'yil':     yil,
                    'deger':   row[vc],
                })

    long_df = pd.DataFrame(records)

    # Wide-format: il × (grup_metrik_yıl)
    wide_df = shp[[ad_col, il_col] + vcols].copy() if il_col and ad_col else shp[vcols].copy()
    col_rename = {vc: f"{colmap[vc][0]}_{colmap[vc][1]}_{colmap[vc][2]}" for vc in vcols if vc in colmap}
    wide_df = wide_df.rename(columns=col_rename)

    return long_df, wide_df

def main():
    colmap = build_colmap()

    # Eşleştirme tablosunu kaydet
    rows = [{'v_sutun': k, 'grup': v[0], 'metrik': v[1], 'yil': v[2]} for k, v in colmap.items()]
    pd.DataFrame(rows).to_csv(os.path.join(OUT_DIR, 'v_kolon_aciklamasi.csv'),
                              index=False, encoding='utf-8-sig')
    print("v_kolon_aciklamasi.csv kaydedildi")

    for bitki in ['arpa', 'bugday']:
        bitki_label = 'Arpa' if bitki == 'arpa' else 'Bugday'
        shp_path = os.path.join(BASE_FLASH, f'IL_SINIRLARI_{bitki}', 'iller_WGS84_COG.shp')
        csv_path = os.path.join(BASE_FLASH, f'turkiye_iller_shp_{bitki_label}', f'Il_{bitki}.csv')

        print(f"\n--- {bitki.upper()} ---")
        long_df, wide_df = decode_shapefile(shp_path, csv_path, bitki_label, colmap)

        long_out = os.path.join(OUT_DIR, f'Il_{bitki}_long.csv')
        wide_out = os.path.join(OUT_DIR, f'Il_{bitki}_wide.csv')

        long_df.to_csv(long_out, index=False, encoding='utf-8-sig')
        wide_df.to_csv(wide_out, index=False, encoding='utf-8-sig')

        print(f"  Long format: {len(long_df)} satır → {long_out}")
        print(f"  Wide format: {len(wide_df)} il, {len(wide_df.columns)} sütun → {wide_out}")

        # Doğrulama: Ankara değerleri
        if 'AD' in wide_df.columns:
            ankara = wide_df[wide_df['AD'].str.contains('ANKARA', na=False, case=False)]
            if not ankara.empty:
                row = ankara.iloc[0]
                print(f"  Ankara Genel Verim TÜİK_2012: {row.get('Genel_Verim_kg_da_TÜİK_2012', '?')}")
                print(f"  Ankara Genel Alan TÜİK_2012:  {row.get('Genel_Alan_da_TÜİK_2012', '?')}")

if __name__ == '__main__':
    main()
