import pandas as pd

PATH = r'D:\_Development\Projects\UYSM_Project_2\yusuf_oguz_calismalari\data\processed\active\vAnaliz1.0.csv'

df = pd.read_csv(PATH, encoding='utf-8-sig', low_memory=False)

yeni_sira = [
    # --- Kimlik / Meta ---
    'dosya_adi__dosyaadi',
    'kismi_not',
    'null_sayisi',
    'bitki_adi__C9',
    'sulama_tipi__G6',
    'fenolojik_evre__G9',
    'tarih__C5',
    'tarih_lab__C42',
    'istasyon_no__C6',
    'rakim__C8',
    'okuma_notu',

    # --- Koordinat ---
    'enlem_dd_final',
    'boylam_dd_final',
    'il_koordinat_final',

    # --- Verim (türetilmiş, ana sonuçlar) ---
    'dane_m2_hesap_gram__C21',
    'dane_m2_gercek_gram__D21',
    'm2_sap_agirlik_kg__C17',

    # --- Ölçüm alanı ham değerleri ---
    'olcum_alani_basak__C11',
    'olcum_alani_carpani__E13',
    'basaksiz_bitki_sayisi__C13',
    'olcum_basak_agirlik_ham__C41',

    # --- Alan ölçekleme (türetilmiş) ---
    'm2_basak_sayisi__C12',
    'm2_basaksiz_bitki__C14',
    'm2_toplam_bitki__C15',

    # --- 10 başak ortalamaları ---
    'ort_basak_uzunluk_cm__B40',
    'ort_basak_agirlik_mg__C40',
    'ort_dane_sayisi__D40',
    'ort_dane_agirlik_mg__E40',
    'bir_basaktaki_ort_dane_agirlik_gram__C20',
    'bin_dane_agirlik_gram__C22',
    'basak_dane_oran__D41',
    'ort_sap_basak_boyu__H39',
    'ort_sap_basak_alti_boyu__I39',
    'ort_sap_boy_cm__J39',

    # --- b1-b10 ham: uzunluk ---
    'b1_uzunluk_cm__B29','b2_uzunluk_cm__B30','b3_uzunluk_cm__B31','b4_uzunluk_cm__B32',
    'b5_uzunluk_cm__B33','b6_uzunluk_cm__B34','b7_uzunluk_cm__B35','b8_uzunluk_cm__B36',
    'b9_uzunluk_cm__B37','b10_uzunluk_cm__B38',

    # --- b1-b10 ham: agirlik ---
    'b1_agirlik_mg__C29','b2_agirlik_mg__C30','b3_agirlik_mg__C31','b4_agirlik_mg__C32',
    'b5_agirlik_mg__C33','b6_agirlik_mg__C34','b7_agirlik_mg__C35','b8_agirlik_mg__C36',
    'b9_agirlik_mg__C37','b10_agirlik_mg__C38',

    # --- b1-b10 ham: dane_sayisi ---
    'b1_dane_sayisi__D29','b2_dane_sayisi__D30','b3_dane_sayisi__D31','b4_dane_sayisi__D32',
    'b5_dane_sayisi__D33','b6_dane_sayisi__D34','b7_dane_sayisi__D35','b8_dane_sayisi__D36',
    'b9_dane_sayisi__D37','b10_dane_sayisi__D38',

    # --- b1-b10 ham: dane_agirlik ---
    'b1_dane_agirlik_mg__E29','b2_dane_agirlik_mg__E30','b3_dane_agirlik_mg__E31','b4_dane_agirlik_mg__E32',
    'b5_dane_agirlik_mg__E33','b6_dane_agirlik_mg__E34','b7_dane_agirlik_mg__E35','b8_dane_agirlik_mg__E36',
    'b9_dane_agirlik_mg__E37','b10_dane_agirlik_mg__E38',

    # --- b1-b10 ham: sap_basak_boyu ---
    'b1_sap_basak_boyu_cm__H29','b2_sap_basak_boyu_cm__H30','b3_sap_basak_boyu_cm__H31','b4_sap_basak_boyu_cm__H32',
    'b5_sap_basak_boyu_cm__H33','b6_sap_basak_boyu_cm__H34','b7_sap_basak_boyu_cm__H35','b8_sap_basak_boyu_cm__H36',
    'b9_sap_basak_boyu_cm__H37','b10_sap_basak_boyu_cm__H38',

    # --- b1-b10 ham: sap_alt ---
    'b1_sap_alt_cm__I29','b2_sap_alt_cm__I30','b3_sap_alt_cm__I31','b4_sap_alt_cm__I32',
    'b5_sap_alt_cm__I33','b6_sap_alt_cm__I34','b7_sap_alt_cm__I35','b8_sap_alt_cm__I36',
    'b9_sap_alt_cm__I37','b10_sap_alt_cm__I38',

    # --- b1-b10 ham: sap_boy ---
    'b1_sap_boy_cm__J29','b2_sap_boy_cm__J30','b3_sap_boy_cm__J31','b4_sap_boy_cm__J32',
    'b5_sap_boy_cm__J33','b6_sap_boy_cm__J34','b7_sap_boy_cm__J35','b8_sap_boy_cm__J36',
    'b9_sap_boy_cm__J37','b10_sap_boy_cm__J38',
]

# Dogrulama
eksik = [c for c in yeni_sira if c not in df.columns]
fazla = [c for c in df.columns if c not in yeni_sira]
if eksik:
    print(f'UYARI - listede var ama df de yok: {eksik}')
if fazla:
    print(f'UYARI - df de var ama listede yok: {fazla}')

assert len(yeni_sira) == len(df.columns), f"Sutun sayisi eslesmiyor: {len(yeni_sira)} != {len(df.columns)}"

df = df[yeni_sira]
df.to_csv(PATH, index=False, encoding='utf-8-sig')
print(f"Kaydedildi: {len(df)} satir, {len(df.columns)} sutun")
