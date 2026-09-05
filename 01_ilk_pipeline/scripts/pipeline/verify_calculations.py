"""
Her xlsx için:
1. Satır 29-38'deki ham 10 başak verisinden kendi ortalamamızı hesaplar
2. Spreadsheet'in E39/C39/D39 değerleriyle kıyaslar
3. Fark varsa işaretler
4. Kendi hesapladığımız dane ağırlığını çıktıya ekler
"""
import os
import openpyxl
import pandas as pd

KLASOR  = r"D:\_Development\Projects\UYSM_Projects\data\source\UYSM-EXECELL HESAPLAMALARI 0-300 DOSYA"
CIKTI   = r"D:\_Development\Projects\UYSM_Projects\data\processed\UYSM_hesap_kontrol.csv"
ESIK    = 0.01   # %1'den fazla fark varsa "uyuşmuyor" say

dosyalar = sorted([f for f in os.listdir(KLASOR) if f.endswith(".xlsx")])
sonuclar = []

for dosya in dosyalar:
    yol = os.path.join(KLASOR, dosya)
    try:
        wb_f = openpyxl.load_workbook(yol, data_only=False)
        wb_v = openpyxl.load_workbook(yol, data_only=True)
        ws_f = wb_f.active
        ws_v = wb_v.active

        def val(ws, row, col):
            """0-indexed col, 1-indexed row"""
            r = ws[row]
            return r[col].value if len(r) > col else None

        def num(v):
            try: return float(v)
            except: return None

        # E13: ölçek faktörü (4 veya 16)
        olcek = num(val(ws_v, 13, 4)) or 4

        # C11: 1/4 m2 başak sayısı
        c11 = num(val(ws_v, 11, 2))

        # C41: tarladan tartılan toplam ağırlık (mgr)
        c41 = num(val(ws_v, 41, 2))

        # Spreadsheet'in kendi hesapladığı toplamlar (satır 39)
        xls_sum_c = num(val(ws_v, 39, 2))  # C39
        xls_sum_d = num(val(ws_v, 39, 3))  # D39
        xls_sum_e = num(val(ws_v, 39, 4))  # E39

        # E39'un formül mü sabit mi olduğunu kontrol et
        e39_formul = val(ws_f, 39, 4)
        e39_formul_mu = str(e39_formul).startswith("=") if e39_formul else False

        # Ham veriden kendi toplamımızı hesapla (satır 29-38 = index 29-38)
        bizim_sum_c = bizim_sum_d = bizim_sum_e = 0.0
        dolu_satir = 0
        for row_idx in range(29, 39):
            c = num(val(ws_v, row_idx, 2))
            d = num(val(ws_v, row_idx, 3))
            e = num(val(ws_v, row_idx, 4))
            if c and d and e:
                bizim_sum_c += c
                bizim_sum_d += d
                bizim_sum_e += e
                dolu_satir += 1

        if dolu_satir == 0:
            wb_f.close(); wb_v.close()
            sonuclar.append({"dosya_adi": dosya, "hata": "ham veri yok"})
            continue

        # Ortalamalar
        bizim_avg_c = bizim_sum_c / dolu_satir
        bizim_avg_d = bizim_sum_d / dolu_satir
        bizim_avg_e = bizim_sum_e / dolu_satir

        # E39 uyuşumu
        e39_fark = abs(bizim_sum_e - xls_sum_e) / bizim_sum_e if bizim_sum_e else None
        e39_uyusumu = (e39_fark is not None and e39_fark < ESIK)

        # Bizim hesapladığımız dane ağırlıkları
        bizim_hesap = None
        bizim_gercek = None

        if c11 and bizim_avg_e:
            bizim_hesap = round((bizim_avg_e / 1000) * c11 * olcek, 4)

        if c41 and bizim_avg_c and bizim_avg_e:
            oran = bizim_avg_e / bizim_avg_c
            bizim_gercek = round(c41 * oran * olcek / 1000, 4)

        # Spreadsheet'in değerleri
        xls_hesap = num(val(ws_v, 21, 2))
        xls_gercek = num(val(ws_v, 21, 3))

        sonuclar.append({
            "dosya_adi"      : dosya,
            "olcek_faktoru"  : int(olcek),
            "dolu_satir"     : dolu_satir,
            "e39_formul_mu"  : e39_formul_mu,
            "e39_uyusumu"    : e39_uyusumu,
            "xls_sum_e"      : round(xls_sum_e, 1) if xls_sum_e else None,
            "bizim_sum_e"    : round(bizim_sum_e, 1),
            "e39_fark_pct"   : round(e39_fark * 100, 2) if e39_fark is not None else None,
            "xls_hesap"      : round(xls_hesap, 2) if xls_hesap else None,
            "bizim_hesap"    : bizim_hesap,
            "xls_gercek"     : round(xls_gercek, 2) if xls_gercek else None,
            "bizim_gercek"   : bizim_gercek,
        })

        wb_f.close(); wb_v.close()

    except Exception as ex:
        sonuclar.append({"dosya_adi": dosya, "hata": str(ex)})

# --- Çıktı ---
df = pd.DataFrame(sonuclar)
df.to_csv(CIKTI, index=False, encoding="utf-8-sig")

print("=== GENEL OZET ===")
hatali        = df["hata"].notna().sum() if "hata" in df.columns else 0
e39_uyusmuyor = (df["e39_uyusumu"] == False).sum()
formul_degil  = (df["e39_formul_mu"] == False).sum()

print(f"Toplam dosya          : {len(df)}")
print(f"Ham veri yok / hata   : {hatali}")
print(f"E39 formul degil      : {formul_degil}")
print(f"E39 uyusmuyor (>%1)   : {e39_uyusmuyor}")

print("\n=== E39 UYUSMAZLIKLARI (ilk 20) ===")
uyusmazlik = df[df["e39_uyusumu"] == False][
    ["dosya_adi","e39_formul_mu","xls_sum_e","bizim_sum_e","e39_fark_pct","xls_hesap","bizim_hesap","xls_gercek","bizim_gercek"]
].head(20)
print(uyusmazlik.to_string(index=False))

print(f"\nKontrol CSV kaydedildi: {CIKTI}")
