# UYSM Projesi — Tarla Ölçüm Verisi ETL Pipeline

> Bu, iki aşamalı çalışmanın **ilk aşaması**. Genel bakış ve devamı için → [üst dizin README](../README.md).

**Hazırlayan:** Yusuf Oğuz  
**Dönem:** 2026 Bahar — Staj / Araştırma Projesi  
**Son güncelleme:** 2026-04-01

---

## Projenin Amacı

Bu proje; tarımsal rekolte tahmini amacıyla Türkiye genelindeki istasyonlardan toplanan buğday ve arpa saha ölçüm verilerini işlemek için geliştirilmiştir.

Ham veri kaynağı: `data/source/UYSM-EXECELL HESAPLAMALARI 0-300 DOSYA/` klasöründe yer alan **291 adet Excel (.xlsx) dosyası**. Her dosya, bir istasyona ait tek bir ölçüm gününü temsil eder ve şunları içerir:

- GPS koordinatları (enlem/boylam, ham tam sayı formatında)
- İstasyon kodu ve ölçüm tarihi
- Bitki türü ve çeşit adı
- 10 adet bireysel başak ölçümü (kılçıklı ve dane ağırlıkları, mg)
- 1 m²'deki başak sayısı
- İki farklı yöntemle hesaplanmış dane ağırlığı (HESAP ve GERÇEK, g/m²)
- Bitki ve başak boyu ölçümleri

Pipeline çıktısı: analiz için hazır, kalite bayrakları eklenmiş tek bir birleşik CSV → `data/processed/UYSM_merged.csv`

---

## Klasör Yapısı

```
UYSM_Projects/
├── README.md
├── .claude/
│   └── settings.json              # Claude Code izin ayarları
│
├── scripts/
│   ├── pipeline/                  # Ana ETL pipeline (çalıştırma sırası aşağıda)
│   │   ├── extract_data.py
│   │   ├── verify_calculations.py
│   │   ├── check_anomalies.py
│   │   ├── explore_coords.py
│   │   ├── add_city_columns.py
│   │   ├── update_city_columns.py
│   │   ├── check_city_match.py
│   │   ├── duplicate_incele.py
│   │   ├── build_merged_v2.py
│   │   ├── update_merged2.py
│   │   ├── build_unified_csv.py
│   │   ├── finalize_data.py
│   │   ├── analyze_dane.py
│   │   └── kopyala_hatali_koordinatlar.py
│   │
│   ├── viz/                       # Görselleştirme scriptleri
│   │   ├── create_map.py
│   │   ├── create_validity_map.py
│   │   ├── visualize.py
│   │   ├── hansay_gorsel.py
│   │   ├── hansay_ilk_gorsel.py
│   │   └── hansay_ilk_temiz_harita.py
│   │
│   └── inspect/                   # Tek seferlik inceleme / debug scriptleri
│       ├── inspect_structure.py
│       ├── inspect_formulas.py
│       ├── inspect_formulas2.py
│       ├── inspect_calc.py
│       ├── inspect_one.py
│       ├── inspect_01118.py
│       ├── test_geocode.py
│       └── read_docx.py
│
├── data/
│   ├── source/                    # Ham kaynak veriler (değiştirilmez)
│   │   ├── UYSM-EXECELL HESAPLAMALARI 0-300 DOSYA/   # 291 xlsx dosyası
│   │   ├── hansay.xlsx            # Hansay istasyon listesi (güncel)
│   │   ├── hansay_ilk.xls         # Hansay istasyon listesi (ilk versiyon)
│   │   └── uysm ek veri.pdf       # Ek referans belgesi
│   │
│   └── processed/                 # Pipeline çıktıları
│       ├── UYSM_merged.csv        # ★ ANA ÇIKTI — 291 satır, tüm sütunlar
│       ├── UYSM_merged_v2.csv     # Ara versiyon (Hansay verisiyle zenginleştirilmiş)
│       ├── UYSM_hesap_kontrol.csv # Hesap doğrulama ara tablosu
│       ├── hansay_koordinatlar.csv
│       ├── hansay_ilk_koordinatlar.csv
│       ├── Koordinati Hatali Veriler/   # Koordinatı hatalı xlsx dosyaları (kopyalanmış)
│       ├── Koordinati Hatali Veriler.zip
│       └── sadece_bizde_24.txt    # Yalnızca bizim datasette olan 24 istasyon
│
├── output/
│   ├── maps/                      # İnteraktif HTML haritalar
│   │   ├── UYSM_harita.html       # Tüm geçerli istasyonlar
│   │   ├── turkey_validity_map.html
│   │   ├── hansay_harita.html
│   │   ├── hansay_ilk_harita.html
│   │   ├── hansay_ilk_temiz_harita.html
│   │   └── hansay_ilk_200_1200_harita.html
│   │
│   └── charts/                    # PNG grafikler
│       ├── UYSM_dagilim.png
│       └── UYSM_hesap_vs_gercek.png
│
└── docs/
    ├── EXCEL_VERI_YAPISI.md       # Excel dosya yapısı ve hücre-sütun eşleştirmesi
    └── HATALI_VERILER.txt         # Tespit edilen tüm veri sorunlarının kayıtı
```

---

## Pipeline Akışı

Scriptler bu sırayla çalıştırılmıştır:

```
1. extract_data.py          → 291 xlsx dosyasından ham veri çıkarır → UYSM_merged.csv (ilk versiyon)
2. verify_calculations.py   → Excel hesaplarını ham veriyle karşılaştırır → UYSM_hesap_kontrol.csv
3. check_anomalies.py       → Uç değer ve tutarsızlık analizi
4. explore_coords.py        → Koordinat dağılımını inceler, sorunluları işaretler
5. add_city_columns.py      → Shapefile ile il eşleştirmesi ekler
6. update_city_columns.py   → İl sütunlarını günceller (buffer analizi ile)
7. check_city_match.py      → İstasyon kodu ↔ koordinat il uyumsuzluklarını saptar
8. duplicate_incele.py      → Tekrarlayan kayıtları inceler
9. build_merged_v2.py       → Hansay verisiyle zenginleştirilmiş v2 oluşturur
10. update_merged2.py       → v2 üzerinde ek güncellemeler
11. build_unified_csv.py    → Tüm doğrulama sütunlarını birleştirip analiz_durumu ekler
12. finalize_data.py        → Son temizlik ve sütun standardizasyonu
13. analyze_dane.py         → İstatistiksel analiz (bitki türü bazında)
14. kopyala_hatali_koordinatlar.py → Koordinatı hatalı dosyaları ayrı klasöre kopyalar
```

Görselleştirme (bağımsız, pipeline'dan sonra):
```
viz/create_map.py             → UYSM_harita.html (folium, interaktif)
viz/create_validity_map.py    → turkey_validity_map.html (koordinat geçerlilik haritası)
viz/visualize.py              → PNG grafikler
viz/hansay_*.py               → Hansay verisi görselleştirmeleri
```

---

## Ana Çıktı: `UYSM_merged.csv` Sütunları

| Sütun | Kaynak | Açıklama |
|-------|--------|----------|
| `dosya_adi` | Dosya adı | Kaynak xlsx dosyası |
| `rapor_no` | J4 hücresi | Rapor numarası |
| `istasyon_no` | C6 hücresi | İl kodu + istasyon (örn. `16.03`) |
| `tarih` | C5 hücresi | Ölçüm tarihi |
| `bitki_adi` | C9 hücresi | `bugday` / `arpa` |
| `cesit_adi` | C10 hücresi | Çeşit adı |
| `enlem` | E3 hücresi (dönüştürülmüş) | Ondalık derece |
| `boylam` | E4 hücresi (dönüştürülmüş) | Ondalık derece |
| `m2_basak_sayisi` | C12 hücresi | 1 m²'deki başak sayısı |
| `xls_hesap_gram` | C21 hücresi | Excel'in HESAP yöntemi dane ağırlığı (g/m²) |
| `xls_gercek_gram` | D21 hücresi | Excel'in GERÇEK yöntemi dane ağırlığı (g/m²) |
| `duzeltilmis_hesap_gram` | Ham satırlardan | Python'da yeniden hesaplanmış HESAP |
| `duzeltilmis_gercek_gram` | Ham satırlardan | Python'da yeniden hesaplanmış GERÇEK |
| `ortalama_bitki_boyu_cm` | C23 hücresi | Bitki boyu (cm) |
| `ortalama_basak_boyu_cm` | C24 hücresi | Başak boyu (cm) |
| `analiz_durumu` | Hesaplanmış | Bkz. aşağı |
| `duzeltme_notu` | Hesaplanmış | Neden düzeltildiği |
| `analize_dahil` | Hesaplanmış | True/False filtre sütunu |

### `analiz_durumu` Değerleri

| Değer | Kayıt Sayısı | Anlam |
|-------|-------------|-------|
| `kullanilabilir` | 219 | Temiz, düzeltme gerektirmemiş |
| `duzeltilmis` | 20 | Hata tespit edildi, ham veriden yeniden hesaplandı |
| `koordinat_disi` | 44 | Koordinat Türkiye sınırları dışında |
| `koordinat_yok` | 4 | Koordinat hücresi boş |
| `veri_hatasi` | 4 | Şablon dosyası veya C41 tutarsızlığı |
| **TOPLAM** | **291** | |

**Analize dahil kayıt sayısı (`analize_dahil == True`): 239**

---

## Tespit Edilen Veri Hataları (Özet)

Detaylar: `docs/HATALI_VERILER.txt`

### Hesap Hataları (düzeltildi)
1. **E39 sabit 948 hatası** (12 dosya): `=SUM(E29:E38)` formülü yerine şablondan kopyalanmış sabit `948` değeri. `xls_hesap_gram` gerçek değerden 10–25× küçük çıkıyordu. Ham veriden yeniden hesaplandı.
2. **9 başak verisi** (8 dosya): Protokol 10 başak gerektiriyor; bu dosyalarda 9 satır dolu. Excel her zaman 10'a böldüğünden ortalama ~%11 küçük. Dolu satır sayısı tespit edilerek bölme düzeltildi.

### Koordinat Sorunları (analize dahil edilmedi)
- **5 dosya**: Açıkça imkânsız koordinatlar (Mısır, Rusya, İran)
- **23 dosya**: Akdeniz/Ege kıyısı — kara sınırının hemen açığına düşüyor (11 km buffer ile de yakalanamadı)
- **16 dosya**: Suriye sınırı ötesi koordinatlar (Gaziantep/Hatay/Şanlıurfa güneyi)
- **4 dosya**: Koordinat hücresi boş veya metin

### Diğer
- **3 dosya**: `C41` tarla tartım değeri beklenen değerden ~7× yüksek (birim karışıklığı şüphesi)
- **2 dosya**: İstasyon kodu büyük ihtimalle yanlış girilmiş (koordinatla eşleşmiyor)

---

## Koordinat Dönüşümü

Ham koordinatlar Excel'de tam sayı olarak girilmiş:

```
decimal = raw_int / 10^(len(str(raw_int)) - 2)
```

Örnekler:
- `3643467` (7 basamak) → `3643467 / 10^5` = **36.43467°**
- `35150`   (5 basamak) → `35150 / 10^3`   = **35.150°**
- `37435578` (8 basamak) → `37435578 / 10^6` = **37.435578°**

---

## Coğrafi Doğrulama

- Shapefile: `D:\_Development\Datasets\Turkey Shapefile\gadm41_TUR_shp\gadm41_TUR_1.shp`
- Her koordinat Türkiye il sınırlarına karşı kontrol edildi (standart + 11 km buffer)
- Kıyı sınırına yakın düşen meşru istasyonlar buffer ile kurtarıldı

---

## Kullanılan Python Kütüphaneleri

| Kütüphane | Kullanım Amacı |
|-----------|----------------|
| `openpyxl` | xlsx dosyalarından ham veri okuma |
| `pandas` | Veri işleme ve analiz |
| `geopandas` | Türkiye sınır shapefile analizi |
| `folium` | İnteraktif HTML harita üretimi |
| `matplotlib` / `seaborn` | Grafikler |
| `shapely` | Buffer geometri hesapları |

Ortam: `D:\_Development\Tools\base_env` (tüm kütüphaneler kurulu)

---

## Önemli Notlar

- **Analizde tercih edilen sütun:** `duzeltilmis_gercek_gram` — tartıma dayalı, daha güvenilir
- **Filtreleme:** `analize_dahil == True` → 239 kayıt
- Script path'leri `D:\_Development\Projects\UYSM_Projects\` tabanını kullanır
- Shapefile bağımlılığı (`D:\_Development\Datasets\...`) bazı scriptler için gereklidir
- Excel dosyaları formatı için → `docs/EXCEL_VERI_YAPISI.md`
- Tüm hata detayları için → `docs/HATALI_VERILER.txt`
