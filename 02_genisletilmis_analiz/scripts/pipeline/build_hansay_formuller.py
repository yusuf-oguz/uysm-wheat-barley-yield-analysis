"""
Hansay 2016 — Formül çıkarıcı
-------------------------------
hansay_ham_full.csv'deki her veri hücresi için o hücrede uygulanan
formülü çeker. Her sütun adı: C21_formul, D21_formul gibi.

Formül yoksa (sabit değer) None yazılır.

Çıktı: yusuf_oguz_calismalari/data/processed/hansay_formuller.csv
"""

import os
import csv
import openpyxl

KAYNAK = (
    r"D:\_Development\Projects\UYSM_Project_2"
    r"\uysm_flash_bellek_degistirilmemis"
    r"\hansay 2016 verim\Verim 8"
    r"\1.EXEL HESAPLAR TABLOLARI (7 CİLT)"
)

CIKTI = (
    r"D:\_Development\Projects\UYSM_Project_2"
    r"\yusuf_oguz_calismalari\data\processed\active\hansay_formuller.csv"
)

# hansay_ham_full.csv'deki veri hücrelerinin Excel adresleri
# (dosyaadi ve okuma_notu sütunları hariç)
VERI_HUCRELERI = [
    "A3", "C3", "E3", "G3", "J3",
    "C4", "E4",
    "C5", "I5",
    "C6", "G6",
    "C7", "I7",
    "C8", "G8",
    "C9", "G9",
    "C10", "G10",
    "A11", "C11", "G11",
    "C12",
    "C13", "E13",
    "C14", "E14",
    "C15",
    "C16",
    "C17",
    "C18",
    "C19",
    "C20",
    "C21", "D21",
    "C22",
    "C23",
    "C24", "J24",
    "C25",
    "C26",
    # Başak ölçümleri (S29-S38)
    "B29", "C29", "D29", "E29", "H29", "I29", "J29",
    "B30", "C30", "D30", "E30", "H30", "I30", "J30",
    "B31", "C31", "D31", "E31", "H31", "I31", "J31",
    "B32", "C32", "D32", "E32", "H32", "I32", "J32",
    "B33", "C33", "D33", "E33", "H33", "I33", "J33",
    "B34", "C34", "D34", "E34", "H34", "I34", "J34",
    "B35", "C35", "D35", "E35", "H35", "I35", "J35",
    "B36", "C36", "D36", "E36", "H36", "I36", "J36",
    "B37", "C37", "D37", "E37", "H37", "I37", "J37",
    "B38", "C38", "D38", "E38", "H38", "I38", "J38",
    # Toplam (S39)
    "B39", "C39", "D39", "E39", "H39", "I39", "J39",
    # Ortalama (S40)
    "B40", "C40", "D40", "E40",
    # S41
    "C41", "D41", "J41",
    # S42
    "C42", "E42",
]

KOLONLAR = ["dosya_adi"] + [f"{h}_formul" for h in VERI_HUCRELERI]


def dosyayi_isle(yol):
    dosya_adi = os.path.basename(yol)
    kayit = {"dosya_adi": dosya_adi}

    try:
        wb = openpyxl.load_workbook(yol, read_only=False, data_only=False)
        ws = wb.active

        for adres in VERI_HUCRELERI:
            hucre = ws[adres]
            val = hucre.value
            if isinstance(val, str) and val.startswith("="):
                kayit[f"{adres}_formul"] = "'" + val
            else:
                kayit[f"{adres}_formul"] = None

        wb.close()

    except Exception as e:
        for adres in VERI_HUCRELERI:
            kayit[f"{adres}_formul"] = None
        kayit["okuma_notu"] = f"HATA: {e}"

    return kayit


def main():
    os.makedirs(os.path.dirname(CIKTI), exist_ok=True)

    dosyalar = sorted([f for f in os.listdir(KAYNAK)
                       if f.lower().endswith(".xlsx") and not f.startswith("~")])
    print(f"Toplam {len(dosyalar)} xlsx dosyası bulundu.")

    sonuclar = []
    hatali = 0

    for i, dosya in enumerate(dosyalar, 1):
        kayit = dosyayi_isle(os.path.join(KAYNAK, dosya))
        sonuclar.append(kayit)
        if kayit.get("okuma_notu"):
            hatali += 1
            print(f"  [HATA] {dosya}: {kayit['okuma_notu']}")
        if i % 100 == 0:
            print(f"  {i}/{len(dosyalar)} işlendi...")

    alan = ["dosya_adi"] + [f"{h}_formul" for h in VERI_HUCRELERI]
    if hatali:
        alan.append("okuma_notu")

    for kayit in sonuclar:
        for s in alan:
            kayit.setdefault(s, None)

    with open(CIKTI, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=alan)
        writer.writeheader()
        writer.writerows(sonuclar)

    print(f"\n{len(sonuclar)} dosya işlendi, {hatali} hata.")
    print(f"Çıktı: {CIKTI}")
    print(f"Boyut: {os.path.getsize(CIKTI) / 1024:.1f} KB")


if __name__ == "__main__":
    main()
